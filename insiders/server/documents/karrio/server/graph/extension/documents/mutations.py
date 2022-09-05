import graphene
from graphene_django.types import ErrorType

import karrio.server.graph.utils as utils
import karrio.server.documents.models as models
import karrio.server.documents.serializers as serializers
import karrio.server.graph.extension.documents.types as types


class CreateDocumentTemplate(utils.ClientMutation):
    template = graphene.Field(types.DocumentTemplateType)

    class Input:
        slug = graphene.String(required=True)
        name = graphene.String(required=True)
        template = graphene.String(required=True)
        description = graphene.String()
        related_object = types.TemplateRelatedObject(required=True)
        active = graphene.Boolean(default_value=True)

    @classmethod
    @utils.authorization_required(["DOCUMENTS_MANAGEMENT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, **data):
        serializer = serializers.DocumentTemplateModelSerializer(
            data=data,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(template=serializer.save())


class UpdateDocumentTemplate(utils.ClientMutation):
    template = graphene.Field(types.DocumentTemplateType)

    class Input:
        id = graphene.String(required=True)
        slug = graphene.String()
        name = graphene.String()
        template = graphene.String()
        description = graphene.String()
        related_object = types.TemplateRelatedObject()
        active = graphene.Boolean()

    @classmethod
    @utils.authorization_required(["DOCUMENTS_MANAGEMENT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, id, **data):
        instance = models.DocumentTemplate.access_by(info.context).get(id=id)

        serializer = serializers.DocumentTemplateModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(template=serializer.save())


class DeleteDocumentTemplate(utils.ClientMutation):
    id = graphene.String()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    @utils.authorization_required(["DOCUMENTS_MANAGEMENT"])
    @utils.authentication_required
    def mutate_and_get_payload(cls, root, info, id, **kwargs):
        template = models.DocumentTemplate.access_by(info.context).get(id=id)

        template.delete(keep_parents=True)

        return cls(id=id)
