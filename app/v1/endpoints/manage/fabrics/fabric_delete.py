from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from .....db import get_session
from ....models.fabric import FabricDbModel
from ....models.switch import SwitchDbModel

router = APIRouter(
    prefix="/api/v1/manage/fabrics",
)


@router.delete("/{fabric_name}", status_code=204)
async def delete_fabric(*, session: Session = Depends(get_session), fabric_name: str):
    """
    # Summary

    Delete a fabric by name.

    DELETE request handler for `/api/v1/manage/fabrics/{fabric_name}`.

    ## NDFC 404 Response (4.0 LA)

    ```json
    {
        "code": 404,
        "description": "",
        "message": f"Fabric f1 not found"
    }
    ```
    """
    fabric = session.get(FabricDbModel, fabric_name)
    if not fabric:
        detail = {"code": 404, "description": "", "errors": None, "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)

    switch_count = session.exec(select(func.count()).select_from(SwitchDbModel).where(SwitchDbModel.fabricName == fabric_name)).one()
    if switch_count > 0:
        detail = {
            "code": 400,
            "description": "",
            "errors": None,
            "message": f"Unable to delete Fabric {fabric_name}.  Please remove all switches in this fabric before deleting.",
        }
        raise HTTPException(status_code=400, detail=detail)

    session.delete(fabric)
    session.commit()
    return {}
