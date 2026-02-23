#!/usr/bin/env bash

curl --request DELETE --url http://localhost:8000/api/v1/manage/fabrics/fabric1 | (python -m json.tool 2>/dev/null || true)
