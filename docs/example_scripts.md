# Example curl Scripts

## Usage examples

Below, we run through a complete CRUD workflow for `/api/v1/infra/aaa/localUsers`

### Create User - POST /api/v1/infa/aaa/localUsers/testuser

``` bash
(nd-mock) arobel@Allen-M4 nd-mock % bash examples/api-v1-infra-aaa-localUsers-POST.bash
{
    "accountStatus": "Active",
    "email": "testuser@example.com",
    "firstName": "Test",
    "lastName": "User",
    "loginID": "testuser",
    "passwordPolicy": {
        "passwordChangeTime": "2026-02-20T20:51:58Z",
        "reuseLimitation": 0,
        "timeIntervalLimitation": 0
    },
    "rbac": {
        "domains": {
            "all": {
                "roles": [
                    "admin"
                ]
            }
        },
        "tenantDomain": "all"
    },
    "remoteIDClaim": "",
    "userID": "5fddda1f-23a0-4bc3-aced-b6edab2a8c2f",
    "xLaunch": false
}
```

### Update User - PUT /api/v1/infa/aaa/localUsers/testuser

``` bash
(nd-mock) arobel@Allen-M4 nd-mock % bash examples/api-v1-infra-aaa-localUsers-PUT.bash
{
    "accountStatus": "Active",
    "email": "testuser@different.net",
    "firstName": "Test",
    "lastName": "User",
    "loginID": "testuser",
    "passwordPolicy": {
        "passwordChangeTime": "2026-02-20T20:57:33Z",
        "reuseLimitation": 0,
        "timeIntervalLimitation": 0
    },
    "rbac": {
        "domains": {
            "all": {
                "roles": [
                    "admin"
                ]
            }
        },
        "tenantDomain": "all"
    },
    "remoteIDClaim": "",
    "userID": "e5b200c0-bb84-4764-bc0d-4258e0402e53",
    "xLaunch": false
}
(nd-mock) arobel@Allen-M4 nd-mock %
```

### List User - GET /api/v1/infa/aaa/localUsers/testuser

``` bash
(nd-mock) arobel@Allen-M4 nd-mock % bash examples/api-v1-infra-aaa-localUsers-GET.bash
{
    "accountStatus": "Active",
    "email": "testuser@different.net",
    "firstName": "Test",
    "lastName": "User",
    "loginID": "testuser",
    "passwordPolicy": {
        "passwordChangeTime": "2026-02-20T20:57:33Z",
        "reuseLimitation": 0,
        "timeIntervalLimitation": 0
    },
    "rbac": {
        "domains": {
            "all": {
                "roles": [
                    "admin"
                ]
            }
        },
        "tenantDomain": "all"
    },
    "remoteIDClaim": "",
    "userID": "e5b200c0-bb84-4764-bc0d-4258e0402e53",
    "xLaunch": false
}
(nd-mock) arobel@Allen-M4 nd-mock %
```

### Delete User - GET /api/v1/infa/aaa/localUsers/testuser

``` bash
(nd-mock) arobel@Allen-M4 nd-mock % bash examples/api-v1-infra-aaa-localUsers-DELETE.bash
# NOTE: No output for a DELETE request since it returns 204 No Content
# Let's run the script again to verify the user is deleted.
(nd-mock) arobel@Allen-M4 nd-mock % bash examples/api-v1-infra-aaa-localUsers-DELETE.bash
{
    "detail": {
        "code": 404,
        "description": "",
        "message": "User testuser not found"
    }
}
(nd-mock) arobel@Allen-M4 nd-mock %
```
