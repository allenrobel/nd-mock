#!/usr/bin/env python
import copy
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ........db import get_session
from .......models.fabric import FabricDbModelV1
from .......models.inventory import SwitchDbModel, SwitchResponseModel
from .common import build_response_switch

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


def build_success_response():
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    response = {"status": "Success"}
    return copy.deepcopy(response)


@router.get(
    "/{fabric_name}/inventory/switchesByFabric",
    response_model=List[SwitchResponseModel],
)
def v1_inventory_switches_by_fabric_get(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    Return a list of switches hosted in fabric_name.

    ## Endpoint

    ### Verb

    GET

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/switchesByFabric
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    fabric_id = db_fabric.id
    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).all()
    if len(db_switches) == 0:
        return []
    return [build_response_switch(db_switch) for db_switch in db_switches]
