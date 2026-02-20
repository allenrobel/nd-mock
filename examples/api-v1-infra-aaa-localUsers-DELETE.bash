#!/usr/bin/env bash

curl -s -X DELETE http://localhost:8000/api/v1/infra/aaa/localUsers/testuser | (python -m json.tool 2>/dev/null || true)
