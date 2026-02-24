# Nexus Dashboard API Behavior — Fabric Operations

Real behavior observed by probing a live Nexus Dashboard 4.2 instance. Use this document when implementing Fabric endpoints to ensure mock fidelity.

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
| **204** | Successful DELETE | Empty |
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

## Implementing Fabric Endpoints — Checklist

- [ ] Error responses use the standard four-field format: `{code, description, errors, message}`
- [ ] Business rule violations (e.g., deleting fabric with children) return **400**, not 500
- [ ] Resource-not-found returns **404**
- [ ] Successful DELETE returns **204** with empty body
- [ ] Duplicate fabric creation returns **400** with brackets around message and cluster name included
- [ ] Error messages match real ND exactly (check spacing, brackets, punctuation)
