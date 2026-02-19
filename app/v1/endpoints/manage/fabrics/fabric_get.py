import json

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel
from .common import FabricLocationModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


def build_response(fabric: FabricDbModel) -> FabricResponseModel:
    """
    # Summary

    Build the representation of the fabric in the response.
    """
    location = FabricLocationModel(
        latitude=fabric.latitude,
        longitude=fabric.longitude,
    )
    management = json.loads(fabric.management)
    response: FabricResponseModel = FabricResponseModel(
        alertSuspend=fabric.alertSuspend,
        name=fabric.name,
        category=fabric.category,
        licenseTier=fabric.licenseTier,
        location=location.model_dump(),
        management=management,
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
def fabric_get(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    fabric = session.get(FabricDbModel, fabric_name)
    if not fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(fabric)
    return response.model_dump()
