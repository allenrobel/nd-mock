#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v2.models.fabric import FabricDbModelV2
from ..common import client_fixture, session_fixture


def _create_fabric(session: Session, name: str = "f1") -> FabricDbModelV2:
    fabric = FabricDbModelV2(
        bgpAsn="65001",
        category="fabric",
        latitude=71.1,
        longitude=61.1,
        licenseTier="advantage",
        name=name,
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/1",
        telemetrySourceVrf="vrf_1",
        telemetryStreamingProtocol="ipv4",
        type="fabric",
    )
    session.add(fabric)
    session.commit()
    return fabric


def test_v2_config_save_post_100(session: Session, client: TestClient):
    """Verify successful configSave POST request."""
    _create_fabric(session)
    response = client.post("/api/v1/manage/fabrics/f1/actions/configSave")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "Config save is completed"


def test_v2_config_save_post_200(client: TestClient):
    """Verify configSave returns 404 for non-existent fabric."""
    response = client.post("/api/v1/manage/fabrics/nonexistent/actions/configSave")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == 404


def test_v2_config_deploy_post_100(session: Session, client: TestClient):
    """Verify successful configDeploy POST request."""
    _create_fabric(session)
    response = client.post("/api/v1/manage/fabrics/f1/actions/configDeploy")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "Configuration deployment completed"


def test_v2_config_deploy_post_200(client: TestClient):
    """Verify configDeploy returns 404 for non-existent fabric."""
    response = client.post("/api/v1/manage/fabrics/nonexistent/actions/configDeploy")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == 404
