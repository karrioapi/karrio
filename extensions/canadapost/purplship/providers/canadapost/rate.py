from canadapost_lib.rating import (
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
    service_standardType,
)
from functools import reduce
from typing import List, Tuple, cast
from purplship.core.utils import Serializable, Element, NF, XP
from purplship.providers.canadapost.utils import Settings
from purplship.core.units import Country, Currency, Packages, Services, Options
from purplship.core.errors import OriginNotServicedError
from purplship.core.models import RateDetails, ChargeDetails, Message, RateRequest
from purplship.providers.canadapost.error import parse_error_response
from purplship.providers.canadapost.units import OptionCode, ServiceType, PackagePresets, MeasurementOptions


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    price_quotes = response.xpath(".//*[local-name() = $name]", name="price-quote")
    quotes: List[RateDetails] = [
        _extract_quote(price_quote_node, settings) for price_quote_node in price_quotes
    ]
    return quotes, parse_error_response(response, settings)


def _extract_quote(price_quote_node: Element, settings: Settings) -> RateDetails:
    price_quote = price_quoteType()
    price_quote.build(price_quote_node)
    currency = Currency.CAD.name
    discounts = [
        ChargeDetails(
            name=d.adjustment_name,
            currency=currency,
            amount=NF.decimal(d.adjustment_cost or 0),
        )
        for d in price_quote.price_details.adjustments.adjustment
    ]
    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=currency,
        transit_days=cast(
            service_standardType, price_quote.service_standard
        ).expected_transit_time,
        service=ServiceType(price_quote.service_code).name,
        base_charge=NF.decimal(price_quote.price_details.base or 0),
        total_charge=NF.decimal(price_quote.price_details.due or 0),
        discount=NF.decimal(reduce(lambda total, d: total + d.amount, discounts, 0.0)),
        duties_and_taxes=NF.decimal(
            float(price_quote.price_details.taxes.gst.valueOf_ or 0)
            + float(price_quote.price_details.taxes.pst.valueOf_ or 0)
            + float(price_quote.price_details.taxes.hst.valueOf_ or 0)
        ),
        extra_charges=list(
            map(
                lambda a: ChargeDetails(
                    name=a.adjustment_name,
                    currency=currency,
                    amount=NF.decimal(a.adjustment_cost or 0),
                ),
                price_quote.price_details.adjustments.adjustment,
            )
        ),
    )


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[mailing_scenario]:
    """Create the appropriate Canada Post rate request depending on the destination

    :param settings: Purplship carrier connection settings
    :param payload: Purplship unified API rate request data
    :return: a domestic or international Canada post compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """
    if payload.shipper.country_code and payload.shipper.country_code != Country.CA.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    package = Packages(payload.parcels, PackagePresets, required=["weight"]).single
    services = Services(payload.services, ServiceType)
    options = Options(payload.options, OptionCode)

    request = mailing_scenario(
        customer_number=settings.customer_number,
        contract_id=None,
        promo_code=None,
        quote_type=None,
        expected_mailing_date=options.shipment_date,
        options=(
            optionsType(
                option=[
                    optionType(
                        option_code=getattr(option, 'key', option),
                        option_amount=getattr(option, 'value', None)
                    )
                    for code, option in options if code in OptionCode
                ]
            )
            if any([c in OptionCode for c, _ in options]) else None
        ),
        parcel_characteristics=parcel_characteristicsType(
            weight=package.weight.map(MeasurementOptions).KG,
            dimensions=dimensionsType(
                length=package.length.map(MeasurementOptions).CM,
                width=package.width.map(MeasurementOptions).CM,
                height=package.height.map(MeasurementOptions).CM,
            ),
            unpackaged=None,
            mailing_tube=None,
            oversized=None,
        ),
        services=(
            servicesType(
                service_code=[svc.value for svc in services]
            )
            if any(services) else None
        ),
        origin_postal_code=payload.shipper.postal_code,
        destination=destinationType(
            domestic=(
                domesticType(postal_code=payload.recipient.postal_code)
                if (payload.recipient.country_code == Country.CA.name)
                else None
            ),
            united_states=(
                united_statesType(zip_code=payload.recipient.postal_code)
                if (payload.recipient.country_code == Country.US.name)
                else None
            ),
            international=(
                internationalType(country_code=payload.recipient.postal_code)
                if (
                    payload.recipient.country_code
                    not in [Country.US.name, Country.CA.name]
                )
                else None
            ),
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: mailing_scenario) -> str:
    return XP.export(
        request, namespacedef_='xmlns="http://www.canadapost.ca/ws/ship/rate-v4"'
    )


def _amount(value):
    if isinstance(value, (bool)):
        return None

    return float(value)
