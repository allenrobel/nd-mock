# Summary

This repository contains a mock REST server that mimicks Nexus Dashboard (ND)
version 4.2.

The idea is to be able to run a lightweight local API-only (no GUI) ND instance
on a laptop to support devOps work on a plane, in a coffee shop, etc.

Specifically, in my case, it'll help me (and hopefully others) write Ansible
modules for ND 4.2.

## Background

About a year ago I wrote an initial mock Nexus Dashboard 3.x REST API server
manually using Python and some popular libraries (FastAPI, SQLModel, and SQLAlchemy).
Now that Cisco is releasing version ND 4.2 with a new API, I decided to start
from scratch and leverage Claude Code exclusively to write the implementation
for Nexus Dashboard version 4.2.  While I've been providing minimal guidance
to Claude (architecture, tech stack, etc), Claude is writing all the code.

Hence, this is a training and proving ground for me to see how adept Claude
agents are at building a mock of Nexus Dashboard.

## Strategy

1. I've provided Claude with the schemas for the new Nexus Dashboard REST API.
From these schema's Claude is writing Pydantic models for payloads, responses,
etc.
2. Claude suggested that I install an MCP server that knows about FastAPI,
Pydantic, and SQLAlchemy so that he is able to reference the latest information
about these libraries. So I let it install this.
3. Claude suggested a number of skills that would be helpful to him in his daily work
and I accepted these as well.
4. I wrote docs/nd-object-hierarchy.md and had Claude review it and use it as a basis for
estimation of object constraints (fabric groups, fabrics, VRFs, networks, switches,
interfaces, etc).  For example, a fabric that contains switches cannot be deleted.
5. More recently (as of 2026-02-23) I gave Claude access to a real Nexus Dashboard
instance (in my case a virtual ND + n9000v switches running on a server in my home)
and allowed him to send DELETE, GET, POST, PUT requests as he sees fit.  This
allowed him to learn real response structures for both success and failure
scenarios and to apply this learning to the mock server. This worked surprisingly
well!

## Goal

When finished, `nd-mock` will allow for minor development and testing of
[ansible-nd](https://github.com/CiscoDevNet/ansible-nd)
modules (and other REST API-based applications) without requiring a
real Nexus Dashboard (ND) instance or even any switches (virtual or
otherwise).

Basically, the mock server will accept GET/POST/PUT/DELETE requests to
endpoints supported by ND and will return responses that align, as closely
as possible, with real ND responses.  Modifications are persisted in a
SQLite database i.e., POST and PUT requests update the database; GET
requests retrieve from the database; and DELETE requests remove items
from the database.

## Getting Started

Please refer to the Installation links at the bottom of this README.

## Initial Performance

For the workflow below, mock ND is about 1,127x faster than real ND.

1. Login
2. Create three fabrics of different types
3. Delete one fabric
4. List all fabrics
5. Modify one fabric
6. List all fabrics
7. Delete all remaining fabrics
8. List all fabrics

Why so fast?  While the `nd-mock` server persists state, it does not have to calculate
switch configurations and push these to actual switches.  It also does not have
to write to a highly redundant database like `etcd`.  There are several other
overheads that are necessary when running a production service like Nexus Dashboard
that a mock server can simply ignore.

### Real ND

```bash
(nd-mock) arobel@Allen-M4 nd-mock % python scripts/perf_test.py --base-url https://192.168.7.8 --username admin --password 'xxxxxxx' --no-verify
Target: https://192.168.7.8

   Login successful (user=admin)
   Created fabric: perf_ebgp (type=vxlanEbgp)
   Created fabric: perf_ibgp (type=vxlanIbgp)
   Created fabric: perf_routed (type=routed)
   Deleted fabric: perf_routed
   Fabrics (2): ['perf_ebgp', 'perf_ibgp']
   Updated fabric: perf_ebgp
     replicationMode: ingress
     management.fabricMtu: 9200
   Fabrics (2): ['perf_ebgp', 'perf_ibgp']
   Deleted fabric: perf_ebgp
   Deleted fabric: perf_ibgp
   Fabrics remaining: 0

============================================================
Step                                           Time
------------------------------------------------------------
1. Login                                    0.2726s
2. POST three fabrics                      26.8399s
3. DELETE one fabric                        1.8298s
4. GET all fabrics                          0.3787s
5. PUT modify fabric                        4.0430s
6. GET all fabrics (after PUT)              0.5091s
7. DELETE all remaining fabrics             3.6846s
8. GET all fabrics (verify deletion)        0.0637s
------------------------------------------------------------
Total                                      37.6214s
============================================================
```

### Mock ND

```bash
(nd-mock) arobel@Allen-M4 nd-mock % python scripts/perf_test.py
Target: http://localhost:8000

   Login successful (user=admin)
   Created fabric: perf_ebgp (type=vxlanEbgp)
   Created fabric: perf_ibgp (type=vxlanIbgp)
   Created fabric: perf_routed (type=routed)
   Deleted fabric: perf_routed
   Fabrics (2): ['perf_ebgp', 'perf_ibgp']
   Updated fabric: perf_ebgp
     replicationMode: ingress
     management.fabricMtu: 9200
   Fabrics (2): ['perf_ebgp', 'perf_ibgp']
   Deleted fabric: perf_ebgp
   Deleted fabric: perf_ibgp
   Fabrics remaining: 0

============================================================
Step                                           Time
------------------------------------------------------------
1. Login                                    0.0081s
2. POST three fabrics                       0.0103s
3. DELETE one fabric                        0.0019s
4. GET all fabrics                          0.0028s
5. PUT modify fabric                        0.0042s
6. GET all fabrics (after PUT)              0.0013s
7. DELETE all remaining fabrics             0.0037s
8. GET all fabrics (verify deletion)        0.0011s
------------------------------------------------------------
Total                                       0.0334s
============================================================
(nd-mock) arobel@Allen-M4 nd-mock %    
```

## [Supported Endpoints](./docs/supported_endpoints.md)

## [Example curl Scripts](./docs/example_scripts.md)

## [Example Ansible Playbooks](./docs/example_playbooks.md)

## [Installation - Container](./docs/installation_container.md)

## [Installation - No Container](./docs/installation_no_container.md)

## Acknowledgements

This work would not be possible without the following.

1. [FastApi](https://fastapi.tiangolo.com)
2. [Cisco Nexus Dashboard](https://www.cisco.com/site/us/en/products/networking/cloud-networking/nexus-platform/index.html)
3. [Podman](https://podman.io)
4. [Pydantic](https://docs.pydantic.dev/latest/)
5. [SQLAlchemy (SQLite)](https://www.sqlalchemy.org)
6. [SQLModel](https://sqlmodel.tiangolo.com)
