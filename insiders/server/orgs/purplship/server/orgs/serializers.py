from enum import Enum
from django.db import transaction

from karrio.server.serializers import ModelSerializer, owned_model_serializer
from karrio.server.orgs.utils import admin_required
from karrio.server.orgs import models


@owned_model_serializer
class OrganizationModelSerializer(ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ("id", "name", "slug")

    @transaction.atomic
    def create(self, data: dict, **kwargs):
        created_by = data.pop("created_by")
        org = super().create(
            {
                "slug": f"{data.get('name').lower()}_org".replace(" ", "").lower(),
                **data,
            }
        )
        # Set as organization user
        org_user = org.add_user(created_by, is_admin=True)
        # Set as organization owner
        org.change_owner(org_user)
        org.save()

        return org

    def update(self, instance, data: dict, context, **kwargs) -> models.Organization:
        admin_required(instance, context)

        if "name" in data and "slug" not in data:
            data.update(
                slug=data["name"].lower().replace(" ", ""),
            )

        return super().update(instance, data)
