"""Karrio Spring tracking API implementation."""

import karrio.schemas.spring.tracking_request as spring_req
import karrio.schemas.spring.tracking_response as spring_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.spring.error as error
import karrio.providers.spring.utils as provider_utils
import karrio.providers.spring.units as provider_units


def _match_status(code: str) -> typing.Optional[str]:
    """Match code against TrackingStatus enum values."""
    if not code:
        return None
    for status in list(provider_units.TrackingStatus):
        if code in status.value:
            return status.name
    return None


def _match_reason(code: str) -> typing.Optional[str]:
    """Match code against TrackingIncidentReason enum values."""
    if not code:
        return None
    for reason in list(provider_units.TrackingIncidentReason):
        if code in reason.value:
            return reason.name
    return None


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse TrackShipment responses from Spring API."""
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    # Only extract details for successful responses (ErrorLevel 0)
    tracking_details = [
        _extract_details(response, settings, tracking_number)
        for tracking_number, response in responses
        if response.get("ErrorLevel") == 0 and response.get("Shipment")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from Spring API response."""
    response = lib.to_object(spring_res.TrackingResponseType, data)
    shipment = response.Shipment

    # Get events and reverse to have most recent first
    events = list(reversed(shipment.Events or []))

    # Get latest event code for status mapping
    latest_code = str(events[0].Code) if events else None

    # Map carrier status to karrio standard tracking status
    status = _match_status(latest_code) or provider_units.TrackingStatus.in_transit.name

    # Build tracking events with all required fields per CARRIER_INTEGRATION_GUIDE.md
    tracking_events = [
        models.TrackingEvent(
            date=lib.fdate(event.DateTime, "%Y-%m-%d %H:%M:%S"),
            description=event.Description,
            code=str(event.Code) if event.Code else None,
            time=lib.flocaltime(event.DateTime, "%Y-%m-%d %H:%M:%S"),
            location=lib.join(event.City, event.State, event.Country, join=True, separator=", "),
            # REQUIRED: timestamp in ISO 8601 format
            timestamp=lib.fiso_timestamp(
                event.DateTime,
                current_format="%Y-%m-%d %H:%M:%S",
            ),
            # REQUIRED: normalized status at event level
            status=_match_status(str(event.Code)),
            # Incident reason for exception events
            reason=_match_reason(str(event.Code)),
        )
        for event in events
    ]

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.TrackingNumber or tracking_number,
        events=tracking_events,
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=shipment.CarrierTrackingUrl,
            package_weight=shipment.Weight,
            package_weight_unit=shipment.WeightUnit,
        ),
        meta=dict(
            service=shipment.Service,
            carrier=shipment.Carrier,
            display_id=shipment.DisplayId,
            shipper_reference=shipment.ShipperReference,
            carrier_tracking_number=shipment.CarrierTrackingNumber,
            carrier_local_tracking_number=shipment.CarrierLocalTrackingNumber,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create TrackShipment requests for Spring API.

    Spring API tracks one shipment at a time, so we create a list of requests
    for each tracking number.
    """
    # Create individual requests for each tracking number using generated schema types
    requests = [
        spring_req.TrackingRequestType(
            Apikey=settings.api_key,
            Command="TrackShipment",
            Shipment=spring_req.ShipmentType(
                TrackingNumber=tracking_number,
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(requests, lambda reqs: [lib.to_dict(r) for r in reqs])
