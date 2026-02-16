import typing
import datetime
import strawberry
from constance import config
from strawberry.types import Info
import django.db.transaction as transaction
from django.utils import timezone
from rest_framework import exceptions

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.iam.models as iam
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.admin.forms as forms
import karrio.server.pricing.models as pricing
import karrio.server.serializers as serializers
import karrio.server.providers.models as providers
import karrio.server.admin.schemas.base.types as types
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.mutations as base
import karrio.server.graph.serializers as graph_serializers
import karrio.server.providers.serializers as providers_serializers
from karrio.server.core.logging import logger


@strawberry.type
class InstanceConfigMutation(utils.BaseMutation):
    configs: typing.Optional[types.InstanceConfigType] = None

    @staticmethod
    @admin.staff_required
    @utils.authentication_required
    def mutate(info: Info, **input) -> "InstanceConfigMutation":
        data = input.get("configs") or {}
        try:
            if conf.settings.tenant:
                conf.settings.tenant.feature_flags = (
                    serializers.process_dictionaries_mutations(
                        ["feature_flags"],
                        {
                            "feature_flags": {
                                k: v
                                for k, v in data.items()
                                if k in conf.settings.CONSTANCE_CONFIG
                                and k not in ["APP_NAME", "APP_WEBSITE"]
                            }
                        },
                        conf.settings.tenant,
                    )
                ).get("feature_flags")
                if "APP_NAME" in data:
                    conf.settings.tenant.name = data["APP_NAME"]
                if "APP_WEBSITE" in data:
                    conf.settings.tenant.website = data["APP_WEBSITE"]

                conf.settings.tenant.save()

            else:
                for k, v in data.items():
                    if k in conf.settings.CONSTANCE_CONFIG:
                        setattr(config, k, v)

            return InstanceConfigMutation(
                configs=types.InstanceConfigType.resolve(info)
            )
        except Exception as e:
            logger.error("Failed to update instance config", error=str(e), exc_info=True)
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
            logger.error("Failed to create user", email=input.get("email"), error=str(e), exc_info=True)
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
class DeleteConnectionMutation(utils.BaseMutation):
    id: str = strawberry.UNSET

    @staticmethod
    @transaction.atomic
    @utils.error_wrapper
    @admin.staff_required
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    def mutate(info: Info, **input) -> "DeleteConnectionMutation":
        # SystemConnection.objects replaces the removed CarrierConnection.system_carriers manager
        instance = providers.SystemConnection.objects.get(id=input["id"])
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
            providers_serializers.SystemConnectionModelSerializer.map(
                data=providers_serializers.CarrierConnectionData.map(data=data).data,
                context=info.context.request,
            )
            .save()
            .instance
        )

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

        # Get SystemConnection instance
        instance = providers.SystemConnection.objects.get(id=id)

        connection = lib.identity(
            providers_serializers.SystemConnectionModelSerializer.map(
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
class CreateMarkupMutation(utils.BaseMutation):
    """Create a new Markup."""

    markup: typing.Optional[types.MarkupType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    @transaction.atomic
    def mutate(
        info: Info,
        **input: inputs.CreateMarkupMutationInput,
    ) -> "CreateMarkupMutation":
        organizations = input.pop("organizations", [])

        instance = pricing.Markup(**input)

        if organizations:
            instance.organization_ids = organizations

        instance.save()

        return CreateMarkupMutation(
            markup=pricing.Markup.objects.get(id=instance.id)
        )  # type:ignore


@strawberry.type
class UpdateMarkupMutation(utils.BaseMutation):
    """Update an existing Markup."""

    markup: typing.Optional[types.MarkupType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    @transaction.atomic
    def mutate(
        info: Info,
        id: str,
        **input: inputs.UpdateMarkupMutationInput,
    ) -> "UpdateMarkupMutation":
        instance = pricing.Markup.objects.get(id=id)

        organizations = input.pop("organizations", None)

        for k, v in input.items():
            if v is not None:
                setattr(instance, k, v)

        if organizations is not None:
            instance.organization_ids = organizations

        instance.save()

        return UpdateMarkupMutation(
            markup=pricing.Markup.objects.get(id=id)
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
        zones_data = data.pop("zones", [])
        surcharges_data = data.pop("surcharges", [])
        service_rates_data = data.pop("service_rates", [])
        services_data = [
            (svc.copy() if isinstance(svc, dict) else dict(svc))
            for svc in data.get("services", [])
        ]

        slug = f"{input.get('name', '').lower()}_sheet".replace(" ", "").lower()
        serializer = graph_serializers.RateSheetModelSerializer(
            data={**data, "slug": slug, "is_system": True},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        rate_sheet = serializer.save()

        # Create services and build temp-to-real ID mapping
        if services_data:
            serializers.save_many_to_many_data(
                "services",
                graph_serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )
            rate_sheet.refresh_from_db()

        temp_to_real_id = serializer.build_temp_to_real_service_map(services_data)

        # Link system connections to rate sheet
        if any(carriers):
            providers.SystemConnection.objects.filter(
                carrier_code=rate_sheet.carrier_name,
                id__in=carriers,
            ).update(rate_sheet=rate_sheet)

        # Process zones, surcharges, and service_rates via serializer
        if zones_data:
            serializer.process_zones(zones_data)
        if surcharges_data:
            serializer.process_surcharges(surcharges_data)
        if service_rates_data:
            serializer.process_service_rates(service_rates_data, temp_to_real_id)

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

        # Handle services updates
        if "services" in data:
            serializers.save_many_to_many_data(
                "services",
                graph_serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )

        # Link/unlink system connections to rate sheet
        if any(carriers):
            connection_qs = providers.SystemConnection.objects.filter(
                carrier_code=rate_sheet.carrier_name,
            )
            connection_qs.filter(id__in=carriers).update(rate_sheet=rate_sheet)
            connection_qs.filter(rate_sheet=rate_sheet).exclude(id__in=carriers).update(
                rate_sheet=None
            )

        return UpdateRateSheetMutation(
            rate_sheet=providers.RateSheet.objects.get(id=input["id"])
        )


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


# ─────────────────────────────────────────────────────────────────────────────
# SHARED ZONE MUTATIONS (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class AddSharedZoneMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.AddSharedZoneMutationInput
    ) -> "AddSharedZoneMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        zone_data = input["zone"]
        zone_dict = {k: v for k, v in zone_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.add_zone(zone_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"zone": str(e)})

        return AddSharedZoneMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateSharedZoneMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateSharedZoneMutationInput
    ) -> "UpdateSharedZoneMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        zone_data = input["zone"]
        zone_dict = {k: v for k, v in zone_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.update_zone(input["zone_id"], zone_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"zone_id": str(e)})

        return UpdateSharedZoneMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteSharedZoneMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.DeleteSharedZoneMutationInput
    ) -> "DeleteSharedZoneMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        try:
            rate_sheet.remove_zone(input["zone_id"])
        except ValueError as e:
            raise exceptions.ValidationError({"zone_id": str(e)})

        return DeleteSharedZoneMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED SURCHARGE MUTATIONS (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class AddSharedSurchargeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.AddSharedSurchargeMutationInput
    ) -> "AddSharedSurchargeMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        surcharge_data = input["surcharge"]
        surcharge_dict = {k: v for k, v in surcharge_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.add_surcharge(surcharge_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge": str(e)})

        return AddSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateSharedSurchargeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateSharedSurchargeMutationInput
    ) -> "UpdateSharedSurchargeMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        surcharge_data = input["surcharge"]
        surcharge_dict = {k: v for k, v in surcharge_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.update_surcharge(input["surcharge_id"], surcharge_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge_id": str(e)})

        return UpdateSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteSharedSurchargeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.DeleteSharedSurchargeMutationInput
    ) -> "DeleteSharedSurchargeMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        try:
            rate_sheet.remove_surcharge(input["surcharge_id"])
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge_id": str(e)})

        return DeleteSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class BatchUpdateSurchargesMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.BatchUpdateSurchargesMutationInput
    ) -> "BatchUpdateSurchargesMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        surcharges = [
            {k: v for k, v in s.items() if not utils.is_unset(v)}
            for s in input["surcharges"]
        ]

        try:
            rate_sheet.batch_update_surcharges(surcharges)
        except ValueError as e:
            raise exceptions.ValidationError({"surcharges": str(e)})

        return BatchUpdateSurchargesMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE RATE MUTATIONS (Service-Zone Rate Mapping)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class UpdateServiceRateMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateServiceRateMutationInput
    ) -> "UpdateServiceRateMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        # Build the rate update dict from input fields
        rate_data = {}
        rate_fields = ["rate", "cost", "min_weight", "max_weight", "transit_days", "transit_time"]
        for field in rate_fields:
            if field in input and not utils.is_unset(input[field]):
                rate_data[field] = input[field]

        try:
            rate_sheet.update_service_rate(
                service_id=input["service_id"],
                zone_id=input["zone_id"],
                rate_data=rate_data
            )
        except ValueError as e:
            raise exceptions.ValidationError({"rate": str(e)})

        return UpdateServiceRateMutation(rate_sheet=rate_sheet)


@strawberry.type
class BatchUpdateServiceRatesMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.BatchUpdateServiceRatesMutationInput
    ) -> "BatchUpdateServiceRatesMutation":
        from rest_framework import exceptions

        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        updates = [
            {k: v for k, v in rate.items() if not utils.is_unset(v)}
            for rate in input["rates"]
        ]

        try:
            rate_sheet.batch_update_service_rates(updates)
        except ValueError as e:
            raise exceptions.ValidationError({"rates": str(e)})

        return BatchUpdateServiceRatesMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteServiceRateMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.DeleteServiceRateMutationInput
    ) -> "DeleteServiceRateMutation":
        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        min_weight = input.get("min_weight")
        max_weight = input.get("max_weight")
        if utils.is_unset(min_weight):
            min_weight = None
        if utils.is_unset(max_weight):
            max_weight = None

        rate_sheet.remove_service_rate(
            service_id=input["service_id"],
            zone_id=input["zone_id"],
            min_weight=min_weight,
            max_weight=max_weight,
        )

        return DeleteServiceRateMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# WEIGHT RANGE MUTATIONS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class AddWeightRangeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.AddWeightRangeMutationInput
    ) -> "AddWeightRangeMutation":
        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        rate_sheet.add_weight_range(
            min_weight=input["min_weight"],
            max_weight=input["max_weight"],
        )

        return AddWeightRangeMutation(rate_sheet=rate_sheet)


