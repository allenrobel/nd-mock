#!/usr/bin/env python
import copy

from fastapi import APIRouter

from ....models.fm_features import V1FmFeaturesResponseModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/fm",
)


def build_change_mgmt():
    """
    # Summary

    Build the response change-mgmt object
    """
    d = {}
    d["name"] = "Change Control"
    d["description"] = "Tracking, Approval, and Rollback of all Configuration Changes"
    d["ui"] = False
    d["predisablecheck"] = "https://dcnm-lan-fabric.cisco-ndfc.svc:9443/rest/chngmgmt/preDisableCheck"
    d["spec"] = ""
    d["admin_state"] = "disabled"
    d["oper_state"] = ""
    d["kind"] = "featurette"
    d["featureset"] = {}
    d["featureset"]["lan"] = {}
    d["featureset"]["lan"]["default"] = False
    return copy.deepcopy(d)


def build_cvisualizer():
    """
    # Summary

    Build the response cvisualizer object
    """
    d = {}
    d["name"] = "Kubernetes Visualizer"
    d["description"] = "Network Visualization of K8s Clusters"
    d["ui"] = False
    d["spec"] = ""
    d["admin_state"] = "disabled"
    d["oper_state"] = ""
    d["kind"] = "feature"
    d["featureset"] = {}
    d["featureset"]["lan"] = {}
    d["featureset"]["lan"]["default"] = False
    return copy.deepcopy(d)


def build_elasticservice():
    """
    # Summary

    Build the response elasticservice object
    """
    d = {}
    d["name"] = "L4-L7 Services"
    d["description"] = "L4-L7 Services"
    d["ui"] = True
    d["hidden"] = True
    d["spec"] = ""
    d["admin_state"] = "enabled"
    d["oper_state"] = "started"
    d["installed"] = "2024-02-05 19:12:57.098455128 +0000 UTC"
    d["kind"] = "feature"
    d["featureset"] = {}
    d["featureset"]["lan"] = {}
    d["featureset"]["lan"]["default"] = True
    return copy.deepcopy(d)


def build_apidoc():
    """
    # Summary

    Build the response apidoc object
    """
    d = {}
    d["url"] = "https://dcnm-elasticservice.cisco-ndfc.svc:9443/v3/api-docs"
    d["subpath"] = "elastic-service"
    d["schema"] = None
    return copy.deepcopy(d)


def build_vxlan():
    """
    # Summary

    Build the response vxlan object
    """
    d = {}
    d["name"] = "Fabric Builder"
    d["description"] = "Automation, Compliance, and Management for NX-OS and Other devices"
    d["ui"] = False
    d["predisablecheck"] = "https://dcnm-lan-fabric.cisco-ndfc.svc:9443/rest/control/fabrics/lanVXLANPreDisableCheck"
    d["spec"] = ""
    d["admin_state"] = "enabled"
    d["oper_state"] = "started"
    d["kind"] = "feature"
    d["featureset"] = {}
    d["featureset"]["lan"] = {}
    d["featureset"]["lan"]["default"] = True
    d["apidoc"] = []
    apidoc = {}
    apidoc["url"] = "https://sgm.cisco-ndfc.svc:9443/api-docs"
    apidoc["subpath"] = ""
    apidoc["schema"] = None
    d["apidoc"].append(apidoc)
    return copy.deepcopy(d)


def build_response():
    """
    # Summary

    Build a response that aligns with the ResponseModel

    ## Notes

    1. If V1FmAboutVersionResponseModel is changed, this function must also be updated
    """
    response = {}
    response["status"] = "success"
    response["data"] = {}
    response["data"]["name"] = ""
    response["data"]["version"] = 201
    response["data"]["features"] = {}
    response["data"]["features"]["change-mgmt"] = build_change_mgmt()
    response["data"]["features"]["cvisualizer"] = build_cvisualizer()
    response["data"]["features"]["elasticservice"] = build_elasticservice()
    response["data"]["features"]["apidoc"] = build_apidoc()
    response["data"]["features"]["vxlan"] = build_vxlan()

    return copy.deepcopy(response)


@router.get(
    "/features",
    response_model=V1FmFeaturesResponseModel,
    description="(v1) Get status of features.",
)
def v1_fm_features_get():
    """
    # Summary

    GET request handler for Feature Manager features.
    """
    return build_response()
