import typing
import logging
import strawberry
from strawberry.types import Info
from rest_framework import exceptions
from django.utils.http import urlsafe_base64_decode
from django_email_verification import confirm as email_verification

from karrio.core.utils import DP
from karrio.server.serializers import SerializerDecorator
from karrio.server.core.utils import ConfirmationToken, send_email
from karrio.server.user.serializers import TokenSerializer, Token
from karrio.server.serializers.abstract import save_many_to_many_data
import karrio.server.manager.serializers as manager_serializers
import karrio.server.manager as manager
import karrio.server.providers.models as providers
import karrio.server.graph.models as graph
import karrio.server.graph.forms as forms
import karrio.server.graph.serializers as serializers
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.types as types
import karrio.server.graph.schemas.utils as utils

logger = logging.getLogger(__name__)


@strawberry.type
class ErrorType:
    field: str
    messages: typing.List[str]

    @staticmethod
    def from_errors(errors):
        return []


@strawberry.type
class BaseMutation:
    errors: typing.Optional[typing.List[ErrorType]] = None


@strawberry.type
class UserUpdateMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.login_required
    def mutate(info: Info, **input: inputs.UpdateUserInput) -> "UserUpdateMutation":
        instance = types.User.objects.get(id=info.context.request.user.id)

        serializer = serializers.UserModelSerializer(
            instance,
            partial=True,
            data=input,
            context=info.context.request,
        )

        if not serializer.is_valid():
            return UserUpdateMutation(errors=serializer.errors)  # type:ignore

        return UserUpdateMutation(user=serializer.save())  # type:ignore


@strawberry.type
class TokenMutation(BaseMutation):
    token: typing.Optional[types.TokenType] = None

    @staticmethod
    @utils.login_required
    def mutate(
        info: Info, refresh: bool = None, password: str = None
    ) -> "UserUpdateMutation":
        tokens = Token.access_by(info.context.request)

        if refresh:
            if len(password or "") == 0:
                raise exceptions.ValidationError(
                    {"password": "Password is required to refresh token"}
                )

            if not info.context.request.user.check_password(password):
                raise exceptions.ValidationError({"password": "Invalid password"})

            if any(tokens):
                tokens.delete()

        token = (
            SerializerDecorator[TokenSerializer](data={}, context=info.context.request)
            .save()
            .instance
        )

        return TokenMutation(token=token)  # type:ignore


@strawberry.type
class EmailChangeMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.login_required
    @utils.password_required
    def mutate(
        info: Info, email: str, password: str, redirect_url: str
    ) -> "EmailChangeMutation":
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

        return EmailChangeMutation(user=info.context.user.id)  # type:ignore


@strawberry.type
class ConfirmEmailChangeMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.login_required
    def mutate(info: Info, token: str) -> "ConfirmEmailChangeMutation":
        validated_token = ConfirmationToken(token)
        user = info.context.user

        if user.id != validated_token["user_id"]:
            raise exceptions.ValidationError({"token": "Token is invalid or expired"})

        if user.email == validated_token["new_email"]:
            raise exceptions.APIException("Email is already confirmed")

        user.email = validated_token["new_email"]
        user.save()

        return ConfirmEmailChangeMutation(
            user=types.User.objects.get(id=validated_token["user_id"])
        )  # type:ignore


@strawberry.type
class RegisterUserMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    def mutate(
        info: Info, **input: inputs.RegisterUserMutationInput
    ) -> "RegisterUserMutation":
        form = forms.UserRegistrationForm(**input)
        user = form.save()

        return RegisterUserMutation(user=user)  # type:ignore


@strawberry.type
class ConfirmEmailMutation(BaseMutation):
    success: bool = False

    @staticmethod
    def mutate(info: Info, token: str) -> "ConfirmEmailMutation":
        success, _ = email_verification.verify_token(token)

        return ConfirmEmailMutation(success=success)  # type:ignore


@strawberry.type
class ChangePasswordMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
    @utils.login_required
    def mutate(
        info: Info, **input: inputs.ChangePasswordMutationInput
    ) -> "ChangePasswordMutation":
        form = forms.PasswordChangeForm(**input, user=info.context.request.user)

        return ChangePasswordMutation(user=form.save())  # type:ignore


@strawberry.type
class ConfirmPasswordResetMutation(BaseMutation):
    user: typing.Optional[types.UserType] = None

    @staticmethod
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

    @staticmethod
    @utils.login_required
    def mutate(
        info: Info, **input: inputs.ConfirmPasswordResetMutationInput
    ) -> "ConfirmPasswordResetMutation":
        form = forms.ConfirmPasswordResetForm(**input, user=info.context.request.user)
        user = ConfirmPasswordResetMutation.get_user(input.get("uid"))  # type:ignore

        return ConfirmPasswordResetMutation(user=form.save())  # type:ignore


