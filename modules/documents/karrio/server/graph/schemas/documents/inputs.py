import typing

import karrio.server.documents.serializers as serializers
import karrio.server.graph.utils as utils
import strawberry

TemplateRelatedObjectEnum: typing.Any = strawberry.enum(serializers.TemplateRelatedObject)


@strawberry.input
class CreateDocumentTemplateMutationInput(utils.BaseInput):
    slug: str
    name: str
    template: str
    active: bool | None = True
    description: str | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    related_object: TemplateRelatedObjectEnum | None = strawberry.UNSET
    options: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateDocumentTemplateMutationInput(utils.BaseInput):
    id: str
    slug: str | None = strawberry.UNSET
    name: str | None = strawberry.UNSET
    template: str | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    related_object: TemplateRelatedObjectEnum | None = strawberry.UNSET
    options: utils.JSON | None = strawberry.UNSET


@strawberry.input
class DocumentTemplateFilter(utils.Paginated):
    name: str | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET
    related_object: TemplateRelatedObjectEnum | None = strawberry.UNSET
