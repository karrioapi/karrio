import datetime
import typing

import karrio.server.documents.filters as filters
import karrio.server.documents.models as models
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.documents.inputs as inputs
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info


@strawberry.type
class DocumentTemplateType:
    object_type: str
    preview_url: str | None
    id: str
    name: str
    slug: str
    template: str
    active: bool
    description: str | None
    related_object: inputs.TemplateRelatedObjectEnum | None
    metadata: utils.JSON | None
    options: utils.JSON | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    created_by: base.UserType | None

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["DocumentTemplateType"]:
        return models.DocumentTemplate.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.DocumentTemplateFilter | None = strawberry.UNSET,
    ) -> utils.Connection["DocumentTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.DocumentTemplateFilter()
        queryset = filters.DocumentTemplateFilter(
            _filter.to_dict(), models.DocumentTemplate.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
