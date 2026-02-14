"""
Tracking update pipeline.

Architecture:
    background_trackers_update (periodic cron)
        └─ update_trackers (dispatcher)
              └─ per carrier group → process_carrier_tracking_batch (Huey sub-task)
                    └─ process_carrier_trackers
                          └─ batches of 10 → fetch → save

The dispatcher (`update_trackers`) runs a single lightweight query to find
stale trackers, groups them by carrier, and enqueues one Huey sub-task per
carrier.  Each sub-task (`process_carrier_trackers`) fetches tracking info
in batches of 10 with a flat inter-batch delay — O(n) total wall-clock.
"""

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

import karrio.server.core.utils as utils
from karrio.server.core.logging import logger
from karrio.server.core.utils import resolve_carrier
import karrio.server.manager.models as models
import karrio.server.tracing.utils as tracing
import karrio.server.core.datatypes as datatypes
import karrio.server.manager.serializers as serializers

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(
    settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200
)
TRACKER_BATCH_SIZE = 10
TRACKER_BATCH_DELAY = int(getattr(settings, "TRACKER_BATCH_DELAY", 3))


# ─────────────────────────────────────────────────────────────────
# Dispatcher
# ─────────────────────────────────────────────────────────────────


def update_trackers(
    delta: datetime.timedelta = datetime.timedelta(
        seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL
    ),
    tracker_ids: typing.List[str] = [],
    schema: str = None,
):
    """Group stale trackers by carrier and enqueue one sub-task per carrier."""
    logger.info(
        "Starting tracker update dispatcher",
        delta_seconds=delta.total_seconds(),
        tracker_count=len(tracker_ids) if tracker_ids else 0,
    )

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

    sorted_data = sorted(active_tracker_data, key=lambda item: _carrier_id(item[1]))
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


# ─────────────────────────────────────────────────────────────────
# Per-carrier batch processor
# ─────────────────────────────────────────────────────────────────


def process_carrier_trackers(tracker_ids: typing.List[str], **kwargs):
    """Fetch tracking info for one carrier's trackers in batches of 10."""
    trackers = list(models.Tracking.objects.filter(id__in=tracker_ids))

    if not trackers:
        logger.info("No trackers found for given IDs", count=len(tracker_ids))
        return

    carrier = resolve_carrier(trackers[0].carrier or {}, context=None)

    if not carrier:
        logger.warning(
            "Could not resolve carrier for tracking batch",
            carrier_snapshot=trackers[0].carrier,
        )
        return

    gateway: Gateway = carrier.gateway
    total_batches = (len(trackers) + TRACKER_BATCH_SIZE - 1) // TRACKER_BATCH_SIZE

    logger.info(
        "Starting carrier tracking batch processing",
        carrier_id=trackers[0].carrier_id,
        total_trackers=len(trackers),
        total_batches=total_batches,
    )

    for i in range(0, len(trackers), TRACKER_BATCH_SIZE):
        batch = trackers[i : i + TRACKER_BATCH_SIZE]
        batch_num = (i // TRACKER_BATCH_SIZE) + 1

        _process_batch(gateway, batch, batch_num, total_batches)

        if i + TRACKER_BATCH_SIZE < len(trackers):
            time.sleep(TRACKER_BATCH_DELAY)

    logger.info(
        "Carrier tracking batch complete",
        carrier_id=trackers[0].carrier_id,
        total_processed=len(trackers),
    )


# ─────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────


def _carrier_id(carrier_snapshot: typing.Optional[dict]) -> str:
    if carrier_snapshot is None:
        return ""
    return carrier_snapshot.get("carrier_id") or ""


def _process_batch(
    gateway: Gateway,
    batch: typing.List[models.Tracking],
    batch_num: int,
    total_batches: int,
):
    """Fetch + save a single batch of up to 10 trackers."""
    try:
        tracking_numbers = [t.tracking_number for t in batch]
        options: dict = functools.reduce(
            lambda acc, t: {**acc, **(t.options or {})}, batch, {}
        )

        request = karrio.Tracking.fetch(
            datatypes.TrackingRequest(
                tracking_numbers=tracking_numbers, options=options
            )
        )
        response = request.from_(gateway).parse()

        _save_tracing(gateway, batch)
        _save_results(response, batch)

        logger.info(
            "Tracking batch processed",
            batch=f"{batch_num}/{total_batches}",
            count=len(batch),
        )

    except Exception as e:
        logger.warning(
            "Tracking batch failed",
            batch=f"{batch_num}/{total_batches}",
            error=str(e),
        )
        logger.exception("Tracking batch error")


def _save_results(response, batch: typing.List[models.Tracking]):
    """Persist tracking details for a single batch."""
    tracking_details, _ = response if response else ([], [])

    for details in tracking_details or []:
        try:
            for tracker in batch:
                if tracker.tracking_number != details.tracking_number:
                    continue

                serializers.update_tracker(
                    tracker,
                    dict(
                        events=details.events,
                        delivered=details.delivered,
                        status=utils.compute_tracking_status(details).value,
                        estimated_delivery=details.estimated_delivery,
                        options={
                            **(tracker.options or {}),
                            tracker.tracking_number: details.meta,
                        },
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
                "Tracker update error",
                tracking_number=details.tracking_number,
            )


def _save_tracing(gateway: Gateway, batch: typing.List[models.Tracking]):
    """Persist API tracing records for a single batch."""
    try:
        context = serializers.get_object_context(batch[0])
        tracing.bulk_save_tracing_records(gateway.tracer, context=context)
    except Exception as e:
        logger.warning("Failed to save tracing records", error=str(e))
