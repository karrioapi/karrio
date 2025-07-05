"""Karrio Veho tracking API implementation."""

import karrio.schemas.veho.tracking_request as veho_req
import karrio.schemas.veho.tracking_response as veho_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


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
    tracking_number: str=None,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data."""
    tracking_details = lib.to_object(veho_res.TrackingResponseType, data)

    status_code = tracking_details.statusCode if hasattr(tracking_details, 'statusCode') else ""
    status_detail = tracking_details.statusDescription if hasattr(tracking_details, 'statusDescription') else ""
    est_delivery = tracking_details.estimatedDeliveryDate if hasattr(tracking_details, 'estimatedDeliveryDate') else None

    events = []
    if hasattr(tracking_details, 'events') and tracking_details.events:
        for event in tracking_details.events:
            events.append({
                "date": event.date if hasattr(event, 'date') else "",
                "time": event.time if hasattr(event, 'time') else "",
                "code": event.code if hasattr(event, 'code') else "",
                "description": event.description if hasattr(event, 'description') else "",
                "location": event.location if hasattr(event, 'location') else ""
            })

    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if status_code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event["date"]),
                description=event["description"],
                code=event["code"],
                time=lib.flocaltime(event["time"]),
                location=event["location"],
            )
            for event in events
        ],
        estimated_delivery=lib.fdate(est_delivery) if est_delivery else None,
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for the carrier API."""
    tracking_numbers = payload.tracking_numbers
    reference = payload.reference

    request = veho_req.TrackingRequestType(
        trackingInfo={
            "trackingNumbers": tracking_numbers,
            "reference": reference,
            "language": payload.language_code or "en",
        },
        accountNumber=settings.account_number,
    )

    return lib.Serializable(request, lib.to_dict) 
