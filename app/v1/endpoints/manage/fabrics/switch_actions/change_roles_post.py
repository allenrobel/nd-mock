from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import ChangeSwitchRoleResponse, SwitchDbModel, SwitchOperationStatus, SwitchRoleBody

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/switchActions/changeRoles", status_code=207, response_model=ChangeSwitchRoleResponse)
def switch_change_roles_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: SwitchRoleBody,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    items = []
    for role_data in body.switchRoles:
        db_switch = session.get(SwitchDbModel, role_data.switchId)
        if not db_switch or db_switch.fabricName != fabric_name:
            items.append(SwitchOperationStatus(status="failure", message=f"Switch {role_data.switchId} not found", switchId=role_data.switchId))
            continue
        db_switch.switchRole = role_data.role
        session.add(db_switch)
        items.append(SwitchOperationStatus(status="success", message="Role changed successfully", switchId=role_data.switchId))

    session.commit()
    return ChangeSwitchRoleResponse(items=items)
