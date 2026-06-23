"""Karrio ParcelOne tracking implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.units as provider_units
import karrio.providers.parcelone.utils as provider_utils
import karrio.schemas.parcelone.tracking_response as tracking


def parse_tracking_response(
    _response: lib.Deserializable[list[tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    """Parse tracking response from ParcelOne TrackLMC REST API."""
    responses = _response.deserialize()
    messages: list[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        [],
    )

    tracking_details = [
        details
        for tracking_number, response in responses
        if (details := _extract_tracking_details(response, tracking_number, settings))
    ]

    return tracking_details, messages


def _extract_tracking_details(
    response: dict,
    tracking_number: str,
    settings: provider_utils.Settings,
) -> models.TrackingDetails | None:
    """Extract tracking details from TrackLMC response.

    The TrackLMC payload is flat: { P1Trackno, TrackingEvents: [...], ... }.
    """
    if not response or response.get("Error"):
        return None

    payload = lib.to_object(tracking.TrackingResponseType, response)
    raw_events = payload.TrackingEvents or []
    if not raw_events:
        return None

    events = sorted(
        [_parse_tracking_event(event) for event in raw_events],
        key=lambda e: e.timestamp or e.date or "",
        reverse=True,
    )

    latest = events[0]
    status = provider_units.TrackingStatus.find(latest.code)
    last_event = raw_events[-1]
    carrier_tracking_no = lib.failsafe(lambda: last_event.CarrierTrackno) or None
    carrier_track_url = lib.failsafe(lambda: last_event.CarrierTrackURL) or None

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=payload.P1Trackno or tracking_number,
        events=events,
        delivered=(status.name == "delivered") if status else False,
        status=status.name if status else None,
        info=models.TrackingInfo(
            carrier_tracking_link=carrier_track_url
            or settings.tracking_link.format(payload.P1Trackno or tracking_number),
        ),
        meta=lib.to_dict(
            dict(
                last_mile_carrier=lib.failsafe(lambda: last_event.Carrier) or None,
                last_mile_carrier_slug=lib.failsafe(lambda: last_event.CarrierSlug) or None,
                last_mile_tracking_number=carrier_tracking_no,
            )
        ),
    )


def _parse_tracking_event(event: tracking.TrackingEventType) -> models.TrackingEvent:
    """Parse a single TrackingEvent entry."""
    raw = event.EventdateUTC or event.EventdateCET or ""
    formats = ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"]
    status = provider_units.TrackingStatus.find(event.Statuscode)
    reason = provider_units.TrackingIncidentReason.find(event.Statuscode)

    return models.TrackingEvent(
        date=lib.fdate(raw, try_formats=formats),
        time=lib.flocaltime(raw, try_formats=formats),
        description=event.Status,
        code=event.Statuscode,
        location=event.Location,
        timestamp=lib.fiso_timestamp(raw, try_formats=formats),
        status=status.name if status else None,
        reason=reason.name if reason else None,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne TrackLMC tracking request.

    GET /shipment/{trackno} on the TrackLMC base URL — one call per tracking number.
    """
    requests = [dict(tracking_number=tracking_number) for tracking_number in payload.tracking_numbers]

    return lib.Serializable(requests, lib.to_dict)
