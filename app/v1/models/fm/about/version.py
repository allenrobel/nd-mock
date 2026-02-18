#!/usr/bin/env python
import uuid

from pydantic import BaseModel
from sqlmodel import Field


class V1FmAboutVersionBase(BaseModel):
    """
    # Summary

    Base class for all other classes in this file.
    """

    version: str = Field()
    mode: str | None = Field(default="LAN")
    isMediaController: bool = Field(default=True)
    dev: bool = Field(default=False)
    isHaEnabled: bool = Field(default=False)
    install: str = Field(default="EASYFABRIC")
    uuid: str = Field(default_factory=uuid.uuid4, primary_key=True)
    is_upgrade_inprogress: bool = Field(default=False)


class V1FmAboutVersionResponseModel(V1FmAboutVersionBase):
    """
    # Summary

    Describes what is returned to clients.
    """
