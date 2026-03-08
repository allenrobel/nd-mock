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
    if not body.username:
        detail = {"code": 0, "description": "", "message": "username cannot be empty or missing"}
        raise HTTPException(status_code=400, detail=detail)

    if not body.snmpV3AuthProtocol:
        detail = {"code": 0, "description": "", "message": "snmpV3AuthProtocol cannot be empty or missing"}
        raise HTTPException(status_code=400, detail=detail)

    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "errors": None, "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    for switch in body.switches:
        existing = session.get(SwitchDbModel, switch.serialNumber)
        if existing:
            detail = {"code": 400, "description": "", "errors": None, "message": f"Switch with serial number {switch.serialNumber} already exists in fabric {existing.fabricName}"}
            raise HTTPException(status_code=400, detail=detail)

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
        raise HTTPException(status_code=500, detail={"code": 500, "description": "", "errors": None, "message": f"Failed to add switches: {error}"}) from error
    return {}
