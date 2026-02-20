#!/usr/bin/env python
# pylint: disable=unused-import
from .app import app
from .v1.endpoints import login
from .v1.endpoints.manage.credentials import switches_get as credentials_switches_get
from .v1.endpoints.manage.credentials import switches_post as credentials_switches_post
from .v1.endpoints.manage.fabrics import fabric_delete
from .v1.endpoints.manage.fabrics import fabric_get
from .v1.endpoints.manage.fabrics import fabric_post
from .v1.endpoints.manage.fabrics import fabric_put
from .v1.endpoints.manage.fabrics import fabrics_get
from .v1.endpoints.manage.fabrics.actions import config_deploy_post
from .v1.endpoints.manage.fabrics.actions import config_save_post
from .v1.endpoints.manage.fabrics.switch_actions import change_roles_post
from .v1.endpoints.manage.fabrics.switch_actions import rediscover_post
from .v1.endpoints.manage.fabrics.switches import summary_get as switches_summary_get
from .v1.endpoints.manage.fabrics.switches import switch_delete
from .v1.endpoints.manage.fabrics.switches import switch_get
from .v1.endpoints.manage.fabrics.switches import switches_get
from .v1.endpoints.manage.fabrics.switches import switches_post
from .v1.endpoints.aaa.local_users import local_user_delete
from .v1.endpoints.aaa.local_users import local_user_get
from .v1.endpoints.aaa.local_users import local_user_post
from .v1.endpoints.aaa.local_users import local_user_put
from .v1.endpoints.aaa.local_users import local_users_get

app.include_router(login.router, tags=["Nexus Dashboard"])
app.include_router(fabric_delete.router, tags=["Manage Fabrics"])
app.include_router(fabric_get.router, tags=["Manage Fabrics"])
app.include_router(fabric_post.router, tags=["Manage Fabrics"])
app.include_router(fabric_put.router, tags=["Manage Fabrics"])
app.include_router(fabrics_get.router, tags=["Manage Fabrics"])
app.include_router(config_deploy_post.router, tags=["Manage Fabric Actions"])
app.include_router(config_save_post.router, tags=["Manage Fabric Actions"])
app.include_router(credentials_switches_get.router, tags=["Manage Credentials"])
app.include_router(credentials_switches_post.router, tags=["Manage Credentials"])
app.include_router(switches_summary_get.router, tags=["Manage Switches"])
app.include_router(switch_get.router, tags=["Manage Switches"])
app.include_router(switches_get.router, tags=["Manage Switches"])
app.include_router(switches_post.router, tags=["Manage Switches"])
app.include_router(switch_delete.router, tags=["Manage Switches"])
app.include_router(change_roles_post.router, tags=["Manage Switch Actions"])
app.include_router(rediscover_post.router, tags=["Manage Switch Actions"])
app.include_router(local_user_delete.router, tags=["AAA Local Users"])
app.include_router(local_user_get.router, tags=["AAA Local Users"])
app.include_router(local_user_post.router, tags=["AAA Local Users"])
app.include_router(local_user_put.router, tags=["AAA Local Users"])
app.include_router(local_users_get.router, tags=["AAA Local Users"])
