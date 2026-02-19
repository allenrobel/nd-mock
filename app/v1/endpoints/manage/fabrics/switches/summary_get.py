from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import CounterNameValue, SwitchDbModel, SwitchesSummaryResponse

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.get("/{fabric_name}/switches/summary", response_model=SwitchesSummaryResponse)
def switches_summary_get(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricName == fabric_name)).all()

    role_counts = Counter(s.switchRole for s in db_switches)
    version_counts = Counter(s.softwareVersion for s in db_switches if s.softwareVersion)

    return SwitchesSummaryResponse(
        role=[CounterNameValue(name=name, count=count) for name, count in role_counts.items()],
        softwareVersion=[CounterNameValue(name=name, count=count) for name, count in version_counts.items()],
    )
