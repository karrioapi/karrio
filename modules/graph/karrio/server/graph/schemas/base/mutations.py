import strawberry
import typing
import datetime
from strawberry.types import Info
from rest_framework import exceptions
from django.utils.http import urlsafe_base64_decode
from django.contrib.contenttypes.models import ContentType
from django_email_verification import confirm as email_verification
from django_otp.plugins.otp_email import models as otp
from django.utils.translation import gettext_lazy as _
from django.db import transaction, models

from karrio.server.core.utils import ConfirmationToken, send_email
from karrio.server.user.serializers import TokenSerializer
from karrio.server.conf import settings
from karrio.server.serializers import (
    save_many_to_many_data,
    process_dictionaries_mutations,
)
from karrio.server.core.logging import logger
import karrio.server.providers.serializers as providers_serializers
import karrio.server.manager.serializers as manager_serializers
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.types as types
import karrio.server.graph.serializers as serializers
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.user.forms as user_forms
import karrio.server.core.gateway as gateway
import karrio.server.graph.models as graph
import karrio.server.graph.forms as forms
import karrio.server.graph.utils as utils
import karrio.server.user.models as auth
import karrio.server.iam.models as iam
import karrio.server.core.models as core
import karrio.lib as lib


@strawberry.type
class UserUpdateMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, **input: inputs.UpdateUserInput) -> "UserUpdateMutation":
        instance = types.User.objects.get(id=info.context.request.user.id)

        serializer = serializers.UserModelSerializer(
            instance,
            partial=True,
            data=process_dictionaries_mutations(["metadata"], input, instance),
            context=info.context.request,
        )

        serializer.is_valid(raise_exception=True)

        return UserUpdateMutation(user=serializer.save())  # type:ignore


@strawberry.type
class WorkspaceConfigMutation(utils.BaseMutation):
    workspace_config: typing.Optional[types.WorkspaceConfigType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.WorkspaceConfigMutationInput
    ) -> "WorkspaceConfigMutation":
        data = dict(config=input.copy())
        workspace = auth.WorkspaceConfig.access_by(info.context.request).first()

        serializer = serializers.WorkspaceConfigModelSerializer(
            workspace,
            partial=workspace is not None,
            data=process_dictionaries_mutations(["config"], data, workspace),
            context=info.context.request,
        )

        serializer.is_valid(raise_exception=True)

        return WorkspaceConfigMutation(
            workspace_config=serializer.save()
        )  # type:ignore


@strawberry.type
class TokenMutation(utils.BaseMutation):
    token: typing.Optional[types.TokenType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info,
        key: str = None,
        refresh: bool = None,
        password: str = None,
    ) -> "UserUpdateMutation":
        tokens = auth.Token.access_by(info.context.request).filter(key=key)

        if refresh:
            if len(password or "") == 0:
                raise exceptions.ValidationError(
                    {"password": "Password is required to refresh token"}
                )

            if not info.context.request.user.check_password(password):
                raise exceptions.ValidationError({"password": "Invalid password"})

            if any(tokens):
                tokens.delete()

        else:
            return TokenMutation(token=tokens.first())  # type:ignore

        token = (
            TokenSerializer.map(data={}, context=info.context.request).save().instance
        )

        return TokenMutation(token=token)  # type:ignore


