from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ......db import get_session
from .....models.fabric import FabricDbModel
from .....models.vrf import VrfAttachmentDbModel, VrfAttachmentQueryRequestBody

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


class VrfDeployResponseModel(BaseModel):
    status: str


@router.post(
    "/{fabric_name}/vrfActions/deploy",
    response_model=VrfDeployResponseModel,
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

    Empty switchIds/vrfNames arrays mean 'all switches/VRFs in fabric'.
    """
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "errors": None, "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    # Build query for pending attachments in this fabric
    stmt = select(VrfAttachmentDbModel).where(
        VrfAttachmentDbModel.fabricName == fabric_name,
        VrfAttachmentDbModel.status == "pending",
    )

    if body.vrfNames:
        stmt = stmt.where(VrfAttachmentDbModel.vrfName.in_(body.vrfNames))  # type: ignore[attr-defined]

    if body.switchIds:
        stmt = stmt.where(VrfAttachmentDbModel.switchId.in_(body.switchIds))  # type: ignore[attr-defined]

    pending_attachments = session.exec(stmt).all()

    # Transition each pending attachment based on the attach flag
    for attachment in pending_attachments:
        if attachment.attach:
            attachment.status = "attached"
        else:
            attachment.status = "notApplicable"
        session.add(attachment)

    session.commit()

    return VrfDeployResponseModel(status="Configuration deployment completed").model_dump()
