#!/usr/bin/env python
# TODO: If SQLModel is ever fixed, remove the mypy directive below.
# https://github.com/fastapi/sqlmodel/discussions/732
# mypy: disable-error-code=call-arg
from datetime import datetime
from enum import Enum

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from ...common.functions.utilities import get_datetime
from ...common.validators.fabric import BgpValue


class AgentIntfEnum(str, Enum):
    """
    # Summary

    Defines choices for AGENT_INTF
    """

    eth0 = "eth0"
    eth1 = "eth1"


class BgpAuthKeyTypeEnum(str, Enum):
    """
    # Summary

    Defines choices for BGP_AUTH_KEY_TYPE
    """

    Three = "3"
    Seven = "7"


class CoppPolicyEnum(str, Enum):
    """
    # Summary

    Defines choices for COPP_POLICY
    """

    dense = "dense"
    lenient = "lenient"
    moderate = "moderate"
    strict = "strict"
    manual = "manual"


class DhcpIpv6EnableEnum(str, Enum):
    """
    # Summary

    Defines choices for DHCP_IPV6_ENABLE
    """

    DHCPv4 = "DHCPv4"
    DHCPv6 = "DHCPv6"


class FabricInterfaceTypeEnum(str, Enum):
    """
    # Summary

    Defines choices for FABRIC_INTERFACE_TYPE
    """

    p2p = "p2p"
    unnumbered = "unnumbered"


class FFEnum(str, Enum):
    """
    # Summary

    Defines choices for FF
    """

    Easy_Fabric = "Easy_Fabric"


class EnableDisableEnum(str, Enum):
    """
    # Summary

    Defines choices for any properties with values constrained to
    "Enable" and "Disable".
    """

    Enable = "Enable"
    Disable = "Disable"


class IsisLevelEnum(str, Enum):
    """
    # Summary

    Defines choices for ISIS_LEVEL
    """

    level_1 = "level-1"
    level_2 = "level-2"


class LinkStateRoutingEnum(str, Enum):
    """
    # Summary

    Defines choices for LINK_STATE_ROUTING
    """

    isis = "is-is"
    ospf = "ospf"


class MacsecAlgorithmEnum(str, Enum):
    """
    # Summary

    Defines choices for MACSEC_ALGORITHM
    """

    AES_128_CMAC = "AES_128_CMAC"
    AES_256_CMAC = "AES_256_CMAC"


class MacsecCipherSuiteEnum(str, Enum):
    """
    # Summary

    Defines choices for MACSEC_CIPHER_SUITE
    """

    GCM_AES_128 = "GCM-AES-128"
    GCM_AES_256 = "GCM-AES-256"
    GCM_AES_XPN_128 = "GCM-AES-XPN-128"
    GCM_AES_XPN_256 = "GCM-AES-XPN-256"


class OverlayModeEnum(str, Enum):
    """
    # Summary

    Defines choices for OVERLAY_MODE
    """

    cli = "cli"
    config_profile = "config-profile"


class PowerRedundancyModeEnum(str, Enum):
    """
    # Summary

    Defines choices for POWER_REDUNDANCY_MODE
    """

    combined = "combined"
    insrc_redundant = "insrc-redundant"
    ps_redundant = "ps-redundant"


class ReplicationModeEnum(str, Enum):
    """
    # Summary

    Defines choices for REPLICATION_MODE
    """

    Ingress = "Ingress"
    Multicast = "Multicast"


class RpCountEnum(int, Enum):
    """
    # Summary

    Defines choices for RP_COUNT
    """

    Two = 2
    Four = 4


class RpModeEnum(str, Enum):
    """
    # Summary

    Defines choices for RP_COUNT
    """

    asm = "asm"
    bidir = "bidir"


class RrCountEnum(int, Enum):
    """
    # Summary

    Defines choices for RR_COUNT
    """

    Two = 2
    Four = 4


class StpBridgePriorityEnum(int, Enum):
    """
    # Summary

    Defines choices for STP_BRIDGE_PRIORITY
    """

    STPP_0 = 0
    STPP_4096 = 4096
    STPP_8192 = 8192
    STPP_12288 = 12288
    STPP_16384 = 16384
    STPP_20480 = 20480
    STPP_24576 = 24576
    STPP_28672 = 28672
    STPP_32768 = 32768
    STPP_36864 = 36864
    STPP_40960 = 40960
    STPP_45056 = 45056
    STPP_49152 = 49152
    STPP_53248 = 53248
    STPP_57344 = 57344
    STPP_61440 = 61440


class StpRootOptionEnum(str, Enum):
    """
    # Summary

    Defines choices for STP_ROOT_OPTION
    """

    mst = "mst"
    rpvst_plus = "rpvst+"
    unmanaged = "unmanaged"


class TempAnycastGatewayEnum(str, Enum):
    """
    # Summary

    Defines choices for temp_anycast_gateway
    """

    anycast_gateway = "anycast_gateway"


class TempVpcDomainMgmtEnum(str, Enum):
    """
    # Summary

    Defines choices for temp_vpc_domain_mgmt
    """

    vpc_domain_mgmt = "vpc_domain_mgmt"


class TempVpcPeerLinkEnum(str, Enum):
    """
    # Summary

    Defines choices for temp_vpc_peer_link
    """

    int_vpc_peer_link_po = "int_vpc_peer_link_po"


class VpcPeerKeepAliveOptionEnum(str, Enum):
    """
    # Summary

    Defines choices for VPC_PEER_KEEP_ALIVE_OPTION
    """

    loopback = "loopback"
    management = "management"


class VrfLiteAutoconfigEnum(str, Enum):
    """
    # Summary

    Defines choices for VRF_LITE_AUTOCONFIG
    """

    Manual = "Manual"
    Back2BackAndToExternal = "Back2Back&ToExternal"


