from typing import Tuple, Dict, List, cast
from ics_courier_lib.services import (
    TracePackge,
    ArrayOfString,
    ResponseTrackingInfo,
    ArrayOfTrackingInfo,
    TrackingInfo,
)
from purplship.core.models import (
    Message,
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
)
from purplship.core.utils import (
    Serializable,
    Element,
    create_envelope,
    Envelope,
    DF,
    XP,
    SF,
)
from purplship.providers.ics_courier.error import parse_error_response
from purplship.providers.ics_courier.utils import Settings


def parse_tracking_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    result: ResponseTrackingInfo = XP.find("TracePackgeResult", response, ResponseTrackingInfo, first=True)
    infos: Dict[str, TrackingInfo] = {}

    for info in cast(ArrayOfTrackingInfo, result.TrackingInfo).TrackingInfo:
        key = str(info.TrackingNum)
        infos[key] = [*(infos.get(key) or []), info]

    details = [
        _extract_tracking_details((tracking_number, events), settings)
        for tracking_number, events in infos.items()
    ]

    return details, parse_error_response(response, settings)


def _extract_tracking_details(infos: Tuple[str, TrackingInfo], settings: Settings) -> TrackingDetails:
    tracking_number, events = infos
    ordered_events = [*reversed(
        sorted(events, key=lambda e: DF.date(e.StatusDate, "%Y-%m-%dT%H:%M:%S"))
    )]

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        events=[
            TrackingEvent(
                date=DF.fdate(event.StatusDate, "%Y-%m-%dT%H:%M:%S"),
                time=DF.ftime(event.StatusDate, "%Y-%m-%dT%H:%M:%S"),
                description=event.Status,
            )
            for event in ordered_events
        ],
        delivered=('Delivered' in ordered_events[0].Status)
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[Envelope]]:
    request = create_envelope(
        body_content=TracePackge(
            TrackNums=ArrayOfString(
                string=payload.tracking_numbers
            ),
            DetailInfo=True,
        )
    )

    return Serializable(request, Settings.serialize)
