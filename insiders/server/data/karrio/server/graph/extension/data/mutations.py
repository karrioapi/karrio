import graphene
from graphene_django.types import ErrorType

import karrio.server.graph.utils as utils
import karrio.server.data.models as models
import karrio.server.data.serializers.data as serializers
import karrio.server.graph.extension.data.types as types


class CreateDataTemplate(utils.ClientMutation):
    template = graphene.Field(types.DataTemplateType)

    class Input:
        slug = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        resource_type = types.ResourceTypeEnum(required=True)
        fields_mapping = types.generic.GenericScalar()

    @classmethod
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, **data):
        serializer = serializers.DataTemplateModelSerializer(
            data=data,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(template=serializer.save())


class UpdateDataTemplate(utils.ClientMutation):
    template = graphene.Field(types.DataTemplateType)

    class Input:
        id = graphene.String(required=True)
        slug = graphene.String()
        name = graphene.String()
        description = graphene.String()
        resource_type = types.ResourceTypeEnum()
        fields_mapping = types.generic.GenericScalar()

    @classmethod
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, id, **data):
        instance = models.DataTemplate.access_by(info.context).get(id=id)

        serializer = serializers.DataTemplateModelSerializer(
            instance,
            data=serializers.process_dictionaries_mutations(
                ["fields_mapping"], data, instance
            ),
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(template=serializer.save())


class DeleteDataTemplate(utils.ClientMutation):
    id = graphene.String()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, id, **kwargs):
        template = models.DataTemplate.access_by(info.context).get(id=id)

        template.delete(keep_parents=True)

        return cls(id=id)
