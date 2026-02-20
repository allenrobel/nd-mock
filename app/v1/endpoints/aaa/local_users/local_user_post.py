import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.local_user import (
    LocalUserDbModel,
    LocalUserGetModel,
    LocalUserPostModel,
    PasswordPolicyGetModel,
    RBACModel,
)

router = APIRouter(
    prefix="/api/v1/infra/aaa",
)


def build_response(db_user: LocalUserDbModel) -> LocalUserGetModel:
    rbac = RBACModel(**json.loads(db_user.rbac))
    password_policy = PasswordPolicyGetModel(**json.loads(db_user.passwordPolicy))
    return LocalUserGetModel(
        accountStatus=db_user.accountStatus,
        email=db_user.email,
        firstName=db_user.firstName,
        lastName=db_user.lastName,
        loginID=db_user.loginID,
        passwordPolicy=password_policy,
        rbac=rbac,
        remoteIDClaim=db_user.remoteIDClaim,
        userID=db_user.userID,
        xLaunch=db_user.xLaunch,
    )


def build_db_user(user: LocalUserPostModel) -> LocalUserDbModel:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    password_policy = {
        "passwordChangeTime": now,
        "reuseLimitation": user.passwordPolicy.reuseLimitation,
        "timeIntervalLimitation": user.passwordPolicy.timeIntervalLimitation,
    }
    return LocalUserDbModel(
        loginID=user.loginID,
        userID=str(uuid.uuid4()),
        accountStatus="Active",
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
        rbac=json.dumps(user.rbac.model_dump()),
        passwordPolicy=json.dumps(password_policy),
        remoteIDClaim=user.remoteIDClaim,
        xLaunch=user.xLaunch,
    )


@router.post("/localUsers", response_model=LocalUserGetModel)
async def local_user_post(*, session: Session = Depends(get_session), user: LocalUserPostModel):
    db_user = session.get(LocalUserDbModel, user.loginID)
    if db_user:
        status_code = 500
        msg = f"User {user.loginID} already exists"
        error_response = {"code": status_code, "description": "", "message": msg}
        raise HTTPException(status_code=status_code, detail=error_response)
    db_user = build_db_user(user)
    session.add(db_user)
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        status_code = 500
        msg = f"Unknown error. Detail: {error}"
        error_response = {"code": status_code, "description": "", "message": msg}
        raise HTTPException(status_code=status_code, detail=error_response) from error
    session.refresh(db_user)
    return build_response(db_user)
