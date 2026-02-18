#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints import login
from .v1.endpoints.cisco.ndfc.api.about import version_get_internal
from .v1.endpoints.configtemplate.rest.config.templates import config_template_by_name
from .v1.endpoints.fm.about import version_get
from .v1.endpoints.fm.features import features_get
from .v1.endpoints.lan_fabric.rest.control.fabrics import config_deploy_post, config_save_post, fabric_delete, fabric_get, fabric_post, fabric_put, fabrics_get
from .v1.endpoints.lan_fabric.rest.control.fabrics.inventory import discover_post, internal_inventory_get, rediscover_post, switches_by_fabric_get, test_reachability_post
from .v1.endpoints.lan_fabric.rest.control.switches import fabric_name_get, overview_get, switch_remove
from .v1.endpoints.lan_fabric.rest.control.switches.roles import roles_get, roles_post
from .v1.endpoints.lan_fabric.rest.lanConfig import getLanSwitchCredentialsWithType, internal_getLanSwitchCredentials
from .v1.endpoints.lan_fabric.rest.topology import role_put as internal_role_put
from .v2.endpoints.manage.credentials import switches_get as v2_credentials_switches_get
from .v2.endpoints.manage.credentials import switches_post as v2_credentials_switches_post
from .v2.endpoints.manage.fabrics import fabric_delete as v2_fabric_delete
from .v2.endpoints.manage.fabrics import fabric_get as v2_fabric_get
from .v2.endpoints.manage.fabrics import fabric_post as v2_fabric_post
from .v2.endpoints.manage.fabrics import fabric_put as v2_fabric_put
from .v2.endpoints.manage.fabrics import fabrics_get as v2_fabrics_get
from .v2.endpoints.manage.fabrics.actions import config_deploy_post as v2_config_deploy_post
from .v2.endpoints.manage.fabrics.actions import config_save_post as v2_config_save_post
from .v2.endpoints.manage.fabrics.switch_actions import change_roles_post as v2_change_roles_post
from .v2.endpoints.manage.fabrics.switch_actions import rediscover_post as v2_rediscover_post
from .v2.endpoints.manage.fabrics.switches import summary_get as v2_switches_summary_get
from .v2.endpoints.manage.fabrics.switches import switch_delete as v2_switch_delete
from .v2.endpoints.manage.fabrics.switches import switch_get as v2_switch_get
from .v2.endpoints.manage.fabrics.switches import switches_get as v2_switches_get
from .v2.endpoints.manage.fabrics.switches import switches_post as v2_switches_post

app.include_router(v2_fabric_delete.router, tags=["Manage Fabrics (v2)"])
app.include_router(v2_fabric_get.router, tags=["Manage Fabrics (v2)"])
app.include_router(v2_fabric_post.router, tags=["Manage Fabrics (v2)"])
app.include_router(v2_fabric_put.router, tags=["Manage Fabrics (v2)"])
app.include_router(v2_fabrics_get.router, tags=["Manage Fabrics (v2)"])
app.include_router(v2_config_deploy_post.router, tags=["Manage Fabric Actions (v2)"])
app.include_router(v2_config_save_post.router, tags=["Manage Fabric Actions (v2)"])
app.include_router(v2_credentials_switches_get.router, tags=["Manage Credentials (v2)"])
app.include_router(v2_credentials_switches_post.router, tags=["Manage Credentials (v2)"])
app.include_router(v2_switches_summary_get.router, tags=["Manage Switches (v2)"])
app.include_router(v2_switch_get.router, tags=["Manage Switches (v2)"])
app.include_router(v2_switches_get.router, tags=["Manage Switches (v2)"])
app.include_router(v2_switches_post.router, tags=["Manage Switches (v2)"])
app.include_router(v2_switch_delete.router, tags=["Manage Switches (v2)"])
app.include_router(v2_change_roles_post.router, tags=["Manage Switch Actions (v2)"])
app.include_router(v2_rediscover_post.router, tags=["Manage Switch Actions (v2)"])
app.include_router(getLanSwitchCredentialsWithType.router, tags=["Credentials (v1)"])
app.include_router(config_deploy_post.router, tags=["Fabrics (v1)"])
app.include_router(config_save_post.router, tags=["Fabrics (v1)"])
app.include_router(fabric_delete.router, tags=["Fabrics (v1)"])
app.include_router(fabric_get.router, tags=["Fabrics (v1)"])
app.include_router(fabric_post.router, tags=["Fabrics (v1)"])
app.include_router(fabric_put.router, tags=["Fabrics (v1)"])
app.include_router(fabrics_get.router, tags=["Fabrics (v1)"])
app.include_router(features_get.router, tags=["Feature Manager (v1)"])
app.include_router(version_get.router, tags=["Feature Manager (v1)"])
app.include_router(version_get_internal.router, tags=["Internal (v1)"])
app.include_router(internal_inventory_get.router, tags=["Internal (v1)"])
app.include_router(internal_role_put.router, tags=["Internal (v1)"])
app.include_router(internal_getLanSwitchCredentials.router, tags=["Internal (v1)"])
app.include_router(discover_post.router, tags=["Inventory (v1)"])
app.include_router(switches_by_fabric_get.router, tags=["Inventory (v1)"])
app.include_router(roles_get.router, tags=["Inventory (v1)"])
app.include_router(roles_post.router, tags=["Inventory (v1)"])
app.include_router(test_reachability_post.router, tags=["Inventory (v1)"])
app.include_router(rediscover_post.router, tags=["Inventory (v1)"])
app.include_router(login.router, tags=["Nexus Dashboard (v1)"])
app.include_router(fabric_name_get.router, tags=["Switches (v1)"])
app.include_router(overview_get.router, tags=["Switches (v1)"])
app.include_router(switch_remove.router, tags=["Switches (v1)"])
app.include_router(config_template_by_name.router, tags=["Templates (v1)"])
