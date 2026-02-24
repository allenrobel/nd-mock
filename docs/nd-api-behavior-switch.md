# Nexus Dashboard API Behavior — Switch Operations

Real behavior observed by probing a live Nexus Dashboard 4.2 instance. Use this document when implementing Switch endpoints to ensure mock fidelity.

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

When implementing endpoints, always use the standard four-field format.

---

## HTTP Status Code Conventions

| Code | When Used | Body |
| --- | --- | --- |
| **200** | Successful GET, PUT, POST (synchronous) | Resource or list |
| **202** | Async operations (add switches, rediscover) | `{}` |
| **207** | Multi-status (change roles) | Per-item `results` array |
| **400** | Business rule / validation violations | Standard error |
| **404** | Resource not found | Standard error |

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

## Implementing Switch Endpoints — Checklist

- [ ] Error responses use the standard four-field format: `{code, description, errors, message}`
- [ ] Business rule violations return **400**, not 500
- [ ] Async add/rediscover operations return **202** with `{}`
- [ ] Multi-status operations (change roles) return **207** with per-item `results` array
- [ ] Summary response wraps counters in `{"counters": [...]}` objects for each category
- [ ] Response shapes match real ND exactly (check for wrapper objects)
