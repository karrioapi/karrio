from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pyups import (
    freight_rate as Rate, 
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

    def create_quote_request(self, payload: T.shipment_request) -> Rate.FreightRateRequest:
        return self.create_freight_rate_request(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> List[Track.TrackRequest]:
        return self.create_track_request(payload)

    def create_shipment_request(self, payload: T.shipment_request) -> Union[FShip.FreightShipRequest, PShip.ShipmentRequest]:
        is_freight = payload.shipment.extra.get('is_freight')
        return (
            self.create_freight_ship_request if is_freight else self.create_package_ship_request
        )(payload)


    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_freight_rate_response(response)

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_track_response(response)

    def parse_shipment_response(self, response: 'XMLElement') -> Tuple[T.ShipmentDetails, List[T.Error]]:
        details = response.xpath('.//*[local-name() = $name]', name="FreightShipResponse") + response.xpath('.//*[local-name() = $name]', name="ShipmentResponse")
        if len(details) > 0:
            shipmentNode = details[0]
            is_freight = 'FreightShipResponse' in shipmentNode.tag
            shipment = self.parse_freight_shipment_response(shipmentNode) if is_freight else self.parse_package_shipment_response(shipmentNode)
        return (
            shipment if len(details) > 0 else None, 
            self.parse_error_response(response)
        )
