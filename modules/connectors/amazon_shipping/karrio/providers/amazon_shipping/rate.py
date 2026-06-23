"""Karrio Amazon Shipping rating implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.units as provider_units
import karrio.providers.amazon_shipping.utils as provider_utils
import karrio.schemas.amazon_shipping.rate_response as amazon


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[list[models.RateDetails], list[models.Message]]:
    """Parse rate response from Amazon Shipping API. See SPECS.md."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    payload = response.get("payload") or {}

    rates = [_extract_details(rate, settings) for rate in payload.get("rates") or []]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from API response."""
    rate = lib.to_object(amazon.Rate, data)

    # Calculate transit days from delivery window
    transit_days = lib.failsafe(
        lambda: (
            (
                lib.to_date(rate.promise.deliveryWindow.start).date()
                - lib.to_date(rate.promise.pickupWindow.start).date()
            ).days
        )
    )

    # Extract rate items as extra charges
    extra_charges = [
        models.ChargeDetails(
            name=item.rateItemNameLocalization or item.rateItemID,
            amount=lib.to_money(item.rateItemCharge.value),
            currency=item.rateItemCharge.unit,
        )
        for item in rate.rateItemList or []
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=provider_units.ShippingService.map(rate.serviceId).name_or_key,
        total_charge=lib.to_money(rate.totalCharge.value),
        currency=rate.totalCharge.unit,
        transit_days=transit_days,
        extra_charges=extra_charges,
        meta=dict(
            rate_id=rate.rateId,
            carrier_id=rate.carrierId,
            carrier_name=rate.carrierName,
            service_id=rate.serviceId,
            service_name=rate.serviceName,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Amazon Shipping rate request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
    )
    customs_declared_value = lib.to_money(customs.duty.declared_value if customs.duty else None)

    label_format = options.amazon_shipping_label_format.state or settings.connection_config.label_format.state or "PNG"

    request = dict(
        shipFrom=dict(
            name=shipper.company_name or shipper.person_name,
            addressLine1=shipper.street,
            addressLine2=shipper.address_line2,
            addressLine3=None,
            companyName=shipper.company_name,
            stateOrRegion=shipper.state_code,
            city=shipper.city,
            countryCode=shipper.country_code,
            postalCode=shipper.postal_code,
            email=shipper.email,
            phoneNumber=shipper.phone_number,
        ),
        shipTo=dict(
            name=recipient.company_name or recipient.person_name,
            addressLine1=recipient.street,
            addressLine2=recipient.address_line2,
            addressLine3=None,
            companyName=recipient.company_name,
            stateOrRegion=recipient.state_code,
            city=recipient.city,
            countryCode=recipient.country_code,
            postalCode=recipient.postal_code,
            email=recipient.email,
            phoneNumber=recipient.phone_number,
        ),
        shipDate=lib.fdatetime(
            options.shipment_date.state,
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%SZ",
        )
        if options.shipment_date.state
        else None,
        packages=[
            dict(
                dimensions=dict(
                    length=package.length.IN,
                    width=package.width.IN,
                    height=package.height.IN,
                    unit="INCH",
                )
                if package.has_dimensions
                else None,
                weight=dict(
                    value=package.weight.LB,
                    unit="POUND",
                ),
                # insuredValue and items are required by the v2 spec (see SPECS.md).
                insuredValue=dict(
                    value=lib.to_money(package.options.declared_value.state or customs_declared_value or 0),
                    unit=package.options.currency.state or "USD",
                ),
                items=[
                    dict(
                        quantity=item.quantity or 1,
                        description=item.description,
                        itemIdentifier=item.sku or item.hs_code,
                        weight=dict(
                            value=item.weight,
                            unit="POUND",
                        )
                        if item.weight
                        else None,
                        itemValue=dict(
                            value=lib.to_money(item.value_amount),
                            unit=item.value_currency or "USD",
                        )
                        if item.value_amount
                        else None,
                    )
                    for item in (package.items or [])
                ],
                packageClientReferenceId=package.parcel.id or str(index),
            )
            for index, package in enumerate(packages, 1)
        ],
        channelDetails=dict(
            channelType=options.amazon_shipping_channel_type.state or "EXTERNAL",
        ),
        labelSpecifications=dict(
            format=label_format,
            size=dict(
                length=settings.connection_config.label_size_length.state or 6,
                width=settings.connection_config.label_size_width.state or 4,
                unit=settings.connection_config.label_size_unit.state or "INCH",
            ),
            dpi=300,
            pageLayout="DEFAULT",
            needFileJoining=False,
            requestedDocumentTypes=["LABEL"],
        ),
        serviceSelection=dict(
            serviceId=list(services) if any(services) else None,
        )
        if any(services)
        else None,
    )

    return lib.Serializable(request, lib.to_dict)
