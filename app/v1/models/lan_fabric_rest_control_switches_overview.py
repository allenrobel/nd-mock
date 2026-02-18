#!/usr/bin/env python

from pydantic import BaseModel
from sqlmodel import Field


class SwitchConfig(BaseModel):
    """
    # Summary

    Switch config state names
    """

    in_sync: int | None = Field(default=0, alias="In-Sync")
    out_of_sync: int | None = Field(default=0, alias="Out-of-Sync")


class SwitchHealth(BaseModel):
    """
    # Summary

    Switch health state names
    """

    Healthy: int | None = Field(default=0)
    Major: int | None = Field(default=0)
    Minor: int | None = Field(default=0)


class SwitchRoles(BaseModel):
    """
    # Summary

    Switch role names
    """

    access: int | None = Field(default=0)
    aggregation: int | None = Field(default=0)
    border: int | None = Field(default=0)
    border_gateway: int | None = Field(default=0)
    border_gateway_spine: int | None = Field(default=0)
    border_gateway_super_spine: int | None = Field(default=0)
    border_spine: int | None = Field(default=0)
    border_super_spine: int | None = Field(default=0)
    core_router: int | None = Field(default=0)
    edge_router: int | None = Field(default=0)
    leaf: int | None = Field(default=0)
    spine: int | None = Field(default=0)
    super_spine: int | None = Field(default=0)
    tor: int | None = Field(default=0)


class V1LanFabricRestControlSwitchesOverviewBase(BaseModel):
    """
    # Summary

    Base class for all other classes in this file.
    """

    switchConfig: SwitchConfig
    switchHealth: SwitchHealth
    switchHWVersions: dict
    switchRoles: SwitchRoles
    switchSWVersions: dict


class V1LanFabricRestControlSwitchesOverviewResponseModel(V1LanFabricRestControlSwitchesOverviewBase):
    """
    # Summary

    Describes what is returned to clients.
    """
