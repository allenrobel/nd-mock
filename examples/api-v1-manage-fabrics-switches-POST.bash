#!/usr/bin/env bash

curl -X 'POST' \
  'http://localhost:8000/api/v1/manage/fabrics/fabric1/switches' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "switches": [
    {
      "hostname": "leaf-301",
      "ip": "192.168.12.31",
      "serialNumber": "FOX14658SD",
      "model": "ND-M89",
      "softwareVersion": "10.3(4)",
      "switchRole": "leaf",
      "vdcId": 0,
      "vdcMac": "00:00:00:00:00:01"
    }
  ],
  "password": "MySuperSecretCredentials",
  "platformType": "nx-os",
  "preserveConfig": false
}'