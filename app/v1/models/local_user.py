# mypy: disable-error-code=call-arg
from typing import List

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class RolesModel(BaseModel):
    roles: List[str] = []


class RBACModel(BaseModel):
    domains: dict[str, RolesModel] = {}
    tenantDomain: str = ""


class PasswordPolicyGetModel(BaseModel):
    passwordChangeTime: str = "0001-01-01T00:00:00Z"
    reuseLimitation: int = 0
    timeIntervalLimitation: int = 0


class PasswordPolicyWriteModel(BaseModel):
    reuseLimitation: int = 0
    timeIntervalLimitation: int = 0


class LocalUserPostModel(BaseModel):
    email: str = ""
    firstName: str = ""
    lastName: str = ""
    loginID: str
    password: str
    passwordPolicy: PasswordPolicyWriteModel = PasswordPolicyWriteModel()
    rbac: RBACModel = RBACModel()
    remoteIDClaim: str = ""
    xLaunch: bool = False


class LocalUserPutModel(BaseModel):
    email: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    loginID: str | None = None
    password: str | None = None
    passwordPolicy: PasswordPolicyWriteModel | None = None
    rbac: RBACModel | None = None
    remoteIDClaim: str | None = None
    xLaunch: bool | None = None


class LocalUserGetModel(BaseModel):
    accountStatus: str = "Active"
    email: str = ""
    firstName: str = ""
    lastName: str = ""
    loginID: str
    passwordPolicy: PasswordPolicyGetModel = PasswordPolicyGetModel()
    rbac: RBACModel = RBACModel()
    remoteIDClaim: str = ""
    userID: str = ""
    xLaunch: bool = False


class LocalUsersListResponse(BaseModel):
    localusers: List[dict]


class LocalUserDbModel(SQLModel, table=True):
    loginID: str = Field(primary_key=True)
    userID: str = ""
    accountStatus: str = Field(default="Active")
    email: str = Field(default="")
    firstName: str = Field(default="")
    lastName: str = Field(default="")
    rbac: str = Field(default="{}")
    passwordPolicy: str = Field(default="{}")
    remoteIDClaim: str = Field(default="")
    xLaunch: bool = Field(default=False)
