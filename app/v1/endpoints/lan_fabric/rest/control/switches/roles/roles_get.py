#!/usr/bin/env python
# mypy: disable-error-code="attr-defined,arg-type"

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ........common.enums.switch import SwitchRoleFriendlyEnum
from ........db import get_session
from .......models.inventory import SwitchDbModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches",
)


class RolesGetResponse(BaseModel):
    """
    # Summary

    GET request response model.
    """

    serialNumber: str
    role: SwitchRoleFriendlyEnum


def build_200_response(success_list):
    """
    # Summary

    Build a response for a 200 success.
    """
    return {"successList": ",".join(success_list), "errorList": []}


@router.get("/roles")
def v1_roles_get(*, session: Session = Depends(get_session), switch_roles: list[RolesGetResponse], serialNumber: str = None):
    """
    # Summary

    GET request handler for retrieving switch roles.

    ## Notes

    1.  We disable the no-member pylint rule because the it complains about
        Instance of 'FieldInfo' has no 'in_' member (no-member)
    2.  We also disable mypy rules due to
        - error: "str" has no attribute "in_"  [attr-defined]
        - error: Argument "role" to "RolesGetResponse" has incompatible type
          "str"; expected "SwitchRoleFriendlyEnum"  [arg-type]
    # TODO: Look into fixing the arg-type mypy error
    """
    # pylint: disable=no-member
    switch_roles = []
    if not serialNumber:
        print("No serial number provided")
        db_switches = session.exec(select(SwitchDbModel)).all()
    else:
        serial_numbers = serialNumber.split(",")
        db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.serialNumber.in_(serial_numbers)))
    for db_switch in db_switches:
        if not db_switch.switchRole:
            continue
        switch_role = RolesGetResponse(serialNumber=db_switch.serialNumber, role=db_switch.switchRole)
        switch_roles.append(switch_role)
    return switch_roles
