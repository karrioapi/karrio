from django.contrib import admin
from organizations.base_admin import BaseOrganizationAdmin
from organizations.base_admin import BaseOrganizationOwnerAdmin
from organizations.base_admin import BaseOrganizationUserAdmin
from organizations.base_admin import BaseOwnerInline

from karrio.server.orgs.models import (
    Organization, OrganizationUser, OrganizationOwner, OrganizationInvitation
)


class OrganizationAdmin(BaseOrganizationAdmin):
    list_display = ["name", "is_active", "created"]
    fields = ('name', 'is_active', 'slug')
    list_filter = ("is_active", "created")


class OrganizationUserAdmin(BaseOrganizationUserAdmin):
    list_display = ["user", "organization", "is_admin", "created"]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner)
admin.site.register(OrganizationInvitation)