class Descriptions:
    """
    # Summary

    Property descriptions.
    """

    # pylint: disable=missing-function-docstring
    def __init__(self):
        pass

    @property
    def aaa_remote_ip_enabled(self):
        """
        AAA_REMOTE_IP_ENABLED
        """
        desc = "Enable AAA IP Authorization. "
        desc += "Enable only when IP Authorization is enabled in the AAA Server."
        return desc

    @property
    def aaa_server_conf(self):
        """
        AAA_REMOTE_IP_ENABLED
        """
        return "AAA Freeform Config"

    @property
    def agent_intf(self):
        return "Agent Interface. Interface to connect to Agent."

    @property
    def anycast_bgw_advertise_pip(self):
        desc = "Anycast Border Gateway advertise-pip. "
        desc += "To advertise Anycast Border Gateway PIP as VTEP. "
        desc += "Effective on MSD fabric after 'Recalculate Config'."
        return desc

    @property
    def anycast_gw_mac(self):
        desc = "Anycast Gateway MAC Address. "
        desc += "Shared MAC address for all leafs (xxxx.xxxx.xxxx)."
        return desc

    @property
    def anycast_lb_id(self):
        desc = "Underlay Anycast Loopback Id. "
        desc += "Used for vPC Peering in VXLANv6 Fabrics (Min:0, Max:1023)."
        return desc

    @property
    def anycast_rp_ip_range(self):
        desc = "Underlay RP Loopback IP Range. "
        desc += "Anycast or Phantom RP IP Address Range."
        return desc

    @property
    def auto_vrflite_ifc_default_vrf(self):
        desc = "Auto Deploy Default VRF. "
        desc += "Whether to auto generate Default VRF interface and BGP "
        desc += "peering configuration on VRF LITE IFC auto deployment. "
        desc += "If set, auto created VRF Lite IFC links will have "
        desc += "'Auto Deploy Default' enabled."
        return desc

    @property
    def bfd_auth_key_id(self):
        return "BFD Authentication Key ID. "

    @property
    def bfd_auth_key(self):
        return "BFD Authentication Key. Encrypted SHA1 secret value."

    @property
    def bfd_enable(self):
        return "Enable BFD. Valid for IPv4 Underlay only."

    @property
    def bfd_ibgp_enable(self):
        return "Enable BFD For iBGP."

    @property
    def bfd_ospf_enable(self):
        return "Enable BFD For OSPF."

    @property
    def bgp_as(self):
        desc = "BGP ASN. "
        desc += "1-4294967295 | 1-65535[.0-65535]. "
        desc += "It is a good practice to have a unique ASN for each Fabric."
        return desc

    @property
    def bgp_auth_enable(self):
        return "Enable BGP Authentication"

    @property
    def bgp_auth_key(self):
        return "Encrypted BGP Authentication Key based on BGP_AUTH_KEY_TYPE."

    @property
    def bgp_auth_key_type(self):
        return "BGP Key Encryption Type: 3 - 3DES, 7 - Cisco."

    @property
    def bootstrap_conf(self):
        desc = "Bootstrap Freeform Config. "
        desc += "Additional CLIs required during device bootup/login "
        desc += "e.g. AAA/Radius."
        return desc

    @property
    def bootstrap_enable(self):
        desc = "Enable Bootstrap. "
        desc += "Automatic IP Assignment For POAP."
        return desc

    @property
    def bootstrap_multisubnet(self):
        desc = "DHCPv4 Multi Subnet Scope. "
        desc += "lines with # prefix are ignored here."
        return desc

    @property
    def brfield_debug_flag(self):
        desc = "!!! Only for brf debugging purpose !!! "
        desc += "Dont' use until you are aware about it."
        return desc

    @property
    def brownfield_skip_overlay_network_attachments(self):
        desc = "Skip Overlay Network Interface Attachments. "
        desc += "Enable to skip overlay network interface attachments "
        desc += "for Brownfield and Host Port Resync cases."
        return desc

    @property
    def cdp_enable(self):
        desc = "Enable CDP for Bootstrapped Switch. "
        desc += "Enable CDP on management interface."
        return desc

    @property
    def copp_policy(self):
        desc = "Fabric Wide CoPP Policy. Customized CoPP policy should be "
        desc += "provided when 'manual' is selected."
        return desc

    @property
    def dci_subnet_range(self):
        return "Address range to assign P2P Interfabric Connections."

    @property
    def default_network(self):
        desc = "Default Overlay Network Template For Leafs."
        return desc

    @property
    def default_pvlan_sec_network(self):
        desc = "Default PVLAN Secondary Network Template."
        return desc

    @property
    def default_queuing_policy_cloudscale(self):
        desc = "N9K Cloud Scale Platform Queuing Policy. "
        desc += "Queuing Policy for all 92xx, -EX, -FX, -FX2, -FX3, -GX "
        desc += "series switches in the fabric."
        return desc

    @property
    def default_queuing_policy_other(self):
        desc = "Other N9K Platform Queuing Policy. "
        desc += "Queuing Policy for all other switches in the fabric."
        return desc

    @property
    def default_queuing_policy_r_series(self):
        desc = "N9K R-Series Platform Queuing Policy. "
        desc += "Queuing Policy for all R-Series switches in the fabric."
        return desc

    @property
    def default_vrf(self):
        return "Default Overlay VRF Template For Leafs."

    @property
    def default_vrf_redis_bgp_rmap(self):
        desc = "Redistribute BGP Route-map Name. "
        desc += "Route Map used to redistribute BGP routes to IGP in default "
        desc += "vrf in auto created VRF Lite IFC links."
        return desc

    @property
    def deployment_freeze(self):
        return "Disable all deployments in this fabric."

    @property
    def dhcp_enable(self):
        desc = "Enable Local DHCP Server. "
        desc += "Automatic IP Assignment For POAP From Local DHCP Server."
        return desc

    @property
    def dhcp_end(self):
        desc = "DHCP Scope End Address. "
        desc += "End Address For Switch POAP."
        return desc

    @property
    def dhcp_ipv6_enable(self):
        desc = "DHCP Version. "
        desc += "One of DHCPv4 or DHCPv6."
        return desc

    @property
    def dhcp_start(self):
        desc = "DHCP Scope Start Address. "
        desc += "Start Address For Switch POAP."
        return desc

    @property
    def dns_server_ip_list(self):
        desc = "DNS Server IPs. "
        desc += "Comma separated list of IP Addresses(v4/v6)."
        return desc

    @property
    def dns_server_vrf(self):
        desc = "DNS Server VRFs. "
        desc += "One VRF for all DNS servers or a comma separated list of VRFs, one per DNS server."
        return desc

    @property
    def enable_aaa(self):
        desc = "Include AAA configs from Manageability tab during device bootup."
        return desc

    @property
    def enable_agent(self):
        return "Enable Agent (developmet purpose only)."

    @property
    def enable_default_queuing_policy(self):
        return "Enable Default Queuing Policies."

    @property
    def enable_evpn(self):
        return "Enable EVPN (extensible virtual private network)."

    @property
    def enable_fabric_vpc_domain_id(self):
        desc = "Enable the same vPC Domain Id <br />for all vPC Pairs. "
        desc += "(Not Recommended)."
        return desc

    @property
    def enable_macsec(self):
        return "Enable MACsec in the fabric."

    @property
    def enable_netflow(self):
        return "Enable Netflow on VTEPs."

    @property
    def enable_ngoam(self):
        desc = "Enable VXLAN OAM. "
        desc += "Enable the Next Generation (NG) OAM feature for all switches "
        desc += "in the fabric to aid in trouble-shooting VXLAN EVPN fabrics."
        return desc

    @property
    def enable_nxapi(self):
        return "Enable HTTPS NX-API"

    @property
    def enable_nxapi_http(self):
        return "Enable HTTP NX-API."

    @property
    def enable_pvlan(self):
        desc = "Enable Private VLAN (PVLAN). "
        desc += "Enable PVLAN on switches except spines and super spines."
        return desc

    @property
    def enable_realtime_backup(self):
        desc = "Hourly Fabric Backup. "
        desc += "Backup hourly only if there is any config deployment since "
        desc += "last backup."
        return desc

    @property
    def enable_scheduled_backup(self):
        desc = "Scheduled Fabric Backup. "
        desc += "Backup at the specified time."
        return desc

    @property
    def enable_tenant_dhcp(self):
        return "Enable Tenant DHCP."

    @property
    def enable_trm(self):
        desc = "Enable Tenant Routed Multicast (TRM). "
        desc += "For Overlay Multicast Support In VXLAN Fabrics."
        return desc

    @property
    def enable_vpc_peer_link_native_vlan(self):
        desc = "Make vPC Peer Link VLAN as Native VLAN."
        return desc

    @property
    def extra_conf_intra_links(self):
        return "Additional CLIs For All Intra-Fabric Links."

    @property
    def extra_conf_leaf(self):
        desc = "Leaf Freeform Config. "
        desc += "Additional CLIs For All Leafs As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def extra_conf_spine(self):
        desc = "Spine Freeform Config. "
        desc += "Additional CLIs For All Spines As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def extra_conf_tor(self):
        desc = "ToR Freeform Config. "
        desc += "Additional CLIs For All ToRs As Captured From "
        desc += "Show Running Configuration."
        return desc

    @property
    def fabric_interface_type(self):
        desc = "Fabric Interface Numbering. "
        desc += "ptp (Numbered Point-to-Point) or unnumbered."
        return desc

    @property
    def fabric_mtu(self):
        desc = "Intra Fabric Interface MTU. "
        desc += "(Min:576, Max:9216). Must be an even number."
        return desc

    @property
    def fabric_name(self):
        desc = "Fabric Name. "
        desc += "Maximum length, 32 characters."
        return desc

    @property
    def fabric_vpc_domain_id(self):
        return "vPC Domain Id to be used on all vPC pairs in the fabric."

    @property
    def fabric_vpc_domain_id_prev(self):
        return "Internal Fabric Wide vPC Domain Id."

    @property
    def fabric_vpc_qos(self):
        desc = "Enable Qos for Fabric vPC-Peering. "
        desc += "Qos on spines for guaranteed delivery of vPC Fabric Peering "
        desc += "communication."
        return desc

    @property
    def feature_ptp(self):
        return "Enable Precision Time Protocol (PTP)."

    @property
    def ff(self):
        return "Template Family."

    @property
    def grfield_debug_flag(self):
        desc = "Enable to clean switch configuration without reload when "
        desc += "PreserveConfig=no."
        return desc

    @property
    def hd_time(self):
        desc = "NVE Source Inteface HoldDown Time (Min:1, Max:1500) in seconds."
        return desc

    @property
    def host_intf_admin_state(self):
        return "Unshut Host Interfaces by Default."

    @property
    def ibgp_peer_template(self):
        desc = "Specifies the iBGP Peer-Template config used for RR and "
        desc += "spines with border role."
        return desc

    @property
    def ibgp_peer_template_leaf(self):
        desc = "Specifies the config used for leaf, border or border gateway. "
        desc += "If this field is empty, the peer template defined in iBGP "
        desc += "Peer-Template Config is used on all BGP enabled devices "
        desc += "(RRs, leafs, border or border gateway roles)."
        return desc

    @property
    def inband_dhcp_servers(self):
        desc = "External DHCP Server IP Addresses. "
        desc += "Comma separated list of IPv4 Addresses (Max 3)."
        return desc

    @property
    def inband_mgmt(self):
        return "Bootstrap Seed Switch Loopback Interface ID"

    @property
    def isis_auth_key(self):
        desc = "IS-IS Authentication Key. "
        desc += "Cisco Type 7 Encrypted."
        return desc

    @property
    def isis_auth_keychain_key_id(self):
        desc = "IS-IS Authentication Key ID. "
        desc += "(Min:0, Max:65535)."
        return desc

    @property
    def isis_auth_keychain_name(self):
        return "IS-IS Authentication Keychain Name."

    @property
    def isis_level(self):
        return "Supported IS levels: level-1, level-2."

    @property
    def isis_overload_elapse_time(self):
        desc = "IS-IS Overload Bit Elapsed Time. "
        desc += "Clear the overload bit after an elapsed time in seconds."
        return desc

    @property
    def isis_overload_enable(self):
        desc = "Set IS-IS Overload Bit. "
        desc += "When enabled, set the overload bit for an elapsed time "
        desc += "after a reload."
        return desc

    @property
    def isis_p2p_enable(self):
        desc = "Enable IS-IS Network Point-to-Point. "
        desc += "This will enable network point-to-point on fabric interfaces "
        desc += "which are numbered."
        return desc

    @property
    def l2_host_intf_mtu(self):
        desc = "Layer 2 Host Interface MTU. "
        desc += "(Min:1500, Max:9216). Must be an even number."
        return desc

    @property
    def l2_segment_id_range(self):
        desc = "Layer 2 VXLAN VNI Range. "
        desc += "Overlay Network Identifier Range (Min:1, Max:16777214)."
        return desc

    @property
    def l3vni_mcast_group(self):
        desc = "Default MDT Address for TRM VRFs. "
        desc += "Default Underlay Multicast group IP assigned for every "
        desc += "overlay VRF."
        return desc

    @property
    def link_state_routing(self):
        return "Underlay Routing Protocol Used for Spine-Leaf Connectivity."

    @property
    def link_state_routing_tag(self):
        return "Underlay Routing Protocol Tag."

    @property
    def loopback0_ip_range(self):
        desc = "Underlay Routing Loopback IP Range. "
        desc += "Typically Loopback0 IP Address Range."
        return desc

    @property
    def loopback0_ipv6_range(self):
        desc = "Underlay Routing Loopback IPv6 Range. "
        desc += "Typically Loopback0 IPv6 Address Range."
        return desc

    @property
    def loopback1_ip_range(self):
        desc = "Underlay VTEP Loopback IP Range. "
        desc += "Typically Loopback1 IP Address Range."
        return desc

    @property
    def loopback1_ipv6_range(self):
        desc = "Underlay VTEP Loopback IPv6 Range. "
        desc += "Typically Loopback1 and Anycast Loopback IPv6 Address Range."
        return desc

    @property
    def macsec_algorithm(self):
        desc = "MACsec Primary Cryptographic Algorithm. AES_128_CMAC or "
        desc += "AES_256_CMAC."
        return desc

    @property
    def macsec_cipher_suite(self):
        desc = "MACsec Cipher Suite. "
        desc += "Configure Cipher Suite."
        return desc

    @property
    def macsec_fallback_algorithm(self):
        return "MACsec Fallback Cryptographic Algorithm."

    @property
    def macsec_fallback_key_string(self):
        desc = "MACsec Fallback Key String. "
        desc += "Cisco Type 7 Encrypted Octet String."
        return desc

    @property
    def macsec_key_string(self):
        desc = "MACsec Primary Key String. "
        desc += "Cisco Type 7 Encrypted Octet String."
        return desc

    @property
    def macsec_report_timer(self):
        desc = "MACsec Status Report Timer. "
        desc += "MACsec Operational Status periodic report timer in minutes."
        return desc

    @property
    def mgmt_gw(self):
        desc = "Switch Mgmt Default Gateway. "
        desc += "Default Gateway For Management VRF On The Switch."
        return desc

    @property
    def mgmt_prefix(self):
        desc = "Switch Mgmt IP Subnet Prefix. "
        desc += "(Min:8, Max:30)."
        return desc

    @property
    def mgmt_v6prefix(self):
        desc = "Switch Mgmt IPv6 Subnet Prefix. "
        desc += "(Min:64, Max:126)."
        return desc

    @property
    def mpls_handoff(self):
        return "Enable MPLS Handoff"

    @property
    def mpls_lb_id(self):
        desc = "Underlay MPLS Loopback Id. "
        desc += "Used for VXLAN to MPLS SR/LDP Handoff (Min:0, Max:1023)."
        return desc

    @property
    def mpls_loopback_ip_range(self):
        desc = "Underlay MPLS Loopback IP Range. "
        desc += "Used for VXLAN to MPLS SR/LDP Handoff."
        return desc

    @property
    def mst_instance_range(self):
        desc = "MST Instance Range. "
        desc += "Example: 0-3,5,7-9, Default is 0."
        return desc

    @property
    def multicast_group_subnet(self):
        desc = "Multicast Group Subnet. "
        desc += "Multicast pool prefix between 8 to 30. "
        desc += "A multicast group IP from this pool is used for BUM traffic "
        desc += "for each overlay network."
        return desc

    @property
    def netflow_exporter_list(self):
        desc = "Netflow Exporter. "
        desc += "One or Multiple Netflow Exporters."
        return desc

    @property
    def netflow_monitor_list(self):
        desc = "Netflow Monitor. "
        desc += "One or Multiple Netflow Monitors."
        return desc

    @property
    def netflow_record_list(self):
        desc = "Netflow Record. "
        desc += "One or Multiple Netflow Records."
        return desc

    @property
    def network_extension_template(self):
        desc = "Network Extension Template. "
        desc += "Default Overlay Network Template For Borders."
        return desc

    @property
    def network_vlan_range(self):
        desc = "Network VLAN Range. "
        desc += "Per Switch Overlay Network VLAN Range (Min:2, Max:4094). "
        desc += "Example: '2300-2999'."
        return desc

    @property
    def ntp_server_ip_list(self):
        desc = "NTP Server IPs. "
        desc += "Comma separated list of IP Addresses(v4/v6). "
        desc += "Example: '1.1.1.1,2001:1:1::1'."
        return desc

    @property
    def ntp_server_vrf(self):
        desc = "NTP Server VRFs. "
        desc += "One VRF for all NTP servers or a comma-separated list of VRFs, "
        desc += "one per NTP server.  If a comma-separated list, must have the "
        desc += "same number of items as NTP_SERVER_IP_LIST. "
        desc += "Example: 'management,default'."
        return desc

    @property
    def nve_lb_id(self):
        desc = "Underlay VTEP Loopback Id. "
        desc += "(Min:0, Max:1023, Default: 1)."
        return desc

    @property
    def ospf_area_id(self):
        desc = "OSPF Area Id in IP address format. "
        desc += "Default: '0.0.0.0'"
        return desc

    @property
    def ospf_auth_enable(self):
        return "Enable OSPF Authentication."

    @property
    def ospf_auth_key(self):
        return "OSPF Authentication Key. 3DES Encrypted."

    @property
    def ospf_auth_key_id(self):
        return "OSPF Authentication Key ID. (Min:0, Max:255)."

    @property
    def overlay_mode(self):
        desc = "Overlay Mode. "
        desc += "VRF/Network configuration using config-profile or CLI. "
        desc += "Valid values: 'cli', 'config-profile'."
        return desc

    @property
    def pim_hello_auth_enable(self):
        return "Enable PIM Hello Authentication."

    @property
    def pim_hello_auth_key(self):
        return "PIM Hello Authentication Key. 3DES Encrypted."

    @property
    def pm_enable(self):
        return "Enable Performance Monitoring."

    @property
    def power_redundancy_mode(self):
        return "Default Power Supply Mode For The Fabric."

    @property
    def ptp_lb_id(self):
        desc = "PTP Source Loopback Id. "
        desc += "(Min:0, Max:1023, Default: 0)."
        return desc

    @property
    def replication_mode(self):
        desc = "Replication Mode for BUM Traffic. "
        desc += "Default: 'Multicast', "
        desc += "Valid values: Ingress, Multicast."
        return desc

    @property
    def router_id_range(self):
        desc = "BGP Router ID Range for IPv6 Underlay. "
        desc += "Default: '10.2.0.0/23'"
        return desc

    @property
    def route_map_sequence_number_range(self):
        desc = "Route Map Sequence Number Range. "
        desc += "Default: '1-65534'"
        return desc

    @property
    def rp_count(self):
        desc = "Number of spines acting as Rendezvous-Point (RP). "
        desc += "Default: 2, "
        desc += "Valid values: 2, 4."
        return desc

    @property
    def rp_lb_id(self):
        desc = "Underlay RP Loopback Id. "
        desc += "(Min:0, Max:1023, Default: 254)."
        return desc

    @property
    def rp_mode(self):
        desc = "Multicast RP Mode. "
        desc += "Valid values: asm, bidir, Default: asm)."
        return desc

    @property
    def rr_count(self):
        desc = "Number of spines acting as Route-Reflectors. "
        desc += "Default: 2, "
        desc += "Valid values: 2, 4."
        return desc

    @property
    def scheduled_time(self):
        desc = "Scheduled Backup Time. "
        desc += "Time (UTC) in 24hr format. (00:00 to 23:59)."
        return desc

    @property
    def seed_switch_core_interfaces(self):
        return "Seed Switch Fabric Interfaces."

    @property
    def service_network_vlan_range(self):
        desc = "Per Switch Overlay Service Network VLAN Range "
        desc += "(Min:2, Max:4094). "
        desc += "Example: '3000-3199'"
        return desc

    @property
    def site_id(self):
        desc = "Site Id. "
        desc += "For EVPN Multi-Site Support (Min:1, Max: 281474976710655). "
        desc += "Defaults to Fabric ASN."
        return desc

    @property
    def snmp_server_host_trap(self):
        desc = "Enable NDFC as Trap Host. "
        desc += "Configure NDFC as a receiver for SNMP traps. "
        desc += "Default: True."
        return desc

    @property
    def spine_switch_core_interfaces(self):
        desc = "Spine Switch Fabric Interfaces. "
        desc += "Core-facing Interface list on all Spines (e.g. e1/1-30,e1/32)."
        return desc

    @property
    def sspine_add_del_debug_flag(self):
        desc = "Allow First Super Spine Add or Last Super Spine Delete "
        desc += "From Topology."
        return desc

    @property
    def static_underlay_ip_alloc(self):
        desc = "Manual Underlay IP Address Allocation. "
        desc += "Enabling this will disable Dynamic Underlay IP Address "
        desc += "Allocations."
        return desc

    @property
    def stp_bridge_priority(self):
        desc = "Spanning Tree Bridge Priority. "
        desc += "Bridge priority for the spanning tree in increments of 4096. "
        desc += "Valid values: 0,4096,8192,12288,16384,20480,24576,28672,"
        desc += "32768,36864,40960,45056,49152,53248,57344,61440"
        return desc

    @property
    def stp_root_option(self):
        desc = "Spanning Tree Root Bridge Protocol. "
        desc += "Which protocol to use for configuring root bridge. "
        desc += "rpvst: Rapid Per-VLAN Spanning Tree, "
        desc += "mst: Multiple Spanning Tree, "
        desc += "unmanaged (default): STP Root not managed by NDFC."
        return desc

    @property
    def stp_vlan_range(self):
        desc = "Spanning Tree VLAN Range. "
        desc += "Vlan range, Example: 1,3-5,7,9-11, Default:1-3967."
        return desc

    @property
    def strict_cc_mode(self):
        desc = "Enable Strict Config Compliance. "
        desc += "Enable bi-directional compliance checks to flag additional "
        desc += "configs in the running config that are not in the "
        desc += "intent/expected config."
        return desc

    @property
    def subinterface_range(self):
        desc = "Subinterface Dot1q Range. "
        desc += "Per Border Dot1q Range For VRF Lite Connectivity "
        desc += "(MinRange:2, MaxRange:4093), "
        desc += "Default: '2-511'."
        return desc

    @property
    def subnet_range(self):
        desc = "Underlay Subnet IP Range. "
        desc += "Address range to assign Numbered and Peer Link SVI IPs. "
        desc += "Default: '10.4.0.0/16'."
        return desc

    @property
    def subnet_target_mask(self):
        return "Underlay Subnet IP Mask."

    @property
    def syslog_server_ip_list(self):
        desc = "Syslog Server IPs. "
        desc += "Comma separated list of IP Addresses(v4/v6)."
        return desc

    @property
    def syslog_server_vrf(self):
        desc = "Syslog Server VRFs. "
        desc += "One VRF for all Syslog servers or a comma-separated list of "
        desc += "VRFs, one per Syslog server.  If a comma-separated list of "
        desc += "VRFs is used, the number of items in the list must equal the "
        desc += "number of items in SYSLOG_SERVER_IP_LIST."
        return desc

    @property
    def syslog_sev(self):
        desc = "Syslog Server Severity. "
        desc += "Comma separated list of Syslog severity values (Min:0, Max:7), "
        desc += "one value per Syslog server. "
        desc += "The number of items in the list must equal the number of "
        desc += "items in SYSLOG_SERVER_IP_LIST."
        return desc

    @property
    def tcam_allocation(self):
        desc = "TCAM commands are automatically generated for VxLAN and vPC "
        desc += "Fabric Peering when Enabled."
        return desc

    @property
    def temp_anycast_gateway(self):
        desc = "Anycast Gateway MAC Configuration."
        return desc

    @property
    def temp_vpc_domain_mgmt(self):
        desc = "vPC Keep-alive Configuration using Management VRF."
        return desc

    @property
    def temp_vpc_peer_link(self):
        desc = "TCAM commands are automatically generated for VxLAN and vPC "
        desc += "Fabric Peering when Enabled."
        return desc

    @property
    def unnum_bootstrap_lb_id(self):
        desc = "Bootstrap Seed Switch Loopback Interface ID. "
        desc += "(Min:0, Max:1023, Default: 253)."
        return desc

    @property
    def unnum_dhcp_end(self):
        desc = "Switch Loopback DHCP Scope End Address. "
        desc += "Must be a subset of IGP/BGP Loopback Prefix Pool."
        return desc

    @property
    def unnum_dhcp_start(self):
        desc = "Switch Loopback DHCP Scope Start Address. "
        desc += "Must be a subset of IGP/BGP Loopback Prefix Pool."
        return desc

    @property
    def v6_subnet_range(self):
        desc = "Underlay Subnet IPv6 Range. "
        desc += "IPv6 Address range to assign Numbered and Peer Link SVI IPs."
        return desc

    @property
    def v6_subnet_target_mask(self):
        desc = "Underlay Subnet IPv6 Mask. "
        desc += "Mask for Underlay Subnet IPv6 Range. "
        desc += "(Min: 126, Max: 127, Default: 126)."
        return desc

    @property
    def vpc_auto_recovery_time(self):
        desc = "vPC Auto Recovery Time (In Seconds). "
        desc += "(Min: 1, Max: 3600, Default: 60)."
        return desc

    @property
    def vpc_delay_restore_time(self):
        desc = "vPC Delay Restore Time For vPC links (In seconds). "
        desc += "(Min: 1, Max: 3600, Default: 60)."
        return desc

    @property
    def vpc_delay_restore(self):
        desc = "vPC Delay Restore Time (In Seconds). "
        desc += "(Min: 1, Max: 3600, Default: 150)."
        return desc

    @property
    def vpc_domain_id_range(self):
        desc = "vPC Domain ID range to use for new pairings. "
        desc += "Default: '1-1000'."
        return desc

    @property
    def vpc_peer_keep_alive_option(self):
        desc = "vPC Peer Keep Alive option. "
        desc += "Use vPC Peer Keep Alive with Loopback or Management. "
        desc += "Valid values: loopback, management."
        return desc

    @property
    def vpc_peer_link_po(self):
        return 'vPC Peer Link Port Channel ID. example: "1-40".'

    @property
    def vpc_peer_link_vlan(self):
        desc = "vPC Peer Link VLAN Range. "
        desc += "VLAN range for vPC Peer Link SVI "
        desc += "(Min:2, Max:4094, Default: 3600)."
        return desc

    @property
    def vrf_extension_template(self):
        desc = "VRF Extension Template. "
        desc = "Default Overlay VRF Template For Borders. "
        desc += "Default value: Default_VRF_Extension_Universal."
        return desc

    @property
    def vrf_lite_autoconfig(self):
        desc = "VRF Lite Inter-Fabric Connection Deployment Options. "
        desc += "If Back2Back&ToExternal is selected, VRF Lite IFCs "
        desc += "are auto created between border devices of two Easy Fabrics, "
        desc += "and between border devices in Easy Fabric and edge routers in "
        desc += "External Fabric. The IP address is taken from the "
        desc += "VRF Lite Subnet IP Range pool."
        return desc

    @property
    def vrf_vlan_range(self):
        return "Per Switch Overlay VRF VLAN Range (Min:2, Max:4094)."


