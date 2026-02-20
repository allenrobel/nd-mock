import json

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.local_user import LocalUserDbModel, LocalUserGetModel, LocalUserPutModel
from .local_user_post import build_response

router = APIRouter(
    prefix="/api/v1/infra/aaa/localUsers",
)


@router.put("/{pathLoginId}", response_model=LocalUserGetModel)
def local_user_put(*, session: Session = Depends(get_session), pathLoginId: str, user: LocalUserPutModel):
    db_user = session.get(LocalUserDbModel, pathLoginId)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {pathLoginId} not found")
    user_data = user.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        if key == "rbac":
            db_user.rbac = json.dumps(value)
        elif key == "passwordPolicy":
            existing = json.loads(db_user.passwordPolicy)
            existing.update(value)
            db_user.passwordPolicy = json.dumps(existing)
        elif key == "password":
            pass
        else:
            setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return build_response(db_user)
