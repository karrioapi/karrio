import logging
import typing
import graphene
from graphene.types import generic
from graphene_django.types import ErrorType
from graphene_django.forms.mutation import DjangoFormMutation
from django_email_verification import confirm as email_verification
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions

from karrio.core.utils import DP
from karrio.server.conf import settings
from karrio.server.core.utils import ConfirmationToken, send_email
from karrio.server.serializers import save_many_to_many_data, SerializerDecorator
from karrio.server.user.serializers import TokenSerializer, Token
import karrio.server.manager.serializers as manager_serializers
import karrio.server.graph.forms as forms
import karrio.server.graph.models as graph
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.graph.serializers as serializers
import karrio.server.graph.extension.base.types as types
import karrio.server.graph.extension.base.inputs as inputs
import karrio.server.graph.utils as utils

logger = logging.getLogger(__name__)


def create_template_mutation(template: str, update: bool = False):
    _type = getattr(types, f"{template}TemplateType")
    _model = getattr(
        inputs,
        f"Update{template}TemplateInput"
        if update
        else f"Create{template}TemplateInput",
    )
    _Base = type(
        "Base",
        (),
        {
            "id": (graphene.String(required=True) if update else None),
            f"{template.lower()}": graphene.Field(_model, required=not update),
        },
    )

    class _Mutation:
        template = graphene.Field(_type)

        class Input(_Base):
            label = graphene.String(required=not update)
            is_default = graphene.Boolean(default=False)

        @classmethod
        @utils.login_required
        def mutate_and_get_payload(cls, root, info, **input):
            data = input.copy()
            instance = (
                graph.Template.access_by(info.context).get(id=input["id"])
                if "id" in input
                else None
            )
            customs_data = data.get("customs", {})

            if "commodities" in customs_data and instance is not None:
                customs = getattr(instance, "customs", None)
                extra = {"context": info.context}
                save_many_to_many_data(
                    "commodities",
                    serializers.CommodityModelSerializer,
                    customs,
                    payload=customs_data,
                    **extra,
                )

            serializer = serializers.TemplateModelSerializer(
                instance,
                data=data,
                context=info.context,
                partial=(instance is not None),
            )

            if not serializer.is_valid():
                return cls(errors=ErrorType.from_errors(serializer.errors))

            template = serializer.save()

            return cls(template=template)

    return type(_model.__name__, (_Mutation, utils.ClientMutation), {})


class SystemCarrierMutation(utils.ClientMutation):
    carrier = graphene.Field(types.SystemConnectionType)

    class Input:
        id = graphene.String(required=True)
        enable = graphene.Boolean(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id: str, enable: bool):
        carrier = providers.Carrier.objects.get(id=id, created_by=None)

        if enable:
            if hasattr(carrier, "active_orgs"):
                carrier.active_orgs.add(info.context.org)
            else:
                carrier.active_users.add(info.context.user)
        else:
            if hasattr(carrier, "active_orgs"):
                carrier.active_orgs.remove(info.context.org)
            else:
                carrier.active_users.remove(info.context.user)

        return SystemCarrierMutation(carrier=carrier)


class TokenMutation(utils.ClientMutation):
    token = graphene.Field(types.TokenType)

    class Input:
        refresh = graphene.Boolean()
        password = graphene.String(help_text="Password required when refresh is True")

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(
        cls, root, info, refresh: bool = None, password: str = None
    ):
        tokens = Token.access_by(info.context)

        if refresh:
            if len(password or "") == 0:
                raise exceptions.ValidationError(
                    {"password": "Password is required to refresh token"}
                )

            if not info.context.user.check_password(password):
                raise exceptions.ValidationError({"password": "Invalid password"})

            if any(tokens):
                tokens.delete()

        token = (
            SerializerDecorator[TokenSerializer](data={}, context=info.context)
            .save()
            .instance
        )

        return TokenMutation(token=token)


class UpdateUser(utils.ClientMutation):
    user = graphene.Field(types.UserType)

    class Input:
        full_name = graphene.String()
        is_active = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **data):
        instance = types.User.objects.get(id=info.context.user.id)

        serializer = serializers.UserModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(user=serializer.save())


class RequestEmailChange(utils.ClientMutation):
    user = graphene.Field(types.UserType)

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        redirect_url = graphene.String(required=True)

    @classmethod
    @utils.login_required
    @utils.password_required
    def mutate_and_get_payload(
        cls, root, info, email, password, redirect_url, **kwargs
    ):
        try:
            token = ConfirmationToken.for_data(
                user=info.context.user,
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
            )
        except Exception as e:
            logger.exception(e)
            raise e

        return cls(user=info.context.user.id)


class ConfirmEmailChange(utils.ClientMutation):
    user = graphene.Field(types.UserType)

    class Input:
        token = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, token, **kwargs):
        validated_token = ConfirmationToken(token)
        user = info.context.user

        if user.id != validated_token["user_id"]:
            raise exceptions.ValidationError({"token": "Token is invalid or expired"})

        if user.email == validated_token["new_email"]:
            raise exceptions.APIException("Email is already confirmed")

        user.email = validated_token["new_email"]
        user.save()

        return cls(user=types.User.objects.get(id=validated_token["user_id"]))


