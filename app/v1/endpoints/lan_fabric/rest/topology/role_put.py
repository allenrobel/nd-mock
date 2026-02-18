from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ......common.enums.switch import SwitchRoleEnum
from ......common.functions.utilities import switch_role_external_to_db
from ......db import get_session
from .....models.inventory import SwitchDbModel
from ..control.switches.models.switch_overview import SwitchOverviewRoles

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/topology/role",
)


class InternalRoleResponseModel(BaseModel):
    """
    # Summary

    The response body for a successful operation.
    """

    tierLevel: int
    newRole: str


class TierLevelEnum(Enum):
    """
    # Summary

    The tier level for each switch role.
    """

    leaf: int = 3
    spine: int = 2
    borderGateway: int = 1
    borderGatewaySpine: int = 2


def build_success_response(switch_db: SwitchDbModel) -> dict[str, Any]:
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Response Body

    ```json
    {
        "tierLevel": 3,
        "newRole": "border gateway spine"
    }    ```
    """
    response_model = InternalRoleResponseModel(tierLevel=TierLevelEnum[switch_db.switchRoleEnum].value, newRole=switch_db.switchRole)
    return response_model.model_dump()


def http_exception_400_invalid_switch(switch_db_id: int) -> HTTPException:
    """
    # Summary

    Build a 400 response body for an invalid switch.

    ## Response Body

    ```json
    {
        "detail": "Invalid switchDbId. switchDbId=1"
    }
    ```
    """
    return HTTPException(status_code=400, detail=f"Invalid switchDbId. switchDbId={switch_db_id}")


def update_sw_overview_role(session: Session, fabric_name: str, current_role: str, new_role: str):
    """
    # Summary

    Update the switch roles portion of the overview table.
    """
    instance = SwitchOverviewRoles()
    instance.session = session
    instance.fabric = fabric_name
    if current_role != "":
        instance.role = current_role
        instance.remove()
    instance = SwitchOverviewRoles()
    instance.session = session
    instance.fabric = fabric_name
    instance.role = new_role
    instance.add()


@router.put(
    "/{switch_db_id}",
    response_model=InternalRoleResponseModel,
    description="(v1) Internal, change switch role.",
)
def v1_internal_role_put(
    *,
    session: Session = Depends(get_session),
    switch_db_id: int,
    newRole: str,
):
    """
    # Summary

    PUT request handler
    """
    role_from_query_param = newRole.replace("%20", " ").lower()
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.switchDbID == switch_db_id)).first()
    if not db_switch:
        raise http_exception_400_invalid_switch(switch_db_id)
    role_key = None
    try:
        role_key = switch_role_external_to_db(role_from_query_param)
    except KeyError as error:
        msg = f"Invalid role: {role_key}. "
        msg += "Maybe you need to replace spaces with %20? "
        msg += "For example: border gateway spine -> border%20gateway%20spine"
        raise HTTPException(status_code=400, detail=msg) from error

    current_role = db_switch.switchRole
    new_role = role_from_query_param
    if current_role == new_role:
        return build_success_response(db_switch)

    update_sw_overview_role(session, db_switch.fabricName, current_role, new_role)

    db_switch.switchRole = new_role
    db_switch.switchRoleEnum = SwitchRoleEnum[role_key].value
    session.add(db_switch)
    session.commit()
    session.refresh(db_switch)
    response = build_success_response(db_switch)
    return response
