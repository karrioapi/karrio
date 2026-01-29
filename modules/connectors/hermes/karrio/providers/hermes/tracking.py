"""Karrio Hermes tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hermes.error as error
import karrio.providers.hermes.utils as provider_utils
import karrio.providers.hermes.units as provider_units
import karrio.schemas.hermes.tracking_response as hermes_res


def _match_status(code: str) -> typing.Optional[str]:
    """Match Hermes event code against TrackingStatus enum values."""
    if not code:
        return None
    for status in list(provider_units.TrackingStatus):
        if code in status.value:
            return status.name
    return None


def _match_reason(code: str) -> typing.Optional[str]:
    """Match Hermes event code against TrackingIncidentReason enum values."""
    if not code:
        return None
    for reason in list(provider_units.TrackingIncidentReason):
        if code in reason.value:
            return reason.name
    return None


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse tracking response from Hermes Shipment Info API."""
    response = _response.deserialize()

    # Parse the response using generated schema
    tracking_response = lib.to_object(hermes_res.TrackingResponseType, response)

    # Collect error messages
    messages: typing.List[models.Message] = []

    # Extract tracking details for each shipment
    tracking_details: typing.List[models.TrackingDetails] = []

    for shipment_info in tracking_response.shipmentinfo or []:
        # Check for errors in individual shipment result
        if shipment_info.result and shipment_info.result.code:
            if shipment_info.result.code.startswith("e"):
                messages.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        code=shipment_info.result.code,
                        message=shipment_info.result.message or "",
                        details=dict(shipment_id=shipment_info.shipmentID),
                    )
                )
                continue

        # Extract tracking details
        details = _extract_details(shipment_info, settings)
        if details:
            tracking_details.append(details)

    return tracking_details, messages


def _extract_details(
    shipment_info: hermes_res.ShipmentinfoType,
    settings: provider_utils.Settings,
) -> typing.Optional[models.TrackingDetails]:
    """Extract tracking details from Hermes shipment info."""
    if not shipment_info.shipmentID:
        return None

    # Get status events (already in chronological order, most recent last in API)
    # Reverse to have most recent first for Karrio convention
    status_list = list(reversed(shipment_info.status or []))

    # Get latest event code for overall status
    latest_code = status_list[0].code if status_list else None
    overall_status = _match_status(latest_code) or provider_units.TrackingStatus.in_transit.name

    # Build tracking events with all required fields per CARRIER_INTEGRATION_GUIDE.md
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%S%z"),
            time=lib.flocaltime(event.timestamp, "%Y-%m-%dT%H:%M:%S%z"),
            description=event.description or "",
            code=event.code,
            location=lib.join(
                event.scanningUnit.city if event.scanningUnit else None,
                event.scanningUnit.countryCode if event.scanningUnit else None,
                join=True,
                separator=", ",
            ),
            # REQUIRED: timestamp in ISO 8601 format (already provided by Hermes)
            timestamp=event.timestamp,
            # REQUIRED: normalized status at event level
            status=_match_status(event.code),
            # Incident reason for exception events
            reason=_match_reason(event.code),
        )
        for event in status_list
    ]

    # Build delivery forecast info if available
    estimated_delivery = None
    if shipment_info.deliveryForecast and shipment_info.deliveryForecast.date:
        estimated_delivery = shipment_info.deliveryForecast.date

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment_info.shipmentID,
        events=events,
        delivered=overall_status == "delivered",
        status=overall_status,
        estimated_delivery=estimated_delivery,
        info=models.TrackingInfo(
            carrier_tracking_link=shipment_info.trackingLink,
            customer_name=None,
            shipment_destination_country=(
                shipment_info.receiverAddress.countryCode
                if shipment_info.receiverAddress
                else None
            ),
            shipment_destination_postal_code=(
                str(shipment_info.receiverAddress.zipCode)
                if shipment_info.receiverAddress and shipment_info.receiverAddress.zipCode
                else None
            ),
        ),
        meta=dict(
            client_id=shipment_info.clientID,
            client_reference=shipment_info.clientReference,
            client_reference2=shipment_info.clientReference2,
            part_number=shipment_info.partNumber,
            international_shipment_id=shipment_info.internationalShipmentID,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking request for Hermes Shipment Info API.

    Hermes uses GET requests with query parameters, so we just return
    the tracking numbers to be used as shipmentID query params.
    """
    return lib.Serializable(payload.tracking_numbers)
