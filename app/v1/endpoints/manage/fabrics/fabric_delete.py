from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .....db import get_session
from ....models.fabric import FabricDbModel

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
        detail = {"code": 404, "description": "", "message": f"Fabric {fabric_name} not found"}
        raise HTTPException(status_code=404, detail=detail)
    session.delete(fabric)
    session.commit()
    return {}
