import karrio.lib as lib
from typing import List, Tuple
from australiapost_lib.tracking import (
    TrackingRequest as CarrierTrackingRequest,
    TrackingResult,
)
from karrio.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from karrio.providers.australiapost.utils import Settings
from karrio.providers.australiapost.error import parse_error_response


def parse_tracking_response(
    _response: lib.Deserializable[dict], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    response = _response.deserialize()
    tracking_results = response.get("tracking_results", [])
    errors = sum(
        [
            _extract_error(lib.to_object(TrackingResult, result), settings)
            for result in tracking_results
            if "errors" in result
        ],
        parse_error_response(response, settings),
    )
    tracking_details = [
        _extract_detail(lib.to_object(TrackingResult, d), settings)
        for d in response.get("tracking_results", [])
        if "trackable_items" in d
    ]

    return tracking_details, errors


def _extract_error(result: TrackingResult, settings: Settings) -> List[Message]:
    return [
        Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.code,
            message=error.message,
            details=dict(tracking_number=result.tracking_id),
        )
        for error in result.errors
    ]


def _extract_detail(detail: TrackingResult, settings: Settings) -> TrackingDetails:
    item = detail.trackable_items[0]

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.tracking_id,
        events=[
            TrackingEvent(
                date=lib.fdate(event.date, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.description,
                location=event.location,
                time=lib.ftime(event.date, "%Y-%m-%dT%H:%M:%S%z"),
            )
            for event in item.events
        ],
        delivered=(detail.status == "Delivered"),
    )


def tracking_request(payload: TrackingRequest, _) -> lib.Serializable:
    request = CarrierTrackingRequest(tracking_ids=",".join(payload.tracking_numbers))

    return lib.Serializable(request, lib.to_dict)
