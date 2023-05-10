import typing
import uuid
import strawberry
from strawberry.types import Info
from django.db import transaction
from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context

import karrio.server.conf as conf
import karrio.server.user.models as auth
import karrio.server.graph.utils as utils
import karrio.server.tenants.graph.schema.types as types
import karrio.server.tenants.graph.schema.inputs as inputs
import karrio.server.tenants.serializers as serializers
import karrio.server.tenants.models as models


@strawberry.type
class CreateTenantMutation(utils.BaseMutation):
    tenant: typing.Optional[types.TenantType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(
        info: Info,
        domain: str,
        **input,
    ) -> "CreateTenantMutation":
        data = {
            **input,
            "feature_flags": (
                input.get("feature_flags")
                or {
                    **conf.FEATURE_FLAGS,
                    "ORG_LEVEL_BILLING": False,
                    "TENANT_LEVEL_BILLING": False,
                }
            ),
        }
        # Create tenant client
        serializer = serializers.TenantModelSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save()

        # Add default tenant domain
        models.Domain.objects.create(domain=domain, tenant=tenant)

        # Setup root user auth token
        with tenant_context(tenant):
            UserModel = get_user_model()
            root_user = UserModel.objects.first()
            root_user.email = input["admin_email"]
            root_user.set_password(str(uuid.uuid4().hex))
            root_user.save()

        return CreateTenantMutation(tenant=tenant)  # type:ignore


@strawberry.type
class UpdateTenantMutation(utils.BaseMutation):
    tenant: typing.Optional[types.TenantType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, schema_name: str, **input) -> "UpdateTenantMutation":
        instance = models.Client.objects.get(schema_name=schema_name)

        serializer = serializers.TenantModelSerializer(
            instance,
            data=input,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateTenantMutation(tenant=serializer.save())  # type:ignore


@strawberry.type
class DeleteTenantMutation(utils.BaseMutation):
    id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, schema_name: str, **input) -> "DeleteTenantMutation":
        instance = models.Client.objects.get(schema_name=schema_name)
        id = instance.pk
        instance.delete(keep_parents=True)

        return DeleteTenantMutation(id=id)  # type:ignore


@strawberry.type
class AddCustomDomainMutation(utils.BaseMutation):
    domain: typing.Optional[types.DomainType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, schema_name: str, **input: inputs.AddCustomDomainMutationInput
    ) -> "AddCustomDomainMutation":
        tenant = models.Client.objects.get(schema_name=schema_name)
        domain = models.Domain.objects.create(
            **{**input, "tenant": tenant, "is_primary": True}
        )

        return AddCustomDomainMutation(domain=domain)  # type:ignore


@strawberry.type
class UpdateCustomDomainMutation(utils.BaseMutation):
    domain: typing.Optional[types.DomainType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, schema_name: str, **input) -> "UpdateCustomDomainMutation":
        instance = models.Domain.objects.get(
            is_primary=True,
            tenant__schema_name=schema_name,
        )

        serializer = serializers.DomainModelSerializer(
            instance,
            data=input,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateCustomDomainMutation(domain=serializer.save())  # type:ignore


@strawberry.type
class DeleteCustomDomainMutation(utils.BaseMutation):
    id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, schema_name: str, **input) -> "DeleteCustomDomainMutation":
        instance = models.Domain.objects.get(
            is_primary=True,
            tenant__schema_name=schema_name,
        )
        id = instance.pk
        instance.delete(keep_parents=True)

        return DeleteCustomDomainMutation(id=id)  # type:ignore
