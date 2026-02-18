# ansible-dcnm.dcnm_inventory - merge state call flow

Endpoint call flow used by the [ansible-dcnm - dcnm_inventory][dcnm_inventory] module for merge state.

## 1. test-reachability

### Endpoint (test-reachability)

```openapi
POST /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/test-reachability
```

#### Body (test-reachability)

```json
{
    "cdpSecondTimeout": 5,
    "discoveryCredForLan": false,
    "maxHops": "0",
    "password": "mypassword",
    "preserveConfig": true,
    "seedIP": "172.22.150.106",
    "snmpV3AuthProtocol": 0,
    "username": "admin"
}
```

#### Response (test-reachability)

```json
[
    {
        "auth": true,
        "deviceIndex": "cvd-2311-leaf(FDO211218HB)",
        "hopCount": 0,
        "ipaddr": "172.22.150.106",
        "known": false,
        "lastChange": null,
        "platform": "N9K-C93180YC-EX",
        "reachable": true,
        "selectable": true,
        "serialNumber": "FDO211218HB",
        "statusReason": "manageable",
        "switchRole": null,
        "sysName": "cvd-2311-leaf",
        "valid": true,
        "vdcId": 0,
        "vdcMac": null,
        "vendor": "Cisco",
        "version": "10.2(5)"
    }
]
```

## 2. discover

### Endpoint (discover)

```openapi
POST /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/discover
```

### Body (discover)

```json
{
    "cdpSecondTimeout": 5,
    "discoveryCredForLan": false,
    "maxHops": "0",
    "password": "mypassword",
    "preserveConfig": true,
    "seedIP": "172.22.150.106",
    "snmpV3AuthProtocol": 0,
    "username": "admin"
}
```

### Response (discover)

```json
{
    "status": "Success"
}
```

## 3. rediscover

### Endpoint (rediscover)

```openapi
POST /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/inventory/rediscover/{serialNumber}
```

### Body (rediscover)

None

### Response (rediscover)

```json
{
    "resultMessage": "OK",
    "resultStatus": 0,
    "resultId": null,
    "resultStats": null
}
```

## 4. getLanSwitchCredentials

### Endpoint (getLanSwitchCredentials)

```openapi
GET /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig/getLanSwitchCredentials
```

### Response (getLanSwitchCredentials)

```json
[
    {
        "credType": "Robot",
        "groupName": "F1",
        "ipAddress": "172.22.150.107",
        "sshPassword": "*****",
        "sshUserName": "admin",
        "switchDbID": "27470",
        "switchName": "cvd-2312-leaf",
        "v3Protocol": "0"
    }
]
```

## 5. internal.topology.role

Set the role of a switch, given switchDbID.  

This is an internal endpoint and will likely be deprecated.  It continues to work in the following versions.

- ND 3.0.1i
  - NDFC 12.1.3b
- ND 3.2.1e
  - NDFC 12.2.2.238
- ND 4.0 LA

### Endpoint (internal.topology.role)

```openapi
PUT /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/topology/role/{switchDbID}?newRole=spine
```

### Response (internal.topology.role)

```json
{
    "tierLevel": 2,
    "newRole": "spine"
}
```

[dcnm_inventory]: <https://github.com/CiscoDevNet/ansible-dcnm/blob/main/plugins/modules/dcnm_inventory.py>
