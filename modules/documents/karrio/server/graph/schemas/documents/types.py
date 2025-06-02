import typing
import datetime
import strawberry

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.documents.inputs as inputs
import karrio.server.documents.models as models
import karrio.server.documents.filters as filters


@strawberry.type
class DocumentTemplateType:
    object_type: str
    preview_url: typing.Optional[str]
    id: str
    name: str
    slug: str
    template: str
    active: bool
    description: typing.Optional[str]
    related_object: typing.Optional[inputs.TemplateRelatedObjectEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[base.UserType]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["DocumentTemplateType"]:
        return models.DocumentTemplate.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.DocumentTemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["DocumentTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.DocumentTemplateFilter()
        queryset = filters.DocumentTemplateFilter(
            _filter.to_dict(), models.DocumentTemplate.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
