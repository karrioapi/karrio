import time
import logging
import datetime
from typing import List, cast, Tuple
from itertools import groupby

from django.conf import settings
from django.utils import timezone

import purplship
from purplship.core.utils import exec_parrallel, DP
from purplship.api.interface import Gateway, IRequestFrom
from purpleserver.core import datatypes
from purpleserver.core.utils import identity
from purpleserver.manager import models, serializers

logger = logging.getLogger(__name__)
Delay = int
RequestBatches = List[Tuple[Gateway, IRequestFrom, Delay, List[models.Tracking]]]
BatchResponse = List[datatypes.Tracking]

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(settings, 'DEFAULT_TRACKERS_UPDATE_INTERVAL', 10800)


def update_trackers(delta: datetime.timedelta = datetime.timedelta(seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL)):
    logger.info("> starting scheduled trackers update")
    time_threshold = timezone.now() - delta

    active_trackers = models.Tracking.objects.filter(delivered=False, updated_at__lt=time_threshold)

    if any(active_trackers):
        trackers_grouped_by_carrier = [list(g) for _, g in groupby(active_trackers, key=lambda t: t.carrier_id)]
        request_batches = sum([create_request_batches(group) for group in trackers_grouped_by_carrier], [])

        responses = exec_parrallel(fetch_tracking_info, request_batches, 2)
        save_updated_trackers(responses, active_trackers)
    else:
        logger.info("no active trackers found needing update")

    logger.info("> ending scheduled trackers update")


def create_request_batches(trackers: List[models.Tracking]) -> RequestBatches:
    start = 0
    end = 5
    batches = []

    while any(trackers[start:end]):
        try:
            # Add a request delay to avoid sending two request batches to a carrier at the same time
            delay = int(((end/5) * 10) - 10)
            # Get the common tracking carrier
            carrier = trackers[0].tracking_carrier
            # Collect the 5 trackers between the start and end indexes
            batch_trackers = trackers[start:end]
            tracking_numbers = [t.tracking_number for t in batch_trackers]

            logger.debug(f"prepare tracking request for {tracking_numbers}")

            # Prepare and send tracking request(s) using the purplship interface.
            request: IRequestFrom = purplship.Tracking.fetch(datatypes.TrackingRequest(tracking_numbers=tracking_numbers))
            gateway: Gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

            batches.append((gateway, request, delay, batch_trackers))

        except Exception as request_error:
            logger.warning(f'failed to prepare tracking batch ({start}, {end}) request')
            logger.error(request_error, exc_info=True)

        end += 5
        start += 5

    return batches


def fetch_tracking_info(request_batch: RequestBatches) -> BatchResponse:
    gateway, request, delay, trackers = request_batch
    logger.debug(f"fetching batch {[t.tracking_number for t in trackers]}")
    time.sleep(delay)  # apply delay before request

    try:
        tracking_details, messages = identity(lambda: request.from_(gateway).parse())
        return tracking_details
    except Exception as request_error:
        logger.warning('batch request failed')
        logger.error(request_error, exc_info=True)

    return []


def save_updated_trackers(responses: List[BatchResponse], trackers: List[models.Tracking]):
    logger.info('> saving updated trackers')

    for tracking_details in responses:

        for details in cast(List[datatypes.Tracking], tracking_details):
            try:
                logger.debug(f"update tracking info for {details.tracking_number}")

                related_trackers = [t for t in trackers if t.tracking_number == details.tracking_number]
                for tracker in related_trackers:
                    # update values only if changed; This is important for webhooks notification
                    changes = []
                    events = DP.to_dict(details.events)

                    if events != tracker.events:
                        tracker.events = events
                        changes.append('events')

                    if details.delivered != tracker.delivered:
                        tracker.delivered = details.delivered
                        changes.append('delivered')

                    if any(changes):
                        tracker.save(update_fields=changes)
                        serializers.update_shipment_tracker(tracker)
                        logger.debug(f"tracking info {details.tracking_number} updated successfully")
                    else:
                        logger.debug(f"no changes detect")

            except Exception as update_error:
                logger.warning(f'failed to update tracker with tracking number: {details.tracking_number}')
                logger.error(update_error, exc_info=True)
