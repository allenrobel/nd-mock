#!/usr/bin/env bash
curl -s -X POST http://localhost:8000/api/v1/infra/aaa/localUsers \
    -H "Content-Type: application/json" \
    -d '{
      "loginID": "testuser",
      "password": "mySuperSecretCredentials",
      "firstName": "Test",
      "lastName": "User",
      "email": "testuser@example.com",
      "rbac": {
        "tenantDomain": "all",
        "domains": {
          "all": {
            "roles": ["admin"]
          }
        }
      }
    }' | python -m json.tool

