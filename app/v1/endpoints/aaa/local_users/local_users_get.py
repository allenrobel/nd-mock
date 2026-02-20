import copy

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .....db import get_session
from ....models.local_user import LocalUserDbModel, LocalUsersListResponse
from .local_user_post import build_response

router = APIRouter(
    prefix="/api/v1/infra/aaa",
)


@router.get("/localUsers", response_model=LocalUsersListResponse)
def local_users_get(*, session: Session = Depends(get_session)) -> LocalUsersListResponse:
    try:
        users = session.exec(select(LocalUserDbModel)).all()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    response = []
    for user in users:
        response.append(copy.deepcopy(build_response(user).model_dump()))
    return LocalUsersListResponse(localusers=response)
