from typing import List, Tuple, TypeVar
from template.carrier_datatype_mock import CarrierRateRequestType
from purplship.mappers.carrier.interface import CarrierNameMapperBase
from purplship.domain.Types import RateRequest, QuoteDetails, Error

CarrierGenericResponseType = TypeVar("T")


class CarrierNameMapperPartial(CarrierNameMapperBase):

    """Response Parsing"""

    def parse_carrier_quote_response(
        self, response: CarrierGenericResponseType
    ) -> Tuple[QuoteDetails, List[Error]]:
        quotes = []
        return (
            [self._extract_quote(quote) for quote in quotes],
            self.parse_error_response(response),
        )

    def _extract_quote(
        self, quotes: List[QuoteDetails], quote: CarrierGenericResponseType
    ) -> List[QuoteDetails]:
        return quotes + [
            QuoteDetails(
                carrier=self.client.carrier_name,
                currency=None,
                delivery_date=None,
                service_name=None,
                service_type=None,
                base_charge=None,
                total_charge=None,
                duties_and_taxes=None,
                discount=None,
                extra_charges=[],
            )
        ]

    """Request Mapping"""

    def create_carrier_quote_request(
        self, payload: RateRequest
    ) -> CarrierRateRequestType:
        return CarrierRateRequestType()