@strawberry.type
class CreateAPIKeyMutation(utils.BaseMutation):
    api_key: typing.Optional[types.APIKeyType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.password_required
    def mutate(
        info: Info, password: str, **input: inputs.CreateAPIKeyMutationInput
    ) -> "CreateAPIKeyMutation":
        context = info.context.request
        data = input.copy()
        permissions = data.pop("permissions", [])
        api_key = TokenSerializer.map(data=data, context=context).save().instance

        if any(permissions):
            _auth_ctx = (
                context.token
                if hasattr(getattr(info.context.request, "token", None), "permissions")
                else context.user
            )
            _ctx_permissions = getattr(_auth_ctx, "permissions", [])
            _invalid_permissions = [_ for _ in permissions if _ not in _ctx_permissions]

            if any(_invalid_permissions):
                raise exceptions.ValidationError({"permissions": "Invalid permissions"})

            _ctx = iam.ContextPermission.objects.create(
                object_pk=api_key.pk,
                content_object=api_key,
                content_type=ContentType.objects.get_for_model(api_key),
            )
            _ctx.groups.set(auth.Group.objects.filter(name__in=permissions))

        return CreateAPIKeyMutation(
            api_key=auth.Token.access_by(context).get(key=api_key.key)
        )  # type:ignore


@strawberry.type
class DeleteAPIKeyMutation(utils.BaseMutation):
    label: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @utils.password_required
    def mutate(
        info: Info, password: str, **input: inputs.DeleteAPIKeyMutationInput
    ) -> "DeleteAPIKeyMutation":
        api_key = auth.Token.access_by(info.context.request).get(**input)
        label = api_key.label
        api_key.delete()

        return DeleteAPIKeyMutation(label=label)  # type:ignore


@strawberry.type
class RequestEmailChangeMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    @utils.password_required
    def mutate(
        info: Info, email: str, password: str, redirect_url: str
    ) -> "RequestEmailChangeMutation":
        try:
            token = ConfirmationToken.for_data(
                user=info.context.request.user,
                data=dict(new_email=email),
            )

            send_email(
                emails=[email],
                subject="Confirm your new email address",
                email_template="karrio/email_change_email.html",
                text_template="karrio/email_change_email.txt",
                context=dict(
                    token=token,
                    link=redirect_url,
                ),
                expiry=(datetime.datetime.now() + datetime.timedelta(hours=2)),
            )
        except Exception as e:
            logger.exception(
                "Email change request failed",
                user_id=info.context.request.user.id,
                error=str(e),
            )
            raise e

        return RequestEmailChangeMutation(user=info.context.request.user)  # type:ignore


@strawberry.type
class ConfirmEmailChangeMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, token: str) -> "ConfirmEmailChangeMutation":
        validated_token = ConfirmationToken(token)
        user = info.context.request.user

        if str(user.id) != validated_token["user_id"]:
            raise exceptions.ValidationError(
                {"token": "auth.Token is invalid or expired"}
            )

        if user.email == validated_token["new_email"]:
            raise exceptions.APIException("Email is already confirmed")

        user.email = validated_token["new_email"]
        user.save()

        return ConfirmEmailChangeMutation(
            user=types.User.objects.get(id=validated_token["user_id"])
        )  # type:ignore


@strawberry.type
class RegisterUserMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    def mutate(
        info: Info, **input: inputs.RegisterUserMutationInput
    ) -> "RegisterUserMutation":
        if settings.ALLOW_SIGNUP == False:
            raise Exception(
                "Signup is not allowed. "
                "Please contact your administrator to create an account."
            )

        try:
            form = user_forms.SignUpForm(data=input)
            if not form.is_valid():
                errors = []
                for field, messages in form.errors.items():
                    for message in messages:
                        errors.append(f"{field}: {message}")
                raise Exception(". ".join(errors))

            user = form.save()

            return RegisterUserMutation(user=user)  # type:ignore
        except Exception as e:
            logger.exception(
                "User registration failed", email=input.get("email"), error=str(e)
            )
            raise e


@strawberry.type
class ConfirmEmailMutation(utils.BaseMutation):
    success: bool = False

    @staticmethod
    def mutate(info: Info, token: str) -> "ConfirmEmailMutation":
        try:
            success, _ = email_verification.verify_token(token)

            return ConfirmEmailMutation(success=success)  # type:ignore
        except Exception as e:
            logger.exception("Email confirmation failed", error=str(e))
            raise e