@strawberry.type
class RemoveWeightRangeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.RemoveWeightRangeMutationInput
    ) -> "RemoveWeightRangeMutation":
        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])

        rate_sheet.remove_weight_range(
            min_weight=input["min_weight"],
            max_weight=input["max_weight"],
        )

        return RemoveWeightRangeMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE ZONE/SURCHARGE ASSIGNMENT MUTATIONS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class UpdateServiceZoneIdsMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateServiceZoneIdsMutationInput
    ) -> "UpdateServiceZoneIdsMutation":
        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        service = rate_sheet.services.get(id=input["service_id"])

        service.zone_ids = input["zone_ids"]
        service.save(update_fields=["zone_ids"])

        return UpdateServiceZoneIdsMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateServiceSurchargeIdsMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.SystemRateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["manage_carriers"])
    @admin.staff_required
    def mutate(
        info: Info, **input: inputs.base.UpdateServiceSurchargeIdsMutationInput
    ) -> "UpdateServiceSurchargeIdsMutation":
        rate_sheet = providers.RateSheet.objects.get(id=input["rate_sheet_id"])
        service = rate_sheet.services.get(id=input["service_id"])

        service.surcharge_ids = input["surcharge_ids"]
        service.save(update_fields=["surcharge_ids"])

        return UpdateServiceSurchargeIdsMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# WORKER MANAGEMENT MUTATIONS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class TriggerTrackerUpdateMutation(utils.BaseMutation):
    task_count: int = 0

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "TriggerTrackerUpdateMutation":
        from karrio.server.events.task_definitions.base import tracking
        import karrio.server.core.utils as core_utils

        tracker_ids = input.get("tracker_ids") or []
        task_count = 0

        @core_utils.run_on_all_tenants
        def _run(**kwargs):
            nonlocal task_count
            result = tracking.update_trackers(
                delta=datetime.timedelta(seconds=0),
                tracker_ids=tracker_ids,
                schema=kwargs.get("schema"),
            )
            if result is not None:
                task_count += result

        _run()

        return TriggerTrackerUpdateMutation(task_count=task_count)


