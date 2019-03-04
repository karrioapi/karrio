from typing import List, Tuple, TypeVar
from template.carrier_datatype_mock import CarrierTrackingRequestType
from purplship.mappers.carrier.interface import CarrierNameMapperBase
from purplship.domain.Types import TrackingRequest, TrackingDetails, Error

CarrierGenericResponseType = TypeVar("T")


class CarrierNameMapperPartial(CarrierNameMapperBase):

    """Response Parsing"""

    def parse_carrier_quote_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[TrackingDetails, List[Error]]:
        tracking = []
        return (
            [self._extract_tracking(detail) for detail in tracking],
            self.parse_error_response(response),
        )

    def _extract_tracking(
        self, tracking: List[TrackingDetails], detail: CarrierGenericResponseType
    ) -> List[TrackingDetails]:
        return tracking + [
            TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=None,
                shipment_date=None,
                events=[],
            )
        ]

    """Request Mapping"""

    def create_carrier_tracking_request(
        self, payload: TrackingRequest
    ) -> CarrierTrackingRequestType:
        return CarrierTrackingRequestType()
