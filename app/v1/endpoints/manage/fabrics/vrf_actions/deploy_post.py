from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.switch import SwitchDbModel
from .....models.vrf import VrfAttachmentDbModel, VrfAttachmentQueryRequestBody, VrfDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


class VrfDeployResponseModel(BaseModel):
    status: str


@router.post(
    "/{fabric_name}/vrfActions/deploy",
    response_model=VrfDeployResponseModel,
    status_code=202,
    description="Deploy pending VRF attachment changes for the specified fabric.",
)
def vrf_deploy_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    body: VrfAttachmentQueryRequestBody,
):
    """
    # Summary

    Deploy pending VRF attachment changes for a fabric.

    POST request handler for `/api/v1/manage/fabrics/{fabric_name}/vrfActions/deploy`.

    Transitions pending attachments based on their attach flag:
    - attach=True + pending → attached
    - attach=False + pending → notApplicable

    Validation order (matches real ND 4.2 behavior):
    1. Fabric must exist (400 if not)
    2. vrfNames must be non-empty (400 if empty)
    3. switchIds must reference valid switches (400 if invalid)
    4. vrfNames must reference valid VRFs (400 if invalid)
    """
    # 1. Validate fabric exists — real ND returns 400, not 404
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 400, "description": "", "errors": None, "message": f"Invalid Fabric name: {fabric_name}"}
        raise HTTPException(status_code=400, detail=detail)

    # 2. vrfNames is mandatory — real ND rejects empty arrays
    if not body.vrfNames:
        detail = {"code": 400, "description": "", "errors": None, "message": "'vrfNames' is a mandatory parameter for this endpoint."}
        raise HTTPException(status_code=400, detail=detail)

    # 3. Validate switchIds if provided
    if body.switchIds:
        db_switches = session.exec(
            select(SwitchDbModel).where(
                SwitchDbModel.fabricName == fabric_name,
                SwitchDbModel.switchId.in_(body.switchIds),  # type: ignore[attr-defined]
            )
        ).all()
        found_switch_ids = {s.switchId for s in db_switches}
        invalid_switch_ids = [sid for sid in body.switchIds if sid not in found_switch_ids]
        if invalid_switch_ids:
            invalid_list = ", ".join(invalid_switch_ids)
            detail = {"code": 400, "description": "", "errors": None, "message": f"Invalid switch serial number(s) : [{invalid_list}]"}
            raise HTTPException(status_code=400, detail=detail)

    # 4. Validate vrfNames
    db_vrfs = session.exec(
        select(VrfDbModel).where(
            VrfDbModel.fabricName == fabric_name,
            VrfDbModel.vrfName.in_(body.vrfNames),  # type: ignore[attr-defined]
        )
    ).all()
    found_vrf_names = {v.vrfName for v in db_vrfs}
    invalid_vrf_names = [name for name in body.vrfNames if name not in found_vrf_names]
    if invalid_vrf_names:
        invalid_list = ", ".join(invalid_vrf_names)
        detail = {"code": 400, "description": "", "errors": None, "message": f"Invalid VRF name(s): {invalid_list}"}
        raise HTTPException(status_code=400, detail=detail)

    # Build query for pending attachments in this fabric
    stmt = select(VrfAttachmentDbModel).where(
        VrfAttachmentDbModel.fabricName == fabric_name,
        VrfAttachmentDbModel.status == "pending",
        VrfAttachmentDbModel.vrfName.in_(body.vrfNames),  # type: ignore[attr-defined]
    )

    if body.switchIds:
        stmt = stmt.where(VrfAttachmentDbModel.switchId.in_(body.switchIds))  # type: ignore[attr-defined]

    pending_attachments = session.exec(stmt).all()

    # No pending attachments — real ND returns 202 with a distinct message
    if not pending_attachments:
        return VrfDeployResponseModel(status="No switches pending for deployment.").model_dump()

    # Transition each pending attachment based on the attach flag
    # Real ND is async (pending → in progress → attached/notApplicable).
    # The mock skips intermediate states and transitions directly to the final state.
    for attachment in pending_attachments:
        if attachment.attach:
            attachment.status = "attached"
        else:
            attachment.status = "notApplicable"
        session.add(attachment)

    session.commit()

    return VrfDeployResponseModel(status="Deployment of VRF(s) has been initiated successfully").model_dump()
