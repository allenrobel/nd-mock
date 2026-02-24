# Summary

Cisco Nexus Dashboard manages network infrastructure using a logical
hierarchy:

Fabric (Group) > Fabric > VRF > Network > Switch > Interface

This structure enables top-down policy deployment, where global settings
are defined at the Fabric level, segmented by VRFs, partitioned into
networks, and deployed onto physical switches.

## Object Hierarchy

* Fabric Group/Multi-Site Domain (MSD): Highest level; manages multiple fabrics and interconnectivity.
* Fabric: A logical container (e.g., VXLAN BGP EVPN) representing a physical site or data center.
* VRF (Virtual Routing and Forwarding): Segmentation within a fabric (Layer 3 overlay).
* Network/Bridge Domain: Subset of a VRF; defines VLANs and subnet connectivity (Layer 2).
* Switch (Leaf/Spine): Physical devices within the fabric where configurations are applied.
* Interface: Physical port (port-channel, access, trunk) on a switch. 

## Key Points

* Inheritance: VRFs and Networks are defined within a fabric and inherited by member switches (when attached to a member switch).
* Topology: Fabric shows the physical layout and link connections.
* Object Relationships: Networks must belong to a VRF, which must reside in a Fabric.
* Management: Switches are added to Fabrics, and configurations (networks, VRFs) are pushed down to the switch interfaces.

## Example constraints

* An object cannot be created if it already exists.
* A Fabric cannot be modified (adding a VRF, Network, etc) if it is in read_only mode.
* A Fabric cannot be deleted if it contains one or more switches.
* A VRF cannot be deleted if it is attached to one or more switches.
* A Network cannot be deleted if it is attached to one or more switches.

## Example operations

### Create VRF

#### Request Create VRF

##### Verb Create VRF

POST

##### Endpoint Create VRF

/api/v1/manage/fabrics/{fabricName}/vrfs

##### Payload Create VRF

```json
{
  "vrfs": [
    {
      "fabricName": "fabric1",
      "vrfName": "MyVRF_50001",
      "vrfType": "vxlanIbgp",
      "coreData": {
        "vrfVlanName": "MyVLAN_2001",
        "vrfInterfaceDescription": "VRF 50001, VLAN 2001",
        "vrfDescription": "PROD",
        "mtu": 9216,
        "routingTag": 12345,
        "vrfRouteMap": "FABRIC-RMAP-REDIST-SUBNET",
        "v6VrfRouteMap": "FABRIC-RMAP-REDIST-SUBNET",
        "maxBgpPaths": 1,
        "maxIbgpPaths": 2,
        "ipv6LinkLocal": true,
        "rtAuto": false,
        "routeTargetImport": [],
        "routeTargetExport": [],
        "evpnRouteTargetImport": [],
        "evpnRouteTargetExport": []
      },
      "fabricData": {
        "bgpBestPathRelax": false,
        "bgpLogNeighborChange": false,
        "trmData": {
          "ipv4Trm": false,
          "v4RpAbsent": false,
          "v4RpExternal": false,
          "v4RpAddress": "",
          "loopbackNumber": null,
          "l3VniMulticastGroup": "",
          "v4MulticastGroup": "",
          "ipv6Trm": false,
          "v6RpAbsent": false,
          "v6RpExternal": false,
          "v6RpAddress": "",
          "v6MulticastGroup": "",
          "mvpnInterAs": false,
          "trmOnBgw": false,
          "mvpnRouteTargetImport": [],
          "mvpnRouteTargetExport": []
        },
        "advertiseHostRoute": false,
        "advertiseDefaultRoute": true,
        "configureStaticDefaultRoute": true,
        "bgpPassword": "",
        "bgpPasswordKeyType": "",
        "bgpAllowAsIn": false,
        "bgpAllowAsInNum": 3,
        "bgpAsOverride": false,
        "bgpDisablePeerAsCheck": false,
        "bgpSoftReconfigAlways": false,
        "netflow": false,
        "netflowMonitor": ""
      },
      "vrfId": 50001,
      "vlanId": 2001
    }
  ]
}
```

#### Response Create VRF

##### Response Success Status Create VRF

207

##### Response Body Create VRF

```json
{
  "results": [
    {
      "status": "success",
      "vrfId": 50001,
      "vrfName": "MyVRF_50001"
    }
  ]
}
```

### Attach / Detach VRFs

#### Request Attach / Detach VRFs

##### Verb Attach / Detach VRFs

POST

##### Endpoint Attach / Detach VRFs

/api/v1/manage/fabrics/{fabricName}/vrfAttachments

##### Payload Attach / Detach VRFs

```json
{
  "attachments": [
    {
      "attach": true,
      "extensionValues": [
        {
          "autoPeerConfig": false,
          "dot1qId": 2,
          "interfaceName": "Ethernet1/8",
          "ipv4Address": "1.10.13.123/24",
          "ipv6Address": "2001:db8::/32",
          "ipv6RouteMapIn": "",
          "ipv6RouteMapOut": "EXTCON-RMAP-FILTER-V6",
          "mtu": 9216,
          "neighborAsn": "6578",
          "neighborIpv4Address": "1.10.13.124",
          "neighborIpv6Address": "2001:db8::1",
          "netflow": false,
          "peerVrfName": "MyVRF_50001",
          "routeMapIn": "",
          "routeMapOut": "EXTCON-RMAP-FILTER",
          "routeTag": 1
        }
      ],
      "extraConfig": "interface Ethernet1/1\n  description Link to core switch\n  no shutdown\n",
      "instanceValues": {
        "loopbackId": 23,
        "loopbackIpv4": "1.1.1.2",
        "loopbackIpv6": "2051:17:200::11"
      },
      "switchId": "FDO245206N5",
      "vlanId": 2000,
      "vrfName": "MyVRF_50000"
    },
    {
      "attach": false,
      "extraConfig": "interface Ethernet1/2\n  description Backup link\n  shutdown\n",
      "instanceValues": {
        "loopbackId": 24,
        "loopbackIpv4": "1.1.1.3",
        "loopbackIpv6": "2051:17:200::11"
      },
      "switchId": "FDO245206N6",
      "vlanId": 3000,
      "vrfName": "MyVRF_50000"
    },
    {
      "attach": true,
      "extraConfig": "interface Ethernet1/3\n  description High-speed connection\n  no shutdown\n",
      "instanceValues": {
        "loopbackId": 26,
        "loopbackIpv4": "1.1.1.4",
        "loopbackIpv6": "2051:17:200::11"
      },
      "switchId": "FDO245206N7",
      "vlanId": 4000,
      "vrfName": "MyVRF_50001"
    }
  ]
}
```

#### Query VRF Attachments

##### Verb Query VRF Attachments

POST

##### Endpoint Query VRF Attachments

 /api/v1/manage/fabrics/fabric1/vrfAttachments/query

##### Payload Query VRF Attachments

```json
{
  "switchIds":["945V7U23QJ7"],
  "vrfNames":["MyVRF_50000"]
}
```

#### Response

##### Response Success Status Query VRF Attachments

200

##### Response Body Query VRF Attachments

```json
{
  "attachments": [
    {
      "attach": false,
      "errorMessage": null,
      "instanceValues": {},
      "showVlan": true,
      "status": "notApplicable",
      "switchId": "945V7U23QJ7",
      "switchName": "LE1",
      "switchRole": "leaf",
      "vrfName": "MyVRF_50000"
    }
  ],
  "meta": {
    "counts": {
      "remaining": 0,
      "total": 1
    }
  }
}
```
