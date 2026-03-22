import typing
import datetime
import functools
from collections import defaultdict

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
RequestBatches = typing.Tuple[Gateway, IRequestFrom, typing.List[models.Tracking]]
BatchResponse = typing.List[typing.Tuple[TrackingDetails, typing.List[Message]]]

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(
    settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200
)
TRACKING_REQUEST_BATCH_SIZE = int(getattr(settings, "TRACKING_REQUEST_BATCH_SIZE", 10))


def get_scheduler_lock_name(schema: typing.Optional[str] = None) -> str:
    return f"background_trackers_update:{schema or 'public'}"


def get_active_trackers(
    delta: datetime.timedelta,
    tracker_ids: typing.Optional[typing.List[str]] = None,
    carrier_id: typing.Optional[str] = None,
) -> typing.List[models.Tracking]:
    queryset = (
        models.Tracking.objects.filter(id__in=tracker_ids)
        if any(tracker_ids or [])
        else models.Tracking.objects.filter(
            delivered=False,
            updated_at__lt=timezone.now() - delta,
        )
    )

    if carrier_id:
        queryset = queryset.filter(carrier__carrier_id=carrier_id)

    return list(queryset.order_by("carrier__carrier_id", "updated_at", "id"))


def group_trackers_by_carrier(
    trackers: typing.Iterable[models.Tracking],
) -> dict[str, typing.List[models.Tracking]]:
    grouped: dict[str, typing.List[models.Tracking]] = defaultdict(list)

    for tracker in trackers:
        grouped[str(tracker.carrier_id)].append(tracker)

    return dict(grouped)


def schedule_tracker_updates(
    delta: datetime.timedelta = datetime.timedelta(
        seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL
    ),
    tracker_ids: typing.Optional[typing.List[str]] = None,
    schema: typing.Optional[str] = None,
) -> int:
    active_trackers = get_active_trackers(delta=delta, tracker_ids=tracker_ids)

    if not any(active_trackers):
        logger.info("No active trackers found needing update")
        return 0

    trackers_by_carrier = group_trackers_by_carrier(active_trackers)
    logger.info(
        "Queueing carrier tracker refresh tasks",
        schema=schema,
        tracker_count=len(active_trackers),
        carrier_count=len(trackers_by_carrier),
    )

    from karrio.server.events.task_definitions.base import update_trackers_for_carrier

    for carrier_key, carrier_trackers in trackers_by_carrier.items():
        update_trackers_for_carrier(
            tracker_ids=[str(tracker.id) for tracker in carrier_trackers],
            carrier_id=carrier_key,
            schema=schema,
        )

    return len(trackers_by_carrier)


def update_trackers(
    delta: datetime.timedelta = datetime.timedelta(
        seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL
    ),
    tracker_ids: typing.Optional[typing.List[str]] = None,
    carrier_id: typing.Optional[str] = None,
):
    logger.info(
        "Starting scheduled trackers update",
        delta_seconds=delta.seconds,
        tracker_count=len(tracker_ids) if tracker_ids else 0,
        carrier_id=carrier_id,
    )
    active_trackers = get_active_trackers(
        delta=delta,
        tracker_ids=tracker_ids,
        carrier_id=carrier_id,
    )

    if any(active_trackers):
        for grouped_carrier_id, carrier_trackers in group_trackers_by_carrier(
            active_trackers
        ).items():
            request_batches = create_request_batches(carrier_trackers)
            responses = [
                fetch_tracking_info(request_batch) for request_batch in request_batches
            ]
            save_tracing_records(request_batches)
            save_updated_trackers(responses, carrier_trackers)
            logger.info(
                "Finished carrier tracker refresh",
                carrier_id=grouped_carrier_id,
                tracker_count=len(carrier_trackers),
                batch_count=len(request_batches),
            )
    else:
        logger.info("No active trackers found needing update")

    logger.info("Finished scheduled trackers update")


def create_request_batches(
    trackers: typing.List[models.Tracking],
) -> typing.List[RequestBatches]:
    batches = []
    carrier = resolve_carrier(trackers[0].carrier, context=None)

    for start in range(0, len(trackers), TRACKING_REQUEST_BATCH_SIZE):
        end = start + TRACKING_REQUEST_BATCH_SIZE
        try:
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

            batches.append((gateway, request, batch_trackers))

        except Exception as request_error:
            logger.warning("Failed to prepare tracking batch request", batch_range=(start, end), error=str(request_error))
            logger.exception("Tracking batch request preparation error", batch_range=(start, end))

    return batches


def fetch_tracking_info(request_batch: RequestBatches) -> BatchResponse:
    gateway, request, trackers = request_batch
    tracking_numbers = [t.tracking_number for t in trackers]
    logger.debug("Fetching tracking batch", tracking_numbers=tracking_numbers)

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
            gateway, _, trackers = request_batch

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
