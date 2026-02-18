from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .......db import get_session
from ......models.fabric import FabricCreate, FabricDbModelV1, FabricResponseModel
from ..switches.models.switch_overview import SwitchOverview
from .common import build_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


@router.post(
    "/{fabric_name}/{template_name}",
    response_model=FabricResponseModel,
    description="(v1) Create a fabric.",
)
def v1_fabric_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    template_name: str,
    fabric: FabricCreate,
):
    """
    # Summary

    POST request handler
    """
    db_fabric = FabricDbModelV1.model_validate(fabric)
    setattr(db_fabric, "FABRIC_NAME", fabric_name)
    setattr(db_fabric, "FF", template_name)

    session.add(db_fabric)
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        msg = f"ND Site with name {fabric_name} already exists."
        raise HTTPException(status_code=500, detail=msg) from error
    session.refresh(db_fabric)

    overview = SwitchOverview()
    overview.fabric = db_fabric.FABRIC_NAME
    overview.session = session
    overview.initialize_db_table()

    response = build_response(db_fabric)
    return response
