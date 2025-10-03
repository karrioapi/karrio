from django.db import transaction

import karrio.lib as lib
import karrio.server.orgs.models as models
import karrio.server.orgs.serializers as serializers


@serializers.owned_model_serializer
class OrganizationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("id", "name", "slug")

    @transaction.atomic
    def create(self, data: dict, **kwargs):
        owner = lib.identity(
            (data.pop("owner") if "owner" in data else None)
            or (data.pop("created_by") if "created_by" in data else None)
        )

        org = super().create(data, **kwargs)

        if owner:
            # Set as organization user
            org_user = org.add_user(owner, is_admin=True)
            # Set as organization owner
            org.change_owner(org_user)

        org.save()
        return org

    def update(self, instance, data: dict, **kwargs) -> models.Organization:
        if "name" in data and "slug" not in data:
            data.update(
                slug=data["name"].lower().replace(" ", ""),
            )

        return super().update(instance, data)
