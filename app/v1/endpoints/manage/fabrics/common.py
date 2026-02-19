from pydantic import BaseModel


class FabricLocationModel(BaseModel):
    """
    # Summary

    The location of the fabric, represented by latitude and longitude.
    """

    latitude: float
    longitude: float
