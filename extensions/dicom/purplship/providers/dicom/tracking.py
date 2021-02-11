from typing import Tuple, List
from dicom_lib.tracking import Tracking
from purplship.core.utils import Serializable, DF
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message
)

from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_tracking_response(response: dict, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for e in response if 'activities' not in e]
    details = [_extract_detail(Tracking(**d), settings) for d in response if 'activities' in d]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: Tracking, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.trackingNumber,
        events=[
            TrackingEvent(
                date=DF.fdate(event.activityDate, '%Y-%m-%dT%H:%M:%SZ'),
                description=event.statusDetail,
                location=event.terminal,
                code=event.status,
                time=DF.ftime(event.activityDate, '%Y-%m-%dT%H:%M:%SZ'),
            )
            for event in detail.activities
        ]
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:
    request = payload.tracking_numbers

    return Serializable(request)
