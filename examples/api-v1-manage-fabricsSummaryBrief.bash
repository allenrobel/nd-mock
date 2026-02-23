#!/usr/bin/env bash

curl --request GET --url http://localhost:8000/api/v1/manage/fabricsSummaryBrief | (python -m json.tool 2>/dev/null || true)
