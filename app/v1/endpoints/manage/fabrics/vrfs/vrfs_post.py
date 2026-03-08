import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.vrf import VRF_TYPES, VrfCreateRequestBody, VrfCreateResponse, VrfCreateResultItem, VrfDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/vrfs")
def vrfs_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: VrfCreateRequestBody,
):
    """
    # Summary

    Create one or more VRFs in a fabric.

    POST request handler for `/api/v1/manage/fabrics/{fabric_name}/vrfs`.

    Always returns 207 Multi-Status with per-item results.
    Nonexistent fabric returns 500 (not 404) matching real ND behavior.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 500, "description": "", "errors": None, "message": f"Invalid Fabric name: {fabric_name}"}
        raise HTTPException(status_code=500, detail=detail)

    valid_types_str = ", ".join(sorted(VRF_TYPES))
    results = []
    for vrf_item in body.vrfs:
        if not vrf_item.vrfType:
            results.append(VrfCreateResultItem(status="failed", message="vrfType is mandatory", vrfName=vrf_item.vrfName, vrfId=vrf_item.vrfId or 0))
            continue

        if vrf_item.vrfType not in VRF_TYPES:
            results.append(VrfCreateResultItem(status="failed", message=f"Invalid vrfType: '{vrf_item.vrfType}'. Valid types are: {valid_types_str}", vrfName=vrf_item.vrfName, vrfId=vrf_item.vrfId or 0))
            continue

        synthetic_id = f"{fabric_name}:{vrf_item.vrfName}"
        existing = session.get(VrfDbModel, synthetic_id)
        if existing:
            results.append(
                VrfCreateResultItem(
                    status="failed",
                    message=f"VRF {vrf_item.vrfName} already exists",
                    vrfName=vrf_item.vrfName,
                    vrfId=vrf_item.vrfId or 0,
                )
            )
            continue

        extra = {}
        if vrf_item.coreData is not None:
            extra["coreData"] = vrf_item.coreData
        if vrf_item.fabricData is not None:
            extra["fabricData"] = vrf_item.fabricData

        db_vrf = VrfDbModel(
            id=synthetic_id,
            fabricName=fabric_name,
            vrfName=vrf_item.vrfName,
            vrfType=vrf_item.vrfType or "",
            vrfId=vrf_item.vrfId or 0,
            vlanId=vrf_item.vlanId or 0,
            vrfStatus=vrf_item.vrfStatus or "",
            tenantName=vrf_item.tenantName or "",
            extraData=json.dumps(extra) if extra else "{}",
        )
        session.add(db_vrf)
        results.append(
            VrfCreateResultItem(
                status="success",
                message="",
                vrfName=vrf_item.vrfName,
                vrfId=vrf_item.vrfId or 0,
            )
        )

    try:
        session.commit()
    except Exception as error:
        session.rollback()
        detail = {"code": 500, "description": "", "errors": None, "message": f"Failed to create VRFs: {error}"}
        raise HTTPException(status_code=500, detail=detail) from error

    response = VrfCreateResponse(results=results)
    return JSONResponse(status_code=207, content=response.model_dump())
