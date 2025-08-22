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
        utils.failsafe(lambda: _bulk_delete_tracing_data(tracing_data))

    if any(event_data):
        logger.info(">> archiving events backlog...")
        utils.failsafe(lambda: event_data.delete())

    if any(api_log_data):
        logger.info(">> archiving API request logs backlog...")
        utils.failsafe(lambda: api_log_data.delete())

    if any(tracking_Data):
        logger.info(">> archiving tracking data backlog...")
        utils.failsafe(lambda: _bulk_delete_tracking_data(tracking_Data))

    if any(shipping_data):
        logger.info(">> archiving shipping data backlog...")
        utils.failsafe(lambda: _bulk_delete_shipment_data(shipping_data))

    if any(order_data):
        logger.info(">> archiving order data backlog...")
        utils.failsafe(lambda: _bulk_delete_order_data(order_data))

    logger.info("> ending scheduled backlog archiving!")


def _bulk_delete_tracing_data(tracing_queryset):
    """Bulk delete tracing data to avoid N+1 queries with organization links."""
    # Check if organizations module is available
    try:
        from karrio.server.orgs.models import TracingRecordLink

        # Get the tracing record IDs that will be deleted
        tracing_ids = list(tracing_queryset.values_list('id', flat=True))

        if tracing_ids:
            # Bulk delete TracingRecordLink entries first to avoid CASCADE N+1 queries
            TracingRecordLink.objects.filter(item_id__in=tracing_ids).delete()

        # Now delete the tracing records themselves
        tracing_queryset.delete()

    except ImportError:
        # Organizations module not installed, just delete normally
        tracing_queryset.delete()


def _bulk_delete_tracking_data(tracking_queryset):
    """Bulk delete tracking data to avoid N+1 queries with organization links."""
    try:
        from karrio.server.orgs.models import TrackingLink
        
        # Get the tracking record IDs that will be deleted
        tracking_ids = list(tracking_queryset.values_list('id', flat=True))
        
        if tracking_ids:
            # Bulk delete TrackingLink entries first to avoid CASCADE N+1 queries
            TrackingLink.objects.filter(item_id__in=tracking_ids).delete()
            
        # Now delete the tracking records themselves
        tracking_queryset.delete()
        
    except ImportError:
        # Organizations module not installed, just delete normally
        tracking_queryset.delete()


def _bulk_delete_shipment_data(shipment_queryset):
    """Bulk delete shipment data to avoid N+1 queries with organization links."""
    try:
        from karrio.server.orgs.models import ShipmentLink
        
        # Get the shipment record IDs that will be deleted
        shipment_ids = list(shipment_queryset.values_list('id', flat=True))
        
        if shipment_ids:
            # Bulk delete ShipmentLink entries first to avoid CASCADE N+1 queries
            ShipmentLink.objects.filter(item_id__in=shipment_ids).delete()
            
        # Now delete the shipment records themselves
        shipment_queryset.delete()
        
    except ImportError:
        # Organizations module not installed, just delete normally
        shipment_queryset.delete()


def _bulk_delete_order_data(order_queryset):
    """Bulk delete order data to avoid N+1 queries with organization links."""
    try:
        from karrio.server.orgs.models import OrderLink
        
        # Get the order record IDs that will be deleted
        order_ids = list(order_queryset.values_list('id', flat=True))
        
        if order_ids:
            # Bulk delete OrderLink entries first to avoid CASCADE N+1 queries
            OrderLink.objects.filter(item_id__in=order_ids).delete()
            
        # Now delete the order records themselves
        order_queryset.delete()
        
    except ImportError:
        # Organizations module not installed, just delete normally
        order_queryset.delete()

