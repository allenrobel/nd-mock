# ndfc_mock - No Container

How to run ndfc_mock outside of a container.

## Ansible Considerations

By default, fastapi starts the uvicorn server to listen on http port 8000.
Hence, if you're using Ansible, ansible.cfg or inventory group_vars would
need to be modified to use this port, per below.

```yaml
ansible_httpapi_use_ssl: no
ansible_httpapi_port: 8000
```

## Installation

To run outside of a container, you must start fastapi in the directory immediately
above `app`.  This is because the endpoint handler that retrieves templates needs
to use the container path to the template files (`./app/templates/*`).  To match
this when running out-of-container, fastapi needs to be run one directory
level above `app` (per the example below).

```bash
git clone https://github.com/allenrobel/ndfc_mock.git
cd ndfc_mock
uv sync
fastapi run app/main.py
# Comment out 'fastapi run main.py' above
# and uncomment 'fastapi dev main.py' below
# to run fastapi in debug mode.
#fastapi dev app/main.py
```

You'll see the uvicorn server startup.  The last two lines will look like:

```bash
      INFO   Application startup complete.
      INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Point your browser at [http://localhost:8000/docs](http://localhost:8000/docs)
for the API documentation.  You can use e.g. Postman for sending requests to
the uvicorn site.

- Note: Running outside of a container will result in database.db being created in the ./app directory.
- Note: When starting with `fastapi dev main.py` the last two lines will not
  contain the ouput shown above, since debugging output will appear after these
  lines. In this case, scroll back up about 25 or so lines to view:

```bash
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