@strawberry.type
class ChangePasswordMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.ChangePasswordMutationInput
    ) -> "ChangePasswordMutation":
        form = forms.PasswordChangeForm(info.context.request.user, data=input)
        if form.is_valid():
            user = form.save()
            return ChangePasswordMutation(user=user)  # type:ignore
        else:
            raise exceptions.ValidationError(form.errors)


@strawberry.type
class RequestPasswordResetMutation(utils.BaseMutation):
    email: str = strawberry.UNSET
    redirect_url: str = strawberry.UNSET

    @staticmethod
    def mutate(
        info: Info, **input: inputs.RequestPasswordResetMutationInput
    ) -> "RequestPasswordResetMutation":
        form = forms.ResetPasswordRequestForm(data=input)

        if form.is_valid():
            form.save(request=info.context.request)
            return RequestPasswordResetMutation(**form.cleaned_data)  # type:ignore
        else:
            raise exceptions.ValidationError(form.errors)


@strawberry.type
class ConfirmPasswordResetMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = types.User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            types.User.DoesNotExist,
            exceptions.ValidationError,
        ):
            user = None
        return user

    @staticmethod
    def mutate(
        info: Info, **input: inputs.ConfirmPasswordResetMutationInput
    ) -> "ConfirmPasswordResetMutation":
        uuid = input.get("uid")
        user = ConfirmPasswordResetMutation.get_user(uuid)  # type:ignore
        form = forms.ConfirmPasswordResetForm(user, data=input)

        if form.is_valid():
            return ConfirmPasswordResetMutation(user=form.save())  # type:ignore
        else:
            raise exceptions.ValidationError(form.errors)


@strawberry.type
class EnableMultiFactorMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.EnableMultiFactorMutationInput
    ) -> "EnableMultiFactorMutation":
        # Retrieve a default device or create a new one.
        device = otp.EmailDevice.objects.filter(
            user__id=info.context.request.user.id
        ).first()
        if device is None:
            device = otp.EmailDevice.objects.create(
                name="default",
                confirmed=False,
                user=info.context.request.user,
            )

        # Send and email challenge if the device isn't confirmed yet.
        if device.confirmed == False:
            device.generate_challenge()

        return EnableMultiFactorMutation(  # type:ignore
            user=types.User.objects.get(pk=info.context.request.user.id)
        )


@strawberry.type
class ConfirmMultiFactorMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.ConfirmMultiFactorMutationInput
    ) -> "ConfirmMultiFactorMutation":
        token = input.get("token")
        # Retrieve a default device or create a new one.
        device = otp.EmailDevice.objects.filter(
            user__id=info.context.request.user.id
        ).first()

        if device is None:
            raise exceptions.APIException(
                _("You need to enable Two factor auth first."), code="2fa_disabled"
            )

        # check if token is valid
        if device.verify_token(token) is False:
            raise exceptions.ValidationError(
                {"otp_token": _("Invalid or Expired OTP token")}, code="otp_invalid"
            )

        device.confirmed = True
        device.save()

        return ConfirmMultiFactorMutation(  # type:ignore
            user=types.User.objects.get(pk=info.context.request.user.id)
        )


@strawberry.type
class DisableMultiFactorMutation(utils.BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DisableMultiFactorMutationInput
    ) -> "DisableMultiFactorMutation":
        # Retrieve a default device or create a new one.
        device = otp.EmailDevice.objects.filter(
            user__id=info.context.request.user.id
        ).first()
        if device is not None:
            device.delete()

        return DisableMultiFactorMutation(  # type:ignore
            user=types.User.objects.get(pk=info.context.request.user.id)
        )


@strawberry.type
class MetadataMutation(utils.BaseMutation):
    id: str = strawberry.UNSET
    metadata: utils.JSON = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info,
        id: str,
        object_type: utils.MetadataObjectTypeEnum,
        added_values: dict = {},
        discarded_keys: list = [],
    ) -> "MetadataMutation":
        object_model = utils.MetadataObjectType[object_type].value
        instance = object_model.access_by(info.context.request).get(id=id)
        instance.metadata = {
            key: value
            for key, value in (instance.metadata or {}).items()
            if key not in discarded_keys
        }
        instance.metadata.update(added_values)
        instance.save(update_fields=["metadata"])

        return MetadataMutation(id=id, metadata=instance.metadata)  # type:ignore


