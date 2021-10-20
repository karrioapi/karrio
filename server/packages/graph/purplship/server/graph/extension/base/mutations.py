import logging
import graphene
from graphene_django.rest_framework import mutation
from graphene_django.forms.mutation import DjangoFormMutation
from django_email_verification import confirm as email_verification
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from purplship.server.serializers import save_many_to_many_data, SerializerDecorator
from purplship.server.user.serializers import TokenSerializer, Token
from purplship.server.providers import models as providers
import purplship.server.graph.forms as forms
import purplship.server.graph.serializers as serializers
import purplship.server.graph.extension.base.types as types

logger = logging.getLogger(__name__)


class SerializerMutation(mutation.SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    @types.login_required
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if 'id' in input:
            instance = cls._meta.model_class.access_by(info.context).get(id=data.pop('id'))

            return {'instance': instance, 'data': data, 'partial': True, 'context': info.context}

        return {'data': data, 'partial': False, 'context': info.context}


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


class CreateTemplate(SerializerMutation):

    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.make_fields_optional(serializers.TemplateModelSerializer)


class UpdateTemplate(SerializerMutation):

    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = serializers.make_fields_optional(serializers.TemplateModelSerializer)

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        kwargs = super().get_serializer_kwargs(root, info, **input)

        instance = kwargs.get('instance')
        customs_data = kwargs.get('data', {}).get('customs', {})

        if 'commodities' in customs_data and instance is not None:
            customs = getattr(instance, 'customs', None)
            extra = {'context': info.context}
            save_many_to_many_data(
                'commodities', serializers.CommodityModelSerializer, customs, payload=customs_data, **extra)

        return kwargs


class SystemCarrierMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.String(required=True)
        enable = graphene.Boolean(required=True)

    carrier = graphene.Field(types.SystemConnectionType)

    @classmethod
    @types.login_required
    def mutate_and_get_payload(cls, root, info, id: str, enable: bool):
        carrier = providers.Carrier.objects.get(id=id, created_by=None)

        if enable:
            if hasattr(carrier, 'active_orgs'):
                carrier.active_orgs.add(info.context.org)
            else:
                carrier.active_users.add(info.context.user)
        else:
            if hasattr(carrier, 'active_orgs'):
                carrier.active_orgs.remove(info.context.org)
            else:
                carrier.active_users.remove(info.context.user)

        return SystemCarrierMutation(carrier=carrier)


class TokenMutation(graphene.relay.ClientIDMutation):
    class Input:
        refresh = graphene.Boolean()

    token = graphene.Field(types.TokenType)

    @classmethod
    @types.login_required
    def mutate_and_get_payload(cls, root, info, refresh: bool = None):
        tokens = Token.access_by(info.context)

        if refresh and any(tokens):
            tokens.delete()

        token = SerializerDecorator[TokenSerializer](data={}, context=info.context).save().instance

        return TokenMutation(token=token)


class UpdateUser(SerializerMutation):

    class Meta:
        model_operations = ("update",)
        serializer_class = serializers.UserModelSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **data):
        instance = cls._meta.model_class.objects.get(id=info.context.user.id)

        return {'instance': instance, 'data': data, 'partial': True}


class RegisterUser(DjangoFormMutation):
    user = graphene.Field(types.UserType)

    class Meta:
        form_class = forms.UserRegistrationForm

    @classmethod
    def perform_mutate(cls, form, info):
        user = form.save()
        return cls(errors=[], user=user, **form.cleaned_data)


class ConfirmEmail(graphene.relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)

    success = graphene.Boolean(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, token: str = None):
        try:
            success, _ = email_verification.verify_token(token)
            return cls(success=success)
        except Exception as e:
            logger.exception(e)
            raise e


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
        user = cls.get_user(input.get('uid'))
        kwargs.update(user=user)

        return kwargs

    @classmethod
    def get_user(cls, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = types.User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, types.User.DoesNotExist, ValidationError):
            user = None
        return user


def create_delete_mutation(name: str, model, **filter):
    class DeleteItem:
        class Input:
            id = graphene.String(required=True)

        id = graphene.String()

        @classmethod
        @types.login_required
        def mutate_and_get_payload(cls, root, info, id: str = None):
            instance = model.access_by(info.context).get(id=id, **filter)
            instance.delete()

            return cls(id=id)

    return type(name, (DeleteItem, graphene.relay.ClientIDMutation), {})