class Defaults:
    """
    # Summary

    Property default values.
    """

    # pylint: disable=missing-function-docstring
    @property
    def bootstrap_multisubnet(self):
        return "#Scope_Start_IP, Scope_End_IP, Scope_Default_Gateway, Scope_Subnet_Prefix"


class FabricBase(SQLModel):
    """
    # Summary

    Base class for all other fabric classes.
    """

    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    abstract_anycast_rp: str | None = Field(default="anycast_rp")
    abstract_bgp_neighbor: str | None = Field(default="evpn_bgp_rr_neighbor")
    abstract_bgp_rr: str | None = Field(default="evpn_bgp_rr")
    abstract_bgp: str | None = Field(default="base_bgp")
    abstract_dhcp: str | None = Field(default="base_dhcp")
    abstract_extra_config_bootstrap: str | None = Field(default="extra_config_bootstrap_11_1")
    abstract_extra_config_leaf: str | None = Field(default="extra_config_leaf")
    abstract_extra_config_spine: str | None = Field(default="extra_config_spine")
    abstract_extra_config_tor: str | None = Field(default="extra_config_tor")
    abstract_feature_leaf: str | None = Field(default="base_feature_leaf_upg")
    abstract_feature_spine: str | None = Field(default="base_feature_spine_upg")
    abstract_isis: str | None = Field(default="base_isis_level2")
    abstract_isis_interface: str | None = Field(default="isis_interface")
    abstract_loopback_interface: str | None = Field(default="int_fabric_loopback_11_1")
    abstract_multicast: str | None = Field(default="base_multicast_11_1")
    abstract_ospf: str | None = Field(default="base_ospf")
    abstract_ospf_interface: str | None = Field(default="ospf_interface_11_1")
    abstract_pim_interface: str | None = Field(default="pim_interface")
    abstract_route_map: str | None = Field(default="route_map")
    abstract_routed_host: str | None = Field(default="int_routed_host")
    abstract_trunk_host: str | None = Field(default="int_trunk_host")
    abstract_vlan_interface: str | None = Field(default="int_fabric_vlan_11_1")
    abstract_vpc_domain: str | None = Field(default="base_vpc_domain_11_1")

    default_network: str | None = Field(default="Default_Network_Universal", description=Descriptions().default_network)
    default_pvlan_sec_network: str | None = Field(default="Pvlan_Secondary_Network", description=Descriptions().default_pvlan_sec_network)
    default_vrf: str | None = Field(default="Default_VRF_Universal", description=Descriptions().default_vrf)

    temp_anycast_gateway: TempAnycastGatewayEnum | None = Field(default=TempAnycastGatewayEnum.anycast_gateway, description=Descriptions().temp_anycast_gateway)
    temp_vpc_domain_mgmt: TempVpcDomainMgmtEnum | None = Field(default=TempVpcDomainMgmtEnum.vpc_domain_mgmt, description=Descriptions().temp_vpc_domain_mgmt)
    temp_vpc_peer_link: TempVpcPeerLinkEnum | None = Field(default=TempVpcPeerLinkEnum.int_vpc_peer_link_po, description=Descriptions().temp_vpc_peer_link)

    vrf_extension_template: str | None = Field(default="Default_VRF_Extension_Universal", description=Descriptions().vrf_extension_template)

    enableRealTimeBackup: bool | None = Field(default=False, description=Descriptions().enable_realtime_backup)
    enableScheduledBackup: bool | None = Field(default=False, description=Descriptions().enable_scheduled_backup)
    scheduledTime: str | None = Field(default="", description=Descriptions().scheduled_time)

    AAA_REMOTE_IP_ENABLED: bool | None = Field(default=False, description=Descriptions().aaa_remote_ip_enabled)
    AAA_SERVER_CONF: str | None = Field(default=None, description=Descriptions().aaa_server_conf)
    ACTIVE_MIGRATION: bool | None = Field(default=False)
    ADVERTISE_PIP_BGP: bool | None = Field(default=False)
    AGENT_INTF: AgentIntfEnum | None = Field(default=None, description=Descriptions().agent_intf)

    ANYCAST_BGW_ADVERTISE_PIP: bool | None = Field(default=False, description=Descriptions().anycast_bgw_advertise_pip)
    ANYCAST_GW_MAC: str | None = Field(default="2020.0000.00aa", description=Descriptions().anycast_gw_mac)
    ANYCAST_LB_ID: int | None = Field(default=10, ge=0, le=1023, description=Descriptions().anycast_lb_id)
    ANYCAST_RP_IP_RANGE: str | None = Field(default="10.254.254.0/24", description=Descriptions().anycast_rp_ip_range)
    ANYCAST_RP_IP_RANGE_INTERNAL: str | None = Field(default=None)

    AUTO_SYMMETRIC_DEFAULT_VRF: bool | None = Field(default=False)
    AUTO_SYMMETRIC_VRF_LITE: bool | None = Field(default=False)
    AUTO_VRFLITE_IFC_DEFAULT_VRF: bool | None = Field(default=False, description=Descriptions().auto_vrflite_ifc_default_vrf)

    BFD_AUTH_ENABLE: bool | None = Field(default=False)
    BFD_AUTH_KEY_ID: int | None = Field(default=100, ge=1, le=255, description=Descriptions().bfd_auth_key_id)
    BFD_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=40, description=Descriptions().bfd_auth_key)
    BFD_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_enable)
    BFD_IBGP_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_ibgp_enable)
    BFD_OSPF_ENABLE: bool | None = Field(default=False, description=Descriptions().bfd_ospf_enable)
    BFD_ISIS_ENABLE: bool | None = Field(default=False)
    BFD_PIM_ENABLE: bool | None = Field(default=False)

    BGP_AS: BgpValue = Field(index=True, description=Descriptions().bgp_as)
    BGP_AS_PREV: str | None = Field(default=None)
    BGP_AUTH_ENABLE: bool | None = Field(default=False, description=Descriptions().bgp_auth_enable)
    BGP_AUTH_KEY_TYPE: BgpAuthKeyTypeEnum | None = Field(default=BgpAuthKeyTypeEnum.Three, description=Descriptions().bgp_auth_key_type)
    BGP_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=256, description=Descriptions().bgp_auth_key)
    BGP_LB_ID: int | None = Field(default=0, ge=0, le=1023)

    BOOTSTRAP_CONF: str | None = Field(default=None, description=Descriptions().bootstrap_conf)
    BOOTSTRAP_ENABLE_PREV: bool | None = Field(default=False)
    BOOTSTRAP_ENABLE: bool | None = Field(default=False, description=Descriptions().bootstrap_enable)
    BOOTSTRAP_MULTISUBNET_INTERNAL: str | None = Field(default=None)
    BOOTSTRAP_MULTISUBNET: str | None = Field(default=Defaults().bootstrap_multisubnet, description=Descriptions().bootstrap_multisubnet)

    BRFIELD_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum.Disable, description=Descriptions().brfield_debug_flag)
    BROWNFIELD_NETWORK_NAME_FORMAT: str | None = Field(default="Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$")
    BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS: bool | None = Field(default=False, description=Descriptions().brownfield_skip_overlay_network_attachments)

    CDP_ENABLE: bool | None = Field(default=False, description=Descriptions().cdp_enable)

    COPP_POLICY: CoppPolicyEnum | None = Field(default=CoppPolicyEnum.strict, description=Descriptions().copp_policy)

    DCI_SUBNET_RANGE: str | None = Field(default="10.33.0.0/16")
    DCI_SUBNET_TARGET_MASK: int | None = Field(default=30, ge=8, le=31)

    # Yes, NDFC mispells these.
    DEAFULT_QUEUING_POLICY_CLOUDSCALE: str | None = Field(default="queuing_policy_default_8q_cloudscale", description=Descriptions().default_queuing_policy_cloudscale)
    DEAFULT_QUEUING_POLICY_OTHER: str | None = Field(default="queuing_policy_default_other", description=Descriptions().default_queuing_policy_other)
    DEAFULT_QUEUING_POLICY_R_SERIES: str | None = Field(default="queuing_policy_default_r_series", description=Descriptions().default_queuing_policy_r_series)
    DEFAULT_VRF_REDIS_BGP_RMAP: str | None = Field(default="extcon-rmap-filter", description=Descriptions().default_vrf_redis_bgp_rmap)

    DEPLOYMENT_FREEZE: bool | None = Field(default=False, description=Descriptions().deployment_freeze)

    DHCP_ENABLE: bool | None = Field(default=False, description=Descriptions().dhcp_enable)
    DHCP_END: str | None = Field(default=None, description=Descriptions().dhcp_end)
    DHCP_END_INTERNAL: str | None = Field(default=None)
    DHCP_IPV6_ENABLE_INTERNAL: str | None = Field(default=None)
    DHCP_IPV6_ENABLE: DhcpIpv6EnableEnum | None = Field(default=DhcpIpv6EnableEnum.DHCPv4, description=Descriptions().dhcp_ipv6_enable)
    DHCP_START: str | None = Field(default=None, description=Descriptions().dhcp_start)
    DHCP_START_INTERNAL: str | None = Field(default=None)

    DNS_SERVER_IP_LIST: str | None = Field(default=None, description=Descriptions().dns_server_ip_list)
    DNS_SERVER_VRF: str | None = Field(default=None, description=Descriptions().dns_server_vrf)

    ENABLE_AAA: bool | None = Field(default=False, description=Descriptions().enable_aaa)
    ENABLE_AGENT: bool | None = Field(default=False, description=Descriptions().enable_agent)
    ENABLE_DEFAULT_QUEUING_POLICY: bool | None = Field(default=False, description=Descriptions().enable_default_queuing_policy)
    ENABLE_EVPN: bool | None = Field(default=True, description=Descriptions().enable_evpn)
    ENABLE_FABRIC_VPC_DOMAIN_ID: bool | None = Field(default=False, description=Descriptions().enable_fabric_vpc_domain_id)
    ENABLE_FABRIC_VPC_DOMAIN_ID_PREV: bool | None = Field(default=False)

    ENABLE_MACSEC: bool | None = Field(default=False, description=Descriptions().enable_macsec)
    ENABLE_NETFLOW: bool | None = Field(default=False, description=Descriptions().enable_netflow)
    ENABLE_NETFLOW_PREV: bool | None = Field(default=False)
    ENABLE_NGOAM: bool | None = Field(default=True, description=Descriptions().enable_ngoam)
    ENABLE_NXAPI_HTTP: bool | None = Field(default=True, description=Descriptions().enable_nxapi_http)
    ENABLE_NXAPI: bool | None = Field(default=True, description=Descriptions().enable_nxapi)

    ENABLE_PBR: bool | None = Field(default=False)
    ENABLE_PVLAN_PREV: bool | None = Field(default=False)
    ENABLE_PVLAN: bool | None = Field(default=False, description=Descriptions().enable_pvlan)

    ENABLE_TENANT_DHCP: bool | None = Field(default=True, description=Descriptions().enable_tenant_dhcp)
    ENABLE_TRM: bool | None = Field(default=False, description=Descriptions().enable_trm)

    ENABLE_VPC_PEER_LINK_NATIVE_VLAN: bool | None = Field(default=False, description=Descriptions().enable_vpc_peer_link_native_vlan)

    EXTRA_CONF_INTRA_LINKS: str | None = Field(default=None, description=Descriptions().extra_conf_intra_links)
    EXTRA_CONF_LEAF: str | None = Field(default=None, description=Descriptions().extra_conf_leaf)
    EXTRA_CONF_SPINE: str | None = Field(default=None, description=Descriptions().extra_conf_spine)
    EXTRA_CONF_TOR: str | None = Field(default=None, description=Descriptions().extra_conf_tor)

    FABRIC_INTERFACE_TYPE: FabricInterfaceTypeEnum | None = Field(default=FabricInterfaceTypeEnum.p2p, description=Descriptions().fabric_interface_type)
    FABRIC_NAME: str | None = Field(default=None, unique=True, index=True, min_length=1, max_length=32, description=Descriptions().fabric_name)
    FABRIC_MTU: int | None = Field(default=9216, ge=576, le=9216, description=Descriptions().fabric_mtu)
    FABRIC_MTU_PREV: int | None = Field(default=9216, ge=576, le=9216)
    FABRIC_TYPE: str | None = Field(default="Switch_Fabric")
    FABRIC_VPC_DOMAIN_ID: int | None = Field(default=1, ge=1, le=1000, description=Descriptions().fabric_vpc_domain_id)
    FABRIC_VPC_DOMAIN_ID_PREV: int | None = Field(default=1, ge=1, le=1000, description=Descriptions().fabric_vpc_domain_id_prev)
    FABRIC_VPC_QOS: bool | None = Field(default=False, description=Descriptions().fabric_vpc_qos)
    FABRIC_VPC_QOS_POLICY_NAME: str | None = Field(default="spine_qos_for_fabric_vpc_peering")

    FEATURE_PTP: bool | None = Field(default=False, description=Descriptions().feature_ptp)
    FEATURE_PTP_INTERNAL: bool | None = Field(default=False)
    FF: FFEnum = Field(default="Easy_Fabric", description=Descriptions().ff)

    GRFIELD_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum.Disable, description=Descriptions().grfield_debug_flag)

    HD_TIME: int | None = Field(default=180, ge=1, le=1500, description=Descriptions().hd_time)
    HOST_INTF_ADMIN_STATE: bool | None = Field(default=False, description=Descriptions().host_intf_admin_state)

    IBGP_PEER_TEMPLATE: str | None = Field(default=None, description=Descriptions().ibgp_peer_template)
    IBGP_PEER_TEMPLATE_LEAF: str | None = Field(default=None, description=Descriptions().ibgp_peer_template_leaf)

    INBAND_DHCP_SERVERS: str | None = Field(default=None, description=Descriptions().inband_dhcp_servers)
    INBAND_MGMT_PREV: bool | None = Field(default=False)
    INBAND_MGMT: bool | None = Field(default=False, description=Descriptions().inband_mgmt)

    ISIS_AUTH_ENABLE: bool | None = Field(default=False)
    ISIS_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=255, description=Descriptions().isis_auth_key)
    ISIS_AUTH_KEYCHAIN_KEY_ID: int | None = Field(default=127, ge=0, le=65535, description=Descriptions().isis_auth_keychain_key_id)
    ISIS_AUTH_KEYCHAIN_NAME: str | None = Field(default=None, min_length=1, max_length=63, description=Descriptions().isis_auth_keychain_name)
    ISIS_LEVEL: IsisLevelEnum | None = Field(default=IsisLevelEnum.level_2, description=Descriptions().isis_level)
    ISIS_OVERLOAD_ELAPSE_TIME: int | None = Field(default=60, ge=5, le=86400, description=Descriptions().isis_overload_elapse_time)
    ISIS_OVERLOAD_ENABLE: bool | None = Field(default=True, description=Descriptions().isis_overload_enable)
    ISIS_P2P_ENABLE: bool | None = Field(default=False, description=Descriptions().isis_p2p_enable)

    L2_HOST_INTF_MTU_PREV: int | None = Field(default=9216, ge=1500, le=9216)
    L2_HOST_INTF_MTU: int | None = Field(default=9216, ge=1500, le=9216, description=Descriptions().l2_host_intf_mtu)
    L2_SEGMENT_ID_RANGE: str | None = Field(default="30000-49000", description=Descriptions().l2_segment_id_range)

    L3_PARTITION_ID_RANGE: str | None = Field(default="50000-59000")
    L3VNI_MCAST_GROUP: str | None = Field(default="239.1.1.0", description=Descriptions().l3vni_mcast_group)

    LINK_STATE_ROUTING_TAG_PREV: str | None = Field(default=None, description=Descriptions().loopback1_ip_range)
    LINK_STATE_ROUTING_TAG: str | None = Field(default="UNDERLAY", min_length=1, max_length=20, description=Descriptions().link_state_routing_tag)
    LINK_STATE_ROUTING: LinkStateRoutingEnum | None = Field(default=LinkStateRoutingEnum.ospf, description=Descriptions().link_state_routing)

    LOOPBACK0_IP_RANGE: str | None = Field(default="10.2.0.0/22", description=Descriptions().loopback0_ip_range)
    LOOPBACK0_IPV6_RANGE: str | None = Field(default="fd00::a02:0/119", description=Descriptions().loopback0_ipv6_range)
    LOOPBACK1_IP_RANGE: str | None = Field(default="10.3.0.0/22", description=Descriptions().loopback1_ip_range)
    LOOPBACK1_IPV6_RANGE: str | None = Field(default="fd00::a03:0/118", description=Descriptions().loopback1_ipv6_range)

    MACSEC_ALGORITHM: MacsecAlgorithmEnum | None = Field(default=MacsecAlgorithmEnum.AES_128_CMAC, description=Descriptions().macsec_algorithm)
    MACSEC_CIPHER_SUITE: MacsecCipherSuiteEnum | None = Field(default=MacsecCipherSuiteEnum.GCM_AES_XPN_256, description=Descriptions().macsec_cipher_suite)
    MACSEC_FALLBACK_ALGORITHM: MacsecAlgorithmEnum | None = Field(default=MacsecAlgorithmEnum.AES_128_CMAC, description=Descriptions().macsec_fallback_algorithm)
    MACSEC_FALLBACK_KEY_STRING: str | None = Field(default=None, min_length=1, max_length=130, description=Descriptions().macsec_fallback_key_string)
    MACSEC_KEY_STRING: str | None = Field(default=None, min_length=1, max_length=130, description=Descriptions().macsec_key_string)
    MACSEC_REPORT_TIMER: int | None = Field(default=5, ge=5, le=60, description=Descriptions().macsec_report_timer)

    MGMT_GW_INTERNAL: str | None = Field(default=None)
    MGMT_GW: str | None = Field(default=None, description=Descriptions().mgmt_gw)
    MGMT_PREFIX_INTERNAL: int | None = Field(default=None)
    MGMT_PREFIX: int | None = Field(default=24, ge=8, le=30, description=Descriptions().mgmt_prefix)
    MGMT_V6PREFIX_INTERNAL: int | None = Field(default=None)
    MGMT_V6PREFIX: int | None = Field(default=64, ge=64, le=126, description=Descriptions().mgmt_v6prefix)

    MPLS_HANDOFF: bool | None = Field(default=False, description=Descriptions().mpls_handoff)
    MPLS_LB_ID: int | None = Field(default=101, ge=0, le=1023, description=Descriptions().mpls_lb_id)
    MPLS_LOOPBACK_IP_RANGE: str | None = Field(default="10.101.0.0/25", description=Descriptions().mpls_loopback_ip_range)

    MSO_CONNECTIVITY_DEPLOYED: str | None = Field(default=None)
    # Yes, NDFC mispells this
    MSO_CONTROLER_ID: str | None = Field(default=None)
    MSO_SITE_GROUP_NAME: str | None = Field(default=None)
    MSO_SITE_ID: str | None = Field(default=None)

    MST_INSTANCE_RANGE: str | None = Field(default="0", description=Descriptions().mst_instance_range)
    MULTICAST_GROUP_SUBNET: str | None = Field(default="239.1.1.0/25", description=Descriptions().multicast_group_subnet)

    NETFLOW_EXPORTER_LIST: str | None = Field(default=None, description=Descriptions().netflow_exporter_list)
    NETFLOW_MONITOR_LIST: str | None = Field(default=None, description=Descriptions().netflow_monitor_list)
    NETFLOW_RECORD_LIST: str | None = Field(default=None, description=Descriptions().netflow_record_list)

    network_extension_template: str | None = Field(default="Default_Network_Extension_Universal", description=Descriptions().network_extension_template)
    NETWORK_VLAN_RANGE: str | None = Field(default="2300-2999", description=Descriptions().network_vlan_range)

    NTP_SERVER_IP_LIST: str | None = Field(default=None, description=Descriptions().ntp_server_ip_list)
    NTP_SERVER_VRF: str | None = Field(default=None, description=Descriptions().ntp_server_vrf)

    NVE_LB_ID: int | None = Field(default=1, ge=0, le=1023, description=Descriptions().nve_lb_id)

    OSPF_AREA_ID: str | None = Field(default="0.0.0.0", description=Descriptions().ospf_area_id)
    OSPF_AUTH_ENABLE: bool | None = Field(default=False, description=Descriptions().ospf_auth_enable)
    OSPF_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=256, description=Descriptions().ospf_auth_key)
    OSPF_AUTH_KEY_ID: int | None = Field(default=127, ge=0, le=255, description=Descriptions().ospf_auth_key_id)

    OVERLAY_MODE_PREV: OverlayModeEnum | None = Field(default=OverlayModeEnum.cli)
    OVERLAY_MODE: OverlayModeEnum | None = Field(default=OverlayModeEnum.cli, description=Descriptions().overlay_mode)

    PHANTOM_RP_LB_ID1: str | None = Field(default=None)
    PHANTOM_RP_LB_ID2: str | None = Field(default=None)
    PHANTOM_RP_LB_ID3: str | None = Field(default=None)
    PHANTOM_RP_LB_ID4: str | None = Field(default=None)

    PIM_HELLO_AUTH_ENABLE: bool | None = Field(default=False, description=Descriptions().pim_hello_auth_enable)
    PIM_HELLO_AUTH_KEY: str | None = Field(default=None, min_length=1, max_length=256, description=Descriptions().pim_hello_auth_key)

    PM_ENABLE_PREV: bool | None = Field(default=False)
    PM_ENABLE: bool | None = Field(default=False, description=Descriptions().pm_enable)

    POWER_REDUNDANCY_MODE: PowerRedundancyModeEnum | None = Field(default=PowerRedundancyModeEnum.ps_redundant, description=Descriptions().power_redundancy_mode)

    PREMSO_PARENT_FABRIC: str | None = Field(default=None)

    PTP_DOMAIN_ID: int | None = Field(default=0, ge=0, le=127)
    PTP_LB_ID: int | None = Field(default=0, ge=0, le=1023, description=Descriptions().ptp_lb_id)

    REPLICATION_MODE: ReplicationModeEnum | None = Field(default=ReplicationModeEnum.Multicast, description=Descriptions().replication_mode)
    ROUTER_ID_RANGE: str | None = Field(default=None, description=Descriptions().router_id_range)
    ROUTE_MAP_SEQUENCE_NUMBER_RANGE: str | None = Field(default=None, description=Descriptions().route_map_sequence_number_range)
    RP_COUNT: RpCountEnum | None = Field(default=RpCountEnum.Two, description=Descriptions().rp_count)
    RP_LB_ID: int | None = Field(default=254, ge=0, le=1023, description=Descriptions().rp_lb_id)
    RP_MODE: RpModeEnum | None = Field(default=RpModeEnum.asm, description=Descriptions().rp_mode)
    RR_COUNT: RrCountEnum | None = Field(default=RrCountEnum.Two, description=Descriptions().rr_count)

    SEED_SWITCH_CORE_INTERFACES: str | None = Field(default=None, description=Descriptions().seed_switch_core_interfaces)
    SERVICE_NETWORK_VLAN_RANGE: str | None = Field(default="3000-3199", description=Descriptions().service_network_vlan_range)
    SITE_ID: str | None = Field(default=None, min_length=1, max_length=15, description=Descriptions().site_id)
    SNMP_SERVER_HOST_TRAP: bool | None = Field(default=True, description=Descriptions().snmp_server_host_trap)

    SPINE_COUNT: int | None = Field(default=0)
    SPINE_SWITCH_CORE_INTERFACES: str | None = Field(default="", description=Descriptions().spine_switch_core_interfaces)

    SSPINE_COUNT: int | None = Field(default=0)
    SSPINE_ADD_DEL_DEBUG_FLAG: EnableDisableEnum | None = Field(default=EnableDisableEnum.Disable, description=Descriptions().sspine_add_del_debug_flag)

    STATIC_UNDERLAY_IP_ALLOC: bool | None = Field(default=False, description=Descriptions().static_underlay_ip_alloc)

    STP_BRIDGE_PRIORITY: StpBridgePriorityEnum | None = Field(default=StpBridgePriorityEnum.STPP_0, description=Descriptions().stp_bridge_priority)
    STP_ROOT_OPTION: StpRootOptionEnum | None = Field(default=StpRootOptionEnum.unmanaged, description=Descriptions().stp_root_option)
    SPT_VLAN_RANGE: str | None = Field(default="1-3967", description=Descriptions().stp_vlan_range)

    STRICT_CC_MODE: bool | None = Field(default=False, description=Descriptions().strict_cc_mode)

    SUBINTERFACE_RANGE: str | None = Field(default="2-511", description=Descriptions().subinterface_range)
    SUBNET_RANGE: str | None = Field(default="10.4.0.0/16", description=Descriptions().subnet_range)
    SUBNET_TARGET_MASK: int | None = Field(default=30, ge=30, le=31, description=Descriptions().subnet_target_mask)

    SYSLOG_SERVER_IP_LIST: str | None = Field(default="", description=Descriptions().syslog_server_ip_list)
    SYSLOG_SERVER_VRF: str | None = Field(default="", description=Descriptions().syslog_server_vrf)
    SYSLOG_SEV: str | None = Field(default="", description=Descriptions().syslog_sev)

    TCAM_ALLOCATION: bool | None = Field(default=True, description=Descriptions().tcam_allocation)
    UNDERLAY_IS_V6: bool | None = Field(default=False)

    UNNUM_BOOTSTRAP_LB_ID: int | None = Field(default=253, ge=0, le=1023, description=Descriptions().unnum_bootstrap_lb_id)
    UNNUM_DHCP_END: str | None = Field(default="", description=Descriptions().unnum_dhcp_end)
    UNNUM_DHCP_END_INTERNAL: str | None = Field(default="")
    UNNUM_DHCP_START: str | None = Field(default="", description=Descriptions().unnum_dhcp_start)
    UNNUM_DHCP_START_INTERNAL: str | None = Field(default="")

    USE_LINK_LOCAL: bool | None = Field(default=False)

    V6_SUBNET_RANGE: str | None = Field(default="fd00::a04:0/112", description=Descriptions().v6_subnet_range)
    V6_SUBNET_TARGET_MASK: int | None = Field(default=126, ge=126, le=127, description=Descriptions().v6_subnet_target_mask)

    VPC_AUTO_RECOVERY_TIME: int | None = Field(default=360, ge=240, le=3600, description=Descriptions().vpc_auto_recovery_time)
    VPC_DELAY_RESTORE_TIME: int | None = Field(default=60, ge=1, le=3600, description=Descriptions().vpc_delay_restore_time)
    VPC_DELAY_RESTORE: int | None = Field(default=150, ge=1, le=3600, description=Descriptions().vpc_delay_restore)
    VPC_DOMAIN_ID_RANGE: str | None = Field(default="1-1000", description=Descriptions().vpc_domain_id_range)
    VPC_ENABLE_IPv6_ND_SYNC: bool | None = Field(default=True)
    VPC_PEER_KEEP_ALIVE_OPTION: VpcPeerKeepAliveOptionEnum | None = Field(default=VpcPeerKeepAliveOptionEnum.management, description=Descriptions().vpc_peer_keep_alive_option)
    VPC_PEER_LINK_PO: str | None = Field(default="500", description=Descriptions().vpc_peer_link_po)
    VPC_PEER_LINK_VLAN: str | None = Field(default="3600", description=Descriptions().vpc_peer_link_vlan)

    VRF_LITE_AUTOCONFIG: VrfLiteAutoconfigEnum | None = Field(default=VrfLiteAutoconfigEnum.Manual, description=Descriptions().vrf_lite_autoconfig)
    VRF_VLAN_RANGE: str | None = Field(default="2000-2299", description=Descriptions().vrf_vlan_range)


