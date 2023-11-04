import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.documents.types as types
import karrio.server.graph.schemas.documents.inputs as inputs
import karrio.server.documents.serializers as serializers
import karrio.server.documents.models as models


@strawberry.type
class CreateDocumentTemplateMutation(utils.BaseMutation):
    template: typing.Optional[types.DocumentTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DOCUMENTS_MANAGEMENT", "manage_data"])
    def mutate(
        info: Info, **input: inputs.CreateDocumentTemplateMutationInput
    ) -> "CreateDocumentTemplateMutation":
        serializer = serializers.DocumentTemplateModelSerializer(
            data=input,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateDocumentTemplateMutation(template=serializer.save())  # type:ignore


@strawberry.type
class UpdateDocumentTemplateMutation(utils.BaseMutation):
    template: typing.Optional[types.DocumentTemplateType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DOCUMENTS_MANAGEMENT", "manage_data"])
    def mutate(
        info: Info, **input: inputs.UpdateDocumentTemplateMutationInput
    ) -> "UpdateDocumentTemplateMutation":
        instance = models.DocumentTemplate.access_by(info.context.request).get(id=input["id"])

        serializer = serializers.DocumentTemplateModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateDocumentTemplateMutation(template=serializer.save())  # type:ignore
