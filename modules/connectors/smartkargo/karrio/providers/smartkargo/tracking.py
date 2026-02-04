"""Karrio SmartKargo tracking API implementation."""

import karrio.schemas.smartkargo.tracking_response as smartkargo_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils
import karrio.providers.smartkargo.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
        if _has_valid_tracking(details)
    ]

    return tracking_details, messages


def _has_valid_tracking(data: dict) -> bool:
    """Check if the response contains valid tracking data."""
    # SmartKargo returns an array of events or an error object
    if isinstance(data, list) and any(data):
        return True
    return False


def _extract_details(
    data: typing.List[dict],
    settings: provider_utils.Settings,
    tracking_number: str,
) -> models.TrackingDetails:
    """Extract tracking details from SmartKargo tracking response.

    SmartKargo returns an array of tracking events, each with:
    - eventType: status code (BKD, RCS, DEP, DDL, etc.)
    - eventDate: ISO datetime string
    - eventLocation: location code
    - description: human-readable description
    """
    # Convert events to typed objects
    events = [
        lib.to_object(smartkargo_res.TrackingResponseElementType, event)
        for event in data
    ]

    # Sort events by date (most recent first)
    sorted_events = sorted(
        events,
        key=lambda e: e.eventDate or "",
        reverse=True,
    )

    # Get latest event for status
    latest_event = sorted_events[0] if sorted_events else None
    latest_status_code = latest_event.eventType if latest_event else ""

    # Map carrier status to karrio standard tracking status
    status = next(
        (
            s.name
            for s in list(provider_units.TrackingStatus)
            if latest_status_code in s.value
        ),
        "in_transit",
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m-%dT%H:%M:%S"),
                description=event.description,
                code=event.eventType,
                time=lib.ftime(event.eventDate, "%Y-%m-%dT%H:%M:%S"),
                location=event.eventLocation,
                timestamp=lib.fiso_timestamp(
                    event.eventDate,
                    current_format="%Y-%m-%dT%H:%M:%S",
                ),
                status=next(
                    (
                        s.name
                        for s in list(provider_units.TrackingStatus)
                        if event.eventType in s.value
                    ),
                    None,
                ),
                reason=next(
                    (
                        r.name
                        for r in list(provider_units.TrackingIncidentReason)
                        if event.eventType in r.value
                    ),
                    None,
                ),
            )
            for event in sorted_events
        ],
        estimated_delivery=None,
        delivered=(status == "delivered"),
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
        ),
        meta=dict(
            prefix=latest_event.prefix if latest_event else None,
            air_waybill=latest_event.airWaybill if latest_event else None,
            package_reference=latest_event.packageReference if latest_event else None,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for SmartKargo API.

    SmartKargo tracking uses GET with packageReference query parameter.
    The proxy handles the actual HTTP request format.
    """
    # Build list of tracking request payloads
    request = [
        dict(tracking_number=tracking_number)
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
