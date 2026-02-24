#!/usr/bin/env bash
curl -s -X GET http://localhost:8000/api/v1/manage/fabrics/fabric1/vrfs?filter= | python -m json.tool

