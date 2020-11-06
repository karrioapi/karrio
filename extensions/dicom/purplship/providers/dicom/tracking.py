from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    Message
)

from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_tracking_response(response: dict, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = parse_error_response(response, settings)
    details = []

    return details, errors


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:

    request = payload.tracking_numbers

    return Serializable(request)
