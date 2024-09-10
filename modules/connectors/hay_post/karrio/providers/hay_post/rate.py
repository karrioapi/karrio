import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hay_post.error as error

import karrio.providers.hay_post.utils as provider_utils
import karrio.providers.hay_post.units as provider_units
import karrio.schemas.hay_post.tariff_request as hay_post


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    rate_response = lib.to_dict(response.get("rates"))

    messages = error.parse_error_response(response, settings)
    rates = [
        (
            _extract_details(response, settings)
            if not isinstance(rate_response, dict)
            else None
        )
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    service = provider_units.ShippingService.map(
        str(data.get("request", {}).get("serviceCategoryDirectionId", 0))
    )
    currency = provider_units.ShippingCurrency.map(
        str(data.get("request", {}).get("currencyId", 0))
    ).name

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(data.get("rates", 0)),
        currency=currency,
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)

    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    service = (
        lib.to_services(payload.services, provider_units.ShippingService).first
        or provider_units.ShippingService.yes_ordered_value
    )

    currency_id = lib.to_int(
        provider_units.ShippingCurrency.map(options.currency.state).value
        or provider_units.ShippingCurrency.AMD.value
    )
    additional_services = [
        int(service.value.code)
        for service in provider_units.ShippingOption
        if service.name in options
    ]

    if not additional_services:
        additional_services.append(
            int(provider_units.ShippingOption.notification.value.code)
        )

    request = hay_post.TariffRequestElementType(
        customerId=int(settings.customer_id),
        serviceCategoryDirectionId=int(service.value),
        weight=packages.weight.value,
        totalPrice=packages.total_value if packages.total_value else 0,
        currencyId=currency_id,
        destinationAddress=hay_post.NAddressType(
            cityVillage=recipient.city,
            address=recipient.address_line1,
            postalCode=recipient.postal_code,
            receiverInfo=hay_post.ReceiverInfoType(
                companyName=recipient.company_name,
                firstName=recipient.person_name,
                phoneNumber=recipient.phone_number,
                email=recipient.email,
            ),
        ),
        returnAddress=hay_post.NAddressType(
            cityVillage=shipper.city,
            address=shipper.address_line1,
            postalCode=shipper.postal_code,
            receiverInfo=hay_post.ReceiverInfoType(
                companyName=shipper.company_name,
                firstName=shipper.person_name,
                phoneNumber=shipper.phone_number,
                email=shipper.email,
            ),
        ),
        additionalServices=additional_services,
    )

    return lib.Serializable(request, lib.to_dict)
