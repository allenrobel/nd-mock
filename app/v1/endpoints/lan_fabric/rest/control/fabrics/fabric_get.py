from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1, FabricResponseModel
from .common import build_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.get(
    "/{fabric_name}",
    response_model=FabricResponseModel,
    description="(v1) Get a fabric by fabric name.",
)
def v1_get_fabric_by_fabric_name(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    GET request handler with fabric_name as path parameter.
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    response = build_response(db_fabric)
    return response
