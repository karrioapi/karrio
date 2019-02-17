from pycaps.rating import (
    mailing_scenario,
    optionsType,
    optionType,
    dimensionsType,
    parcel_characteristicsType,
    servicesType,
    destinationType,
    domesticType,
    united_statesType,
    internationalType,
    price_quoteType,
)
from lxml import etree
from datetime import datetime
from .interface import reduce, Tuple, List, T, CanadaPostMapperBase
from purplship.domain.Types.units import Weight, WeightUnit, Dimension, DimensionUnit
from purplship.mappers.caps.caps_units import OptionCode, ServiceType


class CanadaPostMapperPartial(CanadaPostMapperBase):
    def parse_price_quotes(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        price_quotes = response.xpath(".//*[local-name() = $name]", name="price-quote")
        quotes: List[T.QuoteDetails] = reduce(self._extract_quote, price_quotes, [])
        return (quotes, self.parse_error_response(response))

    def _extract_quote(
        self, quotes: List[T.QuoteDetails], price_quoteNode: etree.ElementBase
    ) -> List[T.QuoteDetails]:
        price_quote = price_quoteType()
        price_quote.build(price_quoteNode)
        discounts = [
            T.ChargeDetails(
                name=d.adjustment_name,
                currency="CAD",
                amount=float(d.adjustment_cost or 0),
            )
            for d in price_quote.price_details.adjustments.adjustment
        ]
        return quotes + [
            T.QuoteDetails(
                carrier=self.client.carrier_name,
                currency="CAD",
                delivery_date=str(price_quote.service_standard.expected_delivery_date),
                service_name=price_quote.service_name,
                service_type=price_quote.service_code,
                base_charge=float(price_quote.price_details.base or 0),
                total_charge=float(price_quote.price_details.due or 0),
                discount=reduce(lambda sum, d: sum + d.amount, discounts, 0.0),
                duties_and_taxes=float(
                    price_quote.price_details.taxes.gst.valueOf_ or 0
                )
                + float(price_quote.price_details.taxes.pst.valueOf_ or 0)
                + float(price_quote.price_details.taxes.hst.valueOf_ or 0),
                extra_charges=list(
                    map(
                        lambda a: T.ChargeDetails(
                            name=a.adjustment_name,
                            currency="CAD",
                            amount=float(a.adjustment_cost or 0),
                        ),
                        price_quote.price_details.adjustments.adjustment,
                    )
                ),
            )
        ]

    def create_mailing_scenario(self, payload: T.shipment_request) -> mailing_scenario:
        package = payload.shipment.items[0]
        requested_services = [
            svc for svc in payload.shipment.services if svc in ServiceType.__members__
        ]
        requested_options = [
            opt
            for opt in payload.shipment.options
            if opt.code in OptionCode.__members__
        ]

        return mailing_scenario(
            customer_number=payload.shipper.account_number,
            contract_id=payload.shipment.extra.get("contract-id"),
            promo_code=payload.shipment.extra.get("promo-code"),
            quote_type=payload.shipment.extra.get("quote-type"),
            expected_mailing_date=payload.shipment.extra.get("expected-mailing-date"),
            options=optionsType(
                option=[
                    optionType(
                        option_amount=option.value.get("option-amount"),
                        option_code=OptionCode[option.code].value,
                    )
                    for option in requested_options
                ]
            )
            if (len(requested_options) > 0)
            else None,
            parcel_characteristics=parcel_characteristicsType(
                weight=Weight(
                    (payload.shipment.total_weight or package.weight),
                    WeightUnit[payload.shipment.weight_unit],
                ).KG,
                dimensions=dimensionsType(
                    length=Dimension(
                        package.length, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    width=Dimension(
                        package.width, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    height=Dimension(
                        package.height, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                ),
                unpackaged=payload.shipment.extra.get("unpackaged"),
                mailing_tube=payload.shipment.extra.get("mailing-tube"),
                oversized=payload.shipment.extra.get("oversized"),
            ),
            services=servicesType(
                service_code=[ServiceType[code].value for code in requested_services]
            )
            if (len(requested_services) > 0)
            else None,
            origin_postal_code=payload.shipper.postal_code,
            destination=destinationType(
                domestic=domesticType(postal_code=payload.recipient.postal_code)
                if (payload.recipient.country_code == "CA")
                else None,
                united_states=united_statesType(zip_code=payload.recipient.postal_code)
                if (payload.recipient.country_code == "US")
                else None,
                international=internationalType(
                    country_code=payload.recipient.country_code
                )
                if (payload.recipient.country_code not in ["US", "CA"])
                else None,
            ),
        )
