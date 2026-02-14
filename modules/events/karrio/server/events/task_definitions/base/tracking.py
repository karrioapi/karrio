import time
import typing
import datetime
import functools
from itertools import groupby

from django.conf import settings
from django.utils import timezone

import karrio.sdk as karrio
import karrio.lib as lib
from karrio.api.gateway import Gateway
from karrio.api.interface import IRequestFrom
from karrio.core.models import TrackingDetails, Message, TrackingEvent

import karrio.server.core.utils as utils
from karrio.server.core.logging import logger
from karrio.server.core.utils import resolve_carrier
import karrio.server.manager.models as models
import karrio.server.tracing.utils as tracing
import karrio.server.core.datatypes as datatypes
import karrio.server.manager.serializers as serializers

Delay = int
RequestBatches = typing.Tuple[
    Gateway, IRequestFrom, Delay, typing.List[models.Tracking]
]
BatchResponse = typing.List[typing.Tuple[TrackingDetails, typing.List[Message]]]

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(
    settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200
)
TRACKER_BATCH_DELAY = int(getattr(settings, "TRACKER_BATCH_DELAY", 3))


def update_trackers(
    delta: datetime.timedelta = datetime.timedelta(
        seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL
    ),
    tracker_ids: typing.List[str] = [],
    schema: str = None,
):
    """Dispatcher: groups trackers by carrier and enqueues per-carrier sub-tasks."""
    logger.info(
        "Starting tracker update dispatcher",
        delta_seconds=delta.total_seconds(),
        tracker_count=len(tracker_ids) if tracker_ids else 0,
    )

    # Single efficient query — only fetch IDs and carrier JSON snapshot
    qs = (
        models.Tracking.objects.filter(id__in=tracker_ids)
        if any(tracker_ids)
        else models.Tracking.objects.filter(
            delivered=False,
            updated_at__lt=timezone.now() - delta,
        )
    )
    active_tracker_data = list(qs.values_list("id", "carrier"))

    if not active_tracker_data:
        logger.info("No active trackers found needing update")
        return

    def _carrier_id(carrier_snapshot):
        if carrier_snapshot is None:
            return ""
        return carrier_snapshot.get("carrier_id") or ""

    sorted_data = sorted(
        active_tracker_data, key=lambda item: _carrier_id(item[1])
    )
    carrier_groups = 0

    for carrier_key, group in groupby(
        sorted_data, key=lambda item: _carrier_id(item[1])
    ):
        ids_for_carrier = [tid for tid, _ in group]
        carrier_groups += 1
        logger.info(
            "Dispatching carrier tracking batch",
            carrier_id=carrier_key,
            tracker_count=len(ids_for_carrier),
        )
        # Import the Huey task and enqueue it
        from karrio.server.events.task_definitions.base import (
            process_carrier_tracking_batch,
        )

        process_carrier_tracking_batch(
            tracker_ids=ids_for_carrier,
            schema=schema,
        )

    logger.info(
        "Tracker update dispatcher complete",
        total_trackers=len(active_tracker_data),
        carrier_groups=carrier_groups,
    )


