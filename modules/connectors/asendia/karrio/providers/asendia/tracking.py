"""Karrio Asendia tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia.error as error
import karrio.providers.asendia.utils as provider_utils
import karrio.providers.asendia.units as provider_units
import karrio.schemas.asendia.tracking_response as asendia_res


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse tracking response from Asendia API."""
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
        if details.get("trackingNumber") or details.get("trackingEvents")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from Asendia response."""
    tracking = lib.to_object(asendia_res.TrackingResponseType, data)
    number = tracking.trackingNumber or tracking_number

    # Sort events (most recent first)
    sorted_events = sorted(
        tracking.trackingEvents or [],
        key=lambda e: e.time or "",
        reverse=True,
    )

    # Get latest event for overall status
    latest_event = next(iter(sorted_events), None)

    # Determine overall status using next() pattern
    status = next(
        (
            s.name
            for s in list(provider_units.TrackingStatus)
            if latest_event and latest_event.code in s.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=number,
        events=[
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
                status=next(
                    (
                        s.name
                        for s in list(provider_units.TrackingStatus)
                        if event.code in s.value
                    ),
                    None,
                ),
                # REQUIRED: Incident reason for delivery exceptions
                reason=next(
                    (
                        r.name
                        for r in list(provider_units.TrackingIncidentReason)
                        if event.code in r.value
                    ),
                    None,
                ),
            )
            for event in sorted_events
        ],
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
