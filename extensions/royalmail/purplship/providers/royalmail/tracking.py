from typing import List, Tuple
from royalmail_lib.tracking import MailPieces
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


def parse_tracking_response(response: List[dict], settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for e in response if 'mailPieces' not in e]
    details = [
        _extract_detail(MailPieces(**d['mailPieces']), settings)
        for d in response if 'mailPieces' in d
    ]

    return details, parse_error_response(errors, settings)


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
    request = payload.tracking_numbers

    return Serializable(request)
