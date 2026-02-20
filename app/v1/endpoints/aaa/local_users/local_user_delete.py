from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.local_user import LocalUserDbModel

router = APIRouter(
    prefix="/api/v1/infra/aaa/localUsers",
)


@router.delete("/{pathLoginId}", status_code=204)
async def local_user_delete(*, session: Session = Depends(get_session), pathLoginId: str):
    user = session.get(LocalUserDbModel, pathLoginId)
    if not user:
        detail = {"code": 404, "description": "", "message": f"User {pathLoginId} not found"}
        raise HTTPException(status_code=404, detail=detail)
    session.delete(user)
    session.commit()
    return {}
