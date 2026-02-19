#!/usr/bin/env python
"""
Performance test script for Nexus Dashboard fabric REST API.

Tests login, fabric CRUD operations, and reports execution times.

Usage:
    # Against the mock server (default)
    python scripts/perf_test.py

    # Against a real ND controller
    python scripts/perf_test.py --base-url https://10.1.1.1 --username admin --password 'MyPass!'

    # With SSL verification disabled (self-signed certs)
    python scripts/perf_test.py --base-url https://10.1.1.1 --no-verify
"""
import argparse
import sys
import time

import requests
import urllib3

# ---------------------------------------------------------------------------
# Configuration — edit BASE_URL for your environment
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:8000"

# Login credentials (mock accepts anything; real ND needs valid creds)
USERNAME = "admin"
PASSWORD = "Admin_1234"
DOMAIN = "local"

# ---------------------------------------------------------------------------
# Fabric payloads — three different management types
# ---------------------------------------------------------------------------
FABRICS = [
    {
        "name": "perf_ebgp",
        "category": "fabric",
        "licenseTier": "advantage",
        "location": {"latitude": 37.3394, "longitude": -121.8950},
        "management": {
            "anycastGatewayMac": "2020.0000.00aa",
            "bgpAsMode": "multiAS",
            "bgpAsn": "65001",
            "bgpLoopbackId": 0,
            "bgpLoopbackIpRange": "10.2.0.0/22",
            "fabricMtu": 9216,
            "intraFabricSubnetRange": "10.4.0.0/16",
            "nveLoopbackId": 1,
            "nveLoopbackIpRange": "10.3.0.0/22",
            "replicationMode": "multicast",
            "targetSubnetMask": 30,
            "type": "vxlanEbgp",
        },
        "securityDomain": "all",
        "telemetryCollection": False,
        "telemetryCollectionType": "inBand",
        "telemetryStreamingProtocol": "ipv4",
        "telemetrySourceInterface": "",
        "telemetrySourceVrf": "",
    },
    {
        "name": "perf_ibgp",
        "category": "fabric",
        "licenseTier": "essentials",
        "location": {"latitude": 40.7128, "longitude": -74.0060},
        "management": {
            "bgpAsn": "65002",
            "type": "vxlanIbgp",
        },
        "securityDomain": "all",
        "telemetryCollection": False,
        "telemetryCollectionType": "inBand",
        "telemetryStreamingProtocol": "ipv4",
        "telemetrySourceInterface": "",
        "telemetrySourceVrf": "",
    },
    {
        "name": "perf_routed",
        "category": "fabric",
        "licenseTier": "essentials",
        "location": {"latitude": 51.5074, "longitude": -0.1278},
        "management": {
            "bgpAsn": "65003",
            "type": "routed",
        },
        "securityDomain": "all",
        "telemetryCollection": False,
        "telemetryCollectionType": "inBand",
        "telemetryStreamingProtocol": "ipv4",
        "telemetrySourceInterface": "",
        "telemetrySourceVrf": "",
    },
]

# Fabric to delete in step 3
DELETE_FABRIC = "perf_routed"

# PUT update payload for step 5
PUT_FABRIC = "perf_ebgp"
PUT_UPDATE = {
    "name": "perf_ebgp",
    "category": "fabric",
    "licenseTier": "advantage",
    "location": {"latitude": 38.0000, "longitude": -122.0000},
    "management": {
        "anycastGatewayMac": "2020.0000.00aa",
        "bgpAsMode": "multiAS",
        "bgpAsn": "65001",
        "bgpLoopbackId": 0,
        "bgpLoopbackIpRange": "10.2.0.0/22",
        "fabricMtu": 9200,
        "intraFabricSubnetRange": "10.4.0.0/16",
        "nveLoopbackId": 1,
        "nveLoopbackIpRange": "10.3.0.0/22",
        "replicationMode": "ingress",
        "targetSubnetMask": 30,
        "type": "vxlanEbgp",
    },
    "securityDomain": "all",
    "telemetryCollection": False,
    "telemetryCollectionType": "inBand",
    "telemetryStreamingProtocol": "ipv4",
    "telemetrySourceInterface": "",
    "telemetrySourceVrf": "",
}


