#!/usr/bin/env python

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ........common.functions.utilities import random_switch_serial_number, random_unicast_mac_address
from ........db import get_session
from .......models.fabric import FabricDbModelV1
from .......models.inventory import SwitchDbModel

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


class ReachabilityRequestBodyModel(BaseModel):
    """
    # Summary

    The body of a POST request to the test-reachability endpoint.

    {
        "maxHops": 0,
        "seedIP":"{{switch_ip4}}",
        "cdpSecondTimeout":5,
        "snmpV3AuthProtocol":0,
        "username":"{{nxos_username}}",
        "password":"{{nxos_password}}",
        "preserveConfig":false
    }
    """

    maxHops: int
    seedIP: str
    cdpSecondTimeout: int
    snmpV3AuthProtocol: int
    username: str
    password: str
    preserveConfig: bool


class ReachabilityResponseModel(BaseModel):
    """
    # Summary

    The response body of a POST request to the test-reachability
    endpoint.

    ```json
    {
        "auth": true,
        "deviceIndex": "cvd-2211-spine(FOX2109PHDD)",
        "hopCount": 0,
        "ipaddr": "172.22.150.114",
        "known": false,
        "lastChange": null,
        "platform": "N9K-C9504",
        "reachable": true,
        "selectable": true,
        "serialNumber": "FOX2109PHDD",
        "statusReason": "manageable",
        "switchRole": null,
        "sysName": "cvd-2211-spine",
        "valid": true,
        "vdcId": 0,
        "vdcMac": null,
        "vendor": "Cisco",
        "version": "10.2(5)"
    }
    ```
    """

    auth: bool
    deviceIndex: str | None
    hopCount: int
    ipaddr: str | None
    known: bool
    lastChange: str | None
    platform: str | None
    reachable: bool
    selectable: bool
    serialNumber: str | None
    statusReason: str
    switchRole: str | None
    sysName: str | None
    valid: bool
    vdcId: int
    vdcMac: str | None
    vendor: str | None
    version: str | None


def build_response_already_managed(switch: SwitchDbModel) -> ReachabilityResponseModel:
    """
    # Summary

    Given a SwitchDbModel object, return a populated ReachabilityResponseModel
    object with the statusReason set to "already managed in {fabric_name}".

    ```json
    {
        "auth": true,
        "deviceIndex": "cvd-111-dci(FDO2443096H)",
        "hopCount": 0,
        "ipaddr": "172.22.150.99",
        "known": true,
        "lastChange": null,
        "platform": "N9K-C9336C-FX2",
        "reachable": true,
        "selectable": false,
        "serialNumber": "FDO2443096H",
        "statusReason": "already managed in F1",
        "sysName": "cvd-111-dci",
        "valid": true,
        "vdcId": 0,
        "vdcMac": null,
        "version": "10.2(2)"
    }
    ```
    """
    return ReachabilityResponseModel(
        auth=True,
        deviceIndex=f"{switch.hostName}({switch.serialNumber})",
        hopCount=0,
        ipaddr=switch.ipAddress,
        known=True,
        lastChange=None,
        platform=switch.model,
        reachable=True,
        selectable=False,
        serialNumber=switch.serialNumber,
        statusReason=f"already managed in {switch.fabricName}",
        switchRole=switch.switchRole,
        sysName=switch.hostName,
        valid=True,
        vdcId=0,
        vdcMac=None,
        vendor=switch.vendor,
        version=switch.version,
    )


def build_response_manageable(switch: SwitchDbModel) -> ReachabilityResponseModel:
    """
    # Summary

    Given a SwitchDbModel object, return a populated ReachabilityResponseModel
    object with the statusReason set to "manageable".
    """
    return ReachabilityResponseModel(
        auth=True,
        deviceIndex=f"{switch.hostName}({switch.serialNumber})",
        hopCount=0,
        ipaddr=switch.ipAddress,
        known=False,
        lastChange=None,
        platform=switch.model,
        reachable=True,
        selectable=True,
        serialNumber=switch.serialNumber,
        statusReason="manageable",
        switchRole=None,
        sysName=switch.hostName,
        valid=True,
        vdcId=0,
        vdcMac=None,
        vendor="Cisco",
        version=switch.version,
    )


