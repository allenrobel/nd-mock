#!/usr/bin/env python
# See the following regarding *_fixture imports
# https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html
# Due to the above, we also need to disable unused-import
# Also, fixtures need to use *args to match the signature of the function they are mocking
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import json
from time import sleep

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.fabric import FabricDbModelV1
from ..common import client_fixture, convert_db_date_to_timestamp, convert_model_date_to_timestamp, session_fixture, timestamps_within_delta


def test_v1_fm_about_version_get_100(client: TestClient):
    """
    # Summary

    Verify successful GET request.

    ## Endpoint

    GET /appcenter/cisco/ndfc/api/v1/fm/features
    """
    response = client.get("/appcenter/cisco/ndfc/api/v1/fm/about/version")
    data = response.json()

    assert response.status_code == 200
    assert data["version"] == "12.1.2e"
    assert data["mode"] == "LAN"
    assert data["isMediaController"] is False
    assert data["dev"] is False
    assert data["isHaEnabled"] is False
    assert data["install"] == "EASYFABRIC"
    assert data["is_upgrade_inprogress"] is False
    print(f"data: {json.dumps(data, indent=4)}")


def test_v1_fm_features_get_100(client: TestClient):
    """
    # Summary

    Verify successful GET request.

    ## Endpoint

    GET /appcenter/cisco/ndfc/api/v1/fm/features
    """
    response = client.get("/appcenter/cisco/ndfc/api/v1/fm/features")
    data = response.json()

    assert response.status_code == 200
    assert "apidoc" in data["data"]["features"]
    assert "change-mgmt" in data["data"]["features"]
    assert "elasticservice" in data["data"]["features"]
    assert "features" in data["data"]
    assert "vxlan" in data["data"]["features"]

    print(f"data: {json.dumps(data, indent=4)}")