@strawberry.type
class DeleteMutation(utils.BaseMutation):
    id: str = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info,
        model,
        validator: typing.Callable = None,
        **input: inputs.DeleteMutationInput,
    ) -> "DeleteMutation":
        id = input.get("id")
        queryset = (
            model.access_by(info.context.request)
            if hasattr(model, "access_by")
            else model.objects
        )
        instance = queryset.get(id=id)

        if validator:
            validator(instance, context=info.context)

        # Get the shipment FK if it exists and is a direct relationship
        # (not a GenericRelation/RelatedManager)
        shipment = getattr(instance, "shipment", None)
        if shipment is not None and not isinstance(shipment, manager.Shipment):
            shipment = None

        instance.delete(keep_parents=True)

        if shipment is not None:
            manager_serializers.reset_related_shipment_rates(shipment)

        return DeleteMutation(id=id)  # type:ignore


@strawberry.type
class CreateRateSheetMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.CreateRateSheetMutationInput
    ) -> "CreateRateSheetMutation":
        data = input.copy()
        carriers = data.pop("carriers", [])
        zones_data = data.pop("zones", [])
        surcharges_data = data.pop("surcharges", [])
        service_rates_data = data.pop("service_rates", [])
        # Note: origin_countries stays in data - saved via serializer
        services_data = [
            (svc.copy() if isinstance(svc, dict) else dict(svc))
            for svc in data.get("services", [])
        ]

        slug = f"{input.get('name', '').lower()}_sheet".replace(" ", "").lower()
        serializer = serializers.RateSheetModelSerializer(
            data={**data, "slug": slug},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        rate_sheet = serializer.save()

        # Create services and build temp-to-real ID mapping
        if services_data:
            save_many_to_many_data(
                "services",
                serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )
            rate_sheet.refresh_from_db()

        temp_to_real_id = serializer.build_temp_to_real_service_map(services_data)

        # Link carriers
        if any(carriers):
            providers.CarrierConnection.access_by(info.context.request).filter(
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
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateRateSheetMutationInput
    ) -> "UpdateRateSheetMutation":
        instance = providers.RateSheet.access_by(info.context.request).get(
            id=input["id"]
        )
        data = input.copy()
        carriers = data.pop("carriers", [])
        # Note: origin_countries stays in data - saved via serializer

        serializer = serializers.RateSheetModelSerializer(
            instance,
            data=data,
            context=info.context.request,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        rate_sheet = serializer.save()

        # Handle services updates
        if "services" in data:
            save_many_to_many_data(
                "services",
                serializers.ServiceLevelModelSerializer,
                rate_sheet,
                payload=data,
                context=info.context.request,
            )

        # Link/unlink carriers
        if any(carriers):
            carrier_qs = providers.CarrierConnection.access_by(info.context.request).filter(
                carrier_code=rate_sheet.carrier_name
            )
            carrier_qs.filter(id__in=carriers).update(rate_sheet=rate_sheet)
            carrier_qs.filter(rate_sheet=rate_sheet).exclude(id__in=carriers).update(
                rate_sheet=None
            )

        return UpdateRateSheetMutation(
            rate_sheet=providers.RateSheet.objects.get(id=input["id"])
        )


@strawberry.type
class DeleteRateSheetServiceMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DeleteRateSheetServiceMutationInput
    ) -> "DeleteRateSheetServiceMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
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
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.AddSharedZoneMutationInput
    ) -> "AddSharedZoneMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        zone_data = input["zone"]
        zone_dict = {k: v for k, v in zone_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.add_zone(zone_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"zone": str(e)})

        return AddSharedZoneMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateSharedZoneMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateSharedZoneMutationInput
    ) -> "UpdateSharedZoneMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        zone_data = input["zone"]
        zone_dict = {k: v for k, v in zone_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.update_zone(input["zone_id"], zone_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"zone_id": str(e)})

        return UpdateSharedZoneMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteSharedZoneMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DeleteSharedZoneMutationInput
    ) -> "DeleteSharedZoneMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

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
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.AddSharedSurchargeMutationInput
    ) -> "AddSharedSurchargeMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        surcharge_data = input["surcharge"]
        surcharge_dict = {k: v for k, v in surcharge_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.add_surcharge(surcharge_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge": str(e)})

        return AddSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateSharedSurchargeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateSharedSurchargeMutationInput
    ) -> "UpdateSharedSurchargeMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        surcharge_data = input["surcharge"]
        surcharge_dict = {k: v for k, v in surcharge_data.items() if not utils.is_unset(v)}

        try:
            rate_sheet.update_surcharge(input["surcharge_id"], surcharge_dict)
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge_id": str(e)})

        return UpdateSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteSharedSurchargeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DeleteSharedSurchargeMutationInput
    ) -> "DeleteSharedSurchargeMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        try:
            rate_sheet.remove_surcharge(input["surcharge_id"])
        except ValueError as e:
            raise exceptions.ValidationError({"surcharge_id": str(e)})

        return DeleteSharedSurchargeMutation(rate_sheet=rate_sheet)


