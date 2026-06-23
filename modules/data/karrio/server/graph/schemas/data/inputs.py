import typing

import karrio.server.data.serializers as serializers
import karrio.server.graph.utils as utils
import strawberry

ResourceTypeEnum: typing.Any = strawberry.enum(serializers.ResourceStatus)
BatchOperationStatusEnum: typing.Any = strawberry.enum(serializers.BatchOperationStatus)


@strawberry.input
class CreateDataTemplateMutationInput(utils.BaseInput):
    slug: str
    name: str
    fields_mapping: utils.JSON
    resource_type: ResourceTypeEnum


@strawberry.input
class DataTemplateFilter(utils.Paginated):
    name: str | None = strawberry.UNSET
    slug: str | None = strawberry.UNSET
    resource_type: list[ResourceTypeEnum] = strawberry.UNSET


@strawberry.input
class UpdateDataTemplateMutationInput(utils.BaseInput):
    id: str
    slug: str | None = strawberry.UNSET
    name: str | None = strawberry.UNSET
    fields_mapping: utils.JSON | None = strawberry.UNSET
    resource_type: ResourceTypeEnum | None = strawberry.UNSET


@strawberry.input
class BatchOperationFilter(utils.Paginated):
    resource_type: list[ResourceTypeEnum] | None = strawberry.UNSET
    status: list[BatchOperationStatusEnum] | None = strawberry.UNSET
