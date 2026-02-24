from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import SwitchDbModel
from .....models.vrf import VrfAttachmentDbModel, VrfAttachmentItem, VrfAttachmentQueryRequestBody, VrfAttachmentQueryResponse, VrfDbModel, VrfListCounts, VrfListMeta

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.post("/{fabric_name}/vrfAttachments/query", response_model=VrfAttachmentQueryResponse)
def vrf_attachments_query(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: VrfAttachmentQueryRequestBody,
):
    """
    # Summary

    Query VRF attachment status for switches in a fabric.

    POST request handler for `/api/v1/manage/fabrics/{fabric_name}/vrfAttachments/query`.

    Empty switchIds/vrfNames arrays mean 'all switches/VRFs in fabric'.
    Builds cross-product of (VRFs × switches) and looks up attachment records.
    Default status is 'notApplicable' when no record exists.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"message": "Fabric not found", "description": "", "code": 404}
        raise HTTPException(status_code=404, detail=detail)

    # Resolve VRFs: empty list = all VRFs in fabric
    if body.vrfNames:
        db_vrfs = session.exec(
            select(VrfDbModel).where(
                VrfDbModel.fabricName == fabric_name,
                VrfDbModel.vrfName.in_(body.vrfNames),  # type: ignore[attr-defined]
            )
        ).all()
    else:
        db_vrfs = session.exec(select(VrfDbModel).where(VrfDbModel.fabricName == fabric_name)).all()

    # Resolve switches: empty list = all switches in fabric
    if body.switchIds:
        db_switches = session.exec(
            select(SwitchDbModel).where(
                SwitchDbModel.fabricName == fabric_name,
                SwitchDbModel.switchId.in_(body.switchIds),  # type: ignore[attr-defined]
            )
        ).all()
    else:
        db_switches = session.exec(select(SwitchDbModel).where(SwitchDbModel.fabricName == fabric_name)).all()

    # Build cross-product and look up attachment records
    attachments = []
    for vrf in db_vrfs:
        for switch in db_switches:
            attachment_id = f"{fabric_name}:{vrf.vrfName}:{switch.switchId}"
            db_attachment = session.get(VrfAttachmentDbModel, attachment_id)

            if db_attachment:
                status = db_attachment.status
                attach = db_attachment.attach
            else:
                status = "notApplicable"
                attach = False

            attachments.append(
                VrfAttachmentItem(
                    attach=attach,
                    errorMessage=None,
                    instanceValues={},
                    showVlan=True,
                    status=status,
                    switchId=switch.switchId,
                    switchName=switch.hostname,
                    switchRole=switch.switchRole,
                    vrfName=vrf.vrfName,
                )
            )

    total = len(attachments)
    meta = VrfListMeta(counts=VrfListCounts(total=total, remaining=0))
    return VrfAttachmentQueryResponse(attachments=attachments, meta=meta)
