from django.contrib import admin
from organizations.base_admin import BaseOrganizationAdmin
from organizations.base_admin import BaseOrganizationOwnerAdmin
from organizations.base_admin import BaseOrganizationUserAdmin
from organizations.base_admin import BaseOwnerInline

from purpleserver.orgs.models import Organization, OrganizationUser, OrganizationOwner


class OrganizationAdmin(BaseOrganizationAdmin):
    fields = ('name', 'is_active', 'slug')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser)
admin.site.register(OrganizationOwner)