def process_carrier_trackers(tracker_ids: typing.List[str], **kwargs):
    """Process one carrier's trackers: flat delays, incremental saves."""
    trackers = list(models.Tracking.objects.filter(id__in=tracker_ids))

    if not trackers:
        logger.info("No trackers found for given IDs", count=len(tracker_ids))
        return

    snapshot = trackers[0].carrier or {}
    conn_id = snapshot.get("connection_id") or snapshot.get("carrier_connection_id")
    carrier = resolve_carrier(snapshot, context=None)

    if not carrier:
        logger.warning(
            "Could not resolve carrier for tracking batch", connection_id=conn_id
        )
        return

    gateway: Gateway = carrier.gateway
    batch_size = 10
    total_batches = (len(trackers) + batch_size - 1) // batch_size

    logger.info(
        "Starting carrier tracking batch processing",
        carrier_id=trackers[0].carrier_id,
        total_trackers=len(trackers),
        total_batches=total_batches,
    )

    for i in range(0, len(trackers), batch_size):
        batch_trackers = trackers[i : i + batch_size]
        batch_num = (i // batch_size) + 1

        try:
            tracking_numbers = [t.tracking_number for t in batch_trackers]
            options: dict = functools.reduce(
                lambda acc, t: {**acc, **(t.options or {})}, batch_trackers, {}
            )

            request: IRequestFrom = karrio.Tracking.fetch(
                datatypes.TrackingRequest(
                    tracking_numbers=tracking_numbers, options=options
                )
            )

            response = request.from_(gateway).parse()

            # Save tracing records for this batch
            _save_batch_tracing(gateway, batch_trackers)

            # Save results immediately (incremental save)
            _save_batch_results(response, batch_trackers)

            logger.info(
                "Tracking batch processed",
                batch=f"{batch_num}/{total_batches}",
                count=len(batch_trackers),
            )

        except Exception as e:
            logger.warning(
                "Tracking batch failed",
                batch=f"{batch_num}/{total_batches}",
                error=str(e),
            )
            logger.exception("Tracking batch error")

        # Flat delay between batches (not progressive)
        if i + batch_size < len(trackers):
            time.sleep(TRACKER_BATCH_DELAY)

    logger.info(
        "Carrier tracking batch complete",
        carrier_id=trackers[0].carrier_id,
        total_processed=len(trackers),
    )


def _save_batch_results(response, batch_trackers: typing.List[models.Tracking]):
    """Save results for a single batch immediately."""
    tracking_details, messages = response if response else ([], [])

    for details in tracking_details or []:
        try:
            related_trackers = [
                t
                for t in batch_trackers
                if t.tracking_number == details.tracking_number
            ]
            for tracker in related_trackers:
                status = utils.compute_tracking_status(details).value
                options = {
                    **(tracker.options or {}),
                    tracker.tracking_number: details.meta,
                }

                serializers.update_tracker(
                    tracker,
                    dict(
                        events=details.events,
                        delivered=details.delivered,
                        status=status,
                        estimated_delivery=details.estimated_delivery,
                        options=options,
                        meta=details.meta,
                        info=lib.to_dict(details.info or {}),
                        images=details.images,
                    ),
                )

        except Exception as e:
            logger.warning(
                "Failed to update tracker",
                tracking_number=details.tracking_number,
                error=str(e),
            )
            logger.exception(
                "Tracker update error", tracking_number=details.tracking_number
            )


def _save_batch_tracing(
    gateway: Gateway, batch_trackers: typing.List[models.Tracking]
):
    """Save tracing records for a single batch."""
    try:
        context = serializers.get_object_context(batch_trackers[0])
        tracing.bulk_save_tracing_records(gateway.tracer, context=context)
    except Exception as e:
        logger.warning("Failed to save tracing records", error=str(e))


# ─────────────────────────────────────────────────────────────────
# Legacy functions kept for backward compatibility
# ─────────────────────────────────────────────────────────────────


def create_request_batches(
    trackers: typing.List[models.Tracking],
    carrier_cache: typing.Dict[str, typing.Any] = None,
) -> typing.List[RequestBatches]:
    if carrier_cache is None:
        carrier_cache = {}

    # Resolve carrier ONCE per group, using cache to avoid redundant DB queries
    snapshot = trackers[0].carrier or {}
    conn_id = snapshot.get("connection_id") or snapshot.get("carrier_connection_id")

    if conn_id and conn_id in carrier_cache:
        carrier = carrier_cache[conn_id]
    else:
        carrier = resolve_carrier(snapshot, context=None)
        if conn_id and carrier:
            carrier_cache[conn_id] = carrier

    if not carrier:
        logger.warning("Could not resolve carrier for tracking group", connection_id=conn_id)
        return []

    start = 0
    end = 10
    batches = []

    while any(trackers[start:end]):
        try:
            # Add a request delay to avoid sending two request batches to a carrier at the same time
            delay = int(((end / 10) * 10) - 10)
            batch_trackers = trackers[start:end]
            tracking_numbers = [t.tracking_number for t in batch_trackers]
            options: dict = functools.reduce(
                lambda acc, t: {**acc, **(t.options or {})}, batch_trackers, {}
            )

            logger.debug("Preparing tracking request", tracking_numbers=tracking_numbers, batch_range=(start, end))

            # Prepare and send tracking request(s) using the karrio interface.
            request: IRequestFrom = karrio.Tracking.fetch(
                datatypes.TrackingRequest(
                    tracking_numbers=tracking_numbers, options=options
                )
            )
            gateway: Gateway = carrier.gateway

            batches.append((gateway, request, delay, batch_trackers))

        except Exception as request_error:
            logger.warning("Failed to prepare tracking batch request", batch_range=(start, end), error=str(request_error))
            logger.exception("Tracking batch request preparation error", batch_range=(start, end))

        end += 10
        start += 10

    return batches


def fetch_tracking_info(request_batch: RequestBatches) -> BatchResponse:
    gateway, request, delay, trackers = request_batch
    tracking_numbers = [t.tracking_number for t in trackers]
    logger.debug("Fetching tracking batch", tracking_numbers=tracking_numbers, delay_seconds=delay)
    time.sleep(delay)  # apply delay before request

    try:
        return utils.identity(lambda: request.from_(gateway).parse())
    except Exception as request_error:
        logger.warning("Tracking batch request failed", tracking_numbers=tracking_numbers, error=str(request_error))
        logger.exception("Tracking batch request error", tracking_numbers=tracking_numbers)

    return []


@utils.error_wrapper
def save_tracing_records(request_batches: typing.List[RequestBatches]):
    logger.info("Saving tracing records", batch_count=len(request_batches))

    try:
        for request_batch in request_batches:
            gateway, _, __, trackers = request_batch

            if not any(trackers):
                continue

            context = serializers.get_object_context(trackers[0])
            tracing.bulk_save_tracing_records(gateway.tracer, context=context)
    except Exception as error:
        logger.warning("Failed to save tracing records", error=str(error))
        logger.exception("Tracing record save error")


def save_updated_trackers(
    responses: typing.List[BatchResponse], trackers: typing.List[models.Tracking]
):
    logger.info("Saving updated trackers", tracker_count=len(trackers))

    for tracking_details, _ in responses:
        for details in tracking_details or []:
            try:
                logger.debug("Updating tracking info", tracking_number=details.tracking_number)
                related_trackers = [
                    t for t in trackers if t.tracking_number == details.tracking_number
                ]
                for tracker in related_trackers:
                    # Compute status from tracking details
                    status = utils.compute_tracking_status(details).value
                    # Merge options with existing tracker options
                    options = {
                        **(tracker.options or {}),
                        tracker.tracking_number: details.meta,
                    }

                    # Use the centralized update_tracker function
                    serializers.update_tracker(
                        tracker,
                        dict(
                            events=details.events,
                            delivered=details.delivered,
                            status=status,
                            estimated_delivery=details.estimated_delivery,
                            options=options,
                            meta=details.meta,
                            info=lib.to_dict(details.info or {}),
                            images=details.images,
                        ),
                    )

            except Exception as update_error:
                logger.warning("Failed to update tracker", tracking_number=details.tracking_number, error=str(update_error))
                logger.exception("Tracker update error", tracking_number=details.tracking_number)
