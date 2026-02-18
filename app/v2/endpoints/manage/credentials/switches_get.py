from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from .....db import get_session
from ....models.credentials import SwitchCredentialDbModel, SwitchCredentials, SwitchCredentialsGetResponse

router = APIRouter(
    prefix="/api/v1/manage/credentials",
)


@router.get("/switches", response_model=SwitchCredentialsGetResponse)
def v2_credentials_switches_get(*, session: Session = Depends(get_session)):
    db_creds = session.exec(select(SwitchCredentialDbModel)).all()
    items = [
        SwitchCredentials(
            credentialStore=cred.credentialStore,
            fabricName=cred.fabricName,
            ip=cred.ip,
            switchId=cred.switchId,
            switchName=cred.switchName,
            switchUsername=cred.switchUsername,
            type=cred.type,
        )
        for cred in db_creds
    ]
    return SwitchCredentialsGetResponse(items=items)