@strawberry.type
class MetadataMutation(BaseMutation):
    id: str = strawberry.UNSET
    metadata: inputs.JSON = strawberry.UNSET

    @staticmethod
    @utils.login_required
    def mutate(
        info: Info,
        id: str,
        object_type: typing.Any,
        added_values: dict = {},
        discarded_keys: list = [],
    ) -> "MetadataMutation":
        instance = object_type.access_by(info.context.request).get(id=id)
        instance.metadata = {
            key: value
            for key, value in (instance.metadata or {}).items()
            if key not in discarded_keys
        }
        instance.metadata.update(added_values)
        instance.save(update_fields=["metadata"])

        return MetadataMutation(id=id, metadata=instance.metadata)  # type:ignore


@strawberry.type
class PartialShipmentMutation(BaseMutation):
    shipment: typing.Optional[types.ShipmentType] = None

    @staticmethod
    @utils.login_required
    def mutate(
        info: Info, **input: inputs.PartialShipmentMutationInput
    ) -> "PartialShipmentMutation":
        shipment = manager.Shipment.access_by(info.context).get(id=id)
        manager_serializers.can_mutate_shipment(shipment, update=True)

        serializer = manager_serializers.Shipment(shipment, data=input, partial=True)

        if not serializer.is_valid():
            return PartialShipmentMutation(  # type:ignore
                errors=ErrorType.from_errors(serializer.errors)
            )

        SerializerDecorator[manager_serializers.ShipmentSerializer](
            shipment,
            context=info.context,
            data=DP.to_dict(serializer.validated_data),
        ).save()

        # refetch the shipment to get the updated state with signals processed
        update = manager.Shipment.access_by(info.context).get(id=id)

        return PartialShipmentMutation(errors=None, shipment=update)  # type:ignore


def create_template_mutation(
    name: str, template_type: str, is_update: bool = False
) -> typing.Type:
    _type: typing.Any = dict(
        address=types.AddressTemplateType,
        customs=types.CustomsTemplateType,
        parcel=types.ParcelTemplateType,
    ).get(template_type)

    @strawberry.type
    class _Mutation(BaseMutation):
        template: _type = None

        @staticmethod
        @utils.login_required
        def mutate(info: Info, **input) -> name:  # type:ignore
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
                return _Mutation(
                    errors=ErrorType.from_errors(serializer.errors)
                )  # type:ignore

            template = serializer.save()

            return _Mutation(template=template)  # type:ignore

    return strawberry.type(type(name, (_Mutation,), {}))


CreateAddressTemplateMutation = create_template_mutation(
    "CreateAddressTemplateMutation", "address"
)
UpdateAddressTemplateMutation = create_template_mutation(
    "UpdateAddressTemplateMutation",
    "address",
)
CreateCustomsTemplateMutation = create_template_mutation(
    "CreateCustomsTemplateMutation", "customs"
)
UpdateCustomsTemplateMutation = create_template_mutation(
    "UpdateCustomsTemplateMutation", "customs"
)
CreateParcelTemplateMutation = create_template_mutation(
    "CreateParcelTemplateMutation", "parcel"
)
UpdateParcelTemplateMutation = create_template_mutation(
    "UpdateParcelTemplateMutation", "parcel"
)


@strawberry.type
class CreateCarrierConnectionMutation(BaseMutation):
    connection: typing.Optional[types.ConnectionType] = None

    @staticmethod
    @utils.login_required
    def mutate(info: Info, **input) -> "CreateCarrierConnectionMutation":
        data = input.copy()

        serializer = serializers.ConnectionModelSerializer(
            data=data,
            context=info.context.request,
        )

        if not serializer.is_valid():
            return CreateCarrierConnectionMutation(  # type:ignore
                errors=ErrorType.from_errors(serializer.errors)
            )

        connection = serializer.save()

        return CreateCarrierConnectionMutation(connection=connection)  # type:ignore


@strawberry.type
class UpdateCarrierConnectionMutation(BaseMutation):
    connection: typing.Optional[types.ConnectionType] = None

    @staticmethod
    @utils.login_required
    def mutate(info: Info, **input) -> "UpdateCarrierConnectionMutation":
        data = input.copy()
        instance = providers.Carrier.access_by(info.context.request).get(id=id)
        serializer = serializers.PartialConnectionModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid(raise_exception=True):
            return UpdateCarrierConnectionMutation(  # type:ignore
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

        connection = serializer.save()

        return UpdateCarrierConnectionMutation(connection=connection)  # type:ignore
