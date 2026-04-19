import datetime
import typing

import karrio.server.data.filters as filters
import karrio.server.data.models as models
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.data.inputs as inputs
import karrio.server.graph.utils as utils
import strawberry
from strawberry.types import Info


@strawberry.type
class DataTemplateType:
    object_type: str
    id: str
    name: str
    slug: str
    fields_mapping: utils.JSON
    description: str | None
    resource_type: inputs.ResourceTypeEnum
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    created_by: base.UserType | None

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["DataTemplateType"]:
        return models.DataTemplate.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.DataTemplateFilter | None = strawberry.UNSET,
    ) -> utils.Connection["DataTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.DataTemplateFilter()
        queryset = filters.DataTemplateFilter(_filter.to_dict(), models.DataTemplate.access_by(info.context.request)).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class BatchObjectType:
    id: int
    status: inputs.ResourceTypeEnum | None


@strawberry.type
class BatchOperationType:
    object_type: str
    id: int
    resource_type: inputs.ResourceTypeEnum
    resources: list[BatchObjectType]
    status: inputs.BatchOperationStatusEnum
    test_mode: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType

    @staticmethod
    @utils.authentication_required
    def resolve(info: Info, id: str) -> typing.Optional["BatchOperationType"]:
        return models.BatchOperation.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: inputs.BatchOperationFilter | None = strawberry.UNSET,
    ) -> utils.Connection["BatchOperationType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.BatchOperationFilter()
        queryset = filters.BatchOperationFilter(
            _filter.to_dict(), models.BatchOperation.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
