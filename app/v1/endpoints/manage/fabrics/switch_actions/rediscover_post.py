from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import RediscoverRequestBody, SwitchDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/switchActions/rediscover", status_code=202)
def switch_rediscover_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: RediscoverRequestBody,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    for switch_id in body.switchIds:
        db_switch = session.get(SwitchDbModel, switch_id)
        if not db_switch or db_switch.fabricName != fabric_name:
            detail = {"code": 404, "description": "", "message": f"Switch {switch_id} not found in fabric {fabric_name}"}
            raise HTTPException(status_code=404, detail=detail)
    return {}
