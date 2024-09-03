"""Karrio SEKO Logistics rating API implementation."""

import karrio.schemas.seko.rating_request as seko
import karrio.schemas.seko.rating_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = None  # parse carrier rate type

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service="",  # extract service from rate
        total_charge=lib.to_money(0.0),  # extract the rate total rate cost
        currency="",  # extract the rate pricing currency
        transit_days=0,  # extract the rate transit days
        meta=dict(
            service_name="",  # extract the rate service human readable name
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to seko specific type
    request = seko.RateRequestType(
        DeliveryReference=None,
        Destination=seko.DestinationType(
            Id=None,
            Name=None,
            Address=seko.AddressType(
                BuildingName=None,
                StreetAddress=None,
                Suburb=None,
                City=None,
                PostCode=None,
                CountryCode=None,
            ),
            ContactPerson=None,
            PhoneNumber=None,
            Email=None,
            DeliveryInstructions=None,
            RecipientTaxId=None,
        ),
        IsSaturdayDelivery=None,
        IsSignatureRequired=None,
        Packages=[
            seko.PackageType(
                Height=None,
                Length=None,
                Id=None,
                Width=None,
                Kg=None,
                Name=None,
                PackageCode=None,
                Type=None,
            )
        ],
    )

    return lib.Serializable(request, lib.to_dict)
