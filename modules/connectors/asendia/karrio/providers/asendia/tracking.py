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
    # Convert to typed object
    tracking = lib.to_object(asendia_res.TrackingResponseType, data)

    # Use tracking number from response or fallback to request
    number = tracking.trackingNumber or tracking_number

    # Extract and sort events (most recent first)
    events = []
    sorted_events = []
    if tracking.trackingEvents:
        sorted_events = sorted(
            tracking.trackingEvents,
            key=lambda e: e.time or "",
            reverse=True,
        )
        events = [
            models.TrackingEvent(
                date=lib.fdate(event.time, "%Y-%m-%dT%H:%M:%SZ"),
                time=lib.ftime(event.time, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.carrierEventDescription,
                code=event.code,
                location=lib.join(
                    event.locationName,
                    event.locationCountry,
                    join=True,
                    separator=", ",
                ),
            )
            for event in sorted_events
        ]

    # Determine status from latest event (first in sorted list)
    latest_event = sorted_events[0] if sorted_events else None
    status = provider_units.parse_tracking_status(
        latest_event.code if latest_event else None,
        latest_event.carrierEventDescription if latest_event else None,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=number,
        events=events,
        delivered=status == provider_units.TrackingStatus.delivered,
        status=status.name,
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
