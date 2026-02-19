from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from ......db import get_session
from .....models.fabric import FabricDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


class ConfigSaveResponseModel(BaseModel):
    status: str


@router.post(
    "/{fabric_name}/actions/configSave",
    response_model=ConfigSaveResponseModel,
    description="Trigger the configuration save operation for the specified fabric or fabric group.",
)
def config_save_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
):
    db_fabric = session.get(FabricDbModel, fabric_name)
    if not db_fabric:
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)
    return ConfigSaveResponseModel(status="Config save is completed").model_dump()
