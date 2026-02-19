# Supported Endpoints

## Manage Fabrics

- `/api/v1/manage/fabrics/{fabric_name}`
  - `delete`
    - Delete Fabric

- `/api/v1/manage/fabrics/{fabric_name}`
  - `get`
    - Fabric Get

- `/api/v1/manage/fabrics/{fabric_name}`
  - `put`
    - Fabric Put

- `/api/v1/manage/fabrics`
  - `post`
    - Fabric Post

- `/api/v1/manage/fabrics`
  - `get`
    - Fabrics Get

## Manage Fabric Actions

- `/api/v1/manage/fabrics/{fabric_name}/actions/configSave`
  - `post`
    - Config Save Post

- `/api/v1/manage/fabrics/{fabric_name}/actions/configDeploy`
  - `post`
    - Config Deploy Post

## Manage Credentials

- `/api/v1/manage/credentials/switches`
  - `get`
    - Credentials Switches Get

- `/api/v1/manage/credentials/switches`
  - `post`
    - Credentials Switches Post

## Manage Switches

- `/api/v1/manage/fabrics/{fabric_name}/switches`
  - `get`
    - Switches Get

- `/api/v1/manage/fabrics/{fabric_name}/switches/{switch_id}`
  - `get`
    - Switch Get

- `/api/v1/manage/fabrics/{fabric_name}/switches`
  - `post`
    - Switches Post

- `/api/v1/manage/fabrics/{fabric_name}/switches/{switch_id}`
  - `delete`
    - Switch Delete

- `/api/v1/manage/fabrics/{fabric_name}/switches/summary`
  - `get`
    - Switches Summary Get

## Manage Switch Actions

- `/api/v1/manage/fabrics/{fabric_name}/switchActions/changeRoles`
  - `post`
    - Change Roles Post

- `/api/v1/manage/fabrics/{fabric_name}/switchActions/rediscover`
  - `post`
    - Rediscover Post

## Nexus Dashboard

- `/login`
  - `post`
    - Login Post
