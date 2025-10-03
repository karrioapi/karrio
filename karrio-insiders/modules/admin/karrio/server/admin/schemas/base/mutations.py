import typing
import logging
import strawberry
from constance import config
from strawberry.types import Info
import django.db.transaction as transaction
from rest_framework import exceptions

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.iam.models as iam
import karrio.server.orgs.models as orgs
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.admin.forms as forms
import karrio.server.orgs.utils as orgs_utils
import karrio.server.pricing.models as pricing
import karrio.server.serializers as serializers
import karrio.server.providers.models as providers
import karrio.server.admin.schemas.base.types as types
import karrio.server.orgs.serializers as org_serializers
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.mutations as base
import karrio.server.graph.serializers as graph_serializers
import karrio.server.providers.serializers as providers_serializers

logger = logging.getLogger(__name__)


@strawberry.type
class InstanceConfigMutation(utils.BaseMutation):
    configs: typing.Optional[types.InstanceConfigType] = None

    @staticmethod
    @admin.staff_required
    @utils.authentication_required
    def mutate(
        info: Info,
        **input: inputs.InstanceConfigMutationInput,
    ) -> "InstanceConfigMutation":
        try:
            if conf.settings.tenant:
                conf.settings.tenant.feature_flags = (
                    serializers.process_dictionaries_mutations(
                        ["feature_flags"],
                        {
                            "feature_flags": {
                                k: v
                                for k, v in input.items()
                                if k in conf.settings.CONSTANCE_CONFIG
                                and k not in ["APP_NAME", "APP_WEBSITE"]
                            }
                        },
                        conf.settings.tenant,
                    )
                ).get("feature_flags")
                if "APP_NAME" in input:
                    conf.settings.tenant.name = input["APP_NAME"]
                if "APP_WEBSITE" in input:
                    conf.settings.tenant.website = input["APP_WEBSITE"]

                conf.settings.tenant.save()

            else:
                for k, v in input.items():
                    if k in conf.settings.CONSTANCE_CONFIG:
                        setattr(config, k, v)

            return InstanceConfigMutation(
                configs=types.InstanceConfigType.resolve(info)
            )
        except Exception as e:
            logger.exception(e)
            raise e


@strawberry.type
class CreateUserMutation(utils.BaseMutation):
    user: typing.Optional[types.SystemUserType] = None

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @utils.authentication_required
    @admin.superuser_required
    def mutate(
        info: Info,
        organization_id: typing.Optional[str] = None,
        permissions: typing.Optional[typing.List[str]] = None,
        **input: inputs.CreateUserMutationInput,
    ) -> "CreateUserMutation":
        try:
            email = input["email"]

            # Check if user already exists
            existing_user = iam.User.objects.filter(email=email).first()

            if existing_user:
                existing_user.is_staff = True

                if input.get("is_superuser") is not None:
                    existing_user.is_superuser = input["is_superuser"]

                existing_user.save()
                user = existing_user
            else:
                # Create new user
                if conf.settings.MULTI_ORGANIZATIONS:
                    import karrio.server.orgs.models as orgs

                    org_id = organization_id or info.context.request.org.id
                    orgs.OrganizationInvitation.objects.create(
                        organization_id=org_id,
                        invitee_identifier=email,
                        invited_by_id=info.context.request.user.id,
                    )

                form = forms.CreateUserForm(input)

                if not form.is_valid():
                    raise exceptions.ValidationError(form.errors)

                user = form.save()

            # Update permissions regardless of whether user was created or updated
            if any(permissions or []):
                user.groups.set(iam.Group.objects.filter(name__in=permissions))

            return CreateUserMutation(
                user=iam.User.objects.get(id=user.id)
            )  # type:ignore
        except Exception as e:
            logger.exception(e)
            raise e


@strawberry.type
class UpdateUserMutation(utils.BaseMutation):
    user: typing.Optional[types.SystemUserType] = None

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @utils.authentication_required
    @admin.superuser_required
    def mutate(
        info: Info,
        id: int,
        permissions: typing.Optional[typing.List[str]] = None,
        **input: inputs.UpdateUserMutationInput,
    ) -> "UpdateUserMutation":
        instance = iam.User.objects.get(id=id)

        if not instance:
            return UpdateUserMutation(user=None)  # type:ignore

        for k, v in input.items():
            setattr(instance, k, v)

        if any(permissions or []):
            instance.groups.set(iam.Group.objects.filter(name__in=permissions))

        instance.save()

        return UpdateUserMutation(user=instance)  # type:ignore


@strawberry.type
class DeleteUserMutation(base.DeleteMutation):
    id: int = strawberry.UNSET


@strawberry.type
class CreateOrganizationAccountMutation(utils.BaseMutation):
    account: typing.Optional[types.OrganizationAccountType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.CreateOrganizationAccountMutationInput
    ) -> "CreateOrganizationAccountMutation":
        account = orgs.Organization.objects.create(**input)

        return CreateOrganizationAccountMutation(
            account=account
        )  # type:ignore


