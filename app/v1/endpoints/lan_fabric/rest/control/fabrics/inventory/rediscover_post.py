#!/usr/bin/env python

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ........db import get_session
from .......models.fabric import FabricDbModelV1
from .......models.inventory import SwitchDbModel

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


@router.post("/{fabric_name}/inventory/rediscover/{serial_number}")
def v1_inventory_rediscover_post(*, session: Session = Depends(get_session), fabric_name: str, serial_number: str):
    """
    # Summary

    Rediscover a switch in fabric fabric_name with serial number serial_number.

    ## Endpoint

    ### Verb

    POST

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/rediscover/{serial_number}
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_id = db_fabric.id
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id).where(SwitchDbModel.serialNumber == serial_number)).first()
    if not db_switch:
        raise HTTPException(status_code=500, detail=f"Invalid Serial Number or IP address. serialNumber={serial_number}")
    db_switch.status = "ok"
    session.add(db_switch)
    session.commit()
    return build_success_response()
