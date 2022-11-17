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
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    price_quotes = lib.find_element("price-quote", response)
    quotes: typing.List[models.RateDetails] = [
        _extract_quote(price_quote_node, settings) for price_quote_node in price_quotes
    ]
    return quotes, provider_error.parse_error_response(response, settings)


def _extract_quote(
    node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    quote = lib.to_object(price_quoteType, node)
    service = provider_units.ServiceType.map(quote.service_code)

    adjustments = getattr(quote.price_details.adjustments, "adjustment", [])
    charges = [
        ("Base charge", quote.price_details.base),
        ("GST", quote.price_details.taxes.gst.valueOf_),
        ("PST", quote.price_details.taxes.pst.valueOf_),
        ("HST", quote.price_details.taxes.hst.valueOf_),
        *((a.adjustment_name, a.adjustment_cost) for a in adjustments),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=units.Currency.CAD.name,
        transit_days=quote.service_standard.expected_transit_time,
        service=service.name_or_key,
        total_charge=lib.to_money(quote.price_details.due or 0),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency=units.Currency.CAD.name,
                amount=lib.to_money(amount),
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=(service.name or quote.service_name)),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[mailing_scenario]:
    """Create the appropriate Canada Post rate request depending on the destination

    :param settings: Karrio carrier connection settings
    :param payload: Karrio unified API rate request data
    :return: a domestic or international Canada post compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """
    if (
        payload.shipper.country_code
        and payload.shipper.country_code != units.Country.CA.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    package = lib.to_packages(
        payload.parcels, provider_units.PackagePresets, required=["weight"]
    ).single
    services = lib.to_services(payload.services, provider_units.ServiceType)
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = mailing_scenario(
        customer_number=settings.customer_number,
        contract_id=settings.contract_id,
        promo_code=None,
        quote_type=None,
        expected_mailing_date=options.shipment_date.state,
        options=(
            optionsType(
                option=[
                    optionType(
                        option_code=option.code,
                        option_amount=lib.to_money(option.state),
                    )
                    for _, option in options.items()
                ]
            )
            if any(options.items())
            else None
        ),
        parcel_characteristics=parcel_characteristicsType(
            weight=package.weight.map(provider_units.MeasurementOptions).KG,
            dimensions=dimensionsType(
                length=package.length.map(provider_units.MeasurementOptions).CM,
                width=package.width.map(provider_units.MeasurementOptions).CM,
                height=package.height.map(provider_units.MeasurementOptions).CM,
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
        origin_postal_code=provider_utils.format_ca_postal_code(
            payload.shipper.postal_code
        ),
        destination=destinationType(
            domestic=(
                domesticType(
                    postal_code=provider_utils.format_ca_postal_code(
                        payload.recipient.postal_code
                    )
                )
                if (payload.recipient.country_code == units.Country.CA.name)
                else None
            ),
            united_states=(
                united_statesType(
                    zip_code=provider_utils.format_ca_postal_code(
                        payload.recipient.postal_code
                    )
                )
                if (payload.recipient.country_code == units.Country.US.name)
                else None
            ),
            international=(
                internationalType(
                    country_code=provider_utils.format_ca_postal_code(
                        payload.recipient.postal_code
                    )
                )
                if (
                    payload.recipient.country_code
                    not in [units.Country.US.name, units.Country.CA.name]
                )
                else None
            ),
        ),
    )

    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: mailing_scenario) -> str:
    return lib.to_xml(
        request, namespacedef_='xmlns="http://www.canadapost.ca/ws/ship/rate-v4"'
    )
