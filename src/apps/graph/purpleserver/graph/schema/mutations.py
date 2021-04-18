import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from rest_framework.authtoken.models import Token

from purpleserver.core.utils import save_many_to_many_data
import purpleserver.graph.serializers as serializers
import purpleserver.graph.schema.types as types


class _SerializerMutation(SerializerMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        data = input.copy()

        if 'id' in input:
            model = cls._meta.model_class
            instance = model.objects.get(id=data.pop('id'), created_by_id=info.context.user.id)

            return {'instance': instance, 'data': data, 'partial': True, 'created_by': info.context.user}

        return {'data': data, 'partial': False, 'created_by': info.context.user}


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
            extra = {'partial': True, 'created_by': info.context.user}
            save_many_to_many_data(
                'commodities', serializers.CommodityModelSerializer, customs, payload=customs_data, **extra)

        return kwargs


class TokenMutation(graphene.relay.ClientIDMutation):
    class Input:
        refresh = graphene.Boolean()

    token = graphene.Field(types.TokenType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, refresh: bool = None):
        user = types.User.objects.get(id=info.context.user.id)

        if refresh and user.auth_token is not None:
            user.auth_token.delete()
            user.save()

        token, created = Token.objects.get_or_create(user=user)

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
            instance = model.objects.access_with(info.context.user).get(id=id, **filter)
            instance.delete()

            return cls(id=id)

    return type(name, (DeleteItem, graphene.relay.ClientIDMutation), {})
