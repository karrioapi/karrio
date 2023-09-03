from typing import Tuple, List
from karrio.schemas.dicom.tracking import Tracking
from karrio.core.utils import Serializable, DF, DP
from karrio.core.models import TrackingRequest, TrackingDetails, TrackingEvent, Message

from karrio.providers.dicom.error import parse_error_response
from karrio.providers.dicom.utils import Settings
import karrio.lib as lib


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[List[TrackingDetails], List[Message]]:
    response = _response.deserialize()
    errors = [e for e in response if "activities" not in e]
    details = [
        _extract_detail(DP.to_object(Tracking, d), settings)
        for d in response
        if "activities" in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: Tracking, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.trackingNumber,
        events=[
            TrackingEvent(
                date=DF.fdate(event.activityDate, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.statusDetail,
                location=event.terminal,
                code=event.status,
                time=DF.ftime(event.activityDate, "%Y-%m-%dT%H:%M:%SZ"),
            )
            for event in detail.activities
        ],
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable:
    request = payload.tracking_numbers

    return Serializable(request)
