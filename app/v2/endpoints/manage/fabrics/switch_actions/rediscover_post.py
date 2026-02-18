from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModelV2
from .....models.switch import RediscoverRequestBody, SwitchDbModelV2

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/switchActions/rediscover", status_code=202)
def v2_switch_rediscover_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: RediscoverRequestBody,
):
    db_fabric = session.get(FabricDbModelV2, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    for switch_id in body.switchIds:
        db_switch = session.get(SwitchDbModelV2, switch_id)
        if not db_switch or db_switch.fabricName != fabric_name:
            detail = {"code": 404, "description": "", "message": f"Switch {switch_id} not found in fabric {fabric_name}"}
            raise HTTPException(status_code=404, detail=detail)
    return {}
