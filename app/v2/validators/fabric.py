from fastapi import HTTPException
from pydantic import AfterValidator
from typing_extensions import Annotated

from ...common.validators.fabric import validate_bgp_asn


MANAGEMENT_TYPES_REQUIRING_BGP = {"vxlanIbgp", "vxlanEbgp", "vxlanCampus", "aimlVxlanIbgp", "aimlVxlanEbgp", "externalConnectivity", "vxlanExternal"}


def validate_fabric_management(fabric_management: dict) -> dict:
    """
    Validate fabric management type.
    """
    mgmt_type = fabric_management.get("type", "")
    bgp_asn = fabric_management.get("bgpAsn")
    if bgp_asn is None and mgmt_type in MANAGEMENT_TYPES_REQUIRING_BGP:
        msg = "management.bgpAsn is missing"
        raise HTTPException(status_code=500, detail=msg)
    if bgp_asn is not None:
        bgp_asn = str(bgp_asn)
        try:
            validate_bgp_asn(bgp_asn=bgp_asn)
        except ValueError as error:
            msg = "Error in validating provided name value pair: [bgpAsn]"
            raise HTTPException(status_code=500, detail=msg) from error
    return fabric_management


FabricManagementType = Annotated[dict, AfterValidator(validate_fabric_management)]
