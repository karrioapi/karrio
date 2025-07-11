import karrio.schemas.canadapost.rating as canadapost
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = [
        (
            f"{_}",
            [
                _extract_details(node, settings)
                for node in lib.find_element("price-quote", response)
            ],
        )
        for _, response in enumerate(responses, start=1)
    ]

    messages = provider_error.parse_error_response(responses, settings)
    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def _extract_details(
    node: lib.Element, settings: provider_utils.Settings
) -> models.RateDetails:
    quote = lib.to_object(canadapost.price_quoteType, node)
    service = provider_units.ServiceType.map(quote.service_code)

    adjustments = getattr(quote.price_details.adjustments, "adjustment", [])
    options = getattr(quote.price_details.options, "option", [])
    charges = [
        ("Base charge", quote.price_details.base),
        ("GST", quote.price_details.taxes.gst.valueOf_),
        ("PST", quote.price_details.taxes.pst.valueOf_),
        ("HST", quote.price_details.taxes.hst.valueOf_),
        *((o.option_name, o.option_price) for o in options),
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
) -> lib.Serializable:
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

    services = lib.to_services(payload.services, provider_units.ServiceType)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    requests = [
        canadapost.mailing_scenario(
            customer_number=settings.customer_number,
            contract_id=settings.contract_id,
            promo_code=None,
            quote_type=None,
            expected_mailing_date=package.options.shipment_date.state,
            options=(
                canadapost.optionsType(
                    option=[
                        canadapost.optionType(
                            option_code=option.code,
                            option_amount=lib.to_money(option.state),
                        )
                        for _, option in package.options.items()
                        if option.state is not False
                    ]
                )
                if any(
                    [
                        option
                        for _, option in package.options.items()
                        if option.state is not False
                    ]
                )
                else None
            ),
            parcel_characteristics=canadapost.parcel_characteristicsType(
                weight=package.weight.map(provider_units.MeasurementOptions).KG,
                dimensions=canadapost.dimensionsType(
                    length=package.length.map(provider_units.MeasurementOptions).CM,
                    width=package.width.map(provider_units.MeasurementOptions).CM,
                    height=package.height.map(provider_units.MeasurementOptions).CM,
                ),
                unpackaged=None,
                mailing_tube=None,
                oversized=None,
            ),
            services=(
                canadapost.servicesType(service_code=[svc.value for svc in services])
                if any(services)
                else None
            ),
            origin_postal_code=provider_utils.format_ca_postal_code(
                payload.shipper.postal_code
            ),
            destination=canadapost.destinationType(
                domestic=(
                    canadapost.domesticType(
                        postal_code=provider_utils.format_ca_postal_code(
                            payload.recipient.postal_code
                        )
                    )
                    if (payload.recipient.country_code == units.Country.CA.name)
                    else None
                ),
                united_states=(
                    canadapost.united_statesType(
                        zip_code=provider_utils.format_ca_postal_code(
                            payload.recipient.postal_code
                        )
                    )
                    if (payload.recipient.country_code == units.Country.US.name)
                    else None
                ),
                international=(
                    canadapost.internationalType(
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
        for package in packages
    ]

    return lib.Serializable(
        requests,
        lambda __: [
            lib.to_xml(
                request,
                namespacedef_='xmlns="http://www.canadapost.ca/ws/ship/rate-v4"',
            )
            for request in __
        ],
    )
