import amazon_mws_lib.rate_request as amazon
from amazon_mws_lib.rate_response import ServiceRate

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.amazon_mws.error as provider_error
import karrio.providers.amazon_mws.units as provider_units
import karrio.providers.amazon_mws.utils as provider_utils


def parse_rate_response(
    response: dict, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    errors: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(data, settings)
            for data in response.get("errors", [])
        ],
        [],
    )
    rates = [
        _extract_details(data, settings) for data in response.get("serviceRates", [])
    ]

    return rates, errors


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(ServiceRate, data)
    transit = (
        lib.to_date(rate.promise.deliveryWindow.start, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        - lib.to_date(rate.promise.receiveWindow.end, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    ).days

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=provider_units.Service.map(rate.serviceType).name_or_key,
        total_charge=lib.to_decimal(rate.totalCharge.value),
        currency=rate.totalCharge.unit,
        transit_days=transit,
        meta=dict(
            service_name=rate.serviceType,
        ),
    )


def rate_request(payload: models.RateRequest, _) -> lib.Serializable:
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options)
    services = lib.to_services(payload.services, provider_units.Service)

    request = amazon.RateRequest(
        shipFrom=amazon.Ship(
            name=payload.shipper.person_name,
            city=payload.shipper.city,
            addressLine1=payload.shipper.address_line1,
            addressLine2=payload.shipper.address_line2,
            stateOrRegion=payload.shipper.state_code,
            email=payload.shipper.email,
            copyEmails=lib.join(payload.shipper.email),
            phoneNumber=payload.shipper.phone_number,
        ),
        shipTo=amazon.Ship(
            name=payload.recipient.person_name,
            city=payload.recipient.city,
            addressLine1=payload.recipient.address_line1,
            addressLine2=payload.recipient.address_line2,
            stateOrRegion=payload.recipient.state_code,
            email=payload.recipient.email,
            copyEmails=lib.join(payload.recipient.email),
            phoneNumber=payload.recipient.phone_number,
        ),
        serviceTypes=list(services),
        shipDate=lib.fdatetime(
            options.shipment_date.state, "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        containerSpecifications=[
            amazon.ContainerSpecification(
                dimensions=amazon.Dimensions(
                    height=package.height.IN,
                    length=package.length.IN,
                    width=package.width.IN,
                    unit="IN",
                ),
                weight=amazon.Weight(
                    value=package.weight.LB,
                    unit="LB",
                ),
            )
            for package in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
