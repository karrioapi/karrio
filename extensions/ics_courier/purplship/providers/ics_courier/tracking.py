from typing import List, Tuple, cast
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
    details = [
        _extract_tracking_details(info, settings)
        for info in cast(ArrayOfTrackingInfo, result.TrackingInfo).TrackingInfo
    ]

    return details, parse_error_response(response, settings)


def _extract_tracking_details(detail: TrackingInfo, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.TrackingNum,
        events=[
            TrackingEvent(
                date=DF.fdate(detail.StatusDate, "%Y-%m-%dT%H:%M:%S"),
                time=DF.ftime(detail.StatusDate, "%Y-%m-%dT%H:%M:%S"),
                description=detail.Status,
            )
        ],
        delivered=False
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
