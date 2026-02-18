#!/usr/bin/env python

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ......db import get_session
from .....models.fabric import FabricDbModelV1
from .....models.inventory import SwitchDbModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig",
)


class GetLanSwitchCredentialsItem(BaseModel):
    """
    # Summary

    A response model for the getLanSwitchCredentialsWithType endpoint.

    ```json
    {
        "credType": "Robot",
        "groupName": "F1",
        "ipAddress": "172.22.150.107",
        "sshPassword": "*****",
        "sshUserName": "admin",
        "switchDbID": "27470",
        "switchName": "cvd-2312-leaf",
        "v3Protocol": "0"
    }
    ```
    """

    credType: str
    groupName: str
    ipAddress: str
    sshPassword: str
    sshUserName: str
    switchDbID: str
    switchName: str
    v3Protocol: str


def build_success_response(db_switch, db_fabric) -> GetLanSwitchCredentialsItem:
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    return GetLanSwitchCredentialsItem(
        credType="Robot",
        groupName=db_fabric.FABRIC_NAME,
        ipAddress=db_switch.ipAddress,
        sshPassword="*****",
        sshUserName="admin",
        switchDbID=str(db_switch.switchDbID),
        switchName=db_switch.hostName,
        v3Protocol="0",
    )


@router.get("/getLanSwitchCredentials")
def v1_getLanSwitchCredentials(*, session: Session = Depends(get_session)) -> List[GetLanSwitchCredentialsItem | None]:
    """
    # Summary

    Get LAN Switch credentials.

    This is an internal (unpublished) endpoint used by ansible-dcnm dcnm_inventory module.

    Once we modify the ansible-dcnm dcnm_inventory module to use the new endpoint, we can
    remove this endpoint handler.

    ## Endpoint

    ### Verb

    GET

    ### Path
    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig/getLanSwitchCredentials
    """
    db_fabric = session.exec(select(FabricDbModelV1)).first()
    if not db_fabric:
        return []
    fabric_id = db_fabric.id
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).first()
    if not db_switch:
        return []
    return [build_success_response(db_switch, db_fabric)]
