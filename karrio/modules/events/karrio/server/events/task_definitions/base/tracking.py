import time
import typing
import logging
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
import karrio.server.manager.models as models
import karrio.server.tracing.utils as tracing
import karrio.server.core.datatypes as datatypes
import karrio.server.manager.serializers as serializers

logger = logging.getLogger(__name__)
Delay = int
RequestBatches = typing.Tuple[
    Gateway, IRequestFrom, Delay, typing.List[models.Tracking]
]
BatchResponse = typing.List[typing.Tuple[TrackingDetails, typing.List[Message]]]

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(
    settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200
)


def update_trackers(
    delta: datetime.timedelta = datetime.timedelta(
        seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL
    ),
    tracker_ids: typing.List[str] = [],
):
    logger.info("> starting scheduled trackers update")

    active_trackers = lib.identity(
        models.Tracking.objects.filter(id__in=tracker_ids)
        if any(tracker_ids)
        else models.Tracking.objects.filter(
            delivered=False,
            updated_at__lt=timezone.now() - delta,
        )
    )

    if any(active_trackers):
        trackers_grouped_by_carrier = [
            list(g) for _, g in groupby(active_trackers, key=lambda t: t.carrier_id)
        ]
        request_batches: typing.List[RequestBatches] = sum(
            [create_request_batches(group) for group in trackers_grouped_by_carrier], []
        )

        responses = lib.run_concurently(fetch_tracking_info, request_batches, 2)
        save_tracing_records(request_batches)
        save_updated_trackers(responses, active_trackers)
    else:
        logger.info("no active trackers found needing update")

    logger.info("> ending scheduled trackers update")


def create_request_batches(
    trackers: typing.List[models.Tracking],
) -> typing.List[RequestBatches]:
    start = 0
    end = 10
    batches = []

    while any(trackers[start:end]):
        try:
            # Add a request delay to avoid sending two request batches to a carrier at the same time
            delay = int(((end / 10) * 10) - 10)
            # Get the common tracking carrier
            carrier = trackers[0].tracking_carrier
            # Collect the 5 trackers between the start and end indexes
            batch_trackers = trackers[start:end]
            tracking_numbers = [t.tracking_number for t in batch_trackers]
            options: dict = functools.reduce(
                lambda acc, t: {**acc, **(t.options or {})}, batch_trackers, {}
            )

            logger.debug(f"prepare tracking request for {tracking_numbers}")

            # Prepare and send tracking request(s) using the karrio interface.
            request: IRequestFrom = karrio.Tracking.fetch(
                datatypes.TrackingRequest(
                    tracking_numbers=tracking_numbers, options=options
                )
            )
            gateway: Gateway = carrier.gateway

            batches.append((gateway, request, delay, batch_trackers))

        except Exception as request_error:
            logger.warning(f"failed to prepare tracking batch ({start}, {end}) request")
            logger.error(request_error, exc_info=True)

        end += 10
        start += 10

    return batches


def fetch_tracking_info(request_batch: RequestBatches) -> BatchResponse:
    gateway, request, delay, trackers = request_batch
    logger.debug(f"fetching batch {[t.tracking_number for t in trackers]}")
    time.sleep(delay)  # apply delay before request

    try:
        return utils.identity(lambda: request.from_(gateway).parse())
    except Exception as request_error:
        logger.warning("batch request failed")
        logger.error(request_error, exc_info=True)

    return []


@utils.error_wrapper
def save_tracing_records(request_batches: typing.List[RequestBatches]):
    logger.info("> saving tracing records...")

    try:
        for request_batch in request_batches:
            gateway, _, __, trackers = request_batch

            if not any(trackers):
                continue

            context = serializers.get_object_context(trackers[0])
            tracing.bulk_save_tracing_records(gateway.tracer, context=context)
    except Exception as error:
        print(error)
        logger.warning("Failed failed saving tracing record...")
        logger.error(error, exc_info=True)


def save_updated_trackers(
    responses: typing.List[BatchResponse], trackers: typing.List[models.Tracking]
):
    logger.info("> saving updated trackers")

    for tracking_details, _ in responses:
        for details in tracking_details or []:
            try:
                logger.debug(f"update tracking info for {details.tracking_number}")
                related_trackers = [
                    t for t in trackers if t.tracking_number == details.tracking_number
                ]
                for tracker in related_trackers:
                    # update values only if changed; This is important for webhooks notification
                    changes = []
                    meta = details.meta or {}
                    status = utils.compute_tracking_status(details).value
                    events = utils.process_events(
                        response_events=details.events,
                        current_events=tracker.events,
                    )
                    options = {
                        **(tracker.options or {}),
                        tracker.tracking_number: details.meta,
                    }
                    info = lib.to_dict(details.info or {})

                    if events != tracker.events:
                        tracker.events = events
                        changes.append("events")

                    if options != tracker.options:
                        tracker.options = options
                        changes.append("options")

                    if details.meta != tracker.meta:
                        tracker.meta = meta
                        changes.append("meta")

                    if details.delivered != tracker.delivered:
                        tracker.delivered = details.delivered
                        changes.append("delivered")

                    if status != tracker.status:
                        tracker.status = status
                        changes.append("status")

                    if details.estimated_delivery != tracker.estimated_delivery:
                        tracker.estimated_delivery = details.estimated_delivery
                        changes.append("estimated_delivery")

                    if details.images is not None and (
                        details.images.delivery_image != tracker.delivery_image
                        or details.images.signature_image != tracker.signature_image
                    ):
                        changes.append("delivery_image")
                        changes.append("signature_image")
                        tracker.delivery_image = (
                            details.images.delivery_image or tracker.delivery_image
                        )
                        tracker.signature_image = (
                            details.images.signature_image or tracker.signature_image
                        )

                    if any(info.keys()) and info != tracker.info:
                        tracker.info = serializers.process_dictionaries_mutations(
                            ["info"], dict(info=info), tracker
                        )["info"]
                        changes.append("info")

                    if any(changes):
                        tracker.save(update_fields=changes)
                        serializers.update_shipment_tracker(tracker)
                        logger.debug(
                            f"tracking info {details.tracking_number} updated successfully"
                        )
                    else:
                        logger.debug(f"no changes detect")

            except Exception as update_error:
                logger.warning(
                    f"failed to update tracker with tracking number: {details.tracking_number}"
                )
                logger.error(update_error, exc_info=True)
