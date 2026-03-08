#!/usr/bin/env python
"""
Performance test — full VRF/Switch lifecycle workflow.

Tests the end-to-end lifecycle of a fabric, two switches, and two VRFs,
including attach/detach and deploy steps.

Steps:
  1.  Login
  2.  Create fabric (vxlanEbgp)
  3.  Add switch_1 and switch_2
  4.  Add vrf_1 and vrf_2
  5.  Attach vrf_1→switch_1 and vrf_2→switch_2  (requires vrfAttachments POST)
  6.  Deploy VRF attachments
  7.  Detach both VRFs                            (requires vrfAttachments POST)
  8.  Deploy VRF detachments
  9.  Query VRF attachment status
  10. Delete switch_1 and switch_2
  11. Delete vrf_1 and vrf_2
  12. Delete fabric

Usage:
    # Against the mock server (default)
    python scripts/perf_test_workflow.py

    # Against a real ND controller
    python scripts/perf_test_workflow.py --base-url https://10.1.1.1 --username admin --password 'MyPass!'

    # With SSL verification disabled (self-signed certs)
    python scripts/perf_test_workflow.py --base-url https://10.1.1.1 --no-verify
"""
import argparse
import sys
import time

import requests
import urllib3

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "http://0.0.0.0:8000"

USERNAME = "admin"
PASSWORD = "Admin_1234"
DOMAIN = "local"

FABRIC_NAME = "fabric_1"

SWITCHES = [
    {
        "hostname": "switch_1",
        "ip": "192.168.12.151",
        "serialNumber": "945V7U23QJ7",
        "model": "N9K-X9364v",
        "softwareVersion": "10.6(2)",
        "switchRole": "leaf",
    },
    {
        "hostname": "switch_2",
        "ip": "192.168.12.152",
        "serialNumber": "9F7HA9NZS8O",
        "model": "N9K-X9364v",
        "softwareVersion": "10.6(2)",
        "switchRole": "leaf",
    },
]

VRFS = [
    {"vrfName": "vrf_1", "vrfId": 50001, "vrfType": "vxlanEbgp"},
    {"vrfName": "vrf_2", "vrfId": 50002, "vrfType": "vxlanEbgp"},
]

# ---------------------------------------------------------------------------
# Timing infrastructure
# ---------------------------------------------------------------------------
timings: list[tuple[str, float, str]] = []  # (label, elapsed, status)
config: dict[str, str] = {"username": USERNAME, "password": PASSWORD, "domain": DOMAIN}

SKIPPED = "SKIP"
PASSED = "OK"
FAILED = "FAIL"


