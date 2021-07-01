import typing
from django.db import transaction

from purpleserver.serializers import ModelSerializer, owned_model_serializer
from purpleserver.orgs import models


@owned_model_serializer
class OrganizationModelSerializer(ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ('id', 'name', 'slug')

    @transaction.atomic
    def create(self, data: dict, **kwargs):
        created_by = data.pop('created_by')
        org = super().create(data)
        # Set as organization user
        org_user = org.add_user(created_by, is_admin=True)
        # Set as organization owner
        org.change_owner(org_user)

        return org

    def update(self, instance, data: dict, context, **kwargs):
        if instance.organization_users.filter(is_admin=True, user__id=context.user.id).first() is None:
            raise Exception("User Not Authorized")

        if 'name' in data and 'slug' not in data:
            data.update(slug=data['name'].replace(" ", ""),)

        return super().update(instance, data)
