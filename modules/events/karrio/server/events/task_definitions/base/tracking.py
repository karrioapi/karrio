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

import datetime
import functools
import time
from itertools import groupby

import karrio.lib as lib
import karrio.sdk as karrio
import karrio.server.core.datatypes as datatypes
import karrio.server.core.utils as utils
import karrio.server.manager.models as models
import karrio.server.manager.serializers as serializers
import karrio.server.tracing.utils as tracing
from django.conf import settings
from django.utils import timezone
from karrio.api.gateway import Gateway
from karrio.server.core.logging import logger
from karrio.server.core.utils import resolve_carrier

DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200)
TRACKER_BATCH_SIZE = 10
TRACKER_BATCH_DELAY = int(getattr(settings, "TRACKER_BATCH_DELAY", 3))
TRACKER_MAX_ACTIVE_DAYS = int(getattr(settings, "TRACKER_MAX_ACTIVE_DAYS", 90))


# ─────────────────────────────────────────────────────────────────
# Dispatcher
# ─────────────────────────────────────────────────────────────────


def _get_max_active_days() -> int:
    """Return the live TRACKER_MAX_ACTIVE_DAYS value from constance (falls back to settings)."""
    try:
        from constance import config as constance_config
        return int(getattr(constance_config, "TRACKER_MAX_ACTIVE_DAYS", TRACKER_MAX_ACTIVE_DAYS))
    except Exception:
        return TRACKER_MAX_ACTIVE_DAYS


def _retire_aged_out_trackers(max_age_cutoff: datetime.datetime) -> int:
    """Mark trackers older than max_age_cutoff as retired.

    Sets status='unknown' and delivered=None so they are excluded from the
    ``delivered=False`` filter on the next polling cycle.
    """
    return models.Tracking.objects.filter(
        delivered=False,
        is_archived=False,  # belt-and-suspenders: manager already excludes archived
        created_at__lt=max_age_cutoff,
    ).update(
        status="unknown",
        delivered=None,
        updated_at=timezone.now(),
    )


def update_trackers(
    delta: datetime.timedelta = datetime.timedelta(seconds=DEFAULT_TRACKERS_UPDATE_INTERVAL),
    tracker_ids: list[str] | None = None,
    schema: str = None,
):
    """Group stale trackers by carrier and enqueue one sub-task per carrier."""
    max_active_days = _get_max_active_days()
    max_age_cutoff = timezone.now() - datetime.timedelta(days=max_active_days)

    logger.info(
        "Starting tracker update dispatcher",
        delta_seconds=delta.total_seconds(),
        tracker_count=len(tracker_ids) if tracker_ids else 0,
        max_active_days=max_active_days,
    )

    # Retire trackers that have exceeded the maximum active age
    if not tracker_ids:
        retired = _retire_aged_out_trackers(max_age_cutoff)
        if retired:
            logger.info(
                "Retired aged-out trackers",
                count=retired,
                max_active_days=max_active_days,
            )

    qs = (
        models.Tracking.objects.filter(id__in=tracker_ids)
        if tracker_ids
        else models.Tracking.objects.filter(
            delivered=False,
            is_archived=False,  # belt-and-suspenders: manager already excludes archived
            updated_at__lt=timezone.now() - delta,
            created_at__gt=max_age_cutoff,
        )
    )
    # Stream the rows and keep only (id, carrier_id) — NOT the full carrier JSON
    # snapshot per row — so a large stale backlog doesn't spike memory here (#641).
    active = [(tid, _carrier_id(carrier)) for tid, carrier in qs.values_list("id", "carrier").iterator(chunk_size=2000)]

    if not active:
        logger.info("No active trackers found needing update")
        return

    active.sort(key=lambda item: item[1])
    carrier_groups = 0

    for carrier_key, group in groupby(active, key=lambda item: item[1]):
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
        total_trackers=len(active),
        carrier_groups=carrier_groups,
    )


# ─────────────────────────────────────────────────────────────────
# Per-carrier batch processor
# ─────────────────────────────────────────────────────────────────