def timed(label: str):
    """Decorator that records execution time and pass/fail/skip status."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            status = result if isinstance(result, str) and result in (SKIPPED, FAILED) else PASSED
            timings.append((label, elapsed, status))
            return result

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------


def _not_implemented(label: str, endpoint: str) -> str:
    print(f"   SKIP — endpoint not yet implemented: {endpoint}")
    timings.append((label, 0.0, SKIPPED))
    return SKIPPED


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------


@timed("1.  Login")
def step_login(session, base_url):
    url = f"{base_url}/api/v1/infra/login"
    body = {"domain": config["domain"], "userName": config["username"], "userPasswd": config["password"]}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("token") or data.get("jwttoken")
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})
    print(f"   Login successful (user={config['username']})")
    return data


@timed("2.  Create fabric (vxlanEbgp)")
def step_create_fabric(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics"
    body = {
        "name": FABRIC_NAME,
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
    }
    resp = session.post(url, json=body)
    resp.raise_for_status()
    print(f"   Created fabric: {FABRIC_NAME} (type=vxlanEbgp)")
    return resp.json()


@timed("3.  Add switch_1 and switch_2")
def step_add_switches(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}/switches"
    body = {"switches": SWITCHES, "username": config["username"], "password": config["password"], "snmpV3AuthProtocol": "MD5"}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    for sw in SWITCHES:
        print(f"   Added switch: {sw['hostname']} (serial={sw['serialNumber']})")


@timed("4.  Add vrf_1 and vrf_2")
def step_add_vrfs(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}/vrfs"
    body = {"vrfs": VRFS}
    resp = session.post(url, json=body)
    # VRF POST always returns 207
    if resp.status_code not in (200, 207):
        resp.raise_for_status()
    data = resp.json()
    for item in data.get("results", []):
        print(f"   VRF {item['vrfName']}: {item['status']}")
    return data


def step_attach_vrfs(session, base_url):
    """
    POST /api/v1/manage/fabrics/{fabric_name}/vrfAttachments

    This endpoint is not yet implemented in the mock.
    When implemented, the request body is expected to be a list of
    {vrfName, switchId, attach: true} items, returning 207 with per-item results.
    """
    label = "5.  Attach vrf_1→switch_1, vrf_2→switch_2"
    return _not_implemented(label, f"POST /api/v1/manage/fabrics/{FABRIC_NAME}/vrfAttachments")


def step_deploy_attachments(session, base_url):
    """Deploy after attach — only meaningful once attach step is implemented."""
    label = "6.  Deploy VRF attachments"
    return _not_implemented(label, f"POST /api/v1/manage/fabrics/{FABRIC_NAME}/vrfActions/deploy (attach)")


def step_detach_vrfs(session, base_url):
    """
    POST /api/v1/manage/fabrics/{fabric_name}/vrfAttachments with attach=false.
    Same endpoint as attach — not yet implemented.
    """
    label = "7.  Detach vrf_1 and vrf_2"
    return _not_implemented(label, f"POST /api/v1/manage/fabrics/{FABRIC_NAME}/vrfAttachments")


def step_deploy_detachments(session, base_url):
    """Deploy after detach — only meaningful once detach step is implemented."""
    label = "8.  Deploy VRF detachments"
    return _not_implemented(label, f"POST /api/v1/manage/fabrics/{FABRIC_NAME}/vrfActions/deploy (detach)")


@timed("9.  Query VRF attachment status")
def step_query_attachments(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}/vrfAttachments/query"
    body = {"switchIds": [], "vrfNames": []}
    resp = session.post(url, json=body)
    resp.raise_for_status()
    data = resp.json()
    total = data.get("meta", {}).get("counts", {}).get("total", 0)
    print(f"   Attachment records: {total}")
    for a in data.get("attachments", []):
        print(f"     {a['vrfName']} → {a['switchName']}: status={a['status']}")
    return data


@timed("10. Delete switch_1 and switch_2")
def step_delete_switches(session, base_url):
    for sw in SWITCHES:
        url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}/switches/{sw['serialNumber']}"
        resp = session.delete(url)
        resp.raise_for_status()
        print(f"   Deleted switch: {sw['hostname']} (serial={sw['serialNumber']})")


@timed("11. Delete vrf_1 and vrf_2")
def step_delete_vrfs(session, base_url):
    for vrf in VRFS:
        url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}/vrfs/{vrf['vrfName']}"
        resp = session.delete(url)
        # VRF DELETE returns 204 on success
        if resp.status_code not in (200, 204):
            resp.raise_for_status()
        print(f"   Deleted VRF: {vrf['vrfName']}")


@timed("12. Delete fabric")
def step_delete_fabric(session, base_url):
    url = f"{base_url}/api/v1/manage/fabrics/{FABRIC_NAME}"
    resp = session.delete(url)
    resp.raise_for_status()
    print(f"   Deleted fabric: {FABRIC_NAME}")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def print_summary():
    status_sym = {PASSED: "ok  ", FAILED: "FAIL", SKIPPED: "skip"}
    print("\n" + "=" * 68)
    print(f"{'Step':<44} {'Status':<6} {'Time':>10}")
    print("-" * 68)
    total = 0.0
    for label, elapsed, status in timings:
        sym = status_sym.get(status, "    ")
        time_str = f"{elapsed:>9.4f}s" if status != SKIPPED else "       n/a"
        print(f"{label:<44} [{sym}] {time_str}")
        total += elapsed
    print("-" * 68)
    print(f"{'Total':<44}        {total:>9.4f}s")
    print("=" * 68)

    skipped = [l for l, _, s in timings if s == SKIPPED]
    if skipped:
        print(f"\nSkipped {len(skipped)} step(s) — endpoint(s) not yet implemented:")
        for label in skipped:
            print(f"  - {label}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="ND VRF/Switch lifecycle performance test")
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

    # Steps that use @timed run themselves; steps without it manage their own timing entry.
    timed_steps = [
        step_login,
        step_create_fabric,
        step_add_switches,
        step_add_vrfs,
    ]
    manual_steps = [
        step_attach_vrfs,
        step_deploy_attachments,
        step_detach_vrfs,
        step_deploy_detachments,
    ]
    timed_steps_2 = [
        step_query_attachments,
        step_delete_switches,
        step_delete_vrfs,
        step_delete_fabric,
    ]

    all_steps = timed_steps + manual_steps + timed_steps_2

    for step in all_steps:
        try:
            step(session, base_url)
        except requests.HTTPError as exc:
            label = getattr(step, "__name__", str(step))
            elapsed = 0.0
            timings.append((label, elapsed, FAILED))
            print(f"\n   FAILED: {exc}")
            print(f"   Response: {exc.response.text[:500]}")
            print_summary()
            sys.exit(1)

    print_summary()


if __name__ == "__main__":
    main()
