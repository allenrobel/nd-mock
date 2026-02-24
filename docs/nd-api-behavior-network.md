# Nexus Dashboard API Behavior — Network Operations

Real behavior observed by probing a live Nexus Dashboard 4.2 instance. Use this document when implementing Network endpoints to ensure mock fidelity.

> **Source**: ND 4.2 at 192.168.7.7 (cluster name: `ND42-119d-n1`). Network behavior has not yet been probed.

---

## Status

Network operations behavior will be documented here as we probe the real ND 4.2 instance. This includes:

- Network creation, update, deletion
- Network attachment/detachment to switches
- Error conditions and edge cases
- Response shapes and status codes
