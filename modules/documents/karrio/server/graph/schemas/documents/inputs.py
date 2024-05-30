import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.documents.serializers as serializers

TemplateRelatedObjectEnum: typing.Any = strawberry.enum(
    serializers.TemplateRelatedObject
)


@strawberry.input
class CreateDocumentTemplateMutationInput(utils.BaseInput):
    slug: str
    name: str
    template: str
    active: typing.Optional[bool] = True
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    related_object: typing.Optional[TemplateRelatedObjectEnum] = strawberry.UNSET


@strawberry.input
class UpdateDocumentTemplateMutationInput(utils.BaseInput):
    id: str
    slug: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    template: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    related_object: typing.Optional[TemplateRelatedObjectEnum] = strawberry.UNSET


@strawberry.input
class DocumentTemplateFilter(utils.Paginated):
    name: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET
    related_object: typing.Optional[TemplateRelatedObjectEnum] = strawberry.UNSET
