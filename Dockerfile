FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY ./pyproject.toml ./uv.lock /code/

RUN uv sync --frozen --no-dev --no-install-project

COPY ./app /code/app

# Disable requirement for HEALTHCHECK since this is not a critical app.
# checkov:skip=CKV_DOCKER_2: required

# Disable requirement for non-root user, since we are running under rootless 
# podman.  See:
#
# https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
# 
# And:
# https://github.com/containers/podman/blob/main/rootless.md
#
# checkov:skip=CKV_DOCKER_3: required

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8080"]
