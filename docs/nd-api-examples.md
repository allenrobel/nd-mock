# Nexus Dashboard API Examples

Detailed request/response examples for ND operations.

## Create VRF

**POST** `/api/v1/manage/fabrics/{fabricName}/vrfs`

**Status**: 207

**Request**:
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

**Response**:
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

## Attach / Detach VRFs

**POST** `/api/v1/manage/fabrics/{fabricName}/vrfAttachments`

**Status**: 207

**Request**:
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

**Response**:
```json
{
  "results": [
    {
      "status": "success",
      "switchId": "945V7U23QJ7",
      "switchName": "LE1",
      "vrfName": "MyVRF_50000"
    }
  ]
}
```

## Query VRF Attachments

**POST** `/api/v1/manage/fabrics/fabric1/vrfAttachments/query`

**Status**: 200

**Request**:
```json
{
  "switchIds": ["945V7U23QJ7"],
  "vrfNames": ["MyVRF_50000"]
}
```

**Response**:
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
