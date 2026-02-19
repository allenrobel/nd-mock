import copy
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricResponseModel, FabricsListMeta, FabricsListResponse
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


@router.get(
    "/fabrics",
    response_model=FabricsListResponse,
)
def fabrics_get(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> FabricsListResponse:
    """
    # Summary

    Endpoint handler for GET /api/v1/manage/fabrics
    """
    try:
        total = session.exec(select(func.count()).select_from(FabricDbModel)).one()
        fabrics = session.exec(select(FabricDbModel).offset(offset).limit(limit)).all()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    response = []
    response_fabric: dict[Any, Any] = {}
    try:
        for fabric in fabrics:
            response_fabric = FabricResponseModel.model_dump(build_response(fabric))
            response.append(copy.deepcopy(response_fabric))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    remaining = max(0, total - offset - len(response))
    meta = FabricsListMeta(total=total, remaining=remaining)
    return FabricsListResponse(fabrics=response, meta=meta)
