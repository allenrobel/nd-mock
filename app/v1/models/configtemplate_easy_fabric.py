#!/usr/bin/env python

from typing import Dict, List

from pydantic import BaseModel
from sqlmodel import Field


class V1ConfigtemplateEasyFabricBase(BaseModel):
    """
    # Summary

    Base class for all other classes in this file.
    """

    instanceClassId: int = Field(default=1000)
    assignedInstanceClassId: int = Field(default=0)
    instanceName: str = Field(default="com.cisco.dcbu.dcm.model.cfgtemplate.ConfigTemplate:name=Easy_Fabric:type=true")
    name: str = Field(default="Easy_Fabric")
    description: str = Field(default="Fabric for a VXLAN EVPN deployment with Nexus 9000 and 3000 switches.")
    userDefined: bool = Field(default=True)
    parameters: List[Dict]
    content: str


class V1ConfigtemplateEasyFabricResponseModel(V1ConfigtemplateEasyFabricBase):
    """
    # Summary

    Describes what is returned to clients.
    """
