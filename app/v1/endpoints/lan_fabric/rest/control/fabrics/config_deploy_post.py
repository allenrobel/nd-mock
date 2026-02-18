from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from .......db import get_session
from ......models.fabric import FabricDbModelV1
from ......models.inventory import SwitchDbModel
from .common import build_404_response

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics",
)


class ConfigDeployResponseModel(BaseModel):
    """
    # Summary

    Response model for the config save endpoint.
    """

    status: str


@router.post(
    "/{fabric_name}/config-deploy/{switch_id}",
    response_model=ConfigDeployResponseModel,
    description="(v1) Deploy the configuration.",
)
def v1_config_deploy_post(
    *,
    session: Session = Depends(get_session),
    fabric_name: str,
    switch_id: str,
):
    """
    # Summary

    config-deploy POST request handler

    ## Path

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/config-deploy{switch_id}
    """
    db_fabric = session.exec(select(FabricDbModelV1).where(FabricDbModelV1.FABRIC_NAME == fabric_name)).first()
    if not db_fabric:
        path = f"{router.prefix}/{fabric_name}/config-save/{switch_id}"
        raise HTTPException(status_code=404, detail=build_404_response(path))
    db_switch = session.exec(select(SwitchDbModel).where(SwitchDbModel.serialNumber == switch_id)).first()
    if not db_switch:
        msg = f"Could not get the fabric name for invalid switch: {switch_id}"
        raise HTTPException(status_code=500, detail=msg)
    response = {}
    response["status"] = "Configuration deployment completed."
    return ConfigDeployResponseModel(**response).model_dump()
