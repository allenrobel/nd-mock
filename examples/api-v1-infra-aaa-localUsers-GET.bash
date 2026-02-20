#!/usr/bin/env bash

curl -s -X GET http://localhost:8000/api/v1/infra/aaa/localUsers | python -m json.tool
