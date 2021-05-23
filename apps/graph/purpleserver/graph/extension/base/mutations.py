import pydoc
import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from django.conf import settings

from purpleserver.serializers import save_many_to_many_data, SerializerDecorator
from purpleserver.user.serializers import TokenSerializer, Token
import purpleserver.graph.serializers as serializers
import purpleserver.graph.extension.base.types as types


class _SerializerMutation(SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if 'id' in input:
            instance = cls._meta.model_class.access_by(info.context).get(id=data.pop('id'))

            return {'instance': instance, 'data': data, 'partial': True, 'context': info.context}

        return {'data': data, 'partial': False, 'context': info.context}


class CreateConnection(_SerializerMutation):

    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.ConnectionModelSerializer


class UpdateConnection(_SerializerMutation):

    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = serializers.PartialConnectionModelSerializer


class CreateTemplate(_SerializerMutation):

    class Meta:
        model_operations = ("create",)
        convert_choices_to_enum = False
        serializer_class = serializers.apply_optional_fields(serializers.TemplateModelSerializer)


class UpdateTemplate(_SerializerMutation):

    class Meta:
        model_operations = ("update",)
        convert_choices_to_enum = False
        serializer_class = serializers.apply_optional_fields(serializers.TemplateModelSerializer)

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


class TokenMutation(graphene.relay.ClientIDMutation):
    class Input:
        refresh = graphene.Boolean()

    token = graphene.Field(types.TokenType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, refresh: bool = None):
        tokens = Token.access_by(info.context)

        if refresh and any(tokens):
            tokens.delete()

        token = SerializerDecorator[TokenSerializer](data={}, context=info.context).save().instance

        return TokenMutation(token=token)


class UserMutation(SerializerMutation):

    class Meta:
        model_operations = ("update",)
        serializer_class = serializers.UserModelSerializer

    @classmethod
    def get_serializer_kwargs(cls, root, info, **data):
        instance = cls._meta.model_class.objects.get(id=info.context.user.id)

        return {'instance': instance, 'data': data, 'partial': True}


def create_delete_mutation(name: str, model, **filter):
    class DeleteItem:
        class Input:
            id = graphene.String(required=True)

        id = graphene.String()

        @classmethod
        def mutate_and_get_payload(cls, root, info, id):
            instance = model.access_by(info.context).get(id=id, **filter)
            instance.delete()

            return cls(id=id)

    return type(name, (DeleteItem, graphene.relay.ClientIDMutation), {})
