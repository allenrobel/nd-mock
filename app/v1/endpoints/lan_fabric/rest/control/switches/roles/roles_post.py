#!/usr/bin/env python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ........common.enums.switch import SwitchRoleEnum, SwitchRoleFriendlyEnum
from ........common.functions.utilities import switch_role_external_to_db
from ........db import get_session
from .......models.inventory import SwitchDbModel
from ...switches.models.switch_overview import SwitchOverviewRoles

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches",
)


class SwitchRoleUpdate(BaseModel):
    """
    # Summary

    POST request body for updating switch roles.
    """

    serialNumber: str
    role: str


def build_200_response(success_list):
    """
    # Summary

    Build a response for a 200 success.
    """
    return {"successList": ",".join(success_list), "errorList": []}


def build_400_response(success_list, failure_list):
    """
    # Summary

    Build a response for a 400 error.
    """
    error_list = []
    for failure in failure_list:
        fail_dict = {}
        fail_dict["serialNumber"] = failure
        fail_dict["Reason"] = "Invalid Switch (or) Switch not in inventory"
        error_list.append(fail_dict)
    return {
        "successList": ",".join(success_list),
        "errorList": error_list,
    }


def update_sw_overview_role(session: Session, fabric_name: str, current_role: str, new_role: str):
    """
    # Summary

    Update the switch roles portion of the overview table.

    current_role should be in external format e.g. "border gateway", not "border_gateway".
    new_role should be in external format e.g. "border gateway", not "border_gateway".
    """
    instance = SwitchOverviewRoles()
    instance.session = session
    instance.fabric = fabric_name
    if current_role != "":
        instance.role = current_role
        instance.remove()
    instance.role = new_role
    instance.add()


@router.post("/roles")
def v1_roles_post(*, session: Session = Depends(get_session), switch_roles: list[SwitchRoleUpdate]):
    """
    # Summary

    POST request handler for updating switch roles.
    """
    success_list = []
    failure_list = []
    result_code = 200
    for switch_role in switch_roles:
        db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.serialNumber == switch_role.serialNumber)).first()
        if not db_switch:
            failure_list.append(switch_role.serialNumber)
            result_code = 400
        else:
            current_role = db_switch.switchRole
            new_role = switch_role.role
            if current_role == new_role:
                continue
            db_switch.switchRoleEnum = SwitchRoleEnum[switch_role_external_to_db(switch_role.role)].value
            db_switch.switchRole = SwitchRoleFriendlyEnum[switch_role_external_to_db(switch_role.role)].value
            session.add(db_switch)
            # TODO: We might create inconsistencies if we update the overview for one
            # switch, but the next switch in this request results in a 400 error.
            # We should consider updating the overview table only if all switches in the
            # request are valid (i.e. after session.commit() below).
            update_sw_overview_role(session, db_switch.fabricName, current_role, new_role)
            success_list.append(switch_role.serialNumber)
    if result_code == 400:
        detail = build_400_response(success_list, failure_list)
        raise HTTPException(status_code=result_code, detail=detail)
    session.commit()
    return build_200_response(success_list)
