from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import purpleserver.tenants.models as models


class TenantsAdmin(AdminSite):
    site_header = "Purplship"
    site_title = "Purplship"
    index_title = "System Configuration"


site = TenantsAdmin(name='system')
site.register(get_user_model())
site.register(Group)
site.register(models.Client)
