# mypy: disable-error-code=call-arg
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Database models
# ---------------------------------------------------------------------------


class VrfDbModel(SQLModel, table=True):
    """VRF database model. Uses synthetic PK = '{fabricName}:{vrfName}'."""

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(primary_key=True)
    fabricName: str = Field(index=True)
    vrfName: str = Field(index=True)
    vrfType: str = ""
    vrfId: int = 0
    vlanId: int = 0
    vrfStatus: str = ""
    tenantName: str = ""
    extraData: str = Field(default="{}")


class VrfAttachmentDbModel(SQLModel, table=True):
    """VRF attachment database model. Uses synthetic PK = '{fabricName}:{vrfName}:{switchId}'."""

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(primary_key=True)
    fabricName: str = Field(index=True)
    vrfName: str = Field(index=True)
    switchId: str = Field(index=True)
    status: str = Field(default="notApplicable")
    attach: bool = Field(default=False)


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class VrfCreateItem(BaseModel):
    """A single VRF in a create request."""

    vrfName: str
    vrfType: Optional[str] = ""
    vrfId: Optional[int] = 0
    vlanId: Optional[int] = 0
    vrfStatus: Optional[str] = ""
    tenantName: Optional[str] = ""
    coreData: Optional[Dict[str, Any]] = None
    fabricData: Optional[Dict[str, Any]] = None


class VrfCreateRequestBody(BaseModel):
    """Request body for POST /fabrics/{fabricName}/vrfs."""

    vrfs: List[VrfCreateItem]


class VrfAttachmentQueryRequestBody(BaseModel):
    """Request body for POST /fabrics/{fabricName}/vrfAttachments/query."""

    switchIds: List[str] = []
    vrfNames: List[str] = []


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class VrfCreateResultItem(BaseModel):
    """Per-item result in a VRF create response."""

    status: str
    message: str = ""
    vrfName: str = ""
    vrfId: int = 0


class VrfCreateResponse(BaseModel):
    """Response for POST /fabrics/{fabricName}/vrfs (always 207)."""

    results: List[VrfCreateResultItem]


class VrfDataResponse(BaseModel):
    """Response model for a single VRF."""

    vrfName: str
    vrfType: str = ""
    vrfId: int = 0
    vlanId: int = 0
    vrfStatus: str = ""
    tenantName: str = ""
    fabricName: str = ""
    coreData: Optional[Dict[str, Any]] = None
    fabricData: Optional[Dict[str, Any]] = None


class VrfListCounts(BaseModel):
    """Counts inside the meta object for VRF list responses."""

    total: int
    remaining: int


class VrfListMeta(BaseModel):
    """Meta object for VRF list responses (uses nested 'counts' key)."""

    counts: VrfListCounts


class VrfListResponse(BaseModel):
    """Response for GET /fabrics/{fabricName}/vrfs."""

    vrfs: List[VrfDataResponse]
    meta: VrfListMeta


class VrfAttachmentItem(BaseModel):
    """Single attachment item in a query response."""

    attach: bool = False
    errorMessage: Optional[str] = None
    instanceValues: Dict[str, Any] = {}
    showVlan: bool = True
    status: str = "notApplicable"
    switchId: str = ""
    switchName: str = ""
    switchRole: str = ""
    vrfName: str = ""


class VrfAttachmentQueryResponse(BaseModel):
    """Response for POST /fabrics/{fabricName}/vrfAttachments/query."""

    attachments: List[VrfAttachmentItem]
    meta: VrfListMeta
