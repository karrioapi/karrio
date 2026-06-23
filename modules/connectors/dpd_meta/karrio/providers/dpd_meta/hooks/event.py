"""Karrio DPD Meta Tracking Push (webhook) event processing."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dpd_meta.units as provider_units
import karrio.providers.dpd_meta.utils as provider_utils


def on_webhook_event(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> tuple[models.WebhookEventDetails, list[models.Message]]:
    """Parse a DPD Tracking Push GET notification → tracking event + ack.

    See SPECS.md › Tracking Push (webhook).
    """
    query = {key: (value[-1] if isinstance(value, list) else value) for key, value in (payload.query or {}).items()}

    pushid = query.get("pushid")
    pnr = query.get("pnr")
    code = query.get("status")

    # Unknown/missing code → None so update_tracker leaves the stored status be.
    status = next(
        (s.name for s in provider_units.PushTrackingStatus if code and code in s.value),
        None,
    )
    delivered = status == provider_units.PushTrackingStatus.delivered.name

    statusdate = query.get("statusdate")  # best-effort; failsafe so a bad value can't 500
    event_date = lib.failsafe(lambda: lib.fdate(statusdate, "%d%m%Y%H%M%S"))
    event_time = lib.failsafe(lambda: lib.flocaltime(statusdate, "%d%m%Y%H%M%S"))

    tracking = (
        models.TrackingDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking_number=pnr,
            status=status,
            delivered=delivered or None,
            events=[
                models.TrackingEvent(
                    date=event_date,
                    time=event_time,
                    code=code,
                    description=provider_units.PUSH_STATUS_DESCRIPTIONS.get(code, code),
                    location=query.get("depot"),
                )
            ],
            info=models.TrackingInfo(
                carrier_tracking_link=settings.tracking_url.format(pnr),
                shipment_service=query.get("services"),
                signed_by=query.get("receiver"),
            ),
            meta=lib.to_dict(
                dict(
                    pushid=pushid,
                    depot=query.get("depot"),
                    reference=query.get("ref"),
                    services=query.get("services"),
                    pod=query.get("pod"),
                )
            ),
        )
        if pnr
        else None
    )

    details = models.WebhookEventDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=pnr,
        tracking=tracking,
        # Mandatory DPD receipt (echo pushid) — always returned, even on no match.
        response=f"<push><pushid>{pushid or ''}</pushid><status>OK</status></push>",
        response_format="xml",
    )

    return details, []
