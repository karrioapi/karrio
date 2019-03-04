from typing import Tuple, List
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain.Types import (
    ShipmentRequest,
    RateRequest,
    PickupRequest,
    PickupCancellationRequest,
    ShipmentDetails,
    QuoteDetails,
    TrackingDetails,
    PickupDetails,
    Error,
)
from .partials import (
    CarrierNameQuoteMapperPartial,
    CarrierNameTrackMapperPartial,
    CarrierNameShipmentMapperPartial,
    CarrierNamePickupMapperPartial,
)


class CarrierNameMapper(
    Mapper,
    CarrierNameQuoteMapperPartial,
    CarrierNameTrackMapperPartial,
    CarrierNameShipmentMapperPartial,
    CarrierNamePickupMapperPartial,
):
    def create_quote_request(self, payload: RateRequest) -> CarrierRateRequestType:
        return self.create_dct_request(payload)

    def create_tracking_request(
        self, payload: TrackingRequest
    ) -> CarrierTrackingRequestType:
        return self.create_carrier_quote_request(payload)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> CarrierShipmentRequestType:
        return self.create_carrier_shipment_request(payload)

    def create_pickup_request(
        self, payload: PickupRequest
    ) -> CarrierPickupBookingRequestType:
        return self.create_carrier_pickup_booking_request(payload)

    def modify_pickup_request(
        self, payload: PickupRequest
    ) -> CarrierPickupModificationRequestType:
        return self.create_carrier_pickup_modification_request(payload)

    def create_pickup_cancellation_request(
        self, payload: PickupCancellationRequest
    ) -> CarrierPickupCancellationRequestType:
        return self.create_carrier_pickup_cancellation_request(payload)

    """Response parsing."""

    def parse_quote_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        return self.parse_dct_response(response)

    def parse_tracking_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[TrackingDetails], List[Error]]:
        return self.parse_dhltracking_response(response)

    def parse_shipment_response(
        self, response: etree.ElementBase
    ) -> Tuple[ShipmentDetails, List[Error]]:
        return self.parse_dhlshipment_respone(response)

    def parse_pickup_response(self, response) -> Tuple[PickupDetails, List[Error]]:
        return self.parse_book_puresponse(response)

    def parse_pickup_cancellation_response(self, response) -> Tuple[dict, List[Error]]:
        return self.parse_cancel_puresponse(response)