@strawberry.type
class UpdateOrganizationAccountMutation(utils.BaseMutation):
    account: typing.Optional[types.OrganizationAccountType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info, id: str, **input: inputs.UpdateOrganizationAccountMutationInput
    ) -> "UpdateOrganizationAccountMutation":
        instance = orgs.Organization.objects.get(id=id)

        for k, v in input.items():
            setattr(instance, k, v)

        if any(input.keys()):
            instance.save()

        return UpdateOrganizationAccountMutation(
            account=orgs.Organization.objects.get(id=id)
        )  # type:ignore


@strawberry.type
class DeleteOrganizationAccountMutation(utils.BaseMutation):
    account_id: str = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(info: Info, id: str) -> "DeleteOrganizationAccountMutation":
        instance = orgs.Organization.objects.get(id=id)

        instance.delete()

        return DeleteOrganizationAccountMutation(account_id=id)  # type:ignore


@strawberry.type
class DisableOrganizationAccountMutation(utils.BaseMutation):
    account: typing.Optional[types.OrganizationAccountType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(info: Info, id: str) -> "DisableOrganizationAccountMutation":
        instance = orgs.Organization.objects.get(id=id)
        instance.is_active = False
        instance.save()

        return DisableOrganizationAccountMutation(account=instance)  # type:ignore


@strawberry.type
class InviteOrganizationUserMutation(utils.BaseMutation):
    account: typing.Optional[types.OrganizationAccountType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info,
        id: str,
        emails: typing.List[str],
        redirect_url: str,
        roles: typing.List[orgs_utils.OrganizationUserRole] = [],
        is_owner: bool = False,
        **kwargs,
    ) -> "InviteOrganizationUserMutation":
        instance = orgs.Organization.objects.get(id=id)
        orgs.send_invitation_emails(
            instance,
            emails,
            redirect_url,
            info.context.request.user,
            roles,
            is_owner,
        )

        return InviteOrganizationUserMutation(account=instance)  # type:ignore


@strawberry.type
class DeleteConnectionMutation(utils.BaseMutation):
    id: str = strawberry.UNSET

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @admin.staff_required
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    def mutate(info: Info, **input) -> "DeleteConnectionMutation":
        instance = providers.Carrier.system_carriers.get(id=input["id"])
        instance.delete()
        return DeleteConnectionMutation(id=input["id"])


@strawberry.type
class CreateSystemCarrierConnectionMutation(utils.BaseMutation):
    connection: typing.Optional[types.SystemCarrierConnectionType] = None

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(info: Info, **input) -> "CreateSystemCarrierConnectionMutation":
        data = input.copy()

        connection = lib.identity(
            providers_serializers.CarrierConnectionModelSerializer.map(
                data=providers_serializers.CarrierConnectionData.map(data=data).data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        connection.is_system = True
        connection.save()

        return CreateSystemCarrierConnectionMutation(  # type:ignore
            connection=connection
        )


@strawberry.type
class UpdateSystemCarrierConnectionMutation(utils.BaseMutation):
    connection: typing.Optional[types.SystemCarrierConnectionType] = None

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(info: Info, **input) -> "UpdateSystemCarrierConnectionMutation":
        data = input.copy()
        id = data.get("id")
        instance = providers.Carrier.objects.get(id=id)
        connection = lib.identity(
            providers_serializers.CarrierConnectionModelSerializer.map(
                instance,
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return UpdateSystemCarrierConnectionMutation(  # type:ignore
            connection=connection
        )


@strawberry.type
class CreateAddonMutation(utils.BaseMutation):
    addon: typing.Optional[types.AddonType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def mutate(
        info: Info,
        **input: inputs.CreateAddonMutationInput,
    ) -> "CreateAddonMutation":
        organizations = input.pop("organizations", [])
        carrier_accounts = input.pop("carrier_accounts", [])
        instance = pricing.Surcharge(**input)

        instance.save()

        if any(carrier_accounts):
            instance.carrier_accounts.set(carrier_accounts)

        if conf.settings.MULTI_ORGANIZATIONS and any(organizations):
            import karrio.server.orgs.models as orgs

            instance.organizations.set(
                orgs.Organization.objects.filter(id__in=organizations)
            )

        return CreateAddonMutation(
            addon=pricing.Surcharge.objects.get(id=instance.id)
        )  # type:ignore


@strawberry.type
class UpdateAddonMutation(utils.BaseMutation):
    addon: typing.Optional[types.AddonType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    @transaction.atomic
    def mutate(
        info: Info,
        id: str,
        **input: inputs.UpdateAddonMutationInput,
    ) -> "UpdateAddonMutation":
        instance = pricing.Surcharge.objects.get(id=id)
        carrier_accounts = input.pop("carrier_accounts", [])
        organizations = input.pop("organizations", [])

        for k, v in input.items():
            setattr(instance, k, v)

        if any(carrier_accounts):
            instance.carrier_accounts.set(carrier_accounts)

        if conf.settings.MULTI_ORGANIZATIONS and any(organizations):
            import karrio.server.orgs.models as orgs

            instance.organizations.set(
                orgs.Organization.objects.filter(id__in=organizations)
            )

        instance.save()

        return UpdateAddonMutation(
            addon=pricing.Surcharge.objects.get(id=id)
        )  # type:ignore


@strawberry.type
class CreateRateSheetMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.CreateRateSheetMutationInput
    ) -> "CreateRateSheetMutation":
        data = input.copy()
        carriers = data.pop("carriers", [])
        slug = f"{input.get('name', '').lower()}_sheet".replace(" ", "").lower()
        serializer = graph_serializers.RateSheetModelSerializer(
            data={**data, "slug": slug, "is_system": True},
            context=info.context.request,
        )

        serializer.is_valid(raise_exception=True)
        rate_sheet = serializer.save()

        if "services" in data:
            serializers.save_many_to_many_data(
                "services",
                graph_serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )

        if any(carriers):
            (
                providers.Carrier.objects.filter(
                    carrier_code=rate_sheet.carrier_name,
                    id__in=carriers,
                    is_system=True,
                ).update(rate_sheet=rate_sheet)
            )

        return CreateRateSheetMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateRateSheetMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateRateSheetMutationInput
    ) -> "UpdateRateSheetMutation":
        data = input.copy()
        carriers = data.pop("carriers", [])
        instance = providers.RateSheet.access_by(info.context.request).get(
            id=input["id"]
        )
        serializer = graph_serializers.RateSheetModelSerializer(
            instance,
            data=data,
            context=info.context.request,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        rate_sheet = serializer.save()

        if "services" in data:
            serializers.save_many_to_many_data(
                "services",
                graph_serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )

        if any(carriers):
            # Link listed carriers to rate sheet
            (
                providers.Carrier.objects.filter(
                    carrier_code=rate_sheet.carrier_name,
                    id__in=carriers,
                    is_system=True,
                ).update(rate_sheet=rate_sheet)
            )
            # Unlink missing carriers from rate sheet
            (
                providers.Carrier.objects.filter(
                    carrier_code=rate_sheet.carrier_name,
                    rate_sheet=rate_sheet,
                    is_system=True,
                )
                .exclude(id__in=carriers)
                .update(rate_sheet=None)
            )

        return UpdateRateSheetMutation(
            rate_sheet=providers.RateSheet.objects.get(id=input["id"])
        )


@strawberry.type
class UpdateRateSheetZoneCellMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateRateSheetZoneCellMutationInput
    ) -> "UpdateRateSheetZoneCellMutation":
        rate_sheet = providers.RateSheet.objects.get(
            id=input["id"]
        )
        service = rate_sheet.services.get(id=input["service_id"])

        try:
            service.update_zone_cell(
                zone_id=input["zone_id"], field=input["field"], value=input["value"]
            )
        except ValueError as e:
            logger.error(f"Invalid zone id: {e}")
            raise exceptions.ValidationError({"zone_id": "invalid zone id"})

        return UpdateRateSheetZoneCellMutation(rate_sheet=rate_sheet)


@strawberry.type
class BatchUpdateRateSheetCellsMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.BatchUpdateRateSheetCellsMutationInput
    ) -> "BatchUpdateRateSheetCellsMutation":
        rate_sheet = providers.RateSheet.objects.get(
            id=input["id"]
        )

        # Group updates by service_id for efficient processing
        service_updates = {}
        for update in input["updates"]:
            service_id = update["service_id"]
            if service_id not in service_updates:
                service_updates[service_id] = []
            service_updates[service_id].append(
                {
                    "zone_id": update["zone_id"],
                    "field": update["field"],
                    "value": update["value"],
                }
            )

        # Use optimized structure if available, otherwise fall back to legacy
        if rate_sheet.zones is not None and rate_sheet.service_rates is not None:
            # Use optimized batch update on rate sheet
            all_updates = []
            for service_id, updates in service_updates.items():
                for update in updates:
                    all_updates.append(
                        {
                            "service_id": service_id,
                            "zone_id": update["zone_id"],
                            "field": update["field"],
                            "value": update["value"],
                        }
                    )
            try:
                rate_sheet.batch_update_service_rates(all_updates)
            except Exception as e:
                logger.error(f"Invalid zone id: {e}")
                raise exceptions.ValidationError(
                    {"rate_sheet": "failed to update rate sheet"}
                )
        else:
            # Fall back to legacy per-service updates
            for service_id, updates in service_updates.items():
                try:
                    service = rate_sheet.services.get(id=service_id)
                    service.batch_update_cells(updates)
                except ValueError as e:
                    logger.error(f"Invalid zone id: {e}")
                    raise exceptions.ValidationError(
                        {"service_id": "failed to update service"}
                    )

        return BatchUpdateRateSheetCellsMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteRateSheetServiceMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.DeleteRateSheetServiceMutationInput
    ) -> "DeleteRateSheetServiceMutation":
        rate_sheet = providers.RateSheet.objects.get(
            id=input["rate_sheet_id"]
        )
        service = rate_sheet.services.get(id=input["service_id"])

        # Remove service from rate sheet and delete it
        rate_sheet.services.remove(service)
        service.delete()

        return DeleteRateSheetServiceMutation(rate_sheet=rate_sheet)
