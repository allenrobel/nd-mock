from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .....db import get_session
from ....models.credentials import SwitchCredentialDbModel, SwitchCredentialsPostRequest

router = APIRouter(
    prefix="/api/v1/manage/credentials",
)


@router.post("/switches", status_code=200)
def credentials_switches_post(*, session: Session = Depends(get_session), body: SwitchCredentialsPostRequest):
    for switch_id in body.switchIds:
        existing = session.exec(select(SwitchCredentialDbModel).where(SwitchCredentialDbModel.switchId == switch_id)).first()
        if existing:
            existing.switchUsername = body.switchUsername or existing.switchUsername
            existing.switchPassword = body.switchPassword or existing.switchPassword
            session.add(existing)
        else:
            db_cred = SwitchCredentialDbModel(
                switchId=switch_id,
                switchUsername=body.switchUsername or "admin",
                switchPassword=body.switchPassword or "*****",
            )
            session.add(db_cred)
    try:
        session.commit()
    except Exception as error:
        session.rollback()
        raise HTTPException(status_code=500, detail={"code": 500, "description": "", "message": f"Failed to save credentials: {error}"}) from error
    return {}
