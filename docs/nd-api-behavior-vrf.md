# Nexus Dashboard API Behavior — VRF Operations

Real behavior observed by probing a live Nexus Dashboard 4.2 instance. Use this document when implementing VRF endpoints to ensure mock fidelity.

> **Source**: ND 4.2 at 192.168.7.7 (cluster name: `ND42-119d-n1`), probed February 2026.

---

## Standard Error Response Format

All error responses follow this structure:

```json
{"code": 400, "description": "", "errors": null, "message": "Human-readable error text"}
```

| Field | Value | Notes |
| --- | --- | --- |
| `code` | Integer | Matches the HTTP status code |
| `description` | `""` | Always empty string |
| `errors` | `null` | Always null |
| `message` | String | Human-readable error description |

**Simplified variant**: Some 404s omit the `errors` field:

```json
{"message": "Fabric not found", "description": "", "code": 404}
```

When implementing endpoints, always use the standard four-field format.

---

## HTTP Status Code Conventions

| Code | When Used | Body |
| --- | --- | --- |
| **200** | Successful GET, PUT, POST (synchronous) | Resource or list |
| **202** | Accepted (async deploy) | Status message |
| **204** | Successful DELETE (unattached VRF) | Empty |
| **207** | Multi-status (create, attach/detach) | Per-item `results` array |
| **400** | Business rule / validation violations | Standard error |
| **404** | Resource not found (simplified format) | Standard error |
| **500** | Internal / unexpected errors | Standard error |

**Key insight**: VRF operations use **207** for multi-status responses, and **400** for nonexistent VRF (not 404 like Fabric).

---

## VRF Behaviors

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

> **Note**: ND returns **400** for nonexistent VRF, not 404. This differs from Fabric behavior.

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
notApplicable  →  (attach)           →  pending (attach=true)
pending        →  (deploy)           →  in progress → attached
attached       →  (detach)           →  pending (attach=false)
pending        →  (deploy)           →  in progress → notApplicable
```

> **Note**: Real ND transitions through an `in progress` intermediate state during deploy. The mock skips this and transitions directly to the final state (`attached` or `notApplicable`).

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

### VRF deploy — request body

```
POST /api/v1/manage/fabrics/fabric1/vrfActions/deploy
```

```json
{"switchIds": ["945V7U23QJ7"], "vrfNames": ["MyVRF_50000"]}
```

- `vrfNames` is **mandatory** (non-empty); empty array returns 400.
- `switchIds` is optional; empty array means all switches in fabric.

### VRF deploy — success with pending attachments → 202

```json
{"status": "Deployment of VRF(s) has been initiated successfully"}
```

### VRF deploy — no pending attachments → 202

```json
{"status": "No switches pending for deployment."}
```

### VRF deploy — nonexistent fabric → 400 (not 404!)

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid Fabric name: NONEXISTENT"}
```

> **Note**: Deploy returns **400** for nonexistent fabric, not 404.

### VRF deploy — empty vrfNames → 400

```json
{"code": 400, "description": "", "errors": null, "message": "'vrfNames' is a mandatory parameter for this endpoint."}
```

### VRF deploy — invalid VRF name → 400

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid VRF name(s): NONEXISTENT_VRF"}
```

### VRF deploy — invalid switchId → 400

```json
{"code": 400, "description": "", "errors": null, "message": "Invalid switch serial number(s) : [FAKE_SWITCH]"}
```

### VRF deploy — validation order

Errors are checked in this order (first failure wins):

1. Fabric existence
2. `vrfNames` non-empty check
3. `switchIds` validity
4. `vrfNames` validity (VRFs exist in fabric)

---

## Implementing VRF Endpoints — Checklist

- [ ] Error responses use the standard four-field format: `{code, description, errors, message}`
- [ ] Business rule violations return **400**, not 500
- [ ] Nonexistent VRF returns **400** (not 404)
- [ ] Unattached VRF deletion returns **204** with empty body
- [ ] Create and attach/detach operations return **207** with per-item `results` array
- [ ] Deploy returns **202** with status message (async operation)
- [ ] Deploy requires non-empty `vrfNames` (400 if empty)
- [ ] Deploy validates switchIds and vrfNames exist (400 if invalid)
- [ ] VRF attachment query includes all required fields (attach, errorMessage, instanceValues, showVlan, status, switchId, switchName, switchRole, vrfName)
- [ ] Attachment state machine respected (notApplicable → pending → attached / notApplicable)
- [ ] Error messages match real ND exactly (check spacing, brackets, punctuation)
