from typing import List, Tuple, TypeVar
from template.carrier_datatype_mock import (
    CarrierPickupBookingRequestType,
    CarrierPickupModificationRequestType,
    CarrierPickupCancellationRequestType,
)
from purplship.mappers.carrier.interface import CarrierNameMapperBase
from purplship.domain.Types import (
    PickupCancellationRequest,
    PickupRequest,
    PickupDetails,
    Error,
)

CarrierGenericResponseType = TypeVar("T")


class CarrierNameMapperPartial(CarrierNameMapperBase):

    """Response Parsing"""

    def parse_carrier_pickup_booking_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[PickupDetails, List[Error]]:
        pickup_response = None
        return (pickup_response, self.parse_error_response(response))

    def parse_carrier_pickup_modification_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[PickupDetails, List[Error]]:
        pickup_response = None
        return (pickup_response, self.parse_error_response(response))

    def parse_carrier_pickup_cancellation_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[dict, List[Error]]:
        pickup_cancellation_response = None
        return (pickup_cancellation_response, self.parse_error_response(response))

    """Request Mapping"""

    def create_carrier_pickup_booking_request(
        self, payload: PickupRequest
    ) -> CarrierPickupBookingRequestType:
        return CarrierPickupBookingRequestType()

    def create_carrier_pickup_modification_request(
        self, payload: PickupRequest
    ) -> CarrierPickupModificationRequestType:
        return CarrierPickupModificationRequestType()

    def create_carrier_pickup_cancellation_request(
        self, payload: PickupCancellationRequest
    ) -> CarrierPickupCancellationRequestType:
        return CarrierPickupCancellationRequestType()
