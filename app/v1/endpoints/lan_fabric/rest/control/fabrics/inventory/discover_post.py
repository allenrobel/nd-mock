#!/usr/bin/env python

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ........db import get_session
from .......models.fabric import FabricDbModelV1
from .......models.inventory import SwitchDbModel, SwitchDiscoverBodyModel
from ...switches.models.switch_overview import SwitchOverviewHealth, SwitchOverviewHw, SwitchOverviewRoles, SwitchOverviewSw, SwitchOverviewSync
from .common import build_db_switch

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def build_success_response():
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    return {"status": "Success"}


def update_health(db_session: Session, fabric_name: str, health: str):
    """
    # Summary

    Update the switch health information associated with SwitchOverview.
    """
    instance = SwitchOverviewHealth()
    instance.session = db_session
    instance.fabric = fabric_name
    # This initializes the table if it doesn't exist.
    instance.initialize_db_table()
    instance.health = health
    instance.add()


def update_hw(db_session: Session, fabric_name: str, model: str):
    """
    # Summary

    Update the switch hardware information associated with SwitchOverview.
    """
    instance = SwitchOverviewHw()
    instance.session = db_session
    instance.fabric = fabric_name
    # This initializes the table if it doesn't exist.
    instance.initialize_db_table()
    instance.model = model
    instance.add()


def update_role(db_session: Session, fabric_name: str, role: str):
    """
    # Summary

    Update the switch role information associated with SwitchOverview.
    """
    instance = SwitchOverviewRoles()
    instance.session = db_session
    instance.fabric = fabric_name
    # This initializes the table if it doesn't exist.
    instance.initialize_db_table()
    instance.role = role
    instance.add()


def update_sw(db_session: Session, fabric_name: str, version: str):
    """
    # Summary

    Update the switch software information associated with SwitchOverview.
    """
    instance = SwitchOverviewSw()
    instance.session = db_session
    instance.fabric = fabric_name
    # This initializes the table if it doesn't exist.
    instance.initialize_db_table()
    instance.version = version
    instance.add()


def update_sync(db_session: Session, fabric_name: str, sync: str):
    """
    # Summary

    Update the switch sync status information associated with SwitchOverview.
    """
    instance = SwitchOverviewSync()
    instance.session = db_session
    instance.fabric = fabric_name
    # This initializes the table if it doesn't exist.
    instance.initialize_db_table()
    instance.sync = sync
    instance.add()


@router.post("/{fabric_name}/inventory/discover")
def v1_inventory_discover_post(*, session: Session = Depends(get_session), fabric_name: str, switch_discovery_body: SwitchDiscoverBodyModel):
    """
    # Summary

    Discover switches for a given fabric_name.

    ## Endpoint

    ### Verb

    POST

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/discover
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_id = db_fabric.id
    # Get all switches in the fabric
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).all()
    # Raise an error if any switches in the discovery body already exist in the fabric
    for db_switch in db_switches:
        if db_switch.serialNumber in [discovery_body.serialNumber for discovery_body in switch_discovery_body.switches]:
            raise HTTPException(status_code=500, detail=f"Switch {db_switch.serialNumber} already exists in fabric {fabric_name}")
        if db_switch.ipAddress in [discovery_body.ipaddr for discovery_body in switch_discovery_body.switches]:
            raise HTTPException(status_code=500, detail=f"Switch {db_switch.ipAddress} already exists in fabric {fabric_name}")
    # Add all switches in the discovery body to the fabric
    for discovery_body in switch_discovery_body.switches:
        db_switch = build_db_switch(discovery_body, db_fabric)
        # For discovered switches, set their initial role to spine
        db_switch.switchRoleEnum = "spine"
        db_switch.switchRole = "spine"
        db_switch.ccStatus = "In-Sync"
        db_switch.operStatus = "Healthy"
        db_switch.fabricId = fabric_id
        session.add(db_switch)
    session.commit()
    # Update the switch overview tables
    for discovery_body in switch_discovery_body.switches:
        update_health(session, fabric_name=fabric_name, health="Healthy")
        update_hw(session, fabric_name=fabric_name, model=discovery_body.platform)
        update_role(session, fabric_name=fabric_name, role="spine")
        update_sw(session, fabric_name=fabric_name, version=discovery_body.version)
        update_sync(session, fabric_name=fabric_name, sync="in_sync")
    response = build_success_response()
    return response
