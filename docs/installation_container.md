# nd-mock - Containerized

nd-mock includes a Dockerfile to build a containerized instance.  This is
tested with Podman, but Docker should also work (though I'm not using Docker
so no guarantees).

You can also run nd-mock outside of a container if you install the dependencies
described in [Installation - No Container](./installation_no_container.md).

## Ansible Considerations

The container is configured to expose http port 8080. Hence, if you're using
Ansible, ansible.cfg or inventory group_vars would need to be modified to use
this port, per below.

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8080
```

## Installation

To run nd-mock within a container, first install Podman or Docker.
The examples below are using Podman.  Then clone the nd-mock
repository and build the container.

```bash
git clone https://github.com/allenrobel/nd-mock.git
cd nd-mock
podman build -t nd-mock .
podman run --detach -p 8080:8080 nd-mock
```

## Uninstall - Container

To delete the container and image after running it, do the following.

```bash
podman ps
```

From the above output, use the randomly-assigned name in the NAMES column
for the next couple commands to stop and remove the container.

```bash
podman stop randomly_assigned_container_name
podman rm randomly_assigned_container_name
```

Then delete the image.

```bash
podman rmi nd-mock
```

### Example

```bash
(py312) AROBEL-M-G793% podman ps
CONTAINER ID  IMAGE                       COMMAND               CREATED         STATUS         PORTS                   NAMES
6ef724456379  localhost/nd-mock:latest  fastapi run app/m...  19 minutes ago  Up 19 minutes  0.0.0.0:8080->8080/tcp  inspiring_villani
(py312) AROBEL-M-G793% podman stop inspiring_villani
inspiring_villani
(py312) AROBEL-M-G793% podman rm inspiring_villani
inspiring_villani
(py312) AROBEL-M-G793% podman rmi nd-mock
Untagged: localhost/nd-mock:latest
Deleted: c4d64f101f97baa2a9ebe5984ffae3eab15f8477ee72817cea5ff499c1caa554
Deleted: bbad8f9629050572ebdf128bb851d433ddc50d8585444fe380bba7c9170c72a5
(py312) AROBEL-M-G793%
```

### Usage

After the container starts, point your browser at
[http://localhost:8080/docs](http://localhost:8080/docs)
for the API documentation.  You can use e.g. Postman for
sending requests to the mock NDFC instance.
