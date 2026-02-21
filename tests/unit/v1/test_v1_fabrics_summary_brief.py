#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.fabric import FabricDbModel, FabricSummaryBriefItem
from ..common import client_fixture, session_fixture


def _create_fabric(
    session: Session,
    name: str = "f1",
    mgmt_type: str = "vxlanIbgp",
    bgp_asn: str = "65001",
    category: str = "fabric",
    latitude: float = 71.1,
    longitude: float = 61.1,
) -> FabricDbModel:
    management = f'{{"bgpAsn": "{bgp_asn}", "type": "{mgmt_type}"}}'
    fabric = FabricDbModel(
        management=management,
        category=category,
        latitude=latitude,
        longitude=longitude,
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


def test_v1_fabrics_summary_brief_100(client: TestClient):
    """
    # Summary

    Verify empty database returns empty fabrics list with 200 status.
    """
    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200
    assert "fabrics" in data
    assert data["fabrics"] == []


def test_v1_fabrics_summary_brief_200(session: Session, client: TestClient):
    """
    # Summary

    Verify single fabric returns correct structure with all required fields.
    """
    _create_fabric(session)

    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200
    assert len(data["fabrics"]) == 1

    fabric = data["fabrics"][0]
    for key in ["fabricName", "securityDomain", "featureUsage", "licenseTier", "local", "ownerCluster", "type", "displayFabricType", "location"]:
        assert key in fabric, f"Missing required field: {key}"

    assert fabric["fabricName"] == "f1"
    assert fabric["securityDomain"] == "all"
    assert fabric["licenseTier"] == "premier"
    assert fabric["local"] is True
    assert fabric["type"] == "vxlanIbgp"
    assert fabric["displayFabricType"] == "Data Center VXLAN EVPN - iBGP"
    assert fabric["location"]["latitude"] == 71.1
    assert fabric["location"]["longitude"] == 61.1
    assert fabric["bgpAsn"] == "65001"
    assert isinstance(fabric["featureUsage"], dict)
    assert isinstance(fabric["ownerCluster"], str)


def test_v1_fabrics_summary_brief_300(session: Session, client: TestClient):
    """
    # Summary

    Verify multiple fabrics are returned with correct count and names.
    """
    _create_fabric(session, name="f1", latitude=71.1, longitude=61.1)
    _create_fabric(session, name="f2", mgmt_type="vxlanEbgp", bgp_asn="65002", latitude=72.2, longitude=62.2)

    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200
    assert len(data["fabrics"]) == 2

    names = {f["fabricName"] for f in data["fabrics"]}
    assert names == {"f1", "f2"}


def test_v1_fabrics_summary_brief_400(session: Session, client: TestClient):
    """
    # Summary

    Verify category filtering: only category="fabric" appears, not fabricGroup.
    """
    _create_fabric(session, name="f1", category="fabric")
    _create_fabric(session, name="fg1", category="fabricGroup", latitude=72.2, longitude=62.2)

    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200
    assert len(data["fabrics"]) == 1
    assert data["fabrics"][0]["fabricName"] == "f1"


def test_v1_fabrics_summary_brief_500(session: Session, client: TestClient):
    """
    # Summary

    Verify displayFabricType mapping for multiple management types.
    """
    _create_fabric(session, name="f1", mgmt_type="vxlanIbgp", latitude=71.1, longitude=61.1)
    _create_fabric(session, name="f2", mgmt_type="vxlanEbgp", latitude=72.2, longitude=62.2)
    _create_fabric(session, name="f3", mgmt_type="aci", latitude=73.3, longitude=63.3)
    _create_fabric(session, name="f4", mgmt_type="routed", latitude=74.4, longitude=64.4)

    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200

    type_map = {f["fabricName"]: f["displayFabricType"] for f in data["fabrics"]}
    assert type_map["f1"] == "Data Center VXLAN EVPN - iBGP"
    assert type_map["f2"] == "Data Center VXLAN EVPN - eBGP"
    assert type_map["f3"] == "ACI"
    assert type_map["f4"] == "Routed"


def test_v1_fabrics_summary_brief_600(session: Session, client: TestClient):
    """
    # Summary

    Verify tenantAssociation defaults to False.
    """
    _create_fabric(session)

    response = client.get("/api/v1/manage/fabricsSummaryBrief")
    data = response.json()

    assert response.status_code == 200
    assert data["fabrics"][0]["tenantAssociation"] is False