class RegisterUser(DjangoFormMutation):
    user = graphene.Field(types.UserType)

    class Meta:
        form_class = forms.UserRegistrationForm

    @classmethod
    def perform_mutate(cls, form, info):
        if not settings.ALLOW_SIGNUP:
            raise Exception(
                "Signup is not allowed. "
                "Please contact your administrator to create an account."
            )

        user = form.save()
        return cls(errors=[], user=user, **form.cleaned_data)


class ConfirmEmail(utils.ClientMutation):
    success = graphene.Boolean(required=True)

    class Input:
        token = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, token: str = None):
        success, _ = email_verification.verify_token(token)
        return cls(success=success)


class ChangePassword(DjangoFormMutation):
    class Meta:
        form_class = forms.PasswordChangeForm

    @classmethod
    @utils.login_required
    def perform_mutate(cls, form, info):
        return super().perform_mutate(form, info)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super().get_form_kwargs(root, info, **input)
        kwargs.update(user=info.context.user)
        return kwargs


class RequestPasswordReset(DjangoFormMutation):
    class Meta:
        form_class = forms.ResetPasswordRequestForm

    @classmethod
    def perform_mutate(cls, form, info):
        form.save(request=info.context)
        return cls(errors=[], **form.cleaned_data)


class ConfirmPasswordReset(DjangoFormMutation):
    class Meta:
        form_class = forms.ConfirmPasswordResetForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super().get_form_kwargs(root, info, **input)
        user = cls.get_user(input.get("uid"))
        kwargs.update(user=user)

        return kwargs

    @classmethod
    def get_user(cls, uidb64):
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


class MutateMetadata(utils.ClientMutation):
    id = graphene.String()
    metadata = generic.GenericScalar()

    class Input:
        id = graphene.String(required=True)
        object_type = utils.MetadataObjectTypeEnum(required=True)
        added_values = generic.GenericScalar(required=False)
        discarded_keys = graphene.List(graphene.String, required=False)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(
        cls,
        root,
        info,
        id: str,
        object_type: typing.Any,
        added_values: dict = {},
        discarded_keys: list = [],
    ):
        instance = object_type.access_by(info.context).get(id=id)
        instance.metadata = {
            key: value
            for key, value in (instance.metadata or {}).items()
            if key not in discarded_keys
        }
        instance.metadata.update(added_values)
        instance.save(update_fields=["metadata"])

        return cls(id=id, errors=None, metadata=instance.metadata)


class PartialShipmentUpdate(utils.ClientMutation):
    shipment = graphene.Field(types.ShipmentType)

    class Input:
        id = graphene.String(required=True)
        recipient = graphene.Field(inputs.UpdateAddressInput, required=False)
        shipper = graphene.Field(inputs.UpdateAddressInput, required=False)
        customs = graphene.Field(inputs.UpdateCustomsInput, required=False)
        parcels = graphene.List(inputs.UpdateParcelInput, required=False)
        payment = graphene.Field(inputs.PaymentInput, required=False)
        options = generic.GenericScalar(required=False)
        reference = graphene.String(required=False)
        metadata = generic.GenericScalar(required=False)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id: str, **inputs):
        shipment = manager.Shipment.access_by(info.context).get(id=id)
        manager_serializers.can_mutate_shipment(shipment, update=True)

        serializer = manager_serializers.Shipment(shipment, data=inputs, partial=True)

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        SerializerDecorator[manager_serializers.ShipmentSerializer](
            shipment,
            context=info.context,
            data=DP.to_dict(serializer.validated_data),
        ).save()

        # refetch the shipment to get the updated state with signals processed
        update = manager.Shipment.access_by(info.context).get(id=id)

        return cls(errors=None, shipment=update)


class _CreateCarrierConnection:
    class Input(inputs.CreateConnectionInput):
        pass

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, **input):
        data = input.copy()

        serializer = serializers.ConnectionModelSerializer(
            data=data,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        carrier = serializer.save()

        return cls(**{carrier.settings.__class__.__name__.lower(): carrier.settings})


CreateCarrierConnection = type(
    "CreateConnection",
    (_CreateCarrierConnection, utils.ClientMutation),
    {name: graphene.Field(type) for name, type in types.CarrierSettings.items()},
)


class _UpdateCarrierConnection:
    class Input(inputs.UpdateConnectionInput):
        id = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id: str, **data):
        instance = providers.Carrier.access_by(info.context).get(id=id)
        serializer = serializers.PartialConnectionModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return UpdateCarrierConnection(
                errors=ErrorType.from_errors(serializer.errors)
            )

        settings_name: str = next((k for k in data.keys()))
        settings_data = data.get(settings_name, {})

        if "services" in settings_data:
            save_many_to_many_data(
                "services",
                serializers.ServiceLevelModelSerializer,
                instance.settings,
                payload=settings_data,
                context=info.context,
            )

        carrier = serializer.save()

        return cls(**{carrier.settings.__class__.__name__.lower(): carrier.settings})


UpdateCarrierConnection = type(
    "UpdateConnection",
    (_UpdateCarrierConnection, utils.ClientMutation),
    {name: graphene.Field(type) for name, type in types.CarrierSettings.items()},
)
