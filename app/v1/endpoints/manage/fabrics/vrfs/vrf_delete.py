from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ......db import get_session
from .....models.vrf import VrfAttachmentDbModel, VrfDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.delete("/{fabric_name}/vrfs/{vrf_name}", status_code=204)
def vrf_delete(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    vrf_name: str,
):
    """
    # Summary

    Delete a VRF from a fabric.

    DELETE request handler for `/api/v1/manage/fabrics/{fabric_name}/vrfs/{vrf_name}`.

    Real ND returns 400 (not 404) for nonexistent VRF.
    Returns 400 if any attachment is not in 'notApplicable' state.
    """
    synthetic_id = f"{fabric_name}:{vrf_name}"
    db_vrf = session.get(VrfDbModel, synthetic_id)
    if not db_vrf:
        detail = {"code": 400, "description": "", "errors": None, "message": "Invalid VRF"}
        raise HTTPException(status_code=400, detail=detail)

    # Check if any attachment is not in notApplicable state
    attachments = session.exec(
        select(VrfAttachmentDbModel).where(
            VrfAttachmentDbModel.fabricName == fabric_name,
            VrfAttachmentDbModel.vrfName == vrf_name,
        )
    ).all()

    for attachment in attachments:
        if attachment.status != "notApplicable":
            detail = {
                "code": 400,
                "description": "",
                "errors": None,
                "message": "Delete is not allowed as the VRF is currently not in 'NA' state",
            }
            raise HTTPException(status_code=400, detail=detail)

    # Clean up attachment records
    for attachment in attachments:
        session.delete(attachment)

    session.delete(db_vrf)
    session.commit()
    return {}