@strawberry.type
class RetryWebhookMutation(utils.BaseMutation):
    event_id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "RetryWebhookMutation":
        from karrio.server.events.models import Event
        from karrio.server.events.task_definitions.base import notify_webhooks

        event_id = input["event_id"]
        event = Event.objects.get(id=event_id)

        notify_webhooks(
            event.type,
            event.data,
            event.created_at,
            ctx=dict(
                test_mode=event.test_mode,
            ),
        )

        return RetryWebhookMutation(event_id=event_id)


@strawberry.type
class RevokeTaskMutation(utils.BaseMutation):
    task_id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "RevokeTaskMutation":
        from huey.contrib.djhuey import HUEY as huey_instance
        from karrio.server.admin.worker.models import TaskExecution

        task_id = input["task_id"]
        huey_instance.revoke_by_id(task_id)

        TaskExecution.objects.filter(task_id=task_id).update(
            status="revoked",
            completed_at=timezone.now(),
            error="Revoked by admin",
        )

        return RevokeTaskMutation(task_id=task_id)


@strawberry.type
class CleanupTaskExecutionsMutation(utils.BaseMutation):
    deleted_count: int = 0

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "CleanupTaskExecutionsMutation":
        from karrio.server.admin.worker.models import TaskExecution

        retention_days = input.get("retention_days") or 7
        statuses = input.get("statuses") or []
        cutoff = timezone.now() - datetime.timedelta(days=retention_days)

        qs = TaskExecution.objects.filter(queued_at__lt=cutoff)
        if statuses:
            qs = qs.filter(status__in=statuses)

        deleted_count, _ = qs.delete()

        return CleanupTaskExecutionsMutation(deleted_count=deleted_count)


