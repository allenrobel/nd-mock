from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import ListSwitchesMetadata, ListSwitchesResponseBody, SwitchDataResponse, SwitchDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.get("/{fabric_name}/switches", response_model=ListSwitchesResponseBody)
def switches_get(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    offset: int = 0,
    limit: int = Query(default=100, le=100, alias="max"),
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    total = session.exec(select(func.count()).select_from(SwitchDbModel).where(SwitchDbModel.fabricName == fabric_name)).one()
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricName == fabric_name).offset(offset).limit(limit)).all()

    switches = [
        SwitchDataResponse(
            switchId=s.switchId,
            fabricManagementIp=s.fabricManagementIp,
            fabricName=s.fabricName,
            fabricType=s.fabricType,
            hostname=s.hostname,
            model=s.model,
            serialNumber=s.serialNumber,
            softwareVersion=s.softwareVersion,
            switchRole=s.switchRole,
            systemUpTime=s.systemUpTime,
            vpcConfigured=s.vpcConfigured,
        )
        for s in db_switches
    ]
    remaining = max(0, total - offset - len(switches))
    meta = ListSwitchesMetadata(total=total, remaining=remaining)
    return ListSwitchesResponseBody(meta=meta, switches=switches)
