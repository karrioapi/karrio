from typing import List, Tuple
from usps_lib.track_field_request import TrackFieldRequest, TrackIDType
from usps_lib.track_response import TrackInfoType, TrackDetailType
from purplship.core.utils import Serializable, Element, XP, DF
from purplship.core.models import (
    TrackingRequest,
    Message,
    TrackingDetails,
    TrackingEvent,
)
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps import Settings


def parse_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    tracks_info = response.xpath(".//*[local-name() = $name]", name="TrackInfo")
    return (
        [_extract_details(tracking_node, settings) for tracking_node in tracks_info],
        parse_error_response(response, settings),
    )


def _extract_details(tracking_node: Element, settings) -> TrackingDetails:
    tracking: TrackInfoType = TrackInfoType()
    tracking.build(tracking_node)
    track_detail_nodes = tracking_node.xpath(
        ".//*[local-name() = $name]", name="TrackDetail"
    )
    details: List[TrackDetailType] = [
        XP.build(TrackDetailType, detail)
        for detail in track_detail_nodes
    ]
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking.TrackInfoID,
        events=[
            TrackingEvent(
                code=str(event.EventCode),
                date=DF.fdate(event.EventDate, "%B %d, %Y"),
                time=DF.ftime(event.EventTime, "%H:%M %p"),
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


def tracking_request(
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


def _request_serializer(request: TrackFieldRequest) -> str:
    return XP.export(request)
