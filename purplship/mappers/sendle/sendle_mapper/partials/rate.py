"""PurplShip Sendle rate mapper module."""

from functools import reduce
from typing import List, Tuple, Union
from purplship.mappers.sendle.sendle_mapper.partials.interface import SendleMapperBase
from purplship.mappers.sendle.sendle_units import Plan
from purplship.domain.Types import (
    RateRequest,
    QuoteDetails,
    Error
)
from pysendle.quotes import (
    DomesticParcelQuote,
    InternationalParcelQuote,
    ParcelQuoteResponse
)

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class SendleMapperPartial(SendleMapperBase):
    def parse_parcel_quote_response(
        self, response: dict
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        parcel_quotes: List[ParcelQuoteResponse] = [
            ParcelQuoteResponse(**p) for p in response
        ] if isinstance(response, list) else []
        return (
            [self._extract_quote(p) for p in parcel_quotes],
            self.parse_error_response([response])
        )

    def _extract_quote(self, parcel_quote: ParcelQuoteResponse) -> QuoteDetails:
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=parcel_quote.plan_name,
            service_type=parcel_quote.plan_name,
            base_charge=parcel_quote.quote.gross.amount,
            duties_and_taxes=parcel_quote.quote.tax.amount,
            total_charge=parcel_quote.quote.net.amount,
            currency=parcel_quote.quote.net.currency,
            delivery_date=parcel_quote.eta.date_range[-1],
            discount=None,
            extra_charges=[]
        )

    def create_parcel_quote_request(self, payload: RateRequest) -> ParcelQuoteRequest:
        return (
            SendleMapperPartial._create_domestic_quote
            if (
                payload.recipient.country_code is None or
                payload.recipient.country_code == 'AU'
            ) else
            SendleMapperPartial._create_international_quote
        )(payload)

    @staticmethod
    def _create_domestic_quote(payload: RateRequest) -> ParcelQuoteRequest:
        return DomesticParcelQuote(
            pickup_suburb=" ".join(payload.shipper.address_lines),
            pickup_postcode=payload.shipper.postal_code,
            delivery_suburb=" ".join(payload.recipient.address_lines),
            delivery_postcode=payload.recipient.postal_code,
            kilogram_weight=payload.shipment.total_weight or payload.shipment.items[0].weight,
            cubic_metre_volume=(
                payload.shipment.extra.get('cubic_metre_volume') or
                payload.shipment.items[0].extra.get('cubic_metre_volume')
            ),
            plan_name=SendleMapperPartial._plan_name(payload)
        )

    @staticmethod
    def _create_international_quote(payload: RateRequest) -> ParcelQuoteRequest:
        return InternationalParcelQuote(
            pickup_suburb=" ".join(payload.shipper.address_lines),
            pickup_postcode=payload.shipper.postal_code,
            delivery_country=payload.recipient.country_code,
            kilogram_weight=payload.shipment.total_weight or payload.shipment.items[0].weight,
            cubic_metre_volume=None,
            plan_name=SendleMapperPartial._plan_name(payload)
        )

    @staticmethod
    def _plan_name(payload: RateRequest) -> str:
        return reduce(
            lambda plan, s: Plan[s].value if s in Plan.__members__ else None,
            payload.shipment.services,
            None
        )
