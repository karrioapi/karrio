from typing import Tuple, List, Union
from functools import reduce
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from purplship.domain.Types.units import Weight, WeightUnit, Dimension, DimensionUnit
from pyups import (
    freight_rate as Rate,
    package_rate as PRate,
    package_track as Track,
    UPSSecurity as Security,
    error as Err,
    freight_ship as FShip,
    package_ship as PShip,
)
from .partials import (
    UPSRateMapperPartial,
    UPSTrackMapperPartial,
    UPSShipmentMapperPartial,
)


class UPSMapper(
    Mapper, UPSRateMapperPartial, UPSTrackMapperPartial, UPSShipmentMapperPartial
):
    def create_quote_request(
        self, payload: T.ShipmentRequest
    ) -> PRate.RateRequest:
        return self.create_package_rate_request(payload)

    def create_freight_quote_request(
        self, payload: T.ShipmentRequest
    ) -> Rate.FreightRateRequest:
        return self.create_freight_rate_request(payload)

    def create_tracking_request(
        self, payload: T.TrackingRequest
    ) -> List[Track.TrackRequest]:
        return self.create_track_request(payload)

    def create_shipment_request(
        self, payload: T.ShipmentRequest
    ) -> PShip.ShipmentRequest:
        return self.create_package_ship_request(payload)

    def create_freight_shipment_request(
        self, payload: T.ShipmentRequest
    ) -> FShip.FreightShipRequest:
        return self.create_freight_ship_request(payload)

    def parse_quote_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        details = response.xpath(
            ".//*[local-name() = $name]", name="FreightRateResponse"
        ) + response.xpath(".//*[local-name() = $name]", name="FreightRateResponse")
        if len(details) > 0:
            return self.parse_freight_rate_response(response)
        else:
            return self.parse_package_rate_response(response)

    def parse_tracking_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_track_response(response)

    def parse_shipment_response(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        details = response.xpath(
            ".//*[local-name() = $name]", name="FreightShipResponse"
        ) + response.xpath(".//*[local-name() = $name]", name="ShipmentResponse")
        if len(details) > 0:
            shipmentNode = details[0]
            is_freight = "FreightShipResponse" in shipmentNode.tag
            shipment = (
                self.parse_freight_shipment_response(shipmentNode)
                if is_freight
                else self.parse_package_shipment_response(shipmentNode)
            )
        return (
            shipment if len(details) > 0 else None,
            self.parse_error_response(response),
        )