def build_response_manageable_force(ip_address: str) -> ReachabilityResponseModel:
    """
    # Summary

    Given a SwitchDbModel object, return a populated ReachabilityResponseModel
    object with the statusReason set to "manageable" by generating a random
    mac address for a new switch.

    ```json
    {
        "auth": false,
        "deviceIndex": "switch(random_mac_address())",
        "hopCount": 0,
        "ipaddr": "10.1.1.2",
        "known": false,
        "lastChange": null,
        "platform": null,
        "reachable": false,
        "selectable": false,
        "serialNumber": null,
        "statusReason": "not reachable",
        "switchRole": null,
        "sysName": "10.1.1.2",
        "valid": false,
        "vdcId": 0,
        "vdcMac": null,
        "vendor": null,
        "version": null
    }
    ```
    """
    hostname = "switch"
    mac_address = random_unicast_mac_address()
    serial_number = random_switch_serial_number()
    print(f"hostname: {hostname}, mac_address: {mac_address}, serial_number: {serial_number}")
    return ReachabilityResponseModel(
        auth=True,
        deviceIndex=f"{hostname}({serial_number})",
        hopCount=0,
        ipaddr=ip_address,
        known=False,
        lastChange=None,
        platform="N9K-C93180YC-EX",
        reachable=True,
        selectable=True,
        serialNumber=serial_number,
        statusReason="manageable",
        switchRole=None,
        sysName=hostname,
        valid=True,
        vdcId=0,
        vdcMac=None,
        vendor="Cisco",
        version="10.2(5)",
    )


def build_response_not_reachable(ip_address: str) -> ReachabilityResponseModel:
    """
    # Summary

    Given a SwitchDbModel object, return a populated ReachabilityResponseModel
    object with the statusReason set to "manageable" by generating a random
    mac address for a new switch.

    ```json
    {
        "auth": false,
        "deviceIndex": "10.1.1.2",
        "hopCount": 0,
        "ipaddr": "10.1.1.2",
        "known": false,
        "lastChange": null,
        "platform": null,
        "reachable": false,
        "selectable": false,
        "serialNumber": null,
        "statusReason": "not reachable",
        "switchRole": null,
        "sysName": "10.1.1.2",
        "valid": false,
        "vdcId": 0,
        "vdcMac": null,
        "vendor": null,
        "version": null
    }
    ```
    """
    return ReachabilityResponseModel(
        auth=False,
        deviceIndex=ip_address,
        hopCount=0,
        ipaddr=ip_address,
        known=False,
        lastChange=None,
        platform=None,
        reachable=False,
        selectable=False,
        serialNumber=None,
        statusReason="not reachable",
        switchRole=None,
        sysName=ip_address,
        valid=False,
        vdcId=0,
        vdcMac=None,
        vendor=None,
        version=None,
    )


@router.post("/{fabric_name}/inventory/test-reachability")
def v1_inventory_test_reachability_post(
    *, session: Session = Depends(get_session), fabric_name: str, test_reachability_body: ReachabilityRequestBodyModel
) -> list[ReachabilityResponseModel]:
    """
    # Summary

    Test reachability of switch and return result.

    ## Endpoint

    ### Verb

    POST

    ### Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/test-reachability
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        raise HTTPException(status_code=404, detail=f"Fabric {fabric_name} not found")
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.ipAddress == test_reachability_body.seedIP)).first()
    if not db_switch:
        response = build_response_manageable_force(test_reachability_body.seedIP)
    elif db_switch.fabricName == fabric_name and db_switch.switchRoleEnum == "":
        response = build_response_manageable(db_switch)
    elif db_switch.fabricName == fabric_name and db_switch.switchRoleEnum != "":
        response = build_response_already_managed(db_switch)
    elif db_switch.fabricName != fabric_name:
        response = build_response_already_managed(db_switch)
    elif db_switch.fabricName == "":
        response = build_response_manageable(db_switch)
    else:
        raise HTTPException(status_code=500, detail=f"Unhandled db_switch state. {db_switch.model_dump()}")
    return [response]
