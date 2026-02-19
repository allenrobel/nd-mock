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
# Disable mypy errors from using the following:
#     test_name = inspect.currentframe().f_code.co_name
# mypy: disable-error-code=union-attr
import inspect
import json

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.fabric import FabricDbModel, FabricResponseModel
from ..common import client_fixture, convert_db_date_to_timestamp, convert_model_date_to_timestamp, session_fixture, timestamps_within_delta
from .data_loader import load_data

print_test_info = True


def load_test_data(file_name: str, test_name: str):
    """
    # Summary

    Load the test data

    ## Parameters

    file_name: The JSON file from which to load the data.
        Example: fabric.json
    test_name: The key within the JSON file containing the data.
        Example: test_v1_fabric_post_100
    """
    data = load_data(file_name)[test_name]
    if print_test_info:
        test_info = data.pop("test_info", None)
        print(f"info: {json.dumps(test_info, indent=4, sort_keys=True)}")
    return data


def test_v1_fabric_post_100(client: TestClient):
    """
    # Summary

    Verify a successful POST request.
    """
    test_name = inspect.currentframe().f_code.co_name
    response = client.post(
        "/api/v1/manage/fabrics",
        json=load_test_data("fabric.json", test_name),
    )
    data = response.json()

    assert response.status_code == 200
    for key in FabricResponseModel.model_fields.keys():
        assert key in data


def test_v1_fabric_post_200(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 500 status_code is returned when management.bgpAsn is missing
    from the body of the POST request.
    """
    test_name = inspect.currentframe().f_code.co_name
    response = client.post(
        "/api/v1/manage/fabrics",
        json=load_test_data("fabric.json", test_name),
    )
    assert response.status_code == 500


def test_v1_fabric_post_210(client: TestClient):
    """
    # Summary

    Verify an unsuccessful POST request.

    A 500 status_code is returned when management.bgpAsn is an
    invalid format in the body of the POST request i.e. fails
    regex validation.
    """
    test_name = inspect.currentframe().f_code.co_name
    response = client.post(
        "/api/v1/manage/fabrics",
        json=load_test_data("fabric.json", test_name),
    )
    assert response.status_code == 500


def test_v1_fabric_post_300(client: TestClient):
    """
    # Summary

    Verify full management object is stored and returned on POST + GET.
    """
    test_name = inspect.currentframe().f_code.co_name
    post_data = load_test_data("fabric.json", test_name)
    management_sent = post_data["management"].copy()

    response = client.post("/api/v1/manage/fabrics", json=post_data)
    data = response.json()

    assert response.status_code == 200
    # bgpAsn is coerced to string
    management_sent["bgpAsn"] = str(management_sent["bgpAsn"])
    assert data["management"] == management_sent

    response = client.get(f"/api/v1/manage/fabrics/{post_data['name']}")
    data = response.json()

    assert response.status_code == 200
    assert data["management"] == management_sent


def test_v1_fabric_get_100(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request for all fabrics.

    1. Create two fabrics.
    3. Commit the fabrics.
    4. Send a GET request to retrieve all fabrics.
    5. Verify response
        -   status_code == 200
        -   management.bgpAsn == expected BGP AS
        -   name == expected fabric name
        -   location.lataitude == expected latitude
        -   location.longitude == expected longitude
    """
    f1 = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "fabric"}',
        category="fabric",
        latitude=71.1,
        longitude=61.1,
        licenseTier="advantage",
        name="f1",
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/1",
        telemetrySourceVrf="vrf_1",
        telemetryStreamingProtocol="ipv4",
    )
    f2 = FabricDbModel(
        management='{"bgpAsn": "65002", "type": "fabric"}',
        category="fabric",
        latitude=72.2,
        longitude=62.2,
        licenseTier="premier",
        name="f2",
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/2",
        telemetrySourceVrf="vrf_2",
        telemetryStreamingProtocol="ipv6",
    )
    session.add(f1)
    session.add(f2)
    session.commit()

    response = client.get("/api/v1/manage/fabrics")
    data = response.json()

    assert response.status_code == 200
    assert "fabrics" in data
    assert "meta" in data
    assert data["meta"]["total"] == 2
    assert data["meta"]["remaining"] == 0
    fabrics = data["fabrics"]
    assert len(fabrics) == 2
    assert fabrics[0]["name"] == "f1"
    assert fabrics[0].get("management", {}).get("bgpAsn") == "65001"
    assert fabrics[0].get("location", {}).get("longitude") == 61.1
    assert fabrics[0].get("location", {}).get("latitude") == 71.1
    assert fabrics[1]["name"] == "f2"
    assert fabrics[1].get("management", {}).get("bgpAsn") == "65002"
    assert fabrics[1].get("location", {}).get("longitude") == 62.2
    assert fabrics[1].get("location", {}).get("latitude") == 72.2


