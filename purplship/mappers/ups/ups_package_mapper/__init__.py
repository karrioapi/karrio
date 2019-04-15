from typing import Tuple, List
from lxml import etree
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pyups import (
    package_rate as PRate,
    package_track as Track,
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

    def create_tracking_request(
        self, payload: T.TrackingRequest
    ) -> List[Track.TrackRequest]:
        return self.create_track_request(payload)

    def create_shipment_request(
        self, payload: T.ShipmentRequest
    ) -> PShip.ShipmentRequest:
        return self.create_package_ship_request(payload)

    def parse_quote_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_package_rate_response(response)

    def parse_tracking_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_track_response(response)

    def parse_shipment_response(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        details = response.xpath(".//*[local-name() = $name]", name="ShipmentResponse")
        return (
            self.parse_package_shipment_response(details[0])
            if len(details) > 0 else None,
            self.parse_error_response(response),
        )
