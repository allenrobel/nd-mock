#!/usr/bin/env bash
curl -s -X POST http://localhost:8000/api/v1/manage/fabrics/fabric1/vrfs \
    -H "Content-Type: application/json" \
    -d '{
  "vrfs": [
    {
      "fabricName": "fabric1",
      "vrfName": "MyVRF_50000",
      "vrfType": "vxlanIbgp",
      "coreData": {
        "vrfVlanName": "MyVLAN_2000",
        "vrfInterfaceDescription": "VRF 50000, VLAN 2000",
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
      "vrfId": 50000,
      "vlanId": 2000
    }
  ]
}' | python -m json.tool

