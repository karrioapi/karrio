from typing import List, Tuple, TypeVar
from functools import reduce
from purplship.mappers.carrier import CarrierNameClient
from purplship.domain.Types import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    PickupRequest,
    QuoteDetails,
    ShipmentDetails,
    TrackingDetails,
    PickupDetails,
    PickupCancellationRequest,
    Error,
)
from template.carrier_datatype_mock import (
    CarrierRateRequestType,
    CarrierTrackingRequestType,
    CarrierShipmentRequestType,
    CarrierPickupBookingRequestType,
    CarrierPickupModificationRequestType,
    CarrierPickupCancellationRequestType,
)

CarrierGenericResponseType = TypeVar("T")


class CarrierNameCapabilities:
    """CarrierName native service requests."""

    """ Requests """

    def create_carrier_quote_request(
        self, payload: RateRequest
    ) -> CarrierRateRequestType:
        pass

    def create_carrier_tracking_request(
        self, payload: TrackingRequest
    ) -> CarrierTrackingRequestType:
        pass

    def create_carrier_shipment_request(
        self, payload: ShipmentRequest
    ) -> CarrierShipmentRequestType:
        pass

    def create_carrier_pickup_booking_request(
        self, payload: PickupRequest
    ) -> CarrierPickupBookingRequestType:
        pass

    def create_carrier_pickup_modification_request(
        self, payload: PickupRequest
    ) -> CarrierPickupModificationRequestType:
        pass

    def create_carrier_pickup_cancellation_request(
        self, payload: PickupCancellationRequest
    ) -> CarrierPickupCancellationRequestType:
        pass

    """ Response """

    def parse_carrier_quote_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        pass

    def parse_carrier_tracking_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[List[TrackingDetails], List[Error]]:
        pass

    def parse_carrier_shipment_respone(
        self, response: CarrierGenericResponseType
    ) -> Tuple[ShipmentDetails, List[Error]]:
        pass

    def parse_carrier_pickup_booking_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[PickupDetails, List[Error]]:
        pass

    def parse_carrier_pickup_modification_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[PickupDetails, List[Error]]:
        pass

    def parse_carrier_pickup_cancellation_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[dict, List[Error]]:
        pass


class CarrierNameMapperBase(CarrierNameCapabilities):
    """CarrierName mapper base class."""

    def __init__(self, client: CarrierNameClient):
        self.client = client

    def parse_error_response(self, response) -> List[Error]:
        errors = []
        return reduce(self._extract_error, errors, [])

    def _extract_error(
        self, errors: List[Error], error: CarrierGenericResponseType
    ) -> List[Error]:
        return errors + [Error(carrier=self.client.carrier_name)]
