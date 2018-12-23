from typing import Tuple, List, Union
from purplship.domain.mapper import Mapper
from purplship.domain import Types as T
from pypurolator.EstimatorService import GetFullEstimateRequestContainer as PackageEstimate
from pypurolator.FreightEstimatingService import GetEstimateRequestContainer as FreightEstimate
from pypurolator.TrackingService import RequestContainer as TrackingRequestContainer
from .partials import (
    PurolatorRateMapperPartial, 
    PurolatorTrackMapperPartial
)


class PurolatorMapper(
        Mapper,
        PurolatorRateMapperPartial,
        PurolatorTrackMapperPartial
    ):        

    def create_quote_request(self, payload: T.shipment_request) -> Union[PackageEstimate, FreightEstimate]:
        is_freight = False
        return (
            self.create_estimate_request if is_freight else self.create_freight_estimate_request
        )(payload)

    def create_tracking_request(self, payload: T.tracking_request) -> TrackingRequestContainer:
        return self.create_tracking_request(payload)



    def parse_quote_response(self, response: 'XMLElement') -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        return self.parse_estimate_response(response)

    def parse_tracking_response(self, response: 'XMLElement') -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        return self.parse_package_tracking_response(response)