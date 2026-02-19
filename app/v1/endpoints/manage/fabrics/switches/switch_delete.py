from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ......db import get_session
from .....models.switch import SwitchDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.delete("/{fabric_name}/switches/{switch_id}", status_code=204)
def switch_delete(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    switch_id: str,
    force: bool = False,
):
    db_switch = session.get(SwitchDbModel, switch_id)
    if not db_switch or db_switch.fabricName != fabric_name:
        detail = {"code": 404, "description": "", "message": f"Switch {switch_id} not found in fabric {fabric_name}"}
        raise HTTPException(status_code=404, detail=detail)
    session.delete(db_switch)
    session.commit()
    return {}