def timed(label):
    """Decorator that prints execution time for a test step."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            timings.append((label, elapsed))
            return result
        return wrapper
    return decorator


timings: list[tuple[str, float]] = []
config: dict[str, str] = {"username": USERNAME, "password": PASSWORD, "domain": DOMAIN}


@timed("1. Login")
def step_login(session, base_url):
    url = f"{base_url}/login"
    body = {"domain": config["domain"], "userName": config["username"], "userPasswd": config["password"]}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("token") or data.get("jwttoken")
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})
    print(f"   Login successful (user={config['username']})")
    return data


@timed("2. POST three fabrics")
def step_post_fabrics(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    for fabric in FABRICS:
        resp = session.post(url, json=fabric)
        resp.raise_for_status()
        print(f"   Created fabric: {fabric['name']} (type={fabric['management']['type']})")


@timed("3. DELETE one fabric")
def step_delete_one(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{DELETE_FABRIC}"
    resp = session.delete(url)
    resp.raise_for_status()
    print(f"   Deleted fabric: {DELETE_FABRIC}")


@timed("4. GET all fabrics")
def step_list_fabrics_1(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    names = [f["name"] for f in data.get("fabrics", [])]
    print(f"   Fabrics ({data['meta']['total']}): {names}")
    return data


@timed("5. PUT modify fabric")
def step_put_fabric(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{PUT_FABRIC}"
    # GET current state, merge updates, then PUT
    get_resp = session.get(url)
    get_resp.raise_for_status()
    current = get_resp.json()
    for key, value in PUT_UPDATE.items():
        if isinstance(value, dict) and isinstance(current.get(key), dict):
            current[key].update(value)
        else:
            current[key] = value
    resp = session.put(url, json=current)
    resp.raise_for_status()
    data = resp.json()
    print(f"   Updated fabric: {PUT_FABRIC}")
    print(f"     replicationMode: {data.get('management', {}).get('replicationMode')}")
    print(f"     management.fabricMtu: {data.get('management', {}).get('fabricMtu')}")
    return data


@timed("6. GET all fabrics (after PUT)")
def step_list_fabrics_2(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    names = [f["name"] for f in data.get("fabrics", [])]
    print(f"   Fabrics ({data['meta']['total']}): {names}")
    return data


@timed("7. DELETE all remaining fabrics")
def step_delete_all(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    resp = session.get(url)
    resp.raise_for_status()
    fabrics = resp.json().get("fabrics", [])
    for fabric in fabrics:
        name = fabric["name"]
        del_resp = session.delete(f"{url}/{name}")
        del_resp.raise_for_status()
        print(f"   Deleted fabric: {name}")


@timed("8. GET all fabrics (verify deletion)")
def step_verify_deletion(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    total = data["meta"]["total"]
    print(f"   Fabrics remaining: {total}")
    if total != 0:
        print("   WARNING: Expected 0 fabrics after deletion!")
    return data


def print_summary():
    print("\n" + "=" * 60)
    print(f"{'Step':<40} {'Time':>10}")
    print("-" * 60)
    total = 0.0
    for label, elapsed in timings:
        print(f"{label:<40} {elapsed:>9.4f}s")
        total += elapsed
    print("-" * 60)
    print(f"{'Total':<40} {total:>9.4f}s")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="ND Fabric API performance test")
    parser.add_argument("--base-url", default=BASE_URL, help=f"Base URL (default: {BASE_URL})")
    parser.add_argument("--username", default=USERNAME, help=f"Login username (default: {USERNAME})")
    parser.add_argument("--password", default=PASSWORD, help=f"Login password (default: {PASSWORD})")
    parser.add_argument("--domain", default=DOMAIN, help=f"Login domain (default: {DOMAIN})")
    parser.add_argument("--no-verify", action="store_true", help="Disable SSL certificate verification")
    args = parser.parse_args()

    config["username"] = args.username
    config["password"] = args.password
    config["domain"] = args.domain

    session = requests.Session()
    session.timeout = 120
    if args.no_verify:
        session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    base_url = args.base_url.rstrip("/")
    print(f"Target: {base_url}\n")

    steps = [
        step_login,
        step_post_fabrics,
        step_delete_one,
        step_list_fabrics_1,
        step_put_fabric,
        step_list_fabrics_2,
        step_delete_all,
        step_verify_deletion,
    ]

    for step in steps:
        try:
            step(session, base_url)
        except requests.HTTPError as exc:
            print(f"\n   FAILED: {exc}")
            print(f"   Response: {exc.response.text[:500]}")
            print_summary()
            sys.exit(1)

    print_summary()


if __name__ == "__main__":
    main()
