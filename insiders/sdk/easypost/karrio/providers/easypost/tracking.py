from typing import Tuple, List
from easypost_lib.trackers_response import Tracker
from karrio.providers.easypost.utils import Settings
from karrio.providers.easypost.units import CarrierId
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
                description=event.message or "",
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
            if event.datetime is not None
        ],
        delivered=(tracker.status == "delivered"),
        meta=dict(
            carrier=CarrierId.map(tracker.carrier).name_or_key,
            tracker_id=tracker.id,
        ),
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[dict]]:
    """Send one or multiple tracking request(s) to EasyPost.
    the payload must match the following schema:
    {
        "tracking_numbers": ["123456789"],
        "options": {
            "123456789": {
                "carrier": "usps",
                "tracker_id": "trk_xxxxxxxx",  # optional
            }
        }
    }
    """
    requests = []

    for tracking_code in payload.tracking_numbers:
        options = payload.options.get(tracking_code)
        if options is None:
            raise ValueError(f"No options found for {tracking_code}")

        if "carrier" not in options:
            raise ValueError(
                "invalid options['tracking_number'].carriers."
                "Please provide a 'carrier_name' for each tracking_number"
            )

        requests.append(
            dict(
                tracking_code=tracking_code,
                carrier=CarrierId.map(options["carrier"]).value_or_key,
                tracker_id=options.get("tracker_id"),
            )
        )

    return Serializable(requests, DP.to_dict)
