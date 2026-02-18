#!/usr/bin/env python
from fastapi import APIRouter
from pydantic import BaseModel

from ..models.login import LoginResponseModel

router = APIRouter(
    prefix="",
)


class LoginRequestBodyModel(BaseModel):
    """
    # Summary

    The body of a POST request to the login endpoint.
    """

    domain: str
    userName: str
    userPasswd: str


def build_rbac(body: LoginRequestBodyModel) -> dict:
    """
    # Summary

    Build the RBAC portion of the response
    """
    roles: list = []
    roles.append(["admin", "WritePriv"])
    roles.append(["app-user", "ReadPriv"])
    rbac = {}
    rbac["domain"] = body.domain
    rbac["rolesR"] = 16777216
    rbac["rolesW"] = 1
    rbac["roles"] = roles
    return rbac


def build_response(body: LoginRequestBodyModel) -> dict:
    """
    # Summary

    Build a login response that aligns with LoginResponseModel

    ## Notes

    1. If LoginResponseModel is changed, this function must also be updated
    """
    response = {}
    response["jwttoken"] = "asdlfkjasdf"
    response["username"] = body.userName
    response["usertype"] = body.domain
    response["rbac"] = [build_rbac(body)]
    response["statusCode"] = 200
    response["token"] = "asdlfkjasdf"
    return response


@router.post(
    "/login",
    response_model=LoginResponseModel,
)
def login_post(body: LoginRequestBodyModel) -> dict:
    """
    # Summary

    Simulate a Nexus Dashboard login response.
    """
    response = LoginResponseModel(**build_response(body))
    return response.model_dump()
