from django.contrib import admin
from organizations.base_admin import BaseOrganizationAdmin
from organizations.base_admin import BaseOrganizationOwnerAdmin
from organizations.base_admin import BaseOrganizationUserAdmin
from organizations.base_admin import BaseOwnerInline

from karrio.server.orgs.models import (
    Organization,
    OrganizationUser,
    OrganizationOwner,
    OrganizationInvitation,
)


class OrganizationAdmin(BaseOrganizationAdmin):
    list_display = ["name", "is_active", "created"]
    fields = ("name", "is_active", "slug")
    list_filter = ("is_active", "created")
    view_on_site = False


class OrganizationUserAdmin(BaseOrganizationUserAdmin):
    list_display = ["user", "organization", "is_admin", "created"]
    fields = ("user", "organization", "roles")
    view_on_site = False

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ("user", "organization")
        return self.readonly_fields

    def test_fields(self, obj):
        return "test"


class TokenLinkInline(admin.TabularInline):
    model = Organization.tokens.through
    max_num = 1
    min_num = 1

    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["org"].queryset = Organization.objects.filter(
            users__id=request.user.id
        ).distinct()
        return formset


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner)
admin.site.register(OrganizationInvitation)
