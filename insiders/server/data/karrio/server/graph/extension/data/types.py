import graphene
from graphene.types import generic

import karrio.server.graph.utils as utils
import karrio.server.data.models as models
import karrio.server.data.serializers as serializers

ResourceTypeEnum = graphene.Enum("ResourceTypeEnum", serializers.RESOURCE_TYPE)
BatchOperationStatusEnum = graphene.Enum(
    "BatchOperationStatusEnum", serializers.OPERATION_STATUS
)


class DataTemplateType(utils.BaseObjectType):
    resource_type = ResourceTypeEnum()
    fields_mapping = generic.GenericScalar()

    class Meta:
        model = models.DataTemplate
        exclude = ("org",)
        interfaces = (utils.CustomNode,)


class BatchObjectType(graphene.ObjectType):
    id = graphene.String(required=True)
    status = BatchOperationStatusEnum()


class BatchOperationType(utils.BaseObjectType):
    status = BatchOperationStatusEnum()
    resource_type = ResourceTypeEnum()
    resources = graphene.List(graphene.NonNull(BatchObjectType), default_value=[])

    class Meta:
        model = models.BatchOperation
        exclude = ("org",)
        interfaces = (utils.CustomNode,)
