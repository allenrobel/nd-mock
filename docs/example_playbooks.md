# Example Ansible Playbooks

## General Notes

We will add example playbooks once the ND Ansible collection has introduced playbooks for Nexus Dashboard v4.2.  For now, please use e.g. Postman or Bruno, etc.

A similar implementation is available for Nexus Dashboard 3.x (but will no longer be maintained).
You can find it at the following link:

[ndfc_mock](https://github.com/allenrobel/ndfc_mock)

## Configuration Notes

In order for Ansible to send to http port 8080 (rather than https port 443),
the following needs to be added either to your ansible.cfg, or to your
inventory group_vars.  Change `ansible_httpapi_port` to 8000 if you're
running ndfc_mock outside of a container.

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8080
```

## ND 4.2

### Create, query, and delete a VXLAN Fabric

TBD

### Notes

For older ND 3.x, please use [ndfc_mock](https://github.com/allenrobel/ndfc_mock) instead.
