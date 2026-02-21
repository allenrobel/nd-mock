import json

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from .....db import get_session
from ....models.fabric import FabricDbModel, FabricLocation, FabricSummaryBriefItem, FabricsSummaryBriefResponse
from .constants import DISPLAY_FABRIC_TYPE_MAP

MOCK_CLUSTER_NAME = "nd-mock-cluster"

router = APIRouter(
    prefix="/api/v1/manage",
)


def build_summary_brief(fabric: FabricDbModel) -> FabricSummaryBriefItem:
    """
    # Summary

    Transform a FabricDbModel into a FabricSummaryBriefItem.
    """
    management = json.loads(fabric.management)
    mgmt_type = management.get("type", "")
    bgp_asn = management.get("bgpAsn")

    location = FabricLocation(
        latitude=fabric.latitude,
        longitude=fabric.longitude,
    )

    display_type = DISPLAY_FABRIC_TYPE_MAP.get(mgmt_type, mgmt_type)

    return FabricSummaryBriefItem(
        fabricName=fabric.name,
        securityDomain=fabric.securityDomain or "all",
        featureUsage={"controller": MOCK_CLUSTER_NAME},
        featureStatus={"controller": "enabled"},
        licenseTier=fabric.licenseTier,
        alertSuspend=fabric.alertSuspend,
        local=True,
        ownerCluster=MOCK_CLUSTER_NAME,
        type=mgmt_type,
        displayFabricType=display_type,
        location=location,
        bgpAsn=bgp_asn,
        # TODO: When VRF/Network models are added, query those tables to determine tenantAssociation dynamically.
        tenantAssociation=False,
    )


@router.get(
    "/fabricsSummaryBrief",
    response_model=FabricsSummaryBriefResponse,
)
def fabrics_summary_brief_get(
    *,
    session: Session = Depends(get_session),
):
    """
    # Summary

    Retrieve brief summary information for all fabrics.

    GET request handler for `/api/v1/manage/fabricsSummaryBrief`.
    """
    fabrics = session.exec(select(FabricDbModel).where(FabricDbModel.category == "fabric")).all()

    items = [build_summary_brief(f) for f in fabrics]
    return FabricsSummaryBriefResponse(fabrics=items)
