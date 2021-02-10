from typing import List, Tuple
from royalmail_lib.track_item import MailPieces
from purplship.core.utils import (
    Serializable,
    DF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.royalmail.utils import Settings
from purplship.providers.royalmail.error import parse_error_response


def parse_tracking_response(response: dict, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    tracking_details = (
        [_extract_detail(MailPieces(**response.get('mailPieces')), settings)]
        if 'mailPieces' in response else []
    )

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: MailPieces, settings: Settings) -> TrackingDetails:

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.mailPieceId,
        events=[
            TrackingEvent(
                date=DF.fdate(event.eventDateTime, '%Y-%m-%dT%H:%M:%S%z'),
                description=event.eventName,
                location=event.locationName,
                code=event.eventCode,
                time=DF.ftime(event.eventDateTime, '%Y-%m-%dT%H:%M:%S%z'),
            ) for event in detail.events
        ],
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[dict]:
    request = dict(
        mailPieceIds=payload.tracking_numbers
    )
    return Serializable(request)
