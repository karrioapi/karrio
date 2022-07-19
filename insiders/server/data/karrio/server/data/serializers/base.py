from enum import Enum
from rest_framework import fields
from karrio.server.core import serializers


class ResourceType(Enum):
    order = "order"
    shipment = "shipment"
    tracking = "tracking"
    billing = "billing"

    @classmethod
    def get_default_mapping(cls, resource_type: str) -> dict:
        from karrio.server.data import resources

        if resource_type == "order":
            return resources.orders.DEFAULT_HEADERS
        if resource_type == "shipment":
            return resources.shipments.DEFAULT_HEADERS
        if resource_type == "tracking":
            return resources.tracking.DEFAULT_HEADERS

        return {}

    @classmethod
    def get_model(cls, resource_type: str) -> dict:
        if resource_type == "order":
            from karrio.server.orders.models import Order

            return Order
        if resource_type == "shipment":
            from karrio.server.manager.models import Shipment

            return Shipment
        if resource_type == "tracking":
            from karrio.server.manager.models import Tracking

            return Tracking

        return None


class ResourceStatus(Enum):
    queued = "queued"
    created = "created"
    failed = "failed"
    processed = "processed"


class BatchOperationStatus(Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


RESOURCE_TYPE = [(c.value, c.value) for c in list(ResourceType)]
OPERATION_STATUS = [(c.value, c.value) for c in list(BatchOperationStatus)]


class ImportData(serializers.Serializer):
    resource_type = fields.ChoiceField(required=True, choices=RESOURCE_TYPE)
    data_template = fields.CharField(required=False)
    data_file = fields.FileField(required=True)


class BatchObject(serializers.EntitySerializer):
    status = fields.ChoiceField(
        choices=OPERATION_STATUS, help_text="The batch operation resource status"
    )


class BatchOperationData(serializers.Serializer):
    status = fields.ChoiceField(choices=OPERATION_STATUS)
    resource_type = fields.ChoiceField(required=True, choices=RESOURCE_TYPE)
    resources = BatchObject(many=True)


class BatchOperation(serializers.EntitySerializer, BatchOperationData):
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    test_mode = fields.BooleanField(required=True)
