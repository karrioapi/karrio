import karrio.schemas.allied_express.rate_request as allied
import karrio.schemas.allied_express.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.allied_express.error as error
import karrio.providers.allied_express.utils as provider_utils
import karrio.providers.allied_express.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[provider_utils.AlliedResponse],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate.data["result"], settings, _response.ctx)
        for rate in [response]
        if not rate.is_error and "result" in (rate.data or {})
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.RateDetails:
    rate = lib.to_object(rating.ResultType, data)
    service = provider_units.ShippingService.map(
        ctx.get("service")
        or settings.connection_config.account_service_type.state
        or settings.service_type
        or "R"
    )
    charges = [
        ("Job charge", lib.to_money(rate.jobCharge)),
        *((s.chargeCode, lib.to_money(s.netValue)) for s in rate.surcharges),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.totalCharge),
        currency=units.Currency.AUD.name,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=amount,
                currency=units.Currency.AUD.name,
            )
            for name, amount in charges
            if amount > 0
        ],
        meta=dict(
            service_name=service.name,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    service = (
        getattr(services.first, "value", None)
        or settings.connection_config.account_service_type.state
        or settings.service_type
        or "R"
    )

    request = allied.RateRequestType(
        bookedBy=shipper.contact,
        account=settings.account,
        instructions=options.instructions.state or "N/A",
        itemCount=len(packages),
        items=[
            allied.ItemType(
                dangerous=(True if pkg.options.dangerous_good.state else False),
                height=pkg.height.map(provider_units.MeasurementOptions).CM,
                length=pkg.length.map(provider_units.MeasurementOptions).CM,
                width=pkg.width.map(provider_units.MeasurementOptions).CM,
                weight=pkg.weight.map(provider_units.MeasurementOptions).KG,
                volume=pkg.volume.map(provider_units.MeasurementOptions).m3,
                itemCount=(pkg.items.quantity if any(pkg.items) else 1),
            )
            for pkg in packages
        ],
        jobStopsP=allied.JobStopsType(
            companyName=(shipper.company_name or shipper.contact),
            contact=shipper.contact,
            emailAddress=shipper.email or " ",
            geographicAddress=allied.GeographicAddressType(
                address1=shipper.address_line1,
                address2=shipper.address_line2 or " ",
                country=shipper.country_code,
                postCode=shipper.postal_code,
                state=shipper.state_code,
                suburb=shipper.city,
            ),
            phoneNumber=shipper.phone_number or "(00) 0000 0000",
        ),
        jobStopsD=allied.JobStopsType(
            companyName=(recipient.company_name or recipient.contact),
            contact=recipient.contact,
            emailAddress=recipient.email or " ",
            geographicAddress=allied.GeographicAddressType(
                address1=recipient.address_line1,
                address2=recipient.address_line2 or " ",
                country=recipient.country_code,
                postCode=recipient.postal_code,
                state=recipient.state_code,
                suburb=recipient.city,
            ),
            phoneNumber=recipient.phone_number or "(00) 0000 0000",
        ),
        referenceNumbers=([payload.reference] if any(payload.reference or "") else []),
        serviceLevel=service,
        weight=packages.weight.map(provider_units.MeasurementOptions).KG,
        volume=packages.volume.map(provider_units.MeasurementOptions).m3,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_json(_)
        .replace("jobStopsP", "jobStops_P")
        .replace("jobStopsD", "jobStops_D"),
        dict(service=service),
    )
