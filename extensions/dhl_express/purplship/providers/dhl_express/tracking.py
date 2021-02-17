from typing import List, Optional, Tuple
from dhl_express_lib.tracking_request_known_1_0 import KnownTrackingRequest
from dhl_express_lib.tracking_response import AWBInfo
from purplship.core.utils import (
    Serializable,
    Element,
    XP,
    DF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from .utils import Settings
from .error import parse_error_response


def parse_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    awb_nodes = response.xpath(".//*[local-name() = $name]", name="AWBInfo")
    tracking_details = [
        _extract_tracking(info_node, settings) for info_node in awb_nodes
    ]
    return (
        [details for details in tracking_details if details is not None],
        parse_error_response(response, settings),
    )


def _extract_tracking(
    info_node: Element, settings: Settings
) -> Optional[TrackingDetails]:
    info = AWBInfo()
    info.build(info_node)
    if info.ShipmentInfo is None:
        return None

    delivered = any(e.ServiceEvent.EventCode == 'OK' for e in info.ShipmentInfo.ShipmentEvent)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.AWBNumber,
        events=list(
            map(
                lambda e: TrackingEvent(
                    date=DF.fdate(e.Date),
                    time=DF.ftime(e.Time),
                    code=e.ServiceEvent.EventCode,
                    location=e.ServiceArea.Description,
                    description=e.ServiceEvent.Description,
                ),
                reversed(info.ShipmentInfo.ShipmentEvent or []),
            )
        ),
        delivered=delivered
    )


def tracking_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[KnownTrackingRequest]:
    request = KnownTrackingRequest(
        Request=settings.Request(),
        LanguageCode=payload.language_code or "en",
        LevelOfDetails=payload.level_of_details or "ALL_CHECK_POINTS",
        AWBNumber=payload.tracking_numbers,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: KnownTrackingRequest) -> str:
    return XP.export(
        request,
        name_="req:KnownTrackingRequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com TrackingRequestKnown.xsd"',
    ).replace('schemaVersion="1."', 'schemaVersion="1.0"')
