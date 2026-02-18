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

## [Supported Endpoints](./docs/supported_endpoints.md)

## [Example Ansible Playbooks](./docs/example_playbooks.md)

## [Installation - Container](./docs/installation_container.md)

## [Installation - No Container](./docs/installation_no_container.md)

## Acknowledgements

This work would not be possible without the following.

1. [FastApi](https://fastapi.tiangolo.com)
2. [SQLModel](https://sqlmodel.tiangolo.com)
3. [Pydantic](https://docs.pydantic.dev/latest/)
4. [Podman](https://podman.io)