@strawberry.type
class BatchUpdateSurchargesMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.BatchUpdateSurchargesMutationInput
    ) -> "BatchUpdateSurchargesMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
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
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateServiceRateMutationInput
    ) -> "UpdateServiceRateMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        # Build the rate update dict from input fields
        rate_data = {}
        rate_fields = ["rate", "cost", "min_weight", "max_weight", "transit_days", "transit_time"]
        for field in rate_fields:
            if field in input and not utils.is_unset(input[field]):
                rate_data[field] = input[field]

        # Update or create the service-zone rate mapping
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
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.BatchUpdateServiceRatesMutationInput
    ) -> "BatchUpdateServiceRatesMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        # Convert rates to the format expected by batch_update_service_rates
        # Format: [{'service_id': str, 'zone_id': str, 'rate': float, 'cost': float, ...}]
        updates = []

        for rate in input["rates"]:
            rate_dict = {k: v for k, v in rate.items() if not utils.is_unset(v)}
            updates.append(rate_dict)

        try:
            rate_sheet.batch_update_service_rates(updates)
        except ValueError as e:
            raise exceptions.ValidationError({"rates": str(e)})

        return BatchUpdateServiceRatesMutation(rate_sheet=rate_sheet)


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE ZONE/SURCHARGE ASSIGNMENT MUTATIONS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class UpdateServiceZoneIdsMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateServiceZoneIdsMutationInput
    ) -> "UpdateServiceZoneIdsMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        service = rate_sheet.services.get(id=input["service_id"])

        service.zone_ids = input["zone_ids"]
        service.save(update_fields=["zone_ids"])

        return UpdateServiceZoneIdsMutation(rate_sheet=rate_sheet)


@strawberry.type
class UpdateServiceSurchargeIdsMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateServiceSurchargeIdsMutationInput
    ) -> "UpdateServiceSurchargeIdsMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )
        service = rate_sheet.services.get(id=input["service_id"])

        service.surcharge_ids = input["surcharge_ids"]
        service.save(update_fields=["surcharge_ids"])

        return UpdateServiceSurchargeIdsMutation(rate_sheet=rate_sheet)


