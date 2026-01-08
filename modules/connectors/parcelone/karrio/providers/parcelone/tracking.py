"""Karrio ParcelOne tracking implementation."""

import typing
import karrio.schemas.parcelone as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse tracking response from ParcelOne TrackLMC REST API."""
    responses = _response.deserialize()
    messages: typing.List[models.Message] = []
    tracking_details: typing.List[models.TrackingDetails] = []

    for tracking_number, response in responses:
        # Parse errors for this response
        response_messages = error.parse_error_response(
            response,
            settings,
            tracking_number=tracking_number,
        )
        messages.extend(response_messages)

        # Extract tracking details if successful
        if response.get("success") == 1 and response.get("results"):
            details = _extract_tracking_details(
                response.get("results"),
                tracking_number,
                settings,
            )
            if details:
                tracking_details.append(details)

    return tracking_details, messages


def _extract_tracking_details(
    result: dict,
    tracking_number: str,
    settings: provider_utils.Settings,
) -> typing.Optional[models.TrackingDetails]:
    """Extract tracking details from API response."""
    tracking_result = lib.to_object(parcelone.TrackingResultType, result)

    # Parse events
    events = sorted(
        [
            _parse_tracking_event(event)
            for event in (tracking_result.Events or [])
        ],
        key=lambda e: e.timestamp or e.date or "",
        reverse=True,
    )

    if not events:
        return None

    latest_event = events[0] if events else None
    status = lib.identity(
        provider_units.TrackingStatus.find(
            tracking_result.StatusCode or (latest_event.code if latest_event else None)
        )
    )

    return models.TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        events=events,
        delivered=(status.name == "delivered") if status else False,
        status=status.name if status else None,
        estimated_delivery=lib.fdate(tracking_result.EstimatedDelivery),
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_link.format(tracking_number),
            signed_by=tracking_result.SignedBy,
        ),
        meta=dict(
            carrier_tracking_id=tracking_result.CarrierTrackingID,
            last_mile_carrier=tracking_result.CarrierIDLMC,
        ),
    )


def _parse_tracking_event(event: parcelone.TrackingEventType) -> models.TrackingEvent:
    """Parse a single tracking event."""
    datetime_str = event.DateTime or ""
    date = lib.fdate(
        datetime_str,
        try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
    )
    time = lib.flocaltime(
        datetime_str,
        try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"],
    )
    status = provider_units.TrackingStatus.find(event.StatusCode)

    return models.TrackingEvent(
        date=date,
        time=time,
        description=event.Description or event.Status,
        code=event.StatusCode,
        location=event.Location,
        timestamp=lib.fiso_timestamp(
            datetime_str,
            current_format="%Y-%m-%dT%H:%M:%S",
        ),
        status=status.name if status else None,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne tracking request.

    The TrackLMC API uses: GET /tracking/{CarrierIDLMC}/{TrackingID}
    For ParcelOne tracking numbers, CarrierIDLMC is typically not needed
    as the tracking ID encodes the carrier information.
    """
    # For each tracking number, we'll need to make a separate API call
    # The carrier_id can be passed as an option if known
    requests = [
        dict(
            tracking_id=tracking_number,
            carrier_id=lib.identity(
                payload.options.get("carrier_id")
                or payload.options.get(f"{tracking_number}_carrier_id")
                or "PA1"  # Default to ParcelOne
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(requests, lib.to_dict)
