import datetime

import django.utils.timezone as timezone
import karrio.server.conf as conf
import karrio.server.core.models as core
import karrio.server.core.utils as utils
import karrio.server.events.models as events
import karrio.server.manager.models as manager
import karrio.server.orders.models as orders
import karrio.server.tracing.models as tracing
from karrio.server.core.logging import logger

# Delete in bounded batches so a large first-run backlog cannot load every id
# into memory and OOM the worker in a single unbounded transaction (GH #1125).
BATCH_SIZE = 1000


def _batched_delete(queryset, pk_field="id"):
    """Delete a queryset in fixed-size batches, one transaction per batch.

    Returns the total number of deleted rows. Each batch resolves a bounded
    page of primary keys and deletes only those, so memory stays flat
    regardless of how much backlog has accumulated.
    """
    ordered = queryset.order_by("pk")
    total_deleted = 0

    while True:
        batch_ids = list(ordered.values_list(pk_field, flat=True)[:BATCH_SIZE])
        if not batch_ids:
            break

        deleted_count = ordered.filter(**{f"{pk_field}__in": batch_ids}).delete()[0]
        total_deleted += deleted_count

        # Stop if a batch deleted nothing to avoid an infinite loop on rows that
        # cannot be removed (e.g. protected relations).
        if not deleted_count:
            break

    return total_deleted


def run_data_archiving(*args, **kwargs):
    now = timezone.now()
    log_retention = now - datetime.timedelta(days=conf.settings.API_LOGS_DATA_RETENTION)
    order_retention = now - datetime.timedelta(days=conf.settings.ORDER_DATA_RETENTION)
    shipment_retention = now - datetime.timedelta(days=conf.settings.SHIPMENT_DATA_RETENTION)
    tracker_retention = now - datetime.timedelta(days=conf.settings.TRACKER_DATA_RETENTION)

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

    events_deleted = utils.failsafe(lambda: _batched_delete(event_data)) or 0
    if events_deleted:
        logger.info(
            "Archiving events backlog",
            retention_days=conf.settings.API_LOGS_DATA_RETENTION,
            deleted_records=events_deleted,
        )

    api_logs_deleted = utils.failsafe(lambda: _batched_delete(api_log_data)) or 0
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


def _batched_delete_with_links(queryset, link_model):
    """Delete a queryset in batches, clearing matching org links per batch.

    Mirrors ``_batched_delete`` but first removes the organization link rows
    (``item_id`` based) for each batch to avoid CASCADE N+1 queries, then
    deletes the batch itself. Bounded memory regardless of backlog (GH #1125).
    """
    ordered = queryset.order_by("pk")
    total_deleted = 0

    while True:
        batch_ids = list(ordered.values_list("id", flat=True)[:BATCH_SIZE])
        if not batch_ids:
            break

        if link_model is not None:
            link_model.objects.filter(item_id__in=batch_ids).delete()

        deleted_count = ordered.filter(id__in=batch_ids).delete()[0]
        total_deleted += deleted_count

        if not deleted_count:
            break

    return total_deleted


def _bulk_delete_tracking_data(tracking_queryset):
    """Batch-delete tracking data, clearing organization links per batch."""
    try:
        from karrio.server.orgs.models import TrackingLink as link_model
    except ImportError:
        # Organizations module not installed.
        link_model = None

    return _batched_delete_with_links(tracking_queryset, link_model)


def _bulk_delete_shipment_data(shipment_queryset):
    """Batch-delete shipment data, clearing organization links per batch."""
    try:
        from karrio.server.orgs.models import ShipmentLink as link_model
    except ImportError:
        # Organizations module not installed.
        link_model = None

    return _batched_delete_with_links(shipment_queryset, link_model)


def _bulk_delete_order_data(order_queryset):
    """Batch-delete order data, clearing organization links per batch."""
    try:
        from karrio.server.orgs.models import OrderLink as link_model
    except ImportError:
        # Organizations module not installed.
        link_model = None

    return _batched_delete_with_links(order_queryset, link_model)
