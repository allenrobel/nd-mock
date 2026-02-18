from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1
from .common import build_404_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


class ConfigSaveResponseModel(BaseModel):
    """
    # Summary

    Response model for the config save endpoint.
    """

    status: str


@router.post(
    "/{fabric_name}/config-save",
    response_model=ConfigSaveResponseModel,
    description="(v1) Save the configuration.",
)
def v1_fabric_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
):
    """
    # Summary

    config-save POST request handler

    ## Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/config-save
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        path = f"{router.prefix}/{fabric_name}/config-save"
        raise HTTPException(status_code=404, detail=build_404_response(path))
    response = {}
    response["status"] = "Config save is completed"
    return ConfigSaveResponseModel(**response).model_dump()
