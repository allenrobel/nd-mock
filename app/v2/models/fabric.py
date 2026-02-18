# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel

from ...common.validators.fabric import BgpValue
from ..validators.fabric import FabricManagementType


class AlertSuspend(str, Enum):
    """
    Choices for the fabric alertSuspend parameter.
    """

    enabled = "enabled"
    disabled = "disabled"


class FabricCategoryEnum(Enum):
    """
    Choices for fabric category parameter.
    """

    fabric = "fabric"
    fabricGroup = "fabricGroup"
    multiClusterFabricGroup = "multiClusterFabricGroup"


class LicenseTier(str, Enum):
    """
    Choices for the fabric licenseTier parameter.
    """

    advantage = "advantage"
    essentials = "essentials"
    premier = "premier"


class ManagementTypeEnum(str, Enum):
    """
    Choices for the fabric management type parameter.
    """

    vxlanIbgp = "vxlanIbgp"
    vxlanEbgp = "vxlanEbgp"
    vxlanCampus = "vxlanCampus"
    aimlVxlanIbgp = "aimlVxlanIbgp"
    aimlVxlanEbgp = "aimlVxlanEbgp"
    aimlRouted = "aimlRouted"
    routed = "routed"
    classicLan = "classicLan"
    classicLanEnhanced = "classicLanEnhanced"
    ipfm = "ipfm"
    ipfmEnhanced = "ipfmEnhanced"
    ipfmGenericMulticast = "ipfmGenericMulticast"
    externalConnectivity = "externalConnectivity"
    vxlanExternal = "vxlanExternal"
    aci = "aci"
    meta = "meta"
    dataBroker = "dataBroker"


class TelemetryCollectionType(Enum):
    """
    Choices for the fabric telemetryCollectionType parameter.
    """

    inBand = "inBand"
    outOfBand = "outOfBand"


class TelemetryStreamingProtocol(Enum):
    """
    Choices for the fabric telemetryStreamingProtocol parameter.
    """

    ipv4 = "ipv4"
    ipv6 = "ipv6"


class FabricManagement(SQLModel):
    """
    Contents of the fabric management object.
    TODO: Add remaining parameters per management type.
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)

    bgpAsn: str | int | None = None
    type: str


class FabricLocation(BaseModel):
    """
    Contents of the fabric location object.
    """

    latitude: float
    longitude: float


class FabricsListMeta(BaseModel):
    """
    Metadata for the fabrics list response.
    """

    total: int
    remaining: int


class FabricsListResponse(BaseModel):
    """
    Wrapper response model for GET /fabrics.
    """

    fabrics: List[dict]
    meta: FabricsListMeta


class FabricResponseModel(SQLModel):
    """
    Representation of the fabric in a response.
    """

    model_config = ConfigDict(use_enum_values=True, coerce_numbers_to_str=True)

    alertSuspend: str = Field(default="disabled")
    category: str = Field(FabricCategoryEnum)
    licenseTier: str = Field(default="premier")
    location: dict = Field(FabricLocation)
    management: FabricManagementType = Field(FabricManagement)
    name: str
    securityDomain: str | None = "all"
    telemetryCollection: bool = Field(default=False)
    telemetryCollectionType: str = Field(TelemetryCollectionType)
    telemetryStreamingProtocol: str = Field(TelemetryStreamingProtocol)
    telemetrySourceInterface: str | None = None
    telemetrySourceVrf: str | None = None


class FabricDbModelV2(SQLModel, table=True):
    """
    Representation of the fabric in the database.

    TODO: Need to add remaining parameters.
    """

    model_config = ConfigDict(use_enum_values=True)

    alertSuspend: str = Field(default="disabled")
    bgpAsn: BgpValue | None = Field(default=None)
    type: str
    latitude: float
    longitude: float
    category: str = Field(FabricCategoryEnum)
    licenseTier: str = Field(default="premier")
    name: str = Field(primary_key=True)
    securityDomain: str = Field(default="all")
    telemetryCollection: bool = Field(default=False)
    telemetryCollectionType: str = Field(TelemetryCollectionType)
    telemetryStreamingProtocol: str = Field(TelemetryStreamingProtocol)
    telemetrySourceInterface: str | None = Field(default="")
    telemetrySourceVrf: str | None = Field(default="")
