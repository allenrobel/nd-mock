# Summary

This is a work in progress with limited functionality as described
below.

When finished, this will allow for minor development and testing of
[ansible-nd](https://github.com/CiscoDevNet/ansible-nd)
modules (and other REST API-based applications) without requiring a
real Nexus Dashboard (ND) instance.

Basically, it will accept GET/POST/PUT/DELETE requests to
endpoints supported by ND and will return responses that
align, as closely as possible, with real ND responses i.e.,
POST and PUT requests update an in-memory SQLlite database;
GET requests retrieve from this database; and DELETE requests
remove items from the database.

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
2. [SQLModel](https://sqlmodel.tiangolo.com)
3. [Pydantic](https://docs.pydantic.dev/latest/)
4. [Podman](https://podman.io)
