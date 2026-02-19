from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel
from .common import FabricLocationModel, FabricManagementModel

router = APIRouter(
    prefix="/api/v1/manage",
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


def build_db_fabric(fabric):
    """
    # Summary

    Build the representation of the fabric in the database.
    """
    fabric_dict = fabric.model_dump()
    db_fabric = FabricDbModel()
    db_fabric.alertSuspend = fabric.alertSuspend
    db_fabric.name = fabric.name
    db_fabric.category = fabric.category
    db_fabric.licenseTier = fabric.licenseTier
    db_fabric.bgpAsn = fabric_dict.get("management", {}).get("bgpAsn")
    db_fabric.type = fabric_dict.get("management", {}).get("type")
    db_fabric.latitude = fabric_dict.get("location", {}).get("latitude")
    db_fabric.longitude = fabric_dict.get("location", {}).get("longitude")
    db_fabric.securityDomain = fabric.securityDomain
    db_fabric.telemetryCollection = fabric.telemetryCollection
    db_fabric.telemetryCollectionType = fabric.telemetryCollectionType
    db_fabric.telemetryStreamingProtocol = fabric.telemetryStreamingProtocol
    db_fabric.telemetrySourceInterface = fabric.telemetrySourceInterface
    db_fabric.telemetrySourceVrf = fabric.telemetrySourceVrf
    return db_fabric


@router.post("/fabrics", response_model=FabricResponseModel)
async def fabric_post(*, session: Session = Depends(get_session), fabric: FabricResponseModel):
    """
    # Summary

    POST request handler
    """
    db_fabric = session.get(FabricDbModel, fabric.name)
    if db_fabric:
        status_code = 500
        msg = f"[Fabric {db_fabric.name} is already present in the cluster "
        msg += f"A fabric with name {db_fabric.name} is already in use on "
        msg += "this cluster]"
        error_response = {}
        error_response["code"] = status_code
        error_response["description"] = ""
        error_response["message"] = msg
        raise HTTPException(status_code=status_code, detail=error_response)
    db_fabric = build_db_fabric(fabric)
    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        status_code = 500
        msg = f"Unknown error. Detail: {error}"
        error_response = {}
        error_response["code"] = status_code
        error_response["description"] = ""
        error_response["message"] = msg
        raise HTTPException(status_code=status_code, detail=error_response) from error
    session.refresh(db_fabric)
    if db_fabric is None:
        raise HTTPException(status_code=500, detail="Failed to create fabric")
    return build_response(db_fabric)
