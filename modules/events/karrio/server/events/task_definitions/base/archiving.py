import logging
import datetime
import django.utils.timezone as timezone

import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.events.models as events
import karrio.server.orders.models as orders
import karrio.server.tracing.models as tracing
import karrio.server.manager.models as manager

logger = logging.getLogger(__name__)


def run_data_archiving(*args, **kwargs):
    now = timezone.now()
    log_retention = now - datetime.timedelta(days=conf.settings.API_LOGS_DATA_RETENTION)
    order_retention = now - datetime.timedelta(days=conf.settings.ORDER_DATA_RETENTION)
    shipment_retention = now - datetime.timedelta(
        days=conf.settings.SHIPMENT_DATA_RETENTION
    )
    tracker_retention = now - datetime.timedelta(
        days=conf.settings.TRACKER_DATA_RETENTION
    )

    shipping_data = manager.Shipment.objects.filter(created_at__lt=shipment_retention)
    tracking_Data = manager.Tracking.objects.filter(created_at__lt=tracker_retention)
    tracing_data = tracing.TracingRecord.objects.filter(created_at__lt=log_retention)
    api_log_data = core.APILog.objects.filter(requested_at__lt=log_retention)
    order_data = orders.Order.objects.filter(created_at__lt=order_retention)
    event_data = events.Event.objects.filter(created_at__lt=log_retention)

    if any(tracing_data):
        logger.info(">> archiving SDK tracing backlog...")
        utils.failsafe(lambda: tracing_data.delete())

    if any(event_data):
        logger.info(">> archiving events backlog...")
        utils.failsafe(lambda: event_data.delete())

    if any(api_log_data):
        logger.info(">> archiving API request logs backlog...")
        utils.failsafe(lambda: api_log_data.delete())

    if any(tracking_Data):
        logger.info(">> archiving tracking data backlog...")
        utils.failsafe(lambda: tracking_Data.delete())

    if any(shipping_data):
        logger.info(">> archiving shipping data backlog...")
        utils.failsafe(lambda: shipping_data.delete())

    if any(order_data):
        logger.info(">> archiving order data backlog...")
        utils.failsafe(lambda: order_data.delete())

    logger.info("> ending scheduled backlog archiving!")
