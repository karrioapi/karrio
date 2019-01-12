from typing import Tuple, List, Union
from functools import reduce
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from purplship.domain.Types.units import (
    Weight,
    WeightUnit,
    Dimension,
    DimensionUnit
)
from pyups import (
    freight_rate as Rate, 
    package_rate as PRate,
    package_track as Track, 
    UPSSecurity as Security, 
    error as Err,
    freight_ship as FShip,
    package_ship as PShip
)
from .partials import (
    UPSRateMapperPartial, 
    UPSTrackMapperPartial, 
    UPSShipmentMapperPartial
)


class UPSMapper(
        Mapper,
        UPSRateMapperPartial,
        UPSTrackMapperPartial,
        UPSShipmentMapperPartial
    ):        

    def create_quote_request(self, payload: T.shipment_request) -> Union[PRate.RateRequest, Rate.FreightRateRequest]:
        return (
            self.create_freight_rate_request if _is_freight(payload) else self.create_package_rate_request
        )(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> List[Track.TrackRequest]:
        return self.create_track_request(payload)

    def create_shipment_request(self, payload: T.shipment_request) -> Union[FShip.FreightShipRequest, PShip.ShipmentRequest]:
        return (
            self.create_freight_ship_request if _is_freight(payload) else self.create_package_ship_request
        )(payload)


    def parse_quote_response(self, response: etree.ElementBase) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        details = response.xpath('.//*[local-name() = $name]', name="FreightRateResponse") + response.xpath('.//*[local-name() = $name]', name="FreightRateResponse")
        if len(details) > 0:
            return self.parse_freight_rate_response(response)
        else:
            return self.parse_package_rate_response(response)

    def parse_tracking_response(self, response: etree.ElementBase) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_track_response(response)

    def parse_shipment_response(self, response: etree.ElementBase) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        details = response.xpath('.//*[local-name() = $name]', name="FreightShipResponse") + response.xpath('.//*[local-name() = $name]', name="ShipmentResponse")
        if len(details) > 0:
            shipmentNode = details[0]
            is_freight = 'FreightShipResponse' in shipmentNode.tag
            shipment = self.parse_freight_shipment_response(shipmentNode) if is_freight else self.parse_package_shipment_response(shipmentNode)
        return (
            shipment if len(details) > 0 else None, 
            self.parse_error_response(response)
        )



def _is_freight(payload: T.shipment_request) -> bool:
    total_weight = Weight(
        payload.shipment.total_weight or reduce(lambda t, i: t + i.weight, payload.shipment.items, 0.0),
        WeightUnit[payload.shipment.weight_unit]
    ).LB
    any_item_size_over_165 = any([
        (
            Dimension(item.length or 0, DimensionUnit[payload.shipment.dimension_unit]).IN > 165 
        ) for item in payload.shipment.items
    ])
    return total_weight > 150 or any_item_size_over_165

