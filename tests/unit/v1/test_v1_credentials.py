#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.credentials import SwitchCredentialDbModel
from ..common import client_fixture, session_fixture


def test_v1_credentials_switches_get_100(client: TestClient):
    """Verify GET returns empty items when no credentials exist."""
    response = client.get("/api/v1/manage/credentials/switches")
    data = response.json()

    assert response.status_code == 200
    assert data["items"] == []


def test_v1_credentials_switches_get_110(session: Session, client: TestClient):
    """Verify GET returns credentials after they are created."""
    cred = SwitchCredentialDbModel(
        switchId="SAL1948TRTT",
        switchUsername="admin",
        switchPassword="*****",
        fabricName="f1",
        ip="172.22.150.107",
        switchName="leaf-1",
        credentialStore="local",
        type="custom",
    )
    session.add(cred)
    session.commit()

    response = client.get("/api/v1/manage/credentials/switches")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["switchId"] == "SAL1948TRTT"
    assert data["items"][0]["switchUsername"] == "admin"
    assert data["items"][0]["fabricName"] == "f1"


def test_v1_credentials_switches_post_100(client: TestClient):
    """Verify POST creates switch credentials."""
    body = {
        "switchIds": ["SAL1948TRTT", "SAL1947TRAB"],
        "switchUsername": "admin",
        "switchPassword": "test123",
    }
    response = client.post("/api/v1/manage/credentials/switches", json=body)

    assert response.status_code == 200

    get_response = client.get("/api/v1/manage/credentials/switches")
    data = get_response.json()

    assert len(data["items"]) == 2
    switch_ids = [item["switchId"] for item in data["items"]]
    assert "SAL1948TRTT" in switch_ids
    assert "SAL1947TRAB" in switch_ids


def test_v1_credentials_switches_post_110(session: Session, client: TestClient):
    """Verify POST updates existing credentials."""
    cred = SwitchCredentialDbModel(
        switchId="SAL1948TRTT",
        switchUsername="old_user",
        switchPassword="old_pass",
    )
    session.add(cred)
    session.commit()

    body = {
        "switchIds": ["SAL1948TRTT"],
        "switchUsername": "new_user",
        "switchPassword": "new_pass",
    }
    response = client.post("/api/v1/manage/credentials/switches", json=body)

    assert response.status_code == 200

    get_response = client.get("/api/v1/manage/credentials/switches")
    data = get_response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["switchUsername"] == "new_user"
