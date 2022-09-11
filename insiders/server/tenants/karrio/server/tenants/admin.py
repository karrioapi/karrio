from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth import get_user_model
from django_tenants.admin import TenantAdminMixin
from constance.admin import ConstanceAdmin, Config

import karrio.server.conf as conf
import karrio.server.user.admin as user_admin
import karrio.server.tenants.models as models


class TenantsAdmin(AdminSite):
    site_header = "Karrio"
    site_title = "Karrio"
    index_title = "System Configuration"


class ClientAdmin(TenantAdminMixin, ModelAdmin):
    list_display = ("name",)

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["feature_flags"].initial = {
            **conf.FEATURE_FLAGS,
            "ORG_LEVEL_BILLING": False,
            "TENANT_LEVEL_BILLING": False,
        }
        return form


site = TenantsAdmin(name="system")
site.register(models.Domain)
site.register(models.Client, ClientAdmin)
site.register(get_user_model(), user_admin.UserAdmin)
site.register(user_admin.Group, user_admin.GroupAdmin)

site.register([Config], ConstanceAdmin)
