from typing import Tuple, List
from amazon_mws_lib.tracking_response import TrackingResponse
from karrio.providers.amazon_mws.utils import Settings
from karrio.core.utils import Serializable, DF, SF, DP
from karrio.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from karrio.providers.amazon_mws.error import parse_error_response


def parse_tracking_response(
    responses: List[Tuple[str, dict]], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    errors: List[Message] = sum(
        [
            parse_error_response(response, settings, dict(tracking_number=id))
            for id, response in responses
            if "errors" in response
        ],
        [],
    )
    trackers = [
        _extract_details(response, settings)
        for _, response in responses
        if "errors" not in response
    ]

    return trackers, errors


def _extract_details(data: dict, settings: Settings) -> TrackingDetails:
    details = DP.to_object(TrackingResponse, data)

    return TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.trackingId,
        events=[
            TrackingEvent(
                date=DF.fdate(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.eventCode,
                code=event.eventCode,
                time=DF.ftime(event.eventTime, "%Y-%m-%dT%H:%M:%SZ"),
                location=SF.concat_str(
                    event.location.city,
                    event.location.stateOrRegion,
                    event.location.postalCode,
                    event.location.countryCode,
                    join=True,
                    separator=", ",
                ),
            )
            for event in details.eventHistory
        ],
        estimated_delivery=DF.fdate(details.promisedDeliveryDate, "%Y-%m-%dT%H:%M:%SZ"),
        delivered=(details.summary.status == "Delivered"),
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable:
    return Serializable(payload.tracking_numbers)
