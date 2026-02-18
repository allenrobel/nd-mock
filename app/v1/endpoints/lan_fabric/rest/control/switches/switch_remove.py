from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1
from ......models.inventory import SwitchDbModel
from ..fabrics.common import build_404_response
from ..switches.models.switch_overview import SwitchOverviewHealth, SwitchOverviewHw, SwitchOverviewRoles, SwitchOverviewSw, SwitchOverviewSync

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def update_health(db_session: Session, fabric_name: str, health: str) -> None:
    """
    # Summary

    Update the switch health information associated with SwitchOverview.
    """
    if health == "":
        return
    instance = SwitchOverviewHealth()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.health = health
    instance.remove()


def update_hw(db_session: Session, fabric_name: str, model: str) -> None:
    """
    # Summary

    Update the switch hardware information associated with SwitchOverview.
    """
    if model == "":
        return
    instance = SwitchOverviewHw()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.model = model
    instance.remove()


def update_role(db_session: Session, fabric_name: str, role: str) -> None:
    """
    # Summary

    Update the switch role information associated with SwitchOverview.
    """
    if role == "":
        return
    instance = SwitchOverviewRoles()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.role = role
    instance.remove()


def update_sw(db_session: Session, fabric_name: str, release: str) -> None:
    """
    # Summary

    Update the switch software information associated with SwitchOverview.
    """
    if release == "":
        return
    instance = SwitchOverviewSw()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.version = release
    instance.remove()


def update_sync(db_session: Session, fabric_name: str, sync: str) -> None:
    """
    # Summary

    Update the switch sync information associated with SwitchOverview.
    """
    if sync == "":
        return
    instance = SwitchOverviewSync()
    instance.session = db_session
    instance.fabric = fabric_name
    instance.sync = sync.lower().replace("-", "_")
    instance.remove()


def remove_switch_from_fabric(session: Session, db_fabric: FabricDbModelV1, serial_number: str) -> bool:
    """
    # Summary

    Remove one switch (specified by switch serial_number) from the fabric
    contained in db_fabric.

    ## Parameters

    session: Session
        The database session.
    db_fabric: FabricDbModelV1
        The fabric from which to remove the switch.
    serial_number: str
        The serial number of the switch to remove.

    ## Returns

    ### bool

    - True if the switch was removed and a session commit is required
    - False otherwise.

    ## Raises

    None
    """
    fabric_id = db_fabric.id
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id).where(SwitchDbModel.serialNumber == serial_number)).first()
    if db_switch is None:
        return False

    fabric_name = db_fabric.FABRIC_NAME

    if fabric_name is None:
        return False

    health = db_switch.operStatus
    model = db_switch.model
    release = db_switch.release
    role = db_switch.switchRole
    sync = db_switch.ccStatus

    update_health(session, fabric_name, health)
    update_hw(session, fabric_name, model)
    update_role(session, fabric_name, role)
    update_sw(session, fabric_name, release)
    update_sync(session, fabric_name, sync)

    session.delete(db_switch)
    return True


description = "(v1) Remove the switch(es), "
description += "specified by serialNumbers, a comma-separated list of "
description += "switch serial numbers, from the fabric specified by fabricName."


@router.delete("/{fabricName}/switches/{serialNumbers}", description=description, summary=description)
def v1_remove_switches_from_fabric(*, session: Session = Depends(get_session), fabricName: str, serialNumbers: str) -> str:
    """
    # Summary

    Switch DELETE request handler

    ## Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/switches/{serialNumber}

    ## Notes

    -   This endpoint supports the removal of one or more switches from a fabric.
    -   The serialNumber query parameter (serial_number here) can be a single serial_number,
        or a comma-separated list of serial_number.

    ## Example responses

    -   The switch(es)=FOX2109PGCS have been removed from the fabric=F1
    -   The switch(es)=FOX2109PGD1,FOX2109PGCS,FOX2109PGD0,FDO211218HH have been removed from the fabric=F1
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabricName)).first()
    if not db_fabric:
        path = f"{router.prefix}/{fabricName}/switches/{serialNumbers}"
        raise HTTPException(status_code=404, detail=build_404_response(path))

    commit = set()
    serial_numbers = serialNumbers.split(",")
    for serial_number in serial_numbers:
        commit.add(remove_switch_from_fabric(session, db_fabric, serial_number))

    if True in commit:
        session.commit()
    # NDFC response
    # The switch(es)=FOX2109PGCS have been removed from the fabric=F1
    # The switch(es)=FOX2109PGD1,FOX2109PGCS,FOX2109PGD0,FDO211218HH have been removed from the fabric=F1
    # NDFC returns 200 whether or not the switch (or switches) were actually removed.
    return f"The switch(es)={serialNumbers} have been removed from the fabric={fabricName}"
