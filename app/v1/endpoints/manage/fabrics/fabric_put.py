#!/usr/bin/env python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel
from .common import FabricLocationModel, FabricManagementModel

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


@router.put(
    "/{fabric_name}",
    response_model=FabricResponseModel,
)
def fabric_put(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricResponseModel,
):
    """
    # Summary

    PUT request handler

    ## Notes to future self

    -   Nested key handling below will break when we add
        nested keys under management to the model, e.g.
        .netflowSettings, .leafTorVpcPortChannelIdRange, etc.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)

    nested_keys = ["management", "location"]
    for key, value in fabric_data.items():
        if key in nested_keys:
            for nested_key, nested_value in value.items():
                setattr(db_fabric, nested_key, nested_value)
        else:
            setattr(db_fabric, key, value)

    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response
