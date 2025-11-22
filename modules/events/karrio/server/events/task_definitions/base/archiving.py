import datetime
import django.utils.timezone as timezone

import karrio.server.conf as conf
import karrio.server.core.utils as utils
from karrio.server.core.logging import logger
import karrio.server.core.models as core
import karrio.server.events.models as events
import karrio.server.orders.models as orders
import karrio.server.tracing.models as tracing
import karrio.server.manager.models as manager


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

    # Prepare querysets once and rely on delete helpers to determine if work was done.
    tracing_data = tracing.TracingRecord.objects.filter(created_at__lt=log_retention)
    event_data = events.Event.objects.filter(created_at__lt=log_retention)
    api_log_data = core.APILog.objects.filter(requested_at__lt=log_retention)
    tracking_data = manager.Tracking.objects.filter(created_at__lt=tracker_retention)
    shipping_data = manager.Shipment.objects.filter(created_at__lt=shipment_retention)
    order_data = orders.Order.objects.filter(created_at__lt=order_retention)

    tracing_deleted = utils.failsafe(lambda: _bulk_delete_tracing_data(tracing_data)) or 0
    if tracing_deleted:
        logger.info(
            "Archiving SDK tracing backlog",
            retention_days=conf.settings.API_LOGS_DATA_RETENTION,
            deleted_records=tracing_deleted,
        )

    events_deleted = utils.failsafe(lambda: event_data.delete()[0]) or 0
    if events_deleted:
        logger.info(
            "Archiving events backlog",
            retention_days=conf.settings.API_LOGS_DATA_RETENTION,
            deleted_records=events_deleted,
        )

    api_logs_deleted = utils.failsafe(lambda: api_log_data.delete()[0]) or 0
    if api_logs_deleted:
        logger.info(
            "Archiving API request logs backlog",
            retention_days=conf.settings.API_LOGS_DATA_RETENTION,
            deleted_records=api_logs_deleted,
        )

    tracking_deleted = utils.failsafe(lambda: _bulk_delete_tracking_data(tracking_data)) or 0
    if tracking_deleted:
        logger.info(
            "Archiving tracking data backlog",
            retention_days=conf.settings.TRACKER_DATA_RETENTION,
            deleted_records=tracking_deleted,
        )

    shipping_deleted = utils.failsafe(lambda: _bulk_delete_shipment_data(shipping_data)) or 0
    if shipping_deleted:
        logger.info(
            "Archiving shipping data backlog",
            retention_days=conf.settings.SHIPMENT_DATA_RETENTION,
            deleted_records=shipping_deleted,
        )

    order_deleted = utils.failsafe(lambda: _bulk_delete_order_data(order_data)) or 0
    if order_deleted:
        logger.info(
            "Archiving order data backlog",
            retention_days=conf.settings.ORDER_DATA_RETENTION,
            deleted_records=order_deleted,
        )

    logger.info("Finished scheduled backlog archiving")


def _bulk_delete_tracing_data(tracing_queryset):
    """Bulk delete tracing data to avoid N+1 queries with organization links."""
    BATCH_SIZE = 1000
    queryset = tracing_queryset.order_by("pk")

    try:
        from karrio.server.orgs.models import TracingRecordLink

        # Process in batches to avoid memory issues
        total_deleted = 0
        while True:
            # Get a batch of IDs to delete
            batch_ids = list(queryset.values_list("id", flat=True)[:BATCH_SIZE])

            if not batch_ids:
                break

            # Bulk delete TracingRecordLink entries first to avoid CASCADE N+1 queries
            TracingRecordLink.objects.filter(item_id__in=batch_ids).delete()

            # Delete the tracing records in this batch
            deleted_count = queryset.filter(id__in=batch_ids).delete()[0]
            total_deleted += deleted_count

            logger.info("Deleted tracing records batch", batch_count=deleted_count, total_deleted=total_deleted)

        return total_deleted

    except ImportError:
        # Organizations module not installed, just delete in batches
        total_deleted = 0
        while True:
            # Get a batch to delete
            batch_ids = list(queryset.values_list("id", flat=True)[:BATCH_SIZE])

            if not batch_ids:
                break

            deleted_count = queryset.filter(id__in=batch_ids).delete()[0]
            total_deleted += deleted_count

            logger.info("Deleted tracing records batch", batch_count=deleted_count, total_deleted=total_deleted)

        return total_deleted


def _bulk_delete_tracking_data(tracking_queryset):
    """Bulk delete tracking data to avoid N+1 queries with organization links."""
    queryset = tracking_queryset.order_by("pk")

    try:
        from karrio.server.orgs.models import TrackingLink

        # Get the tracking record IDs that will be deleted
        tracking_ids = list(queryset.values_list("id", flat=True))

        if tracking_ids:
            # Bulk delete TrackingLink entries first to avoid CASCADE N+1 queries
            TrackingLink.objects.filter(item_id__in=tracking_ids).delete()

        # Now delete the tracking records themselves
        deleted = queryset.delete()[0]

    except ImportError:
        # Organizations module not installed, just delete normally
        deleted = queryset.delete()[0]

    return deleted


def _bulk_delete_shipment_data(shipment_queryset):
    """Bulk delete shipment data to avoid N+1 queries with organization links."""
    queryset = shipment_queryset.order_by("pk")

    try:
        from karrio.server.orgs.models import ShipmentLink

        # Get the shipment record IDs that will be deleted
        shipment_ids = list(queryset.values_list("id", flat=True))

        if shipment_ids:
            # Bulk delete ShipmentLink entries first to avoid CASCADE N+1 queries
            ShipmentLink.objects.filter(item_id__in=shipment_ids).delete()

        # Now delete the shipment records themselves
        deleted = queryset.delete()[0]

    except ImportError:
        # Organizations module not installed, just delete normally
        deleted = queryset.delete()[0]

    return deleted


def _bulk_delete_order_data(order_queryset):
    """Bulk delete order data to avoid N+1 queries with organization links."""
    queryset = order_queryset.order_by("pk")

    try:
        from karrio.server.orgs.models import OrderLink

        # Get the order record IDs that will be deleted
        order_ids = list(queryset.values_list("id", flat=True))

        if order_ids:
            # Bulk delete OrderLink entries first to avoid CASCADE N+1 queries
            OrderLink.objects.filter(item_id__in=order_ids).delete()

        # Now delete the order records themselves
        deleted = queryset.delete()[0]

    except ImportError:
        # Organizations module not installed, just delete normally
        deleted = queryset.delete()[0]

    return deleted

