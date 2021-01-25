from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django_tenants.admin import TenantAdminMixin

from purpleserver.user.admin import UserAdmin
import purpleserver.tenants.models as models


class TenantsAdmin(AdminSite):
    site_header = "Purplship"
    site_title = "Purplship"
    index_title = "System Configuration"


class ClientAdmin(TenantAdminMixin, ModelAdmin):
        list_display = ('name', )


site = TenantsAdmin(name='system')
site.register(get_user_model(), UserAdmin)
site.register(Group, GroupAdmin)
site.register(models.Client, ClientAdmin)
site.register(models.Domain)
