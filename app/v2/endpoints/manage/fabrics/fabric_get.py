from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.fabric import FabricDbModelV2, FabricResponseModel
from .common import FabricLocationModel, FabricManagementModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


def build_response(fabric: FabricDbModelV2) -> FabricResponseModel:
    """
    # Summary

    Build the representation of the fabric in the response.
    """
    location = FabricLocationModel(
        latitude=fabric.latitude,
        longitude=fabric.longitude,
    )
    management = FabricManagementModel(
        bgpAsn=fabric.bgpAsn,
        type=fabric.type,
    )
    response: FabricResponseModel = FabricResponseModel(
        alertSuspend=fabric.alertSuspend,
        name=fabric.name,
        category=fabric.category,
        licenseTier=fabric.licenseTier,
        location=location.model_dump(),
        management=management.model_dump(),
        securityDomain=fabric.securityDomain,
        telemetryCollection=fabric.telemetryCollection,
        telemetryCollectionType=fabric.telemetryCollectionType,
        telemetryStreamingProtocol=fabric.telemetryStreamingProtocol,
        telemetrySourceInterface=fabric.telemetrySourceInterface,
        telemetrySourceVrf=fabric.telemetrySourceVrf,
    )
    return response


@router.get(
    "/{fabric_name}",
    response_model=FabricResponseModel,
)
def v2_fabric_get(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    fabric = session.get(FabricDbModelV2, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(fabric)
    return response.model_dump()
