from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.local_user import LocalUserDbModel, LocalUserGetModel
from .local_user_post import build_response

router = APIRouter(
    prefix="/api/v1/infra/aaa/localUsers",
)


@router.get("/{pathLoginId}", response_model=LocalUserGetModel)
def local_user_get(*, session: Session = Depends(get_session), pathLoginId: str):
    user = session.get(LocalUserDbModel, pathLoginId)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {pathLoginId} not found")
    return build_response(user).model_dump()
