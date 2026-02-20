#!/usr/bin/env bash

curl -s -X GET http://localhost:8000/api/v1/infra/aaa/localUsers/testuser | python -m json.tool
