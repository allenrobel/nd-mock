from enum import Enum


class interfaceStatus(Enum):
    """
    Interface admin/operational status
    """

    up: str = "up"
    down: str = "down"


class interfaceSpeed(Enum):
    """
    Interface speed
    """

    auto: str = "auto"
    speed10mb: str = "10Mb"
    speed100mb: str = "100Mb"
    speed1gb: str = "1Gb"
    speed2_5gb: str = "2.5Gb"
    speed5gb: str = "5Gb"
    speed10gb: str = "10Gb"
    speed25gb: str = "25Gb"
    speed40gb: str = "40Gb"
    speed50gb: str = "50Gb"
    speed100gb: str = "100Gb"
    speed200gb: str = "200Gb"
    speed400gb: str = "400Gb"
    speed800gb: str = "800Gb"


class interfaceUsage(Enum):
    """
    Interface usage options
    """

    apic: str = "apic"
    discovery: str = "discovery"
    epg: str = "epg"
    fc: str = "fc"
    fcpc: str = "fcpc"
    fex: str = "fex"
    ipn: str = "ipn"
    l3Out: str = "l3Out"
    layer3: str = "layer3"
    macsec: str = "macsec"
    pc: str = "pc"
    spine: str = "spine"
    tier1Leaf: str = "tier1Leaf"
    tier2Leaf: str = "tier2Leaf"
    uplink: str = "uplink"
    vfc: str = "vfc"
    vfcpc: str = "vfcpc"
    vpc: str = "vpc"
