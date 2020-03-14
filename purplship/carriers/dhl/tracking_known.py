from typing import List, Optional, Tuple
from pydhl.tracking_request_known_1_0 import KnownTrackingRequest
from pydhl.tracking_response import AWBInfo
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import TrackingEvent, TrackingDetails, TrackingRequest, Error
from .utils import Settings
from .error import parse_error_response


def parse_known_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Error]]:
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

    return TrackingDetails(
        carrier=settings.carrier_name,
        tracking_number=info.AWBNumber,
        shipment_date=str(info.ShipmentInfo.ShipmentDate),
        events=list(
            map(
                lambda e: TrackingEvent(
                    date=str(e.Date),
                    time=str(e.Time),
                    signatory=e.Signatory,
                    code=e.ServiceEvent.EventCode,
                    location=e.ServiceArea.Description,
                    description=e.ServiceEvent.Description,
                ),
                info.ShipmentInfo.ShipmentEvent,
            )
        ),
    )


def known_tracking_request(
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
    return export(
        request,
        name_="req:KnownTrackingRequest",
        namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com TrackingRequestKnown.xsd"',
    )
