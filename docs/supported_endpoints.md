# Supported Endpoints

- V1 denotes Nexus Dashboard 3.x endpoint
- V2 denotes Nexus Dashboard 4.x endpoint
- We are migrating endpoints out of Default and into their respective tags over the next week or so...

## Manage Fabrics (v2)

- `/api/v1/manage/fabrics/{fabric_name}`
  - `delete`
    - V2 Delete Fabric

- `/api/v1/manage/fabrics/{fabric_name}`
  - `get`
    - V2 Fabric Get

- `/api/v1/manage/fabrics/{fabric_name}`
  - `put`
    - V2 Fabric Put

- `/api/v1/manage/fabrics`
  - `post`
    - V2 Fabric Post

- `/api/v1/manage/fabrics`
  - `get`
    - V2 Fabrics Get

## Credentials (v1)

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig/getLanSwitchCredentialsWithType`
  - `get`
    - V1 Getlanswitchcredentialswithtype

## Fabrics (v1)

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/config-deploy/{switch_id}`
  - `post`
    - V1 Config Deploy Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/config-save`
  - `post`
    - V1 Fabric Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}`
  - `delete`
    - V1 Fabric Delete

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}`
  - `get`
    - V1 Get Fabric By Fabric Name

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}`
  - `post`
    - V1 Fabric Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/{template_name}`
  - `put`
    - V1 Fabric Put

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/`
  - `get`
    - V1 Fabrics Get

## Feature Manager (v1)

- `/appcenter/cisco/ndfc/api/v1/fm/features`
  - `get`
    - V1 Fm Features Get

- `/appcenter/cisco/ndfc/api/v1/fm/about/version`
  - `get`
    - V1 Version Get

## Internal (v1)

- `/appcenter/cisco/ndfc/api/about/version`
  - `get`
    - V1 Version Get

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory`
  - `get`
    - V1 Inventory Switches By Fabric Get

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/topology/role/{switch_db_id}`
  - `put`
    - V1 Internal Role Put

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/lanConfig/getLanSwitchCredentials`
  - `get`
    - V1 Getlanswitchcredentials

## Inventory (v1)

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/discover`
  - `post`
    - V1 Inventory Discover Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/switchesByFabric`
  - `get`
    - V1 Inventory Switches By Fabric Get

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/roles`
  - `get`
    - V1 Roles Get

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/roles`
  - `post`
    - V1 Roles Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/test-reachability`
  - `post`
    - V1 Inventory Test Reachability Post

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/inventory/rediscover/{serial_number}`
  - `post`
    - V1 Inventory Rediscover Post

## Nexus Dashboard (v1)

- `/login`
  - `post`
    - Login Post

## Switches (v1)

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/{switch_serial_number}/fabric-name`
  - `get`
    - V1 Get Fabric Name By Switch Serial Number

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/{fabric_name}/overview`
  - `get`
    - V1 Switches Overview Get

- `/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/switches/{serialNumbers}`
  - `delete`
    - (v1) Remove the switch(es), specified by serialNumbers, a comma-separated list of switch serial numbers, from the fabric specified by fabricName.

## Templates (v1)

- `/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/{template_name}`
  - `get`
    - V1 Get Configtemplate By Name
