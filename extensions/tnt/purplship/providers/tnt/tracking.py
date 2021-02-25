from typing import List, Tuple
from purplship.core.utils import (
    Serializable,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.tnt.utils import Settings
from purplship.providers.tnt.error import parse_error_response


def parse_tracking_response(response, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = []  # retrieve details from `response`
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: 'CarrierTrackingDetail', settings: Settings) -> TrackingDetails:
    # return TrackingDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #
    #     tracking_number=detail.[tracking_number],
    #     events=[],
    # )
    pass


def tracking_request(payload: TrackingRequest, settings: Settings) -> Serializable['CarrierTrackingRequest']:
    # request = CarrierTrackingRequest(
    # )
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierTrackingRequest') -> str:
    pass
