#!/usr/bin/env python
import copy
import uuid

from fastapi import APIRouter

from ......models.fm.about.version import V1FmAboutVersionResponseModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/about",
)


def build_response():
    """
    # Summary

    Build a response that aligns with the ResponseModel

    ## Notes

    1. If V1FmAboutVersionResponseModel is changed, this function must also be updated
    """
    response = {}
    response["version"] = "12.1.2e"
    response["mode"] = "LAN"
    response["isMediaController"] = False
    response["dev"] = False
    response["isHaEnabled"] = False
    response["install"] = "EASYFABRIC"
    response["uuid"] = f"{uuid.uuid4()}"
    response["is_upgrade_inprogress"] = False
    return copy.deepcopy(response)


@router.get(
    "/version",
    response_model=V1FmAboutVersionResponseModel,
)
def v1_version_get():
    """
    # Summary

    GET request handler for fm/about/version
    """
    return build_response()