@strawberry.type
class PartialShipmentMutation(utils.BaseMutation):
    shipment: typing.Optional[types.ShipmentType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.PartialShipmentMutationInput
    ) -> "PartialShipmentMutation":
        try:
            id = input["id"]
            shipment = manager.Shipment.access_by(info.context.request).get(id=id)
            manager_serializers.can_mutate_shipment(
                shipment, update=True, payload=input
            )

            manager_serializers.ShipmentSerializer.map(
                shipment,
                context=info.context.request,
                data=process_dictionaries_mutations(["options"], input, shipment),
            ).save()

            # refetch the shipment to get the updated state with signals processed
            update = manager.Shipment.access_by(info.context.request).get(id=id)

            return PartialShipmentMutation(errors=None, shipment=update)  # type:ignore
        except Exception as e:
            logger.exception(
                "Shipment mutation failed", shipment_id=input.get("id"), error=str(e)
            )
            raise e


@strawberry.type
class ChangeShipmentStatusMutation(utils.BaseMutation):
    shipment: typing.Optional[types.ShipmentType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.ChangeShipmentStatusMutationInput
    ) -> "ChangeShipmentStatusMutation":
        shipment = manager.Shipment.access_by(info.context.request).get(id=input["id"])

        if shipment.status in [
            utils.ShipmentStatusEnum.draft.name,
            utils.ShipmentStatusEnum.cancelled.name,
        ]:
            raise exceptions.ValidationError(
                _(f"{shipment.status} shipment cannot be changed to {input['status']}"),
                code="invalid_operation",
            )

        if getattr(shipment, "tracker", None) is not None:
            raise exceptions.ValidationError(
                _(f"this shipment is tracked automatically by API"),
                code="invalid_operation",
            )

        shipment.status = input["status"]
        shipment.save(update_fields=["status"])

        return ChangeShipmentStatusMutation(shipment=shipment)  # type:ignore


def _clear_default_address_templates(info, exclude_id=None):
    """Clear is_default flag on all address templates except the specified one."""
    queryset = manager.Address.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    )
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    for address in queryset:
        address.meta = {**(address.meta or {}), "is_default": False}
        address.save(update_fields=["meta"])


def _clear_default_parcel_templates(info, exclude_id=None):
    """Clear is_default flag on all parcel templates except the specified one."""
    queryset = manager.Parcel.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    )
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    for parcel in queryset:
        parcel.meta = {**(parcel.meta or {}), "is_default": False}
        parcel.save(update_fields=["meta"])


