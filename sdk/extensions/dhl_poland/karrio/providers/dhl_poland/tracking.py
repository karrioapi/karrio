from typing import List, Tuple, Dict
from dhl_poland_lib.services import (
    getTrackAndTraceInfo,
    TrackAndTraceResponse,
    TrackAndTraceEvent,
)
from karrio.core.models import (
    Message,
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
)
from karrio.core.utils import (
    Serializable,
    Element,
    create_envelope,
    Envelope,
    DF,
    XP,
    SF,
)
from karrio.providers.dhl_poland.error import parse_error_response
from karrio.providers.dhl_poland.utils import Settings


def parse_tracking_response(
    response: Dict[str, Element], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    details = [
        _extract_tracking_details(node, settings)
        for node in response.values()
        if XP.find("getTrackAndTraceInfoResult", node, first=True) is not None
    ]
    errors: List[Message] = sum(
        [
            parse_error_response(node, settings, dict(tracking_number=number))
            for number, node in response.items()
            if XP.find("Fault", node, first=True) is not None
        ],
        [],
    )

    return details, errors


def _extract_tracking_details(node: Element, settings: Settings) -> TrackingDetails:
    track: TrackAndTraceResponse = XP.find(
        "getTrackAndTraceInfoResult", node, TrackAndTraceResponse, first=True
    )
    events = [XP.build(TrackAndTraceEvent, item) for item in XP.find("item", node)]

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=track.shipmentId,
        events=[
            TrackingEvent(
                date=DF.fdate(event.timestamp, "%Y-%m-%d %H:%M:%S"),
                description=event.description,
                location=event.terminal,
                code=event.status,
                time=DF.ftime(event.timestamp, "%Y-%m-%d %H:%M:%S"),
            )
            for event in events
        ],
        delivered=any(track.receivedBy or ""),
    )


def tracking_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[Dict[str, Envelope]]:
    requests = {
        tracking_number: create_envelope(
            body_prefix="",
            body_content=getTrackAndTraceInfo(
                authData=settings.auth_data,
                shipmentId=tracking_number,
            ),
        )
        for tracking_number in payload.tracking_numbers
    }

    return Serializable(
        requests,
        lambda requests: {
            number: settings.serialize(
                request,
                "getTrackAndTraceInfo",
                settings.server_url,
            )
            for number, request in requests.items()
        },
    )
