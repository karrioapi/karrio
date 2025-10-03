import logging

import karrio.server.core.utils as utils
import karrio.server.manager.models as models
import karrio.server.serializers as serializers
from karrio.server.manager.serializers import (
    fetch_shipment_rates,
    can_mutate_shipment,
    buy_shipment_label,
)

logger = logging.getLogger(__name__)


@utils.error_wrapper
def process_shipments(shipment_ids=[]):
    logger.info("> starting batch shipments processing")

    shipments = models.Shipment.objects.filter(id__in=shipment_ids, status="draft")

    if any(shipments):
        for shipment in shipments:
            process_shipment(shipment)
    else:
        logger.info("no shipment found")

    logger.info("> ending batch shipments processing")


@utils.error_wrapper
def process_shipment(shipment):
    preferred_service = shipment.options.get("preferred_service")
    should_purchase = any(preferred_service or "")
    should_update = should_purchase or len(shipment.rates) == 0
    context = serializers.get_object_context(shipment)

    can_mutate_shipment(
        shipment,
        update=should_update,
        purchase=should_purchase,
    )

    if len(shipment.rates) == 0:
        shipment = fetch_shipment_rates(shipment, context=context)

    if should_purchase:
        shipment = buy_shipment_label(
            shipment,
            context=context,
            service=preferred_service,
        )
