"""Karrio Teleship tracking API implementation."""

import karrio.schemas.teleship.tracking_response as teleship_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    # Aggregate error messages using functional sum pattern
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, **dict(tracking_number=tracking_number))
            for tracking_number, response in responses
        ],
        start=[],
    )

    # Extract tracking details using list comprehension (skip error responses)
    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
        if details and not details.get("messages")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data"""
    # Convert to typed object for safe attribute access
    tracking = lib.to_object(teleship_res.TrackingResponseType, data)

    # Extract events using functional list comprehension
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") if event.timestamp else None,
            time=lib.ftime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ", "%H:%M:%S") if event.timestamp else None,
            description=event.description or "",
            code=event.status or "",
            location=event.location or "",
        )
        for event in (tracking.events or [])
    ]

    # Map carrier status to karrio standard using functional pattern
    status = provider_units.TrackingStatus.map(tracking.status or "").name_or_key

    # Build location string from shipFrom and shipTo
    ship_from_location = lib.identity(
        ", ".join(filter(None, [
            tracking.shipFrom.city if tracking.shipFrom else None,
            tracking.shipFrom.country if tracking.shipFrom else None,
        ]))
        if tracking.shipFrom else None
    )

    ship_to_location = lib.identity(
        ", ".join(filter(None, [
            tracking.shipTo.city if tracking.shipTo else None,
            tracking.shipTo.state if tracking.shipTo else None,
            tracking.shipTo.country if tracking.shipTo else None,
        ]))
        if tracking.shipTo else None
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number or tracking.trackingNumber,
        events=events,
        delivered=status == "delivered",
        status=status,
        estimated_delivery=lib.fdate(tracking.estimatedDelivery, "%Y-%m-%d") if tracking.estimatedDelivery else None,
        info=models.TrackingInfo(
            shipment_service=tracking.firstMile.carrier if tracking.firstMile else None,
            carrier_tracking_link=settings.tracking_url.format(tracking_number or tracking.trackingNumber),
            customer_name=tracking.shipTo.city if tracking.shipTo else None,
            shipment_destination_country=tracking.shipTo.country if tracking.shipTo else None,
            shipment_origin_country=tracking.shipFrom.country if tracking.shipFrom else None,
        ),
        meta=dict(
            shipment_id=tracking.shipmentId,
            customer_reference=tracking.customerReference,
            ship_date=tracking.shipDate,
            ship_from=ship_from_location,
            ship_to=ship_to_location,
            first_mile_carrier=tracking.firstMile.carrier if tracking.firstMile else None,
            first_mile_tracking=tracking.firstMile.trackingNumber if tracking.firstMile else None,
            last_mile_carrier=tracking.lastMile.carrier if tracking.lastMile else None,
            last_mile_tracking=tracking.lastMile.trackingNumber if tracking.lastMile else None,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for the carrier API"""
    # Return tracking numbers as serializable for proxy to handle
    return lib.Serializable(payload.tracking_numbers)