@strawberry.type
class ResetStuckTasksMutation(utils.BaseMutation):
    updated_count: int = 0

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "ResetStuckTasksMutation":
        from karrio.server.admin.worker.models import TaskExecution

        threshold_minutes = input.get("threshold_minutes") or 60
        statuses = input.get("statuses") or ["executing", "queued"]
        cutoff = timezone.now() - datetime.timedelta(minutes=threshold_minutes)

        updated_count = TaskExecution.objects.filter(
            status__in=statuses,
            queued_at__lt=cutoff,
        ).update(
            status="error",
            error="Reset by admin",
            completed_at=timezone.now(),
        )

        return ResetStuckTasksMutation(updated_count=updated_count)


@strawberry.type
class TriggerDataArchivingMutation(utils.BaseMutation):
    success: bool = False

    @staticmethod
    @utils.authentication_required
    @admin.superuser_required
    def mutate(info: Info, **input) -> "TriggerDataArchivingMutation":
        from karrio.server.events.task_definitions.base import archiving
        import karrio.server.core.utils as core_utils

        @core_utils.run_on_all_tenants
        def _run(**kwargs):
            core_utils.failsafe(
                lambda: archiving.run_data_archiving(),
                "An error occured during data archiving: $error",
            )

        _run()

        return TriggerDataArchivingMutation(success=True)
