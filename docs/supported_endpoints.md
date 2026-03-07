# Supported Endpoints


## Nexus Dashboard

- `/api/v1/infra/login`
  - `post`
    - Login Post

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

- `/api/v1/manage/fabricsSummaryBrief`
  - `get`
    - Fabrics Summary Brief Get

## Manage Fabric Actions

- `/api/v1/manage/fabrics/{fabric_name}/actions/configDeploy`
  - `post`
    - Config Deploy Post

- `/api/v1/manage/fabrics/{fabric_name}/actions/configSave`
  - `post`
    - Config Save Post

## Manage Credentials

- `/api/v1/manage/credentials/switches`
  - `get`
    - Credentials Switches Get

- `/api/v1/manage/credentials/switches`
  - `post`
    - Credentials Switches Post

## Manage Switches

- `/api/v1/manage/fabrics/{fabric_name}/switches/summary`
  - `get`
    - Switches Summary Get

- `/api/v1/manage/fabrics/{fabric_name}/switches/{switch_id}`
  - `get`
    - Switch Get

- `/api/v1/manage/fabrics/{fabric_name}/switches/{switch_id}`
  - `delete`
    - Switch Delete

- `/api/v1/manage/fabrics/{fabric_name}/switches`
  - `get`
    - Switches Get

- `/api/v1/manage/fabrics/{fabric_name}/switches`
  - `post`
    - Switches Post

## Manage Switch Actions

- `/api/v1/manage/fabrics/{fabric_name}/switchActions/changeRoles`
  - `post`
    - Switch Change Roles Post

- `/api/v1/manage/fabrics/{fabric_name}/switchActions/rediscover`
  - `post`
    - Switch Rediscover Post

## Manage VRFs

- `/api/v1/manage/fabrics/{fabric_name}/vrfs/{vrf_name}`
  - `delete`
    - Vrf Delete

- `/api/v1/manage/fabrics/{fabric_name}/vrfs`
  - `get`
    - Vrfs Get

- `/api/v1/manage/fabrics/{fabric_name}/vrfs`
  - `post`
    - Vrfs Post

## Manage VRF Actions

- `/api/v1/manage/fabrics/{fabric_name}/vrfActions/deploy`
  - `post`
    - Vrf Deploy Post

## Manage VRF Attachments

- `/api/v1/manage/fabrics/{fabric_name}/vrfAttachments/query`
  - `post`
    - Vrf Attachments Query

## AAA Local Users

- `/api/v1/infra/aaa/localUsers/{pathLoginId}`
  - `delete`
    - Local User Delete

- `/api/v1/infra/aaa/localUsers/{pathLoginId}`
  - `get`
    - Local User Get

- `/api/v1/infra/aaa/localUsers/{pathLoginId}`
  - `put`
    - Local User Put

- `/api/v1/infra/aaa/localUsers`
  - `get`
    - Local Users Get

- `/api/v1/infra/aaa/localUsers`
  - `post`
    - Local User Post
