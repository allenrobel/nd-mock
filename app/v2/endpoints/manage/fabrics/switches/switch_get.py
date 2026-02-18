from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.switch import SwitchDataResponse, SwitchDbModelV2

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.get("/{fabric_name}/switches/{switch_id}", response_model=SwitchDataResponse)
def v2_switch_get(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    switch_id: str,
):
    db_switch = session.get(SwitchDbModelV2, switch_id)
    if not db_switch or db_switch.fabricName != fabric_name:
        detail = {"code": 404, "description": "", "message": f"Switch {switch_id} not found in fabric {fabric_name}"}
        raise HTTPException(status_code=404, detail=detail)
    return SwitchDataResponse(
        switchId=db_switch.switchId,
        fabricManagementIp=db_switch.fabricManagementIp,
        fabricName=db_switch.fabricName,
        fabricType=db_switch.fabricType,
        hostname=db_switch.hostname,
        model=db_switch.model,
        serialNumber=db_switch.serialNumber,
        softwareVersion=db_switch.softwareVersion,
        switchRole=db_switch.switchRole,
        systemUpTime=db_switch.systemUpTime,
        vpcConfigured=db_switch.vpcConfigured,
    )
