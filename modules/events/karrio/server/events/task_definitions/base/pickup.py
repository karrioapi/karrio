import datetime
from django.utils import timezone

from karrio.server.core.logging import logger
import karrio.server.manager.models as models


def close_past_pickups():
    """Auto-close one_time pickups whose pickup_date has passed.

    Only closes pickups that are:
    - Still in "scheduled" status
    - Have pickup_type == "one_time" (stored in meta)
    - Have a pickup_date strictly before today

    Recurring and daily pickups without an end_date are excluded to avoid
    prematurely closing open-ended recurring schedules.
    """
    today = timezone.now().date()

    # Get all scheduled pickups with pickup_date in the past
    past_pickups = models.Pickup.objects.filter(
        status="scheduled",
        pickup_date__lt=today,
    )

    # Separate one_time pickups (always close) from recurring/daily pickups
    one_time_ids = []
    recurring_expired_ids = []

    for pickup in past_pickups.values("id", "meta"):
        meta = pickup.get("meta") or {}
        pickup_type = meta.get("pickup_type", "one_time")

        if pickup_type == "one_time":
            one_time_ids.append(pickup["id"])
        elif pickup_type in ("daily", "recurring"):
            # Only close recurring/daily pickups that have an explicit end_date
            # that has passed. Leave open-ended recurring pickups alone.
            recurrence = meta.get("recurrence") or {}
            end_date_str = recurrence.get("end_date")

            if end_date_str:
                try:
                    end_date = datetime.date.fromisoformat(end_date_str)
                    if end_date < today:
                        recurring_expired_ids.append(pickup["id"])
                except (ValueError, TypeError):
                    pass

    ids_to_close = one_time_ids + recurring_expired_ids

    if not ids_to_close:
        logger.info("No past pickups to auto-close")
        return

    count = models.Pickup.objects.filter(id__in=ids_to_close).update(
        status="closed",
    )

    logger.info(
        "Auto-closed past pickups",
        count=count,
        one_time=len(one_time_ids),
        recurring_expired=len(recurring_expired_ids),
    )