class FabricDbModelV1(FabricBase, table=True):
    """
    # Summary

    Define the fabric table in the database.
    """

    model_config = ConfigDict(use_enum_values=True)
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=get_datetime)

    updated_at: datetime | None = Field(
        default_factory=get_datetime,
        sa_column_kwargs={"onupdate": get_datetime},
    )


class FabricCreate(FabricBase):
    """
    # Summary

    Used to validate POST request content.
    """

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class NvPairs(FabricBase):
    """
    # Summary

    Defines the contents of the nvPairs object within a fabric
    response.
    """

    model_config = ConfigDict(use_enum_values=True)

    # created_at: datetime | None
    # updated_at: datetime | None


class FabricResponseModel(SQLModel):
    """
    # Summary

    Describes what is returned to clients.
    """

    model_config = ConfigDict(use_enum_values=True)

    id: int
    nvPairs: NvPairs


class FabricUpdate(SQLModel):
    """
    # Summary

    Used to validate PUT requests.
    """

    model_config = ConfigDict(use_enum_values=True)

    AAA_REMOTE_IP_ENABLED: bool | None = None
    AAA_SERVER_CONF: str | None = None
    ACTIVE_MIGRATION: bool | None = None
    ADVERTISE_PIP_BGP: bool | None = None
    AGENT_INTF: AgentIntfEnum | None = None

    ANYCAST_BGW_ADVERTISE_PIP: bool | None = None
    ANYCAST_GW_MAC: str | None = None
    ANYCAST_LB_ID: int | None = None
    ANYCAST_RP_IP_RANGE: str | None = None

    AUTO_SYMMETRIC_DEFAULT_VRF: bool | None = None
    AUTO_SYMMETRIC_VRF_LITE: bool | None = None
    AUTO_VRFLITE_IFC_DEFAULT_VRF: bool | None = None

    BFD_AUTH_ENABLE: bool | None = None
    BFD_AUTH_KEY_ID: int | None = None
    BFD_AUTH_KEY: str | None = None
    BFD_ENABLE: bool | None = None
    BFD_IBGP_ENABLE: bool | None = None
    BFD_OSPF_ENABLE: bool | None = None
    BFD_ISIS_ENABLE: bool | None = None
    BFD_PIM_ENABLE: bool | None = None

    BGP_AS: BgpValue | None = None
    BGP_AUTH_ENABLE: bool | None = None
    BGP_AUTH_KEY_TYPE: BgpAuthKeyTypeEnum | None = None
    BGP_AUTH_KEY: str | None = None
    BGP_LB_ID: int | None = None

    BOOTSTRAP_CONF: str | None = None
    BOOTSTRAP_ENABLE: bool | None = None
    BOOTSTRAP_MULTISUBNET: str | None = None

    BRFIELD_DEBUG_FLAG: EnableDisableEnum | None = None
    BROWNFIELD_NETWORK_NAME_FORMAT: str | None = None
    BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS: bool | None = None

    CDP_ENABLE: bool | None = None

    COPP_POLICY: CoppPolicyEnum | None = None

    DCI_SUBNET_RANGE: str | None = None
    DCI_SUBNET_TARGET_MASK: int | None = None

    # Yes, NDFC mispells these.
    DEAFULT_QUEUING_POLICY_CLOUDSCALE: str | None = None
    DEAFULT_QUEUING_POLICY_OTHER: str | None = None
    DEAFULT_QUEUING_POLICY_R_SERIES: str | None = None
    DEFAULT_VRF_REDIS_BGP_RMAP: str | None = None

    DEPLOYMENT_FREEZE: bool | None = None

    DHCP_ENABLE: bool | None = None
    DHCP_END: str | None = None
    DHCP_IPV6_ENABLE: DhcpIpv6EnableEnum | None = None
    DHCP_START: str | None = None

    DNS_SERVER_IP_LIST: str | None = None
    DNS_SERVER_VRF: str | None = None

    ENABLE_AAA: bool | None = None
    ENABLE_AGENT: bool | None = None
    ENABLE_DEFAULT_QUEUING_POLICY: bool | None = None
    ENABLE_EVPN: bool | None = None
    ENABLE_FABRIC_VPC_DOMAIN_ID: bool | None = None

    ENABLE_MACSEC: bool | None = None
    ENABLE_NETFLOW: bool | None = None
    ENABLE_NGOAM: bool | None = None
    ENABLE_NXAPI_HTTP: bool | None = None
    ENABLE_NXAPI: bool | None = None

    ENABLE_PBR: bool | None = None
    ENABLE_PVLAN: bool | None = None

    ENABLE_TENANT_DHCP: bool | None = None
    ENABLE_TRM: bool | None = None

    ENABLE_VPC_PEER_LINK_NATIVE_VLAN: bool | None = None

    EXTRA_CONF_INTRA_LINKS: str | None = None
    EXTRA_CONF_LEAF: str | None = None
    EXTRA_CONF_SPINE: str | None = None
    EXTRA_CONF_TOR: str | None = None

    FABRIC_INTERFACE_TYPE: FabricInterfaceTypeEnum | None = None
    FABRIC_NAME: str | None = None
    FABRIC_MTU: int | None = None
    FABRIC_TYPE: str | None = None
    FABRIC_VPC_DOMAIN_ID: int | None = None
    FABRIC_VPC_QOS: bool | None = None
    FABRIC_VPC_QOS_POLICY_NAME: str | None = None

    FEATURE_PTP: bool | None = None

    GRFIELD_DEBUG_FLAG: EnableDisableEnum | None = None

    HD_TIME: int | None = None
    HOST_INTF_ADMIN_STATE: bool | None = None

    IBGP_PEER_TEMPLATE: str | None = None
    IBGP_PEER_TEMPLATE_LEAF: str | None = None

    INBAND_DHCP_SERVERS: str | None = None
    INBAND_MGMT: bool | None = None

    ISIS_AUTH_ENABLE: bool | None = None
    ISIS_AUTH_KEY: str | None = None
    ISIS_AUTH_KEYCHAIN_KEY_ID: int | None = None
    ISIS_AUTH_KEYCHAIN_NAME: str | None = None
    ISIS_LEVEL: IsisLevelEnum | None = None
    ISIS_OVERLOAD_ELAPSE_TIME: int | None = None
    ISIS_OVERLOAD_ENABLE: bool | None = None
    ISIS_P2P_ENABLE: bool | None = None

    L2_HOST_INTF_MTU: int | None = None
    L2_SEGMENT_ID_RANGE: str | None = None

    L3_PARTITION_ID_RANGE: str | None = None
    L3VNI_MCAST_GROUP: str | None = None

    LINK_STATE_ROUTING: LinkStateRoutingEnum | None = None
    LINK_STATE_ROUTING_TAG: str | None = None

    LOOPBACK0_IP_RANGE: str | None = None
    LOOPBACK0_IPV6_RANGE: str | None = None
    LOOPBACK1_IP_RANGE: str | None = None
    LOOPBACK1_IPV6_RANGE: str | None = None

    MACSEC_ALGORITHM: MacsecAlgorithmEnum | None = None
    MACSEC_CIPHER_SUITE: MacsecCipherSuiteEnum | None = None
    MACSEC_FALLBACK_ALGORITHM: MacsecAlgorithmEnum | None = None
    MACSEC_FALLBACK_KEY_STRING: str | None = None
    MACSEC_KEY_STRING: str | None = None
    MACSEC_REPORT_TIMER: int | None = None

    MGMT_GW: str | None = None
    MGMT_PREFIX: int | None = None
    MGMT_V6PREFIX: int | None = None

    MPLS_HANDOFF: bool | None = None
    MPLS_LB_ID: int | None = None
    MPLS_LOOPBACK_IP_RANGE: str | None = None

    MSO_CONNECTIVITY_DEPLOYED: str | None = None
    # Yes, NDFC mispells this
    MSO_CONTROLER_ID: str | None = None
    MSO_SITE_GROUP_NAME: str | None = None
    MSO_SITE_ID: str | None = None

    MST_INSTANCE_RANGE: str | None = None
    MULTICAST_GROUP_SUBNET: str | None = None

    NETFLOW_EXPORTER_LIST: str | None = None
    NETFLOW_MONITOR_LIST: str | None = None
    NETFLOW_RECORD_LIST: str | None = None

    network_extension_template: str | None = None
    NETWORK_VLAN_RANGE: str | None = None

    NTP_SERVER_IP_LIST: str | None = None
    NTP_SERVER_VRF: str | None = None

    NVE_LB_ID: int | None = None

    OSPF_AREA_ID: str | None = None
    OSPF_AUTH_ENABLE: bool | None = None
    OSPF_AUTH_KEY: str | None = None
    OSPF_AUTH_KEY_ID: int | None = None

    OVERLAY_MODE: OverlayModeEnum | None = None

    PHANTOM_RP_LB_ID1: str | None = None
    PHANTOM_RP_LB_ID2: str | None = None
    PHANTOM_RP_LB_ID3: str | None = None
    PHANTOM_RP_LB_ID4: str | None = None

    PIM_HELLO_AUTH_ENABLE: bool | None = None
    PIM_HELLO_AUTH_KEY: str | None = None

    PM_ENABLE: bool | None = None

    POWER_REDUNDANCY_MODE: PowerRedundancyModeEnum | None = None

    PTP_DOMAIN_ID: int | None = None
    PTP_LB_ID: int | None = None

    REPLICATION_MODE: ReplicationModeEnum | None = None
    ROUTER_ID_RANGE: str | None = None
    ROUTE_MAP_SEQUENCE_NUMBER_RANGE: str | None = None
    RP_COUNT: RpCountEnum | None = None
    RP_LB_ID: int | None = None
    RP_MODE: RpModeEnum | None = None
    RR_COUNT: RrCountEnum | None = None

    SEED_SWITCH_CORE_INTERFACES: str | None = None
    SERVICE_NETWORK_VLAN_RANGE: str | None = None
    SITE_ID: str | None = None
    SNMP_SERVER_HOST_TRAP: bool | None = None

    SPINE_SWITCH_CORE_INTERFACES: str | None = None

    SSPINE_ADD_DEL_DEBUG_FLAG: EnableDisableEnum | None = None

    STATIC_UNDERLAY_IP_ALLOC: bool | None = None

    STP_BRIDGE_PRIORITY: StpBridgePriorityEnum | None = None
    STP_ROOT_OPTION: StpRootOptionEnum | None = None
    SPT_VLAN_RANGE: str | None = None

    STRICT_CC_MODE: bool | None = None

    SUBINTERFACE_RANGE: str | None = None
    SUBNET_RANGE: str | None = None
    SUBNET_TARGET_MASK: int | None = None

    SYSLOG_SERVER_IP_LIST: str | None = None
    SYSLOG_SERVER_VRF: str | None = None
    SYSLOG_SEV: str | None = None

    TCAM_ALLOCATION: bool | None = None
    UNDERLAY_IS_V6: bool | None = None

    UNNUM_BOOTSTRAP_LB_ID: int | None = None
    UNNUM_DHCP_END: str | None = None
    UNNUM_DHCP_START: str | None = None

    USE_LINK_LOCAL: bool | None = None

    V6_SUBNET_RANGE: str | None = None
    V6_SUBNET_TARGET_MASK: int | None = None

    VPC_AUTO_RECOVERY_TIME: int | None = None
    VPC_DELAY_RESTORE_TIME: int | None = None
    VPC_DELAY_RESTORE: int | None = None
    VPC_DOMAIN_ID_RANGE: str | None = None
    VPC_ENABLE_IPv6_ND_SYNC: bool | None = None
    VPC_PEER_KEEP_ALIVE_OPTION: VpcPeerKeepAliveOptionEnum | None = None
    VPC_PEER_LINK_PO: str | None = None
    VPC_PEER_LINK_VLAN: str | None = None

    VRF_LITE_AUTOCONFIG: VrfLiteAutoconfigEnum | None = None
    VRF_VLAN_RANGE: str | None = None
