import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.data.serializers as serializers

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
    name: typing.Optional[str] = strawberry.UNSET
    slug: typing.Optional[str] = strawberry.UNSET
    resource_type: typing.List[ResourceTypeEnum] = strawberry.UNSET


@strawberry.input
class UpdateDataTemplateMutationInput(utils.BaseInput):
    id: str
    slug: typing.Optional[str] = strawberry.UNSET
    name: typing.Optional[str] = strawberry.UNSET
    fields_mapping: typing.Optional[utils.JSON] = strawberry.UNSET
    resource_type: typing.Optional[ResourceTypeEnum] = strawberry.UNSET


@strawberry.input
class BatchOperationFilter(utils.Paginated):
    resource_type: typing.Optional[typing.List[ResourceTypeEnum]] = strawberry.UNSET
    status: typing.Optional[typing.List[BatchOperationStatusEnum]] = strawberry.UNSET
