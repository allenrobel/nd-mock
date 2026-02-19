from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


class ConfigDeployResponseModel(BaseModel):
    status: str


@router.post(
    "/{fabric_name}/actions/configDeploy",
    response_model=ConfigDeployResponseModel,
    description="Trigger the configuration deploy operation for the specified fabric or fabric group.",
)
def config_deploy_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)
    return ConfigDeployResponseModel(status="Configuration deployment completed").model_dump()
