#!/usr/bin/env python

from fastapi import APIRouter, Depends
from sqlmodel import Session

from .......db import get_session
from .models.switch_overview import SwitchOverviewResponse

router = APIRouter(
    prefix="/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches",
)


@router.get(
    "/{fabric_name}/overview",
    description="Return summary of fabric inventory.",
)
def v1_switches_overview_get(
    fabric_name: str,
    session: Session = Depends(get_session),
):
    """
    # Summary

    GET request handler
    """
    response = SwitchOverviewResponse()
    response.fabric = fabric_name
    response.session = session
    response.refresh()
    return response.response_dict()
