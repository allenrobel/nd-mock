from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1, FabricResponseModel, FabricUpdate
from .common import build_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.put(
    "/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
    description="(v1) Modify a fabric.",
)
def v1_fabric_put(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    fabric: FabricUpdate,
):
    """
    # Summary

    PUT request handler
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_data = fabric.model_dump(exclude_unset=True)

    for key, value in fabric_data.items():
        setattr(db_fabric, key, value)

    session.add(db_fabric)
    session.commit()
    session.refresh(db_fabric)
    response = build_response(db_fabric)
    return response
