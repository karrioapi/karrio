import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.documents.mutations as mutations
import karrio.server.graph.schemas.documents.inputs as inputs
import karrio.server.graph.schemas.documents.types as types
import karrio.server.documents.models as models

extra_types: list = []


@strawberry.type
class Query:
    document_template: types.DocumentTemplateType = strawberry.field(
        resolver=types.DocumentTemplateType.resolve
    )
    document_templates: utils.Connection[types.DocumentTemplateType] = strawberry.field(
        resolver=types.DocumentTemplateType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_document_template(
        self, info: Info, input: inputs.CreateDocumentTemplateMutationInput
    ) -> mutations.CreateDocumentTemplateMutation:
        return mutations.CreateDocumentTemplateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_document_template(
        self, info: Info, input: inputs.UpdateDocumentTemplateMutationInput
    ) -> mutations.UpdateDocumentTemplateMutation:
        return mutations.UpdateDocumentTemplateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_document_template(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info,
            model=models.DocumentTemplate,
            **input.to_dict()
        )
