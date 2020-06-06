from typing import List, Tuple
from pyusps.trackfieldrequest import TrackFieldRequest, TrackIDType
from pyusps.trackresponse import TrackInfoType, TrackDetailType
from purplship.core.utils import export, Serializable, Element, format_date, format_time
from purplship.core.models import (
    TrackingRequest,
    Message,
    TrackingDetails,
    TrackingEvent,
)
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_track_field_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    tracks_info = response.xpath(".//*[local-name() = $name]", name="TrackInfo")
    return (
        [_extract_tracking(tracking_node, settings) for tracking_node in tracks_info],
        parse_error_response(response, settings),
    )


def _extract_tracking(tracking_node: Element, settings) -> TrackingDetails:
    tracking: TrackInfoType = TrackInfoType()
    tracking.build(tracking_node)
    track_detail_nodes = tracking_node.xpath(
        ".//*[local-name() = $name]", name="TrackDetail"
    )
    details: List[TrackDetailType] = [
        (lambda t: (t, t.build(detail)))(TrackDetailType())[0]
        for detail in track_detail_nodes
    ]
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking.TrackInfoID,
        events=[
            TrackingEvent(
                code=str(event.EventCode),
                date=format_date(event.EventDate, "%B %d, %Y"),
                time=format_time(event.EventTime, "%H:%M %p"),
                description=event.ActionCode,
                location=", ".join(
                    [
                        location
                        for location in [
                            event.EventCity,
                            event.EventState,
                            event.EventCountry,
                            str(event.EventZIPCode),
                        ]
                        if location is not None
                    ]
                ),
            )
            for event in details
        ],
    )


def track_field_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[TrackFieldRequest]:
    request = TrackFieldRequest(
        USERID=settings.username,
        Revision="1",
        ClientIp=None,
        SourceID=None,
        TrackID=[
            TrackIDType(ID=tracking_number, DestinationZipCode=None, MailingDate=None)
            for tracking_number in payload.tracking_numbers
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: TrackFieldRequest) -> dict:
    return {"API": "TrackV2", "XML": export(request)}
