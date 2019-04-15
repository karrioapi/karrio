from typing import Tuple, List
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pyups import (
    freight_rate as Rate,
    freight_ship as FShip,
)
from .partials import (
    UPSRateMapperPartial,
    UPSShipmentMapperPartial,
)


class UPSMapper(
    Mapper, UPSRateMapperPartial, UPSShipmentMapperPartial
):
    def create_quote_request(
        self, payload: T.ShipmentRequest
    ) -> Rate.FreightRateRequest:
        return self.create_freight_rate_request(payload)

    def create_shipment_request(
        self, payload: T.ShipmentRequest
    ) -> FShip.FreightShipRequest:
        return self.create_freight_ship_request(payload)

    def parse_quote_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_freight_rate_response(response)

    def parse_shipment_response(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        details = response.xpath(".//*[local-name() = $name]", name="FreightShipResponse")
        return (
            self.parse_freight_shipment_response(details[0])
            if len(details) > 0 else None,
            self.parse_error_response(response),
        )