@strawberry.type
class CreateAddressMutation(utils.BaseMutation):
    """Create a saved address using Address model with meta.label."""

    address: typing.Optional[types.AddressTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "CreateAddressMutation":
        data = input.copy()

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        # If setting as default, clear existing default
        if meta.get("is_default"):
            _clear_default_address_templates(info)

        # Ensure is_default has a value
        if "is_default" not in meta:
            meta["is_default"] = False

        serializer = serializers.AddressModelSerializer(
            data={**data, "meta": meta},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        address = serializer.save()

        return CreateAddressMutation(address=address)  # type:ignore


@strawberry.type
class UpdateAddressMutation(utils.BaseMutation):
    """Update a saved address."""

    address: typing.Optional[types.AddressTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "UpdateAddressMutation":
        data = input.copy()
        id = data.pop("id")

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta_updates = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        instance = manager.Address.access_by(info.context.request).get(id=id)

        # Verify this is a template (has meta.label)
        if not (instance.meta or {}).get("label"):
            raise utils.ValidationError(
                "This address is not a template. Only templates can be updated here."
            )

        # Update meta field
        meta = {**(instance.meta or {}), **meta_updates}

        # If setting as default, clear existing default
        if meta_updates.get("is_default"):
            _clear_default_address_templates(info, exclude_id=id)

        serializer = serializers.AddressModelSerializer(
            instance,
            data={**data, "meta": meta},
            context=info.context.request,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        address = serializer.save()

        return UpdateAddressMutation(address=address)  # type:ignore


@strawberry.type
class CreateParcelMutation(utils.BaseMutation):
    """Create a saved parcel using Parcel model with meta.label."""

    parcel: typing.Optional[types.ParcelTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "CreateParcelMutation":
        data = input.copy()

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        # If setting as default, clear existing default
        if meta.get("is_default"):
            _clear_default_parcel_templates(info)

        # Ensure is_default has a value
        if "is_default" not in meta:
            meta["is_default"] = False

        serializer = serializers.ParcelModelSerializer(
            data={**data, "meta": meta},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        parcel = serializer.save()

        return CreateParcelMutation(parcel=parcel)  # type:ignore


@strawberry.type
class UpdateParcelMutation(utils.BaseMutation):
    """Update a saved parcel."""

    parcel: typing.Optional[types.ParcelTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "UpdateParcelMutation":
        data = input.copy()
        id = data.pop("id")

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta_updates = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        instance = manager.Parcel.access_by(info.context.request).get(id=id)

        # Verify this is a template (has meta.label)
        if not (instance.meta or {}).get("label"):
            raise utils.ValidationError(
                "This parcel is not a template. Only templates can be updated here."
            )

        # Update meta field
        meta = {**(instance.meta or {}), **meta_updates}

        # If setting as default, clear existing default
        if meta_updates.get("is_default"):
            _clear_default_parcel_templates(info, exclude_id=id)

        serializer = serializers.ParcelModelSerializer(
            instance,
            data={**data, "meta": meta},
            context=info.context.request,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        parcel = serializer.save()

        return UpdateParcelMutation(parcel=parcel)  # type:ignore


@strawberry.type
class DeleteAddressMutation(utils.BaseMutation):
    """Delete a saved address."""

    id: str = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, **input) -> "DeleteAddressMutation":
        id = input.get("id")
        instance = manager.Address.access_by(info.context.request).get(id=id)

        # Verify this is a saved address (has meta.label)
        if not (instance.meta or {}).get("label"):
            raise utils.ValidationError(
                "This address is not a saved address. Only saved addresses can be deleted here."
            )

        instance.delete(keep_parents=True)
        return DeleteAddressMutation(id=id)  # type:ignore


@strawberry.type
class DeleteParcelMutation(utils.BaseMutation):
    """Delete a saved parcel."""

    id: str = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, **input) -> "DeleteParcelMutation":
        id = input.get("id")
        instance = manager.Parcel.access_by(info.context.request).get(id=id)

        # Verify this is a saved parcel (has meta.label)
        if not (instance.meta or {}).get("label"):
            raise utils.ValidationError(
                "This parcel is not a saved parcel. Only saved parcels can be deleted here."
            )

        instance.delete(keep_parents=True)
        return DeleteParcelMutation(id=id)  # type:ignore


def _clear_default_product_templates(info, exclude_id=None):
    """Clear is_default flag on all product templates except the specified one."""
    queryset = manager.Commodity.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    )
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    for commodity in queryset:
        commodity.meta = {**(commodity.meta or {}), "is_default": False}
        commodity.save(update_fields=["meta"])


@strawberry.type
class CreateProductMutation(utils.BaseMutation):
    """Create a saved product using Commodity model with meta.label."""

    product: typing.Optional[types.ProductTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "CreateProductMutation":
        data = input.copy()

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        # If setting as default, clear existing default
        if meta.get("is_default"):
            _clear_default_product_templates(info)

        # Ensure is_default has a value
        if "is_default" not in meta:
            meta["is_default"] = False

        serializer = serializers.CommodityModelSerializer(
            data={**data, "meta": meta},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return CreateProductMutation(product=product)  # type:ignore


@strawberry.type
class UpdateProductMutation(utils.BaseMutation):
    """Update a saved product."""

    product: typing.Optional[types.ProductTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @transaction.atomic
    def mutate(info: Info, **input) -> "UpdateProductMutation":
        data = input.copy()
        id = data.pop("id")

        # Extract meta from input (flat structure)
        meta_input = data.pop("meta", {})
        meta_updates = {
            k: v
            for k, v in meta_input.items()
            if not utils.is_unset(v)
        }

        instance = manager.Commodity.access_by(info.context.request).get(id=id)

        # Verify this is a template (has meta.label)
        if not instance.is_template:
            raise utils.ValidationError(
                "This commodity is not a template. Only templates can be updated here."
            )

        # Update meta field
        meta = {**(instance.meta or {}), **meta_updates}

        # If setting as default, clear existing default
        if meta_updates.get("is_default"):
            _clear_default_product_templates(info, exclude_id=id)

        serializer = serializers.CommodityModelSerializer(
            instance,
            data={**data, "meta": meta},
            context=info.context.request,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return UpdateProductMutation(product=product)  # type:ignore


@strawberry.type
class CreateCarrierConnectionMutation(utils.BaseMutation):
    connection: types.CarrierConnectionType = None

    @staticmethod
    @utils.error_wrapper
    @utils.authentication_required
    def mutate(info: Info, **input) -> "CreateCarrierConnectionMutation":
        data = input.copy()

        connection = lib.identity(
            providers_serializers.CarrierConnectionModelSerializer.map(
                data=providers_serializers.CarrierConnectionData.map(data=data).data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return CreateCarrierConnectionMutation(  # type:ignore
            connection=connection
        )


@strawberry.type
class UpdateCarrierConnectionMutation(utils.BaseMutation):
    connection: types.CarrierConnectionType = None

    @staticmethod
    @utils.error_wrapper
    @utils.authentication_required
    def mutate(info: Info, **input) -> "UpdateCarrierConnectionMutation":
        data = input.copy()
        id = data.get("id")
        instance = providers.CarrierConnection.access_by(info.context.request).get(id=id)
        connection = lib.identity(
            providers_serializers.CarrierConnectionModelSerializer.map(
                instance,
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return UpdateCarrierConnectionMutation(  # type:ignore
            connection=connection
        )


@strawberry.type
class SystemCarrierMutation(utils.BaseMutation):
    carrier: typing.Optional[types.SystemConnectionType] = None

    @staticmethod
    @utils.error_wrapper
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.SystemCarrierMutationInput
    ) -> "SystemCarrierMutation":
        from karrio.server.providers.serializers import BrokeredConnectionModelSerializer

        pk = input.get("id")
        context = info.context.request
        system_connection = providers.SystemConnection.objects.get(pk=pk)

        # Build serializer data from input
        # Map 'config' to 'config_overrides' and 'enable' to 'is_enabled'
        data = {"system_connection_id": pk}

        if "enable" in input:
            data["is_enabled"] = input.get("enable")

        if "config" in input:
            data["config_overrides"] = input.get("config") or {}

        # Use the serializer to create or update the BrokeredConnection
        # The @owned_model_serializer decorator handles org linking automatically
        brokered = (
            BrokeredConnectionModelSerializer.map(
                data=data,
                context=context,
            )
            .save()
            .instance
        )

        return SystemCarrierMutation(
            carrier=system_connection
        )  # type: ignore


@strawberry.type
class CreateMetafieldMutation(utils.BaseMutation):
    metafield: typing.Optional[types.MetafieldType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.CreateMetafieldInput
    ) -> "CreateMetafieldMutation":
        data = input.copy()

        metafield = (
            serializers.MetafieldModelSerializer.map(
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return CreateMetafieldMutation(metafield=metafield)


@strawberry.type
class UpdateMetafieldMutation(utils.BaseMutation):
    metafield: typing.Optional[types.MetafieldType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.UpdateMetafieldInput
    ) -> "UpdateMetafieldMutation":
        data = input.copy()
        instance = core.Metafield.access_by(info.context.request).get(id=data.get("id"))

        metafield = (
            serializers.MetafieldModelSerializer.map(
                instance,
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return UpdateMetafieldMutation(metafield=metafield)
