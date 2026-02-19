#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.fabric import FabricDbModel
from app.v1.models.switch import SwitchDbModel
from ..common import client_fixture, session_fixture


def _create_fabric(session: Session, name: str = "f1") -> FabricDbModel:
    fabric = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "vxlanIbgp"}',
        category="fabric",
        latitude=71.1,
        longitude=61.1,
        licenseTier="premier",
        name=name,
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/1",
        telemetrySourceVrf="vrf_1",
        telemetryStreamingProtocol="ipv4",
    )
    session.add(fabric)
    session.commit()
    return fabric


def _create_switch(session: Session, fabric_name: str = "f1", switch_id: str = "SAL1111", hostname: str = "leaf1", role: str = "leaf") -> SwitchDbModel:
    switch = SwitchDbModel(
        switchId=switch_id,
        fabricName=fabric_name,
        fabricManagementIp="10.1.1.1",
        hostname=hostname,
        model="N9K-C93180YC-FX",
        serialNumber=switch_id,
        softwareVersion="10.3(3)",
        switchRole=role,
    )
    session.add(switch)
    session.commit()
    return switch


def test_v1_switches_post_100(session: Session, client: TestClient):
    """Verify successful switch discovery POST."""
    _create_fabric(session)
    body = {
        "switches": [
            {"hostname": "leaf1", "ip": "10.1.1.1", "serialNumber": "SAL1111", "model": "N9K-C93180YC-FX"},
            {"hostname": "spine1", "ip": "10.1.1.2", "serialNumber": "SAL2222", "model": "N9K-C9336C-FX2"},
        ]
    }
    response = client.post("/api/v1/manage/fabrics/f1/switches", json=body)
    assert response.status_code == 202


def test_v1_switches_post_200(client: TestClient):
    """Verify switch POST returns 404 for non-existent fabric."""
    body = {"switches": [{"hostname": "leaf1", "ip": "10.1.1.1", "serialNumber": "SAL1111", "model": "N9K"}]}
    response = client.post("/api/v1/manage/fabrics/nonexistent/switches", json=body)
    assert response.status_code == 404


def test_v1_switches_get_100(session: Session, client: TestClient):
    """Verify GET returns switches with meta."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1")
    _create_switch(session, switch_id="SAL2222", hostname="spine1", role="spine")

    response = client.get("/api/v1/manage/fabrics/f1/switches")
    data = response.json()

    assert response.status_code == 200
    assert data["meta"]["total"] == 2
    assert data["meta"]["remaining"] == 0
    assert len(data["switches"]) == 2


def test_v1_switches_get_200(client: TestClient):
    """Verify GET returns 404 for non-existent fabric."""
    response = client.get("/api/v1/manage/fabrics/nonexistent/switches")
    assert response.status_code == 404


def test_v1_switch_get_100(session: Session, client: TestClient):
    """Verify GET single switch."""
    _create_fabric(session)
    _create_switch(session)

    response = client.get("/api/v1/manage/fabrics/f1/switches/SAL1111")
    data = response.json()

    assert response.status_code == 200
    assert data["switchId"] == "SAL1111"
    assert data["hostname"] == "leaf1"


def test_v1_switch_get_200(session: Session, client: TestClient):
    """Verify GET returns 404 for non-existent switch."""
    _create_fabric(session)
    response = client.get("/api/v1/manage/fabrics/f1/switches/NONEXISTENT")
    assert response.status_code == 404


def test_v1_switch_delete_100(session: Session, client: TestClient):
    """Verify DELETE switch."""
    _create_fabric(session)
    _create_switch(session)

    response = client.delete("/api/v1/manage/fabrics/f1/switches/SAL1111")
    assert response.status_code == 204

    response = client.get("/api/v1/manage/fabrics/f1/switches/SAL1111")
    assert response.status_code == 404


def test_v1_switch_delete_200(session: Session, client: TestClient):
    """Verify DELETE returns 404 for non-existent switch."""
    _create_fabric(session)
    response = client.delete("/api/v1/manage/fabrics/f1/switches/NONEXISTENT")
    assert response.status_code == 404


def test_v1_switches_summary_100(session: Session, client: TestClient):
    """Verify switches summary endpoint."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", hostname="leaf1", role="leaf")
    _create_switch(session, switch_id="SAL2222", hostname="spine1", role="spine")

    response = client.get("/api/v1/manage/fabrics/f1/switches/summary")
    data = response.json()

    assert response.status_code == 200
    roles = {item["name"]: item["count"] for item in data["role"]}
    assert roles["leaf"] == 1
    assert roles["spine"] == 1


def test_v1_switch_change_roles_100(session: Session, client: TestClient):
    """Verify switch role change."""
    _create_fabric(session)
    _create_switch(session, switch_id="SAL1111", role="leaf")

    body = {"switchRoles": [{"role": "border", "switchId": "SAL1111"}]}
    response = client.post("/api/v1/manage/fabrics/f1/switchActions/changeRoles", json=body)
    data = response.json()

    assert response.status_code == 207
    assert data["items"][0]["status"] == "success"

    response = client.get("/api/v1/manage/fabrics/f1/switches/SAL1111")
    assert response.json()["switchRole"] == "border"


def test_v1_switch_change_roles_200(session: Session, client: TestClient):
    """Verify change roles returns failure for non-existent switch."""
    _create_fabric(session)
    body = {"switchRoles": [{"role": "border", "switchId": "NONEXISTENT"}]}
    response = client.post("/api/v1/manage/fabrics/f1/switchActions/changeRoles", json=body)
    data = response.json()

    assert response.status_code == 207
    assert data["items"][0]["status"] == "failure"


def test_v1_switch_rediscover_100(session: Session, client: TestClient):
    """Verify switch rediscover."""
    _create_fabric(session)
    _create_switch(session)

    response = client.post("/api/v1/manage/fabrics/f1/switchActions/rediscover", json={"switchIds": ["SAL1111"]})
    assert response.status_code == 202


def test_v1_switch_rediscover_200(session: Session, client: TestClient):
    """Verify rediscover returns 404 for non-existent switch."""
    _create_fabric(session)
    response = client.post("/api/v1/manage/fabrics/f1/switchActions/rediscover", json={"switchIds": ["NONEXISTENT"]})
    assert response.status_code == 404
