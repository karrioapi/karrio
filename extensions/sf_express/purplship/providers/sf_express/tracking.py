from typing import List, Tuple
from sf_express_lib.route_response import RouteResponseType, RouteType
from sf_express_lib.route_request import (
    Request,
    BodyType,
    RouteRequestType,
)
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
from purplship.providers.sf_express.utils import Settings
from purplship.providers.sf_express.error import parse_error_response


def parse_tracking_response(response, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = response.xpath(".//*[local-name() = $name]", name="RouteResponse")
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: Element, settings: Settings) -> TrackingDetails:
    route = XP.build(RouteResponseType, detail)
    events: List[RouteType] = route.Route

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=route.mailno,
        events=[
            TrackingEvent(
                date=DF.fdate(event.accept_time, "%Y-%m-%d %H:%M:%S"),
                description=event.remark,
                location=event.accept_address,
                code=event.opcode,
                time=DF.ftime(event.accept_time, "%Y-%m-%d %H:%M:%S"),
            ) for event in events
        ]
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[RouteRequestType]:
    request = Request(
        service='RouteService',
        lang='en-US',
        Head=None,
        Body=BodyType(
            RouteRequest=[
                RouteRequestType(
                    tracking_type=1,
                    method_type=1,
                    tracking_number=number,
                    check_phoneNo=None,
                ) for number in payload.tracking_numbers
            ]
        )
    )

    return Serializable(request, XP.to_xml)
