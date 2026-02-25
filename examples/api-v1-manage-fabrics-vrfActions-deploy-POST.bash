#!/usr/bin/env bash

curl --request POST \
  --url http://localhost:8000/api/v1/manage/fabrics/fabric1/vrfActions/deploy \
  --header 'content-type: application/json' \
  --data '{
  "switchIds": [
    "FOX14658SD"
  ],
  "vrfNames": [
    "MyVRF_50000"
  ]
}' | (python -m json.tool 2>/dev/null || true)
