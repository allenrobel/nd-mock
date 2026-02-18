from enum import Enum


class PlatformEnum(Enum):
    """
    Choices for switch platform
    """

    aci: str = "aci"
    nxos: str = "nx-os"


class SwitchConfigSyncStatusEnum(Enum):
    """
    Choices for switch configuration sync status
    """

    inSync: str = "inSync"
    outOfSync: str = "outOfSync"
    inProgress: str = "inProgress"
    notApplicable: str = "notApplicable"


class SwitchRoleEnum(Enum):
    """
    Choices for switchRoleEnum field in Switch model.
    """

    access: str = "access"
    aggregation: str = "aggregation"
    border: str = "border"
    border_gateway: str = "borderGateway"
    border_gateway_spine: str = "borderGatewaySpine"
    border_gateway_super_spine: str = "borderGatewaySuperSpine"
    border_spine: str = "borderSpine"
    border_super_spine: str = "borderSuperSpine"
    core_router: str = "coreRouter"
    edge_router: str = "edgeRouter"
    leaf: str = "leaf"
    spine: str = "spine"
    super_spine: str = "superSpine"
    tier2_leaf: str = "tier2Leaf"
    tor: str = "tor"


class SwitchRoleFriendlyEnum(Enum):
    """
    switchRole field in Switch model.
    """

    access: str = "access"
    aggregation: str = "aggregation"
    border: str = "border"
    border_gateway: str = "border gateway"
    border_gateway_spine: str = "border gateway spine"
    border_gateway_super_spine: str = "border gateway super spine"
    border_spine: str = "border spine"
    border_super_spine: str = "border super spine"
    core_router: str = "core router"
    edge_router: str = "edge router"
    leaf: str = "leaf"
    spine: str = "spine"
    super_spine: str = "super spine"
    tier2_leaf: str = "tier2 leaf"
    tor: str = "tor"


class SwitchUnmanageableCauseEnum(Enum):
    """
    Choices for unmanageableCause field in Switch model.
    """

    none: str = ""
    Unreachable: str = "Unreachable"


class VpcRoleEnum(Enum):
    """
    Choices for vpc role
    """

    operationalPrimary: str = "operationalPrimary"
    operationalSecondary: str = "operationalSecondary"
    primary: str = "primary"
    secondary: str = "secondary"
