from typing import List, Tuple, cast
from dhl_parcel_pl_lib.services import getTrackAndTraceInfo
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
from purplship.providers.dhl_parcel_pl.error import parse_error_response
from purplship.providers.dhl_parcel_pl.utils import Settings


def parse_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    pass


def _extract_tracking_details(node: Element, settings: Settings) -> TrackingDetails:
    pass


def tracking_request(
    payload: TrackingRequest, settings: Settings
) -> Serializable[List[Envelope]]:
    requests = [
        create_envelope(
            body_prefix="",
            body_content=getTrackAndTraceInfo(
                authData=settings.auth_data,
                shipmentId=tracking_number,
            ),
        )
        for tracking_number in payload.tracking_numbers
    ]

    return Serializable(
        requests,
        lambda reqs: [
            settings.serialize(req, request_name="getTrackAndTraceInfo") for req in reqs
        ],
    )
