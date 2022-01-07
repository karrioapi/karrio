import logging
import typing
import graphene
from graphene.types import generic
from graphene_django.types import ErrorType
from graphene_django.rest_framework import mutation
from graphene_django.forms.mutation import DjangoFormMutation
from django_email_verification import confirm as email_verification
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from purplship.server.serializers import save_many_to_many_data, SerializerDecorator
from purplship.server.user.serializers import TokenSerializer, Token
from purplship.server.providers import models as providers
from purplship.server.graph import models as graph
import purplship.server.graph.forms as forms
import purplship.server.graph.serializers as serializers
import purplship.server.graph.extension.base.types as types
import purplship.server.graph.extension.base.inputs as inputs

logger = logging.getLogger(__name__)


class SerializerMutation(mutation.SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    @types.login_required
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if "id" in input:
            instance = cls._meta.model_class.access_by(info.context).get(
                id=data.pop("id")
            )

            return {
                "instance": instance,
                "data": data,
                "partial": True,
                "context": info.context,
            }

        return {"data": data, "partial": False, "context": info.context}


class ClientMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    errors = graphene.List(
        ErrorType, description="May contain more than one error for same field."
    )


class CreateConnection(SerializerMutation):
    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.ConnectionModelSerializer


class UpdateConnection(SerializerMutation):
    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = serializers.PartialConnectionModelSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        kwargs = super().get_serializer_kwargs(root, info, **input)

        instance = kwargs.get("instance")
        settings_name = next(
            (k for k in kwargs.get("data", {}).keys() if "settings" in k), ""
        )
        settings_data = kwargs.get("data", {}).get(settings_name, {})

        if "services" in settings_data and instance is not None:
            services = settings_data.pop("services")
            settings = getattr(instance, "settings", None)
            extra = {"context": info.context}
            save_many_to_many_data(
                "services",
                serializers.ServiceLevelModelSerializer,
                settings,
                payload=dict(services=services),
                **extra,
            )

        return kwargs


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
        @types.login_required
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
                return cls(
                    template=None, errors=ErrorType.from_errors(serializer.errors)
                )

            template = (
                SerializerDecorator[serializers.TemplateModelSerializer](
                    instance, data=data, context=info.context
                )
                .save()
                .instance
            )
            serializers.ensure_unique_default_related_data(data, context=info.context)
            return cls(template=template)

    return type(_model.__name__, (_Mutation, ClientMutation), {})


class SystemCarrierMutation(ClientMutation):
    carrier = graphene.Field(types.SystemConnectionType)

    class Input:
        id = graphene.String(required=True)
        enable = graphene.Boolean(required=True)

    @classmethod
    @types.login_required
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


class TokenMutation(ClientMutation):
    token = graphene.Field(types.TokenType)

    class Input:
        refresh = graphene.Boolean()

    @classmethod
    @types.login_required
    def mutate_and_get_payload(cls, root, info, refresh: bool = None):
        tokens = Token.access_by(info.context)

        if refresh and any(tokens):
            tokens.delete()

        token = (
            SerializerDecorator[TokenSerializer](data={}, context=info.context)
            .save()
            .instance
        )

        return TokenMutation(token=token)


class UpdateUser(SerializerMutation):
    class Meta:
        model_operations = ("update",)
        serializer_class = serializers.UserModelSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **data):
        instance = cls._meta.model_class.objects.get(id=info.context.user.id)

        return {"instance": instance, "data": data, "partial": True}


class RegisterUser(DjangoFormMutation):
    user = graphene.Field(types.UserType)

    class Meta:
        form_class = forms.UserRegistrationForm

    @classmethod
    def perform_mutate(cls, form, info):
        user = form.save()
        return cls(errors=[], user=user, **form.cleaned_data)


class ConfirmEmail(ClientMutation):
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
    @types.login_required
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
            ValidationError,
        ):
            user = None
        return user


def create_delete_mutation(name: str, model, **filter):
    class _DeleteMutation:
        id = graphene.String()

        class Input:
            id = graphene.String(required=True)

        @classmethod
        @types.login_required
        def mutate_and_get_payload(cls, root, info, id: str = None):
            instance = model.access_by(info.context).get(id=id, **filter)
            instance.delete()

            return cls(id=id)

    return type(name, (_DeleteMutation, ClientMutation), {})


class MutateMetadata(ClientMutation):
    id = graphene.String()
    metadata = generic.GenericScalar()

    class Input:
        id = graphene.String(required=True)
        object_type = types.MetadataObjectTypeEnum(required=True)
        added_values = generic.GenericScalar(required=False)
        discarded_keys = graphene.List(graphene.String, required=False)

    @classmethod
    @types.login_required
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
