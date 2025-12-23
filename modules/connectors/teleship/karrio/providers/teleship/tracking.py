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
            error.parse_error_response(
                response, settings, **dict(tracking_number=tracking_number)
            )
            for tracking_number, response in responses
        ],
        start=[],
    )

    # Extract tracking details using list comprehension (skip error responses)
    tracking_details = [
        _extract_details(details, settings)
        for tracking_number, details in responses
        if details and not details.get("messages")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data"""

    tracking = lib.to_object(teleship_res.TrackingResponseType, data)
    last_event = next(iter(tracking.events or []), None)
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if last_event and last_event.code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking.trackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%SZ"),
                time=lib.flocaltime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.description,
                code=event.code,
                location=event.location,
                timestamp=lib.fiso_timestamp(
                    event.timestamp,
                    current_format="%Y-%m-%dT%H:%M:%SZ",
                ),
                status=next(
                    (
                        s.name
                        for s in list(provider_units.TrackingStatus)
                        if event.code in s.value
                    ),
                    None,
                ),
            )
            for event in tracking.events
        ],
        delivered=status == "delivered",
        status=status,
        estimated_delivery=lib.fdate(
            tracking.estimatedDelivery,
            try_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"],
        ),
        info=models.TrackingInfo(
            shipment_service=tracking.firstMile.carrier,
            carrier_tracking_link=settings.tracking_url.format(tracking.trackingNumber),
            customer_name=tracking.shipTo.address.city,
            shipment_destination_country=tracking.shipTo.address.country,
            shipment_origin_country=tracking.shipFrom.address.country,
        ),
        meta=dict(
            shipment_id=tracking.shipmentId,
            customer_reference=tracking.customerReference,
            ship_date=tracking.shipDate,
            last_mile_carrier=tracking.lastMile.carrier,
            last_mile_tracking=tracking.lastMile.trackingNumber,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for the carrier API"""
    # Return tracking numbers as serializable for proxy to handle
    return lib.Serializable(payload.tracking_numbers)
