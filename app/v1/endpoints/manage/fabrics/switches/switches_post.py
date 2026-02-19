from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import AddSwitchesRequestBody, SwitchDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/switches", status_code=202)
def switches_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: AddSwitchesRequestBody,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    for switch in body.switches:
        db_switch = SwitchDbModel(
            switchId=switch.serialNumber,
            fabricName=fabric_name,
            fabricManagementIp=switch.ip,
            hostname=switch.hostname,
            model=switch.model,
            serialNumber=switch.serialNumber,
            softwareVersion=switch.softwareVersion or "",
            switchRole=switch.switchRole or "leaf",
        )
        session.add(db_switch)
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=500, detail={"code": 500, "description": "", "message": f"Failed to add switches: {error}"}) from error
    return {}
