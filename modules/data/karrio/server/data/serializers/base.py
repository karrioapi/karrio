import karrio.lib as lib
import rest_framework.fields as fields
import karrio.server.serializers as serializers


class ResourceType(lib.StrEnum):
    order = "orders"
    shipment = "shipments"
    trackers = "trackers"
    billing = "billing"

    @classmethod
    def get_default_mapping(cls, resource_type: str) -> dict:
        from karrio.server.data import resources

        if resource_type == "orders":
            return resources.orders.DEFAULT_HEADERS
        if resource_type == "shipments":
            return resources.shipments.DEFAULT_HEADERS
        if resource_type == "trackers":
            return resources.trackers.DEFAULT_HEADERS

        return {}

    @classmethod
    def get_model(cls, resource_type: str) -> dict:
        if resource_type == "orders":
            from karrio.server.orders.models import Order

            return Order
        if resource_type == "shipments":
            from karrio.server.manager.models import Shipment

            return Shipment
        if resource_type == "trackers":
            from karrio.server.manager.models import Tracking

            return Tracking

        return None

    @classmethod
    def get_serialiazer(cls, resource_type: str) -> dict:
        if resource_type == "orders":
            from karrio.server.data.serializers import BatchOrderData

            return BatchOrderData
        if resource_type == "shipments":
            from karrio.server.data.serializers import BatchShipmentData

            return BatchShipmentData
        if resource_type == "trackers":
            from karrio.server.data.serializers import BatchTrackerData

            return BatchTrackerData

        return None


class ResourceStatus(lib.StrEnum):
    queued = "queued"
    created = "created"
    has_errors = "has_errors"
    incomplete = "incomplete"
    processed = "processed"


class BatchOperationStatus(lib.StrEnum):
    queued = "queued"
    running = "running"
    failed = "failed"
    completed = "completed"
    completed_with_errors = "completed_with_errors"


RESOURCE_TYPE = [(c.value, c.value) for c in list(ResourceType)]
OPERATION_STATUS = [(c.value, c.value) for c in list(BatchOperationStatus)]


class ImportData(serializers.Serializer):
    resource_type = fields.ChoiceField(required=True, choices=RESOURCE_TYPE)
    data_template = fields.CharField(required=False)
    data_file = fields.FileField(required=True)


class BatchObject(serializers.EntitySerializer):
    status = fields.ChoiceField(
        choices=OPERATION_STATUS,
        help_text="The batch operation resource status",
    )
    errors = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Resource processing errors",
    )


class BatchOperationData(serializers.Serializer):
    status = fields.ChoiceField(choices=OPERATION_STATUS)
    resource_type = fields.ChoiceField(required=True, choices=RESOURCE_TYPE)
    resources = BatchObject(many=True)


class BatchOperation(serializers.EntitySerializer, BatchOperationData):
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    test_mode = fields.BooleanField(required=True)
