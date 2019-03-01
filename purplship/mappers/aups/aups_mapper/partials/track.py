"""PurplShip Australia Post Tracking service mapper module."""

from functools import reduce
from .interface import Tuple, List, AustraliaPostMapperBase
from purplship.domain.Types import (
    TrackingRequest,
    Error,
    TrackingEvent,
    TrackingDetails
)
from pyaups.track_item import (
    TrackingResponse,
    TrackingResult
)


class AustraliaPostMapperPartial(AustraliaPostMapperBase):
    def parse_track_items_response(
        self, response: dict
    ) -> Tuple[List[TrackingDetails], List[Error]]:
        tracking_response: TrackingResponse = TrackingResponse(**response)
        return (
            reduce(self._extract_tracking, tracking_response.tracking_results, []),
            self.parse_error_response(response)
        )

    def _extract_tracking(
        self, trackings: List[TrackingDetails], tracking_result: TrackingResult
    ) -> List[TrackingDetails]:
        return trackings + [
            TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=tracking_result.tracking_id,
                shipment_date=None,
                events=[
                    TrackingEvent(
                        date=str(event.date),
                        signatory=None,
                        code=None,
                        location=event.location,
                        description=event.description,
                    ) for event in tracking_result.consignment.events
                ],
            )
        ]

    def create_track_items_request(self, payload: TrackingRequest) -> List[str]:
        return payload.tracking_numbers