def process_carrier_trackers(tracker_ids: list[str], **kwargs):
    """Fetch tracking info for one carrier's trackers in batches of 10.

    Trackers are loaded ONE batch at a time (not all up-front) so a large
    per-carrier backlog can't spike the worker's memory — full Tracking rows
    carry events/messages JSON, so materialising tens of thousands of them at
    once OOM-killed the worker (#641). Only ``tracker_ids`` (lightweight) and the
    current ≤10-row batch are ever resident. All ids in one dispatch belong to
    the same carrier (the dispatcher groups by carrier), so the gateway is
    resolved once from the first batch and reused.
    """
    total = len(tracker_ids)
    total_batches = (total + TRACKER_BATCH_SIZE - 1) // TRACKER_BATCH_SIZE
    gateway: Gateway | None = None
    carrier_id = None
    processed = 0
    batch_num = 0

    for i in range(0, total, TRACKER_BATCH_SIZE):
        batch = list(models.Tracking.objects.filter(id__in=tracker_ids[i : i + TRACKER_BATCH_SIZE]))
        if not batch:
            continue

        if gateway is None:
            carrier = resolve_carrier(batch[0].carrier or {}, context=None)
            if not carrier:
                logger.warning(
                    "Could not resolve carrier for tracking batch",
                    carrier_snapshot=batch[0].carrier,
                )
                return
            gateway = carrier.gateway
            carrier_id = batch[0].carrier_id
            logger.info(
                "Starting carrier tracking batch processing",
                carrier_id=carrier_id,
                total_trackers=total,
                total_batches=total_batches,
            )

        batch_num += 1
        _process_batch(gateway, batch, batch_num, total_batches)
        processed += len(batch)

        if i + TRACKER_BATCH_SIZE < total:
            time.sleep(TRACKER_BATCH_DELAY)

    if gateway is None:
        logger.info("No trackers found for given IDs", count=total)
        return

    logger.info(
        "Carrier tracking batch complete",
        carrier_id=carrier_id,
        total_processed=processed,
    )


# ─────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────


def _carrier_id(carrier_snapshot: dict | None) -> str:
    if carrier_snapshot is None:
        return ""
    return carrier_snapshot.get("carrier_id") or ""


def _process_batch(
    gateway: Gateway,
    batch: list[models.Tracking],
    batch_num: int,
    total_batches: int,
):
    """Fetch + save a single batch of up to 10 trackers."""
    try:
        tracking_numbers = [t.tracking_number for t in batch]
        options: dict = functools.reduce(lambda acc, t: {**acc, **(t.options or {})}, batch, {})

        request = karrio.Tracking.fetch(datatypes.TrackingRequest(tracking_numbers=tracking_numbers, options=options))
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


def _save_results(response, batch: list[models.Tracking]):
    """Persist tracking details for a single batch using bulk operations.

    Applies change detection in memory for each tracker, then saves all
    changed trackers in a single bulk_update call to avoid N+1 UPDATE queries.
    """
    tracking_details, _ = response if response else ([], [])
    changed_trackers = []

    for details in tracking_details or []:
        try:
            tracker = next(
                (t for t in batch if t.tracking_number == details.tracking_number),
                None,
            )
            if tracker is None:
                continue

            changes = serializers.apply_tracker_changes(
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

            if changes:
                changed_trackers.append((tracker, changes))

        except Exception as e:
            logger.warning(
                "Failed to apply tracker changes",
                tracking_number=details.tracking_number,
                error=str(e),
            )
            logger.exception(
                "Tracker change error",
                tracking_number=details.tracking_number,
            )

    # Single bulk save for all changed trackers + batch shipment status updates
    try:
        serializers.bulk_save_trackers(changed_trackers)
    except Exception as e:
        logger.warning("Bulk save failed, falling back to individual saves", error=str(e))
        for tracker, changes in changed_trackers:
            try:
                tracker.save(update_fields=changes)
                serializers.update_shipment_tracker(tracker)
            except Exception as inner_e:
                logger.exception(
                    "Fallback save failed",
                    tracker_id=tracker.id,
                    error=str(inner_e),
                )


def _save_tracing(gateway: Gateway, batch: list[models.Tracking]):
    """Persist API tracing records for a single batch."""
    try:
        context = serializers.get_object_context(batch[0])
        tracing.bulk_save_tracing_records(gateway.tracer, context=context)
    except Exception as e:
        logger.warning("Failed to save tracing records", error=str(e))
