import graphene
from graphene_django.rest_framework import mutation
from graphene_django.forms.mutation import DjangoFormMutation

from purplship.server.serializers import save_many_to_many_data, SerializerDecorator
from purplship.server.user.views import SignUpForm
from purplship.server.user.serializers import TokenSerializer, Token
from purplship.server.providers import models as providers
import purplship.server.graph.serializers as serializers
import purplship.server.graph.extension.base.types as types


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
        form_class = SignUpForm

    @classmethod
    def perform_mutate(cls, form, info):
        user = form.save()
        return cls(errors=[], user=user, **form.cleaned_data)


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
