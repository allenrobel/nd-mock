import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.vrf import VrfDataResponse, VrfDbModel, VrfListCounts, VrfListMeta, VrfListResponse

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


def build_vrf_response(db_vrf: VrfDbModel) -> VrfDataResponse:
    """Deserialize the extraData JSON blob into the nested response fields."""
    extra = json.loads(db_vrf.extraData) if db_vrf.extraData else {}
    return VrfDataResponse(
        vrfName=db_vrf.vrfName,
        vrfType=db_vrf.vrfType,
        vrfId=db_vrf.vrfId,
        vlanId=db_vrf.vlanId,
        vrfStatus=db_vrf.vrfStatus,
        tenantName=db_vrf.tenantName,
        fabricName=db_vrf.fabricName,
        coreData=extra.get("coreData"),
        fabricData=extra.get("fabricData"),
    )


@router.get("/{fabric_name}/vrfs", response_model=VrfListResponse)
def vrfs_get(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    offset: int = 0,
    limit: int = Query(default=100, alias="max"),
):
    """
    # Summary

    List all VRFs in a fabric.

    GET request handler for `/api/v1/manage/fabrics/{fabric_name}/vrfs`.

    Nonexistent fabric returns 404 with simplified format (no 'errors' field),
    matching real ND behavior.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"message": "Fabric not found", "description": "", "code": 404}
        raise HTTPException(status_code=404, detail=detail)

    total = session.exec(select(func.count()).select_from(VrfDbModel).where(VrfDbModel.fabricName == fabric_name)).one()
    db_vrfs = session.exec(select(VrfDbModel).where(VrfDbModel.fabricName == fabric_name).offset(offset).limit(limit)).all()

    vrfs = [build_vrf_response(v) for v in db_vrfs]
    remaining = max(0, total - offset - len(vrfs))
    meta = VrfListMeta(counts=VrfListCounts(total=total, remaining=remaining))
    return VrfListResponse(vrfs=vrfs, meta=meta)
