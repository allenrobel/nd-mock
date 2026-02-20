#!/usr/bin/env bash
curl -s -X PUT http://localhost:8000/api/v1/infra/aaa/localUsers/testuser \
    -H "Content-Type: application/json" \
    -d '{
      "loginID": "testuser",
      "password": "mySuperDuperSecretCredentials",
      "firstName": "Test",
      "lastName": "User",
      "email": "testuser@different.net",
      "rbac": {
        "tenantDomain": "all",
        "domains": {
          "all": {
            "roles": ["admin"]
          }
        }
      }
    }' | python -m json.tool

