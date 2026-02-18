# Example Ansible Playbooks

## Configuration Notes

In order for Ansible to send to http port 8080 (rather than https port 443),
the following needs to be added either to your ansible.cfg, or to your
inventory group_vars.  Change `ansible_httpapi_port` to 8000 if you're
running ndfc_mock outside of a container.

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8080
```

## ND 3.x

### Create, query, and delete a VXLAN Fabric

```yaml
---
-   hosts: ndfc
    check_mode: false
    gather_facts: false
    tasks:
    - name: Create VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: merged
        config:
        -   FABRIC_NAME: f1
            FABRIC_TYPE: VXLAN_EVPN
            BGP_AS: "65001"
      register: result
    - debug:
        var: result
    tasks:
    - name: Query VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: query
        config:
        -   FABRIC_NAME: f1
      register: result
    - debug:
        var: result
    - name: Delete VXLAN Fabric
      cisco.dcnm.dcnm_fabric:
        state: deleted
        config:
        -   FABRIC_NAME: f1
      register: result
    - debug:
        var: result
```

### Notes

1. For the deleted-state `dcnm_fabric` playbook task to return success, the fabric
cannot contain any switches.  The `dcnm_fabric` Ansible module uses the
following GET request to determine the number of switches in the fabric.

   `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/<fabric_name>/overview`
  
2. For now, a stub handler is implemented which returns zero switches to
allow the deleted-state playbook task to work.  This will be replaced
soon with appropriate inventory handlers and database tables to support
fabric switch addition/deletion.
