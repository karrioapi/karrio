from typing import Tuple, List, Dict
from easypost_lib.trackers_response import Tracker
from karrio.providers.easypost.utils import Settings
from karrio.core.utils import Serializable, DF, SF, DP
from karrio.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from karrio.providers.easypost.error import parse_error_response


def parse_tracking_response(
    responses: List[Tuple[str, dict]], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [
        parse_error_response(response, settings, dict(tracking_number=code))
        for code, response in responses
        if "error" in response
    ]
    trackers = [
        _extract_details(response, settings)
        for _, response in responses
        if "error" not in response
    ]

    return trackers, errors


def _extract_details(data: dict, settings: Settings) -> TrackingDetails:
    tracker = DP.to_object(Tracker, data)

    return TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracker.tracking_code,
        events=[
            TrackingEvent(
                date=DF.fdate(event.datetime, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.message,
                code=event.status,
                time=DF.ftime(event.datetime, "%Y-%m-%dT%H:%M:%SZ"),
                location=SF.concat_str(
                    event.tracking_location.city,
                    event.tracking_location.state,
                    event.tracking_location.zip,
                    event.tracking_location.country,
                    join=True,
                    separator=", ",
                ),
            )
            for event in tracker.tracking_details
        ],
        delivered=False,
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[dict]]:
    carrier = (payload.options or {}).get("carrier")

    if carrier is None:
        raise ValueError("options.carrier is required")

    request = [
        dict(
            tracking_code=tracking_code,
            carrier=carrier,
        )
        for tracking_code in payload.tracking_numbers
    ]

    return Serializable(request)
