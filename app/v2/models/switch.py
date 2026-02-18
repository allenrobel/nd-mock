# mypy: disable-error-code=call-arg
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel


class SwitchRoleEnum(str, Enum):
    leaf = "leaf"
    spine = "spine"
    border = "border"
    border_spine = "border_spine"
    border_gateway = "border_gateway"
    border_gateway_spine = "border_gateway_spine"
    super_spine = "super_spine"
    border_super_spine = "border_super_spine"
    access = "access"
    aggregation = "aggregation"
    edge_router = "edge_router"
    core_router = "core_router"
    tor = "tor"
    controller = "controller"


class SwitchDataResponse(BaseModel):
    """Response model for a single switch (matches manage.json switchData schema)."""

    switchId: str
    fabricManagementIp: str = ""
    fabricName: str = ""
    fabricType: str = ""
    hostname: str = ""
    model: str = ""
    serialNumber: str = ""
    softwareVersion: str = ""
    switchRole: str = "leaf"
    systemUpTime: str = ""
    vpcConfigured: bool = False


class ListSwitchesMetadata(BaseModel):
    total: int
    remaining: int


class ListSwitchesResponseBody(BaseModel):
    """Response model for GET /fabrics/{fabricName}/switches."""

    meta: ListSwitchesMetadata
    switches: List[SwitchDataResponse]


class SwitchDiscoveryItem(BaseModel):
    hostname: str
    ip: str
    serialNumber: str
    model: str
    softwareVersion: Optional[str] = None
    switchRole: Optional[str] = "leaf"
    vdcId: Optional[int] = None
    vdcMac: Optional[str] = None


class AddSwitchesRequestBody(BaseModel):
    switches: List[SwitchDiscoveryItem]
    password: Optional[str] = None
    platformType: Optional[str] = "nx-os"
    preserveConfig: Optional[bool] = True


class SwitchRoleData(BaseModel):
    role: str
    switchId: str


class SwitchRoleBody(BaseModel):
    switchRoles: List[SwitchRoleData]


class SwitchOperationStatus(BaseModel):
    status: str
    message: str = ""
    switchId: str = ""


class ChangeSwitchRoleResponse(BaseModel):
    items: List[SwitchOperationStatus]


class RediscoverRequestBody(BaseModel):
    switchIds: List[str]


class CounterNameValue(BaseModel):
    name: str
    count: int


class SwitchesSummaryResponse(BaseModel):
    anomalyLevel: List[CounterNameValue] = []
    configSyncStatus: List[CounterNameValue] = []
    role: List[CounterNameValue] = []
    softwareVersion: List[CounterNameValue] = []


class SwitchDbModelV2(SQLModel, table=True):
    """V2 switch database model."""

    model_config = ConfigDict(use_enum_values=True)

    switchId: str = Field(primary_key=True)
    fabricName: str = Field(index=True)
    fabricManagementIp: str = ""
    fabricType: str = ""
    hostname: str = ""
    model: str = ""
    serialNumber: str = Field(index=True, unique=True)
    softwareVersion: str = ""
    switchRole: str = Field(default="leaf")
    systemUpTime: str = ""
    vpcConfigured: bool = Field(default=False)
