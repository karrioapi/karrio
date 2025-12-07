"""Karrio DPD Group rating API implementation."""

import karrio.schemas.dpd_group.rate_request as dpd_group_req
import karrio.schemas.dpd_group.rate_response as dpd_group_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils
import karrio.providers.dpd_group.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings) 
        for rate in response.get("rates", [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(dpd_group_res.RateType, data)
    service = provider_units.ShippingService.map(rate.productCode or "CL")

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.totalAmount),
        currency=rate.currency or "EUR",
        transit_days=rate.transitDays,
        meta=dict(
            service_name=service.value_or_key,
            product_code=rate.productCode,
            product_name=rate.productName,
            delivery_date=rate.deliveryDate,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        options=lib.to_shipping_options(
            payload.options,
            initializer=provider_units.shipping_options_initializer,
        ),
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    # Get requested services or use defaults
    services = payload.services or [
        service.value for service in provider_units.ShippingService
    ]

    # Build rate request using generated schema types
    request = dpd_group_req.RateRequestType(
        shipperAddress=dpd_group_req.ErAddressType(
            postalCode=shipper.postal_code,
            city=shipper.city,
            country=shipper.country_code,
        ),
        receiverAddress=dpd_group_req.ErAddressType(
            postalCode=recipient.postal_code,
            city=recipient.city,
            country=recipient.country_code,
        ),
        parcels=[
            dpd_group_req.ParcelType(
                weight=package.weight.KG,
                length=package.length.CM,
                width=package.width.CM,
                height=package.height.CM,
            )
            for package in packages
        ],
        productCodes=services,
    )

    return lib.Serializable(request, lib.to_dict)
