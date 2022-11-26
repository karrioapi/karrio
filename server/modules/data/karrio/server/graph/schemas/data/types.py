import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.schemas.data.inputs as inputs
import karrio.server.data.models as models
import karrio.server.data.filters as filters


@strawberry.type
class DataTemplateType:
    object_type: str
    id: str
    name: str
    slug: str
    fields_mapping: utils.JSON
    description: typing.Optional[str]
    resource_type: inputs.ResourceTypeEnum
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[base.UserType]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["DataTemplateType"]:
        return models.DataTemplate.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.DataTemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["DataTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.DataTemplateFilter()
        queryset = filters.DataTemplateFilter(
            _filter.to_dict(), models.DataTemplate.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class BatchObjectType:
    id: int
    status: typing.Optional[inputs.ResourceTypeEnum]


@strawberry.type
class BatchOperationType:
    object_type: str
    id: int
    resource_type: inputs.ResourceTypeEnum
    resources: typing.List[BatchObjectType]
    status: inputs.BatchOperationStatusEnum
    test_mode: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: base.UserType

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    def resolve(info, id: str) -> typing.Optional["BatchOperationType"]:
        return models.BatchOperation.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["DATA_IMPORT_EXPORT"])
    def resolve_list(
        info,
        filter: typing.Optional[inputs.BatchOperationFilter] = strawberry.UNSET,
    ) -> utils.Connection["BatchOperationType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.BatchOperationFilter()
        queryset = filters.BatchOperationFilter(
            _filter.to_dict(), models.BatchOperation.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())
