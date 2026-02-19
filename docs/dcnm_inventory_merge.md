# ansible-dcnm.dcnm_inventory - merge state call flow

Endpoint call flow used by the [ansible-dcnm - dcnm_inventory][dcnm_inventory] module for merge state.

These are the v2 (manage) API endpoints introduced in Nexus Dashboard 4.x. The v1 (`lan-fabric/rest`) endpoints are deprecated in ND 4.2 and will be removed in ND 4.3.

## 1. Add switches (discover)

### Endpoint (add switches)

```openapi
POST /api/v1/manage/fabrics/{fabric_name}/switches
```

### Body (add switches)

```json
{
    "switches": [
        {
            "hostname": "cvd-2311-leaf",
            "ip": "172.22.150.106",
            "serialNumber": "FDO211218HB",
            "model": "N9K-C93180YC-EX",
            "softwareVersion": "10.2(5)",
            "switchRole": "leaf"
        }
    ],
    "password": "mypassword",
    "platformType": "nx-os",
    "preserveConfig": true
}
```

### Response (add switches)

HTTP 202 Accepted

```json
{}
```

## 2. Rediscover switches

### Endpoint (rediscover)

```openapi
POST /api/v1/manage/fabrics/{fabric_name}/switchActions/rediscover
```

### Body (rediscover)

```json
{
    "switchIds": ["FDO211218HB"]
}
```

### Response (rediscover)

HTTP 202 Accepted

```json
{}
```

## 3. Get switch credentials

### Endpoint (get switch credentials)

```openapi
GET /api/v1/manage/credentials/switches
```

### Response (get switch credentials)

```json
{
    "items": [
        {
            "credentialStore": "local",
            "fabricName": "F1",
            "ip": "172.22.150.107",
            "switchId": "FDO211218HB",
            "switchName": "cvd-2312-leaf",
            "switchUsername": "admin",
            "type": "custom"
        }
    ]
}
```

## 4. Change switch roles

### Endpoint (change roles)

```openapi
POST /api/v1/manage/fabrics/{fabric_name}/switchActions/changeRoles
```

### Body (change roles)

```json
{
    "switchRoles": [
        {
            "switchId": "FDO211218HB",
            "role": "spine"
        }
    ]
}
```

### Response (change roles)

HTTP 207 Multi-Status

```json
{
    "items": [
        {
            "status": "success",
            "message": "Role changed successfully",
            "switchId": "FDO211218HB"
        }
    ]
}
```

[dcnm_inventory]: <https://github.com/CiscoDevNet/ansible-dcnm/blob/main/plugins/modules/dcnm_inventory.py>
