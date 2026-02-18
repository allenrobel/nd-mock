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


class GetLanSwitchCredentialsWithTypeItem(BaseModel):
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


def build_success_response(db_switch, db_fabric) -> GetLanSwitchCredentialsWithTypeItem:
    """
    # Summary

    Build a 200 response body for a successful operation.

    ## Notes

    """
    return GetLanSwitchCredentialsWithTypeItem(
        credType="Robot",
        groupName=db_fabric.FABRIC_NAME,
        ipAddress=db_switch.ipAddress,
        sshPassword="*****",
        sshUserName="admin",
        switchDbID=str(db_switch.switchDbID),
        switchName=db_switch.hostName,
        v3Protocol="0",
    )


@router.get("/getLanSwitchCredentialsWithType")
def v1_getLanSwitchCredentialsWithType(*, session: Session = Depends(get_session)) -> List[GetLanSwitchCredentialsWithTypeItem | None]:
    """
    # Summary

    Get LAN Switch credentials.

    ## Endpoint

    ### Verb

    GET

    ### Path
    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig/getLanSwitchCredentialsWithType
    """
    db_fabric = session.exec(select(FabricDbModelV1)).first()
    if not db_fabric:
        return []
    fabric_id = db_fabric.id
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricId == fabric_id)).first()
    if not db_switch:
        return []
    return [build_success_response(db_switch, db_fabric)]
