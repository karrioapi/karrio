"""PurplShip Australia Post Tracking service mapper module."""

from functools import reduce
from typing import List, Tuple, Callable
from purplship.carriers.aups.error import parse_error_response
from purplship.core.utils.serializable import Serializable
from purplship.core.settings import Settings
from purplship.core.models import TrackingRequest, Error, TrackingEvent, TrackingDetails
from pyaups.track_item import TrackingResponse, TrackingResult


def parse_track_items_response(
    response: dict, settings: Settings
) -> Tuple[List[TrackingDetails], List[Error]]:
    tracking_response: TrackingResponse = TrackingResponse(**response)
    return (
        reduce(_extract_tracking(settings), tracking_response.tracking_results, []),
        parse_error_response(
            {
                "errors": response.get("errors", [])
                + reduce(
                    lambda r, t: r + t.get("errors", []),
                    response.get("tracking_results", []),
                    [],
                )
            },
            settings,
        ),
    )


def _extract_tracking(
    settings: Settings
) -> Callable[[List[TrackingDetails], TrackingResult], List[TrackingDetails]]:
    def extract(
        tracking: List[TrackingDetails], tracking_result: TrackingResult
    ) -> List[TrackingDetails]:
        if not not tracking_result.errors:
            return tracking
        return tracking + [
            TrackingDetails(
                carrier=settings.carrier_name,
                tracking_number=tracking_result.tracking_id,
                shipment_date=None,
                events=[
                    TrackingEvent(
                        date=str(event.date),
                        signatory=None,
                        code=None,
                        location=event.location,
                        description=event.description,
                    )
                    for event in tracking_result.consignment.events
                ],
            )
        ]

    return extract


def track_items_request(payload: TrackingRequest) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers, _request_serializer)


def _request_serializer(tracking_ids: List[str]) -> str:
    return ",".join(tracking_ids)
