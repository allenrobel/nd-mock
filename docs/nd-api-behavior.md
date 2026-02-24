# Nexus Dashboard API Behavior Reference

Real behavior observed by probing a live Nexus Dashboard 4.2 instance. Use this document when implementing new mock endpoints to ensure fidelity with real ND.

> **Source**: ND 4.2 at 192.168.7.7 (cluster name: `ND42-119d-n1`), probed February 2026.
> **Instance inventory at time of probing**: 1 fabric (`fabric1`, vxlanIbgp), 6 switches, 2 VRFs, 0 networks.

---

## Standard Error Response Format

All error responses follow this structure:

```json
{"code": 400, "description": "", "errors": null, "message": "Human-readable error text"}
```

| Field | Value | Notes |
|-------|-------|-------|
| `code` | Integer | Matches the HTTP status code |
| `description` | `""` | Always empty string |
| `errors` | `null` | Always null |
| `message` | String | Human-readable error description |

**Simplified variant**: Some 404s (e.g. `GET /vrfs` from nonexistent fabric) omit the `errors` field:

```json
{"message": "Fabric not found", "description": "", "code": 404}
```

When implementing new endpoints in the mock, always use the standard four-field format.

---

## HTTP Status Code Conventions

| Code | When Used | Body |
|------|-----------|------|
| **200** | Successful GET, PUT, POST (synchronous) | Resource or list |
| **202** | Async operations (add switches, rediscover) | `{}` |
| **204** | Successful DELETE | Empty |
| **207** | Multi-status (VRF create, attach/detach, change roles) | Per-item `results` array |
| **400** | Business rule / validation violations | Standard error |
| **404** | Resource not found | Standard error |
| **500** | Internal / unexpected errors | Standard error |

**Key insight**: ND uses **400** (not 500) for business rule violations like deleting a fabric that has children or creating a duplicate resource.

---

## Fabric Behaviors

### DELETE fabric with child switches → 400

```
DELETE /api/v1/manage/fabrics/fabric1
```

```json
{"code": 400, "description": "", "errors": null, "message": "Unable to delete Fabric fabric1.  Please remove all switches in this fabric before deleting."}
```

> **Note**: There are **two spaces** after the first period in the message. This is how real ND returns it.

### POST duplicate fabric → 400

```
POST /api/v1/manage/fabrics
```

```json
{"code": 400, "description": "", "errors": null, "message": "[Fabric named fabric1 is already present in the cluster: ND42-119d-n1]"}
```

> **Note**: The message is wrapped in **square brackets** and includes the cluster name.

### GET / DELETE / PUT nonexistent fabric → 404

```json
{"code": 404, "description": "", "errors": null, "message": "Fabric NONEXISTENT not found"}
```

### displayFabricType — returns raw type string

The `fabricsSummaryBrief` endpoint returns `displayFabricType` as the **raw management type** (e.g. `"vxlanIbgp"`), **not** a human-readable display name. The OpenAPI schema example showing `"Data Center VXLAN EVPN - iBGP"` does not match observed behavior.

---

## Switch Behaviors

### Summary response shape — counters wrapper

```
GET /api/v1/manage/fabrics/{fabric_name}/switches/summary
```

Each category wraps its counter array in a `{"counters": [...]}` object:

```json
{
  "role": {"counters": [{"count": 2, "name": "borderGateway"}, {"count": 2, "name": "leaf"}, {"count": 2, "name": "spine"}]},
  "softwareVersion": {"counters": [{"count": 6, "name": "10.6(2)"}]},
  "configSyncStatus": {"counters": [{"count": 5, "name": "notApplicable"}, {"count": 1, "name": "inSync"}]},
  "anomalyLevel": {"counters": []}
}
```

Categories: `anomalyLevel`, `configSyncStatus`, `role`, `softwareVersion`.

### Async operations

- **Add switches** (`POST .../switches`): Returns **202** with `{}`
- **Rediscover** (`POST .../switchActions/rediscover`): Returns **202** with `{}`
- **Change roles** (`POST .../switchActions/changeRoles`): Returns **207** with per-item results

---

## VRF Behaviors (Probed, Not Yet Implemented in Mock)

### DELETE unattached VRF → 204

```
DELETE /api/v1/manage/fabrics/fabric1/vrfs/MyVRF_50000
```

Returns **204** with empty body.

### DELETE attached VRF → 400

```json
{"code": 400, "description": "", "errors": null, "message": "Delete is not allowed as the VRF is currently not in 'NA' state"}
```

### DELETE nonexistent VRF → 400 (not 404!)

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid VRF"}
```

> **Note**: ND returns **400** for nonexistent VRF, not 404. This differs from fabric behavior.

### POST duplicate VRF → 207 with per-item failure

```json
{"results": [{"message": "VRF MyVRF_50000 already exists", "status": "failed", "vrfId": 50000, "vrfName": "MyVRF_50000"}]}
```

### POST VRF in nonexistent fabric → 500

```json
{"code": 500, "description": "", "errors": null, "message": "Invalid Fabric name: NONEXISTENT"}
```

### GET VRFs from nonexistent fabric → 404 (simplified format)

```json
{"message": "Fabric not found", "description": "", "code": 404}
```

> **Note**: This response omits the `errors` field.

### VRF attachment state machine

```
notApplicable  →  (attach + deploy)  →  attached
attached       →  (detach)           →  pending
pending        →  (deploy)           →  notApplicable
```

### VRF attach/detach → 207

```
POST /api/v1/manage/fabrics/fabric1/vrfAttachments
```

```json
{"results": [{"status": "success", "switchId": "945V7U23QJ7", "switchName": "LE1", "vrfName": "MyVRF_50000"}]}
```

### VRF attach — invalid switch → 400

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid switchId. NONEXISTENT could not be found in any fabric."}
```

### VRF attach — invalid VRF → 400

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid VRF: NONEXISTENT_VRF"}
```

### VRF attachment query response shape

```
POST /api/v1/manage/fabrics/fabric1/vrfAttachments/query
```

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
  "meta": {"counts": {"remaining": 0, "total": 4}}
}
```

---

## Implementing New Endpoints — Checklist

When adding a new mock endpoint, verify:

- [ ] Error responses use the standard four-field format: `{code, description, errors, message}`
- [ ] Business rule violations return **400**, not 500
- [ ] Resource-not-found returns **404** (except VRFs which use 400)
- [ ] Async operations return **202** with `{}`
- [ ] Multi-status operations return **207** with per-item `results` array
- [ ] Successful DELETE returns **204** with empty body
- [ ] Response shapes match real ND (check for wrapper objects like `counters`)
- [ ] Error messages match real ND exactly (check spacing, brackets, punctuation)
