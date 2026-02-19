# mypy: disable-error-code=call-arg
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CredentialTypeEnum(str, Enum):
    default = "default"
    custom = "custom"
    robot = "robot"


class SwitchCredentials(BaseModel):
    credentialStore: str = "local"
    fabricName: str
    ip: str
    switchId: str
    switchName: str
    switchUsername: str
    type: CredentialTypeEnum = CredentialTypeEnum.custom


class SwitchCredentialsGetResponse(BaseModel):
    items: List[SwitchCredentials]


class SwitchCredentialsPostRequest(BaseModel):
    switchIds: List[str]
    switchUsername: Optional[str] = None
    switchPassword: Optional[str] = None
    remoteCredentialStoreKey: Optional[str] = None
    remoteCredentialStoreType: Optional[str] = None


class SwitchCredentialDbModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    switchId: str = Field(index=True, unique=True)
    switchUsername: str = "admin"
    switchPassword: str = "*****"
    fabricName: str = ""
    ip: str = ""
    switchName: str = ""
    credentialStore: str = "local"
    type: str = "custom"
