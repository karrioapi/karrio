"""Karrio Asendia tracking API implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.asendia.error as error
import karrio.providers.asendia.units as provider_units
import karrio.providers.asendia.utils as provider_utils
import karrio.schemas.asendia.tracking_response as asendia_res


def _match_status(code: str) -> str | None:
    """Match code against TrackingStatus enum values."""
    if not code:
        return None
    for status in list(provider_units.TrackingStatus):
        if code in status.value:
            return status.name
    return None


def _match_reason(code: str) -> str | None:
    """Match code against TrackingIncidentReason enum values."""
    if not code:
        return None
    for reason in list(provider_units.TrackingIncidentReason):
        if code in reason.value:
            return reason.name
    return None


def parse_tracking_response(
    _response: lib.Deserializable[list[tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> tuple[list[models.TrackingDetails], list[models.Message]]:
    """Parse tracking response from Asendia API."""
    responses = _response.deserialize()

    messages: list[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(response, settings, tracking_number)
        for tracking_number, response in responses
        if isinstance(response, list) and len(response) > 0
    ]

    return tracking_details, messages


def _extract_details(
    events_list: list,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from Asendia bare-array response."""
    # API returns a bare list of TrackingEvent objects; tracking_number comes from the proxy tuple
    raw_events = [lib.to_object(asendia_res.TrackingEventType, e) for e in events_list]

    # Sort events (most recent first)
    sorted_events = sorted(
        raw_events,
        key=lambda e: e.time or "",
        reverse=True,
    )

    # Build events list
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.time, "%Y-%m-%dT%H:%M:%SZ"),
            time=lib.flocaltime(event.time, "%Y-%m-%dT%H:%M:%SZ"),
            description=event.carrierEventDescription,
            code=event.code,
            location=lib.join(
                event.locationName,
                event.locationCountry,
                join=True,
                separator=", ",
            ),
            # REQUIRED: ISO 8601 timestamp
            timestamp=lib.fiso_timestamp(
                event.time,
                current_format="%Y-%m-%dT%H:%M:%SZ",
            ),
            # REQUIRED: Normalized status at event level
            status=_match_status(event.code),
            # Incident reason for delivery exceptions
            reason=_match_reason(event.code),
        )
        for event in sorted_events
    ]

    # Determine overall status from latest event
    latest_event = events[0] if events else None
    status = latest_event.status if latest_event else None
    status = status or provider_units.TrackingStatus.in_transit.name

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=events,
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for Asendia API.

    Asendia uses GET /api/customers/{customerId}/tracking/{trackingNumber}
    The proxy handles concurrent requests for multiple tracking numbers.
    """
    return lib.Serializable(payload.tracking_numbers)
