from pydantic import BaseModel


class FabricLocationModel(BaseModel):
    """
    # Summary

    The location of the fabric, represented by latitude and longitude.
    """

    latitude: float
    longitude: float


class FabricManagementModel(BaseModel):
    """
    # Summary

    The management information for the fabric.

    TODO: This model should be moved to a shared location and
    include all parameters.  For now, we're supporting only
    mandatory parameters for testing.
    """

    bgpAsn: str
    type: str
