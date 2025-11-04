"""Karrio MyDHL tracking API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract tracking details and events from the response to populate TrackingDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., TrackingRequestType),
# while XML schema types don't have this suffix (e.g., TrackingRequest).

import karrio.schemas.mydhl.tracking_request as mydhl_req
import karrio.schemas.mydhl.tracking_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


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
    Extract tracking details from carrier response data

    data: The carrier-specific tracking data structure
    settings: The carrier connection settings
    tracking_number: The tracking number being tracked

    Returns a TrackingDetails object with extracted tracking information
    """
    # Convert the carrier data to a proper object for easy attribute access
    
    # For JSON APIs, convert dict to proper response object
    tracking_details = lib.to_object(mydhl_res.TrackingResponseType, data)

    # Extract tracking status and information
    status_code = tracking_details.statusCode if hasattr(tracking_details, 'statusCode') else ""
    status_detail = tracking_details.statusDescription if hasattr(tracking_details, 'statusDescription') else ""
    est_delivery = tracking_details.estimatedDeliveryDate if hasattr(tracking_details, 'estimatedDeliveryDate') else None

    # Extract events
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
    

    # Map carrier status to karrio standard tracking status
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
    """
    Create a tracking request for the carrier API

    payload: The standardized TrackingRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract the tracking number(s) from payload
    tracking_numbers = payload.tracking_numbers
    reference = payload.reference

    
    # For JSON API request
    request = mydhl_req.TrackingRequestType(
        trackingInfo={
            "trackingNumbers": tracking_numbers,
            "reference": reference,
            "language": payload.language_code or "en",
        },
        # Add account credentials
        accountNumber=settings.account_number,
    )
    

    return lib.Serializable(request, lib.to_dict)
