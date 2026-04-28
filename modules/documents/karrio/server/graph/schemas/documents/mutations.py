import karrio.server.documents.models as models
import karrio.server.documents.serializers as serializers
import karrio.server.graph.schemas.documents.inputs as inputs
import karrio.server.graph.schemas.documents.types as types
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info


@strawberry.type
class CreateDocumentTemplateMutation(utils.BaseMutation):
    template: types.DocumentTemplateType | None = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, **input: inputs.CreateDocumentTemplateMutationInput) -> "CreateDocumentTemplateMutation":
        serializer = serializers.DocumentTemplateModelSerializer(
            data=input,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateDocumentTemplateMutation(template=serializer.save())  # type:ignore


@strawberry.type
class UpdateDocumentTemplateMutation(utils.BaseMutation):
    template: types.DocumentTemplateType | None = None

    @staticmethod
    @utils.authentication_required
    def mutate(info: Info, **input: inputs.UpdateDocumentTemplateMutationInput) -> "UpdateDocumentTemplateMutation":
        instance = models.DocumentTemplate.access_by(info.context.request).get(id=input["id"])

        serializer = serializers.DocumentTemplateModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateDocumentTemplateMutation(template=serializer.save())  # type:ignore
