"""Karrio Landmark Global tracking API implementation."""

import karrio.schemas.landmark.track_request as landmark_req
import karrio.schemas.landmark.track_response as landmark_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.landmark.error as error
import karrio.providers.landmark.utils as provider_utils
import karrio.providers.landmark.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(
                response, settings, tracking_number=tracking_number
            )
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings)
        for number, details in responses
        if len(lib.find_element("TrackingNumber", details)) > 0
    ]

    return tracking_details, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data"""

    details = lib.find_element("ShipmentDetails", data, landmark_res.ShipmentDetailsType, first=True)
    package = lib.find_element("Package", data, landmark_res.PackageType, first=True)
    events = lib.find_element("Event", data, landmark_res.EventType)

    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if events[0].EventCode in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=package.TrackingNumber,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.DateTime, "%m/%d/%Y %I:%M %p"),
                time=lib.flocaltime(event.DateTime, "%m/%d/%Y %I:%M %p"),
                description=event.Status,
                code=event.EventCode,
                location=event.Location,
            )
            for event in package.Events.Event
        ],
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(package.LandmarkTrackingNumber),
        ),
        meta=dict(carrier=details.EndDeliveryCarrier),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking requests for the carrier API"""
    # Create a request for each tracking number
    requests = [
        landmark_req.TrackRequest(
            Login=landmark_req.LoginType(
                Username=settings.username,
                Password=settings.password,
            ),
            Test=settings.test_mode,
            ClientID=settings.client_id,
            Reference=payload.reference,
            TrackingNumber=tracking_number,
            PackageReference=None,
            RetrievalType="Historical",
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(
        requests,
        lambda __: [
            lib.typed(number=_.TrackingNumber, request=lib.to_xml(_))
            for _ in __
        ]
    )
