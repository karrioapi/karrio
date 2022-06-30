import tablib
import logging
from datetime import datetime
from django.db import transaction

from karrio.server.serializers import owned_model_serializer
import karrio.server.data.serializers as serializers
import karrio.server.data.models as models
import karrio.server.manager.models as manager
import karrio.server.orders.models as orders
import karrio.server.data.resources as resources

logger = logging.getLogger(__name__)


@owned_model_serializer
class ImportDataSerializer(serializers.ImportData):
    @transaction.atomic
    def create(
        self, validated_data: dict, context: dict, **kwargs
    ) -> models.BatchOperation:
        resource = resources.tracking.tracking_resource({}, context)
        dataset = tablib.Dataset().load(
            validated_data["data_file"].read().decode(),
            headers=["tracking_number", "carrier"],
        )
        result = resource.import_data(dataset, dry_run=True)

        print(result.__dict__)

        return dict(
            status="queued",
            data_type="tracking",
            resources=[],
            test_mode=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
