#!/usr/bin/env python
# pylint: disable=unused-import
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=invalid-name
# mypy: disable-error-code=union-attr
import inspect
import json

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.v1.models.local_user import LocalUserDbModel, LocalUserGetModel
from ..common import client_fixture, session_fixture
from .data_loader import load_data

print_test_info = True


def load_test_data(file_name: str, test_name: str):
    data = load_data(file_name)[test_name]
    if print_test_info:
        test_info = data.pop("test_info", None)
        print(f"info: {json.dumps(test_info, indent=4, sort_keys=True)}")
    return data


def _seed_user(session: Session, login_id: str = "testuser1") -> LocalUserDbModel:
    user = LocalUserDbModel(
        loginID=login_id,
        userID="00000000-0000-0000-0000-000000000001",
        accountStatus="Active",
        email=f"{login_id}@example.com",
        firstName="Test",
        lastName="User",
        rbac=json.dumps({"domains": {"all": {"roles": ["Admin"]}}, "tenantDomain": ""}),
        passwordPolicy=json.dumps({"passwordChangeTime": "2024-01-01T00:00:00Z", "reuseLimitation": 3, "timeIntervalLimitation": 24}),
        remoteIDClaim="",
        xLaunch=False,
    )
    session.add(user)
    session.commit()
    return user


def test_v1_local_user_post_100(client: TestClient):
    """
    Verify a successful POST request.
    """
    test_name = inspect.currentframe().f_code.co_name
    response = client.post(
        "/api/v1/infra/aaa/localUsers",
        json=load_test_data("local_user.json", test_name),
    )
    data = response.json()

    assert response.status_code == 200
    for key in LocalUserGetModel.model_fields.keys():
        assert key in data
    assert data["loginID"] == "testuser1"
    assert data["accountStatus"] == "Active"
    assert data["userID"] != ""
    assert "passwordChangeTime" in data["passwordPolicy"]


def test_v1_local_user_post_200(session: Session, client: TestClient):
    """
    Verify duplicate POST returns error.
    """
    _seed_user(session)
    test_name = inspect.currentframe().f_code.co_name
    response = client.post(
        "/api/v1/infra/aaa/localUsers",
        json=load_test_data("local_user.json", test_name),
    )
    assert response.status_code == 500
    data = response.json()
    assert data["detail"]["code"] == 500


def test_v1_local_user_get_100(session: Session, client: TestClient):
    """
    Verify GET request for all local users.
    """
    _seed_user(session, "user1")
    _seed_user(session, "user2")

    response = client.get("/api/v1/infra/aaa/localUsers")
    data = response.json()

    assert response.status_code == 200
    assert "localusers" in data
    assert len(data["localusers"]) == 2


def test_v1_local_user_get_110(session: Session, client: TestClient):
    """
    Verify GET request by loginID.
    """
    _seed_user(session)

    response = client.get("/api/v1/infra/aaa/localUsers/testuser1")
    data = response.json()

    assert response.status_code == 200
    assert data["loginID"] == "testuser1"
    assert data["email"] == "testuser1@example.com"
    assert data["userID"] == "00000000-0000-0000-0000-000000000001"


def test_v1_local_user_get_120(client: TestClient):
    """
    Verify GET request for nonexistent user returns 404.
    """
    response = client.get("/api/v1/infra/aaa/localUsers/nonexistent")
    assert response.status_code == 404


def test_v1_local_user_put_100(session: Session, client: TestClient):
    """
    Verify PUT request updates user fields.
    """
    _seed_user(session)

    update_data = {
        "email": "updated@example.com",
        "firstName": "Updated",
        "lastName": "Name",
    }
    response = client.put("/api/v1/infra/aaa/localUsers/testuser1", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "updated@example.com"
    assert data["firstName"] == "Updated"
    assert data["lastName"] == "Name"
    assert data["loginID"] == "testuser1"


def test_v1_local_user_put_110(client: TestClient):
    """
    Verify PUT request for nonexistent user returns 404.
    """
    response = client.put("/api/v1/infra/aaa/localUsers/nonexistent", json={"email": "x@x.com"})
    assert response.status_code == 404


def test_v1_local_user_delete_100(session: Session, client: TestClient):
    """
    Verify DELETE request.
    """
    _seed_user(session)

    response = client.delete("/api/v1/infra/aaa/localUsers/testuser1")
    assert response.status_code == 204

    user_in_db = session.get(LocalUserDbModel, "testuser1")
    assert user_in_db is None


def test_v1_local_user_delete_110(client: TestClient):
    """
    Verify DELETE request for nonexistent user returns 404.
    """
    response = client.delete("/api/v1/infra/aaa/localUsers/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["code"] == 404
    assert data["detail"]["message"] == "User nonexistent not found"
