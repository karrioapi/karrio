"""Karrio MyDHL tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units
import karrio.schemas.mydhl.tracking_response as mydhl_res


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
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """
    Extract tracking details from MyDHL tracking response

    data: The MyDHL tracking response data
    settings: The carrier connection settings
    tracking_number: The tracking number being tracked

    Returns a TrackingDetails object with extracted tracking information
    """
    # Convert to typed object using generated schema
    tracking_response = lib.to_object(mydhl_res.TrackingResponseType, data)

    # Get the first shipment (MyDHL returns array of shipments)
    shipment = next(
        (s for s in (tracking_response.shipments or []) if s),
        None
    )

    if not shipment:
        return models.TrackingDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking_number=tracking_number,
            events=[],
        )

    # Extract events using functional pattern
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.date) if event.date else None,
            description=event.description or "",
            code=event.typeCode or "",
            time=lib.flocaltime(event.time) if event.time else None,
            location=(
                event.serviceArea[0].description
                if event.serviceArea and len(event.serviceArea) > 0
                else None
            ),
        )
        for event in (shipment.events or [])
    ]

    # Map MyDHL status to Karrio standard status
    status = provider_units.TrackingStatus.map(
        shipment.status or "in_transit"
    ).name

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number or str(shipment.shipmentTrackingNumber),
        events=events,
        estimated_delivery=(
            lib.fdate(shipment.estimatedTimeOfDelivery)
            if shipment.estimatedTimeOfDelivery
            else None
        ),
        delivered=(status == "delivered"),
        status=status,
        meta=dict(
            product_code=shipment.productCode,
            shipment_timestamp=shipment.shipmentTimestamp,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a tracking request for MyDHL API

    MyDHL uses GET with path parameters, so we just return the tracking numbers.

    payload: The standardized TrackingRequest from karrio
    settings: The carrier connection settings

    Returns tracking numbers as a serializable list
    """
    # MyDHL tracking uses GET /shipments/{trackingNumber}/tracking
    # So we just return the list of tracking numbers
    return lib.Serializable(payload.tracking_numbers)
