from typing import List, Tuple
from sf_express_lib.request import Request
from sf_express_lib.tracking import (
    TrackingRequest as SFTrackingRequest,
    RouteResp
)
from purplship.core.utils import (
    Serializable,
    DP,
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
    tracking_details = [
        _extract_detail(RouteResp(**d), settings)
        for d in response.get('msgData', {}).get('routeResps', [])
    ]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: RouteResp, settings: Settings) -> TrackingDetails:

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.mailNo,
        events=[
            TrackingEvent(
                date=DF.fdate(event.acceptTime, "%Y-%m-%d %H:%M:%S"),
                description=event.remark,
                location=event.acceptAddress,
                code=event.opCode,
                time=DF.ftime(event.acceptTime, "%Y-%m-%d %H:%M:%S"),
            ) for event in detail.routes
        ]
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[Request]:
    request = Request(
        requestID="EXP_RECE_SEARCH_ROUTES",
        msgData=SFTrackingRequest(
            language="1",
            trackingType="1",
            methodType="1",
            trackingNumber=payload.tracking_numbers
        )
    )

    return Serializable(request, DP.jsonify)