def test_v1_fabric_get_110(session: Session, client: TestClient):
    """
    # Summary

    Verify GET request with fabric_name in the path.

    1. Create fabric
    2. Send GET request with fabric_name in the path.
    3. Verify the response
        -   status_code == 200
        -   management.bgpAsn == expected BGP AS
        -   name == expected fabric name
        -   location.lataitude == expected latitude
        -   location.longitude == expected longitude
    """
    f1 = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "fabric"}',
        category="fabric",
        name="f1",
        latitude=71.1,
        longitude=61.1,
        licenseTier="advantage",
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceVrf="vrf_1",
        telemetrySourceInterface="Ethernet1/1",
        telemetryStreamingProtocol="ipv4",
    )
    session.add(f1)
    session.commit()

    response = client.get(f"/api/v1/manage/fabrics/{f1.name}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "f1"
    assert data.get("management", {}).get("bgpAsn") == "65001"
    assert data.get("location", {}).get("latitude") == 71.1
    assert data.get("location", {}).get("longitude") == 61.1


def test_v1_fabric_put_100(session: Session, client: TestClient):
    """
    # Summary

    Verify PUT request updates fabric parameters.

        1. Create fabric
        2. GET request to retrieve fabric
        3. Verify fabric parameters
        4. PUT request to update fabric parameters
        3. Verify the PUT response
            a. location.latitude is updated
            b. location.longitude is updated
            d. telemetryCollectionType is updated
            e. telemetryStreamingProtocol is updated
    """
    f1 = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "fabric"}',
        category="fabric",
        latitude=71.1,
        longitude=61.1,
        licenseTier="advantage",
        name="f1",
        securityDomain="all",
        telemetryCollectionType="inBand",
        telemetrySourceInterface="Ethernet1/1",
        telemetrySourceVrf="vrf_1",
        telemetryStreamingProtocol="ipv4",
    )
    session.add(f1)
    session.commit()

    response = client.get(f"/api/v1/manage/fabrics/{f1.name}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "f1"
    assert data.get("management", {}).get("bgpAsn") == "65001"
    assert data.get("location", {}).get("latitude") == 71.1
    assert data.get("location", {}).get("longitude") == 61.1
    assert data.get("telemetryCollectionType") == "inBand"
    assert data.get("telemetryStreamingProtocol") == "ipv4"

    print(f"data: {data}")

    new_data = {
        "location": {
            "latitude": 72.1,
            "longitude": 62.1,
        },
        "telemetryStreamingProtocol": "ipv6",
        "telemetryCollectionType": "outOfBand",
    }
    data |= new_data
    print(f"data: {data}")

    response = client.put(f"/api/v1/manage/fabrics/{f1.name}", json=data)
    print(f"response: {response}")

    data = response.json()

    assert response.status_code == 200
    assert data.get("location", {}).get("latitude") == 72.1
    assert data.get("location", {}).get("longitude") == 62.1
    assert data.get("telemetryCollectionType") == "outOfBand"
    assert data.get("telemetryStreamingProtocol") == "ipv6"


def test_v1_fabric_delete_100(session: Session, client: TestClient):
    """
    # Summary

    1. Create fabric
    2. Delete fabric

    Verify that fabric is deleted with 204 status_code.
    """
    f1 = FabricDbModel(
        management='{"bgpAsn": "65001", "type": "fabric"}',
        category="fabric",
        latitude=60.1,
        longitude=60.1,
        licenseTier="advantage",
        name="f1",
        securityDomain="all",
        telemetryStreamingProtocol="ipv6",
        telemetryCollectionType="inBand",
        telemetrySourceVrf="management",
        telemetrySourceInterface="Ethernet1/1",
    )
    session.add(f1)
    session.commit()

    response = client.delete(f"/api/v1/manage/fabrics/{f1.name}")
    fabric_in_db = session.get(FabricDbModel, f1.name)

    assert response.status_code == 204

    assert fabric_in_db is None


def test_v1_fabric_delete_110(session: Session, client: TestClient):
    """
    # Summary

    Attempt to delete a fabric that does not exist

    Verify the response.
    """
    response = client.delete("/api/v1/manage/fabrics/foo")
    fabric_in_db = session.get(FabricDbModel, "foo")

    response_decode = response.json()
    print(f"response_decode: {response_decode}")
    assert response.status_code == 404
    assert response_decode["detail"]["code"] == 404
    assert response_decode["detail"]["description"] == ""
    assert response_decode["detail"]["message"] == "Fabric foo not found"

    assert fabric_in_db is None
