"""PurplShip Sendle Tracking service mapper module."""

from typing import Tuple, List
from .interface import SendleMapperBase
from purplship.domain.Types import (
    TrackingRequest,
    Error,
    TrackingEvent,
    TrackingDetails
)
from pysendle.tracking import TrackingResponse


class SendleMapperPartial(SendleMapperBase):
    def parse_parcel_tracking_response(self, response: dict) -> Tuple[List[TrackingDetails], List[Error]]:
        tracking: List[TrackingResponse] = [
            (p.get('ref'), TrackingResponse(**p.get('response')))
            for p in response
            if 'tracking_events' in p.get('response')
        ]
        errors: List[dict] = [p.get('response') for p in response]
        return (
            [self._extract_tracking(t) for t in tracking],
            self.parse_error_response(errors)
        )

    def _extract_tracking(self, response: Tuple[str, TrackingResponse]) -> TrackingDetails:
        tracking_number, detail = response
        return TrackingDetails(
            carrier=self.client.carrier_name,
            tracking_number=tracking_number,
            shipment_date=None,
            events=[
                TrackingEvent(
                    date=event.scan_time,
                    signatory=None,
                    code=event.event_type,
                    location=event.destination_location,
                    description=event.description,
                ) for event in detail.tracking_events
            ],
        )

    def create_parcel_tracking_request(self, payload: TrackingRequest) -> List[str]:
        return payload.tracking_numbers
