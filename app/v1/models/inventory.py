# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from typing import List

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel

from ...common.enums.switch import SwitchUnmanageableCauseEnum


class SwitchBase(SQLModel):
    """
    Base representation of a switch.
    """

    activeSupSlot: int
    availPorts: int
    ccStatus: str
    cfsSyslogStatus: int
    colDBId: int
    connUnitStatus: int
    consistencyState: bool
    contact: str | None
    cpuUsage: int
    deviceType: str
    displayHdrs: str | None
    displayValues: str | None
    domain: str | None
    domainID: int
    elementType: str | None
    fabricId: int
    fabricName: str
    fabricTechnology: str
    fcoeEnabled: bool
    fex: bool
    fid: int
    freezeMode: str | None
    health: int
    hostName: str
    index: int
    intentedpeerName: str
    interfaces: str | None
    ipAddress: str
    ipDomain: str
    isEchSupport: bool
    isLan: bool
    isNonNexus: bool
    isPmCollect: bool
    isSharedBorder: bool
    isTrapDelayed: bool
    isVpcConfigured: bool
    is_smlic_enabled: bool
    keepAliveState: str | None
    lastScanTime: int
    licenseDetail: str | None
    licenseViolation: bool
    linkName: str | None
    location: str | None = Field(default="")
    logicalName: str
    managable: bool
    mds: bool
    membership: str | None = Field(default="")
    memoryUsage: int
    mgmtAddress: str | None = Field(default="")
    mode: str
    model: str
    modelType: int
    moduleIndexOffset: int
    modules: str | None
    monitorMode: str | None
    name: str | None
    network: str | None
    nonMdsModel: str | None
    npvEnabled: bool
    numberOfPorts: int
    operMode: str | None
    operStatus: str
    peer: str | None
    peerSerialNumber: str | None
    peerSwitchDbId: int
    peerlinkState: str | None
    ports: int
    present: bool
    primaryIP: str
    primarySwitchDbID: int
    principal: str | None
    protoDiscSettings: str | None
    recvIntf: str | None
    release: str
    role: str | None
    sanAnalyticsCapable: bool
    scope: str | None
    secondaryIP: str
    secondarySwitchDbID: int
    sendIntf: str | None
    serialNumber: str
    sharedBorder: bool
    sourceInterface: str
    sourceVrf: str
    standbySupState: int
    status: str
    swType: str | None
    swUUID: str
    swUUIDId: int | None
    swWwn: str | None
    swWwnName: str | None
    switchDbID: int
    switchRole: str = Field(default="spine")
    switchRoleEnum: str = Field(default="spine")
    sysDescr: str
    systemMode: str = Field(default="Normal")
    uid: int
    unmanagableCause: str = Field(default=SwitchUnmanageableCauseEnum.none)
    upTime: int
    upTimeNumber: int
    upTimeStr: str
    usedPorts: int
    username: str | None
    vdcId: int
    vdcMac: str | None
    vdcName: str
    vendor: str
    version: str | None
    vpcDomain: int
    vrf: str
    vsanWwn: str | None
    vsanWwnName: str | None
    waitForSwitchModeChg: bool
    wwn: str | None

    class Config:
        """
        Configuration for the model.
        """

        use_enum_values = True
        validate_default = True


class SwitchResponseModel(SwitchBase):
    """
    Representation of a switch in a response.
    """

    fexMap: dict

    class Config:
        """
        Configuration for the model.
        """

        use_enum_values = True


class SwitchDbModel(SwitchBase, table=True):
    """
    Representation of a switch in the database.
    """

    model_config = ConfigDict(use_enum_values=True)

    hostName: str = Field(index=True)
    ipAddress: str = Field(index=True, unique=True)
    switchDbID: int | None = Field(default=None, primary_key=True)
    serialNumber: str = Field(index=True, unique=True)


class SwitchDiscoverItem(BaseModel):
    """
    Representation of a switch in a SwitchDiscoverBodyModel.
    """

    deviceIndex: str
    serialNumber: str
    sysName: str
    platform: str
    version: str
    ipaddr: str

    class Config:
        """
        Configuration for the model.
        """

        use_enum_values = True


class SwitchDiscoverSuccessResponseModel(BaseModel):
    """
    Representation of a switch discovery success response.
    """

    status: str

    class Config:
        """
        Configuration for the model.
        """

        use_enum_values = True


class SwitchDiscoverBodyModel(BaseModel):
    """
    Representation of a switch discovery request body.
    """

    seedIP: str
    username: str
    password: str
    preserveConfig: bool
    switches: List[SwitchDiscoverItem]

    class Config:
        """
        Configuration for the model.
        """

        use_enum_values = True
