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
)
from typing import List, Tuple
from karrio.core.utils import Serializable, Element, NF, XP
from karrio.providers.canadapost.utils import Settings, format_ca_postal_code
from karrio.core.units import Country, Currency, Packages, Services, Options
from karrio.core.errors import OriginNotServicedError
from karrio.core.models import RateDetails, ChargeDetails, Message, RateRequest
from karrio.providers.canadapost.error import parse_error_response
from karrio.providers.canadapost.units import (
    ShippingOption,
    ServiceType,
    PackagePresets,
    MeasurementOptions,
    CUSTOM_OPTIONS,
)


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    price_quotes = XP.find("price-quote", response)
    quotes: List[RateDetails] = [
        _extract_quote(price_quote_node, settings) for price_quote_node in price_quotes
    ]
    return quotes, parse_error_response(response, settings)


def _extract_quote(node: Element, settings: Settings) -> RateDetails:
    quote = XP.to_object(price_quoteType, node)
    service = ServiceType.map(quote.service_code)

    adjustments = getattr(quote.price_details.adjustments, "adjustment", [])
    charges = [
        ("Base charge", quote.price_details.base),
        ("GST", quote.price_details.taxes.gst.valueOf_),
        ("PST", quote.price_details.taxes.pst.valueOf_),
        ("HST", quote.price_details.taxes.hst.valueOf_),
        *((a.adjustment_name, a.adjustment_cost) for a in adjustments),
    ]

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=Currency.CAD.name,
        transit_days=quote.service_standard.expected_transit_time,
        service=service.name_or_key,
        total_charge=NF.decimal(quote.price_details.due or 0),
        extra_charges=[
            ChargeDetails(
                name=name,
                currency=Currency.CAD.name,
                amount=NF.decimal(amount),
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=(service.name or quote.service_name)),
    )


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[mailing_scenario]:
    """Create the appropriate Canada Post rate request depending on the destination

    :param settings: Karrio carrier connection settings
    :param payload: Karrio unified API rate request data
    :return: a domestic or international Canada post compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """
    if payload.shipper.country_code and payload.shipper.country_code != Country.CA.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    package = Packages(payload.parcels, PackagePresets, required=["weight"]).single
    services = Services(payload.services, ServiceType)
    options = ShippingOption.to_options(
        payload.options,
        package_options=package.options,
        is_international=(
            payload.recipient.country_code is not None
            and payload.recipient.country_code != "CA"
        ),
    )

    request = mailing_scenario(
        customer_number=settings.customer_number,
        contract_id=settings.contract_id,
        promo_code=None,
        quote_type=None,
        expected_mailing_date=options.shipment_date,
        options=(
            optionsType(
                option=[
                    optionType(
                        option_code=code,
                        option_amount=value,
                    )
                    for _, code, value in options.as_list()
                ]
            )
            if any(options.as_list())
            else None
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
            servicesType(service_code=[svc.value for svc in services])
            if any(services)
            else None
        ),
        origin_postal_code=format_ca_postal_code(payload.shipper.postal_code),
        destination=destinationType(
            domestic=(
                domesticType(
                    postal_code=format_ca_postal_code(payload.recipient.postal_code)
                )
                if (payload.recipient.country_code == Country.CA.name)
                else None
            ),
            united_states=(
                united_statesType(
                    zip_code=format_ca_postal_code(payload.recipient.postal_code)
                )
                if (payload.recipient.country_code == Country.US.name)
                else None
            ),
            international=(
                internationalType(
                    country_code=format_ca_postal_code(payload.recipient.postal_code)
                )
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
