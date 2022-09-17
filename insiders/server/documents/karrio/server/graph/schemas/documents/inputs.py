import typing
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.documents.serializers as serializers

TemplateRelatedObjectEnum: typing.Any = strawberry.enum(serializers.TemplateRelatedObject)


@strawberry.input
class CreateDocumentTemplateMutationInput(utils.BaseInput):
    slug: str
    name: str
    template: str
    related_object: TemplateRelatedObjectEnum
    active: typing.Optional[bool] = True
    description: typing.Optional[str] = None


@strawberry.input
class UpdateDocumentTemplateMutationInput(utils.BaseInput):
    id: str
    slug: typing.Optional[str] = None
    name: typing.Optional[str] = None
    template: typing.Optional[str] = None
    active: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    related_object: typing.Optional[TemplateRelatedObjectEnum] = None


@strawberry.input
class DocumentTemplateFilter(utils.Paginated):
    name: typing.Optional[str] = strawberry.UNSET
    related_object: typing.Optional[TemplateRelatedObjectEnum] = strawberry.UNSET
