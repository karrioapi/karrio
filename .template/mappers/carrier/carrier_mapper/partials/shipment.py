from typing import List, Tuple, TypeVar
from template.carrier_datatype_mock import CarrierShipmentRequestType
from purplship.mappers.carrier.interface import CarrierNameMapperBase
from purplship.domain.Types import ShipmentRequest, ShipmentDetails, Error

CarrierGenericResponseType = TypeVar("T")


class CarrierNameMapperPartial(CarrierNameMapperBase):

    """Response Parsing"""

    def parse_carrier_quote_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[ShipmentDetails, List[Error]]:
        return (
            ShipmentDetails(
                carrier=self.client.carrier_name,
                tracking_numbers=[],
                shipment_date=None,
                services=[],
                charges=[],
                documents=[],
                reference=None,
                total_charge=None,
            ),
            self.parse_error_response(response),
        )

    """Request Mapping"""

    def create_carrier_shipment_request(
        self, payload: ShipmentRequest
    ) -> CarrierShipmentRequestType:
        return CarrierShipmentRequestType()
