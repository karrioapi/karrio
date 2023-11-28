import karrio.schemas.asendia_us.rate_request as asendia
import karrio.schemas.asendia_us.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.asendia_us.error as error
import karrio.providers.asendia_us.utils as provider_utils
import karrio.providers.asendia_us.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings) for rate in response.get("shippingRates") or []
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.ShippingRateType, data)
    service = provider_units.ShippingService.map(rate.productCode)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.rate),
        currency=rate.currencyType or "USD",
        meta=dict(
            service_name=service.name_or_key,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    package = lib.to_packages(payload.parcels).single
    service = lib.to_services(payload.services, provider_units.ShippingService).first

    request = asendia.RateRequestType(
        accountNumber=settings.account_number,
        subAccountNumber=settings.connection_config.sub_account_number.state,
        processingLocation=settings.connection_config.processing_location.state,
        recipientPostalCode=payload.recipient.postal_code,
        recipientCountryCode=payload.recipient.country_code,
        totalPackageWeight=package.weight.value,
        weightUnit=provider_units.WeightUnit.map(package.weight_unit.value).value,
        dimLength=package.length.value,
        dimWidth=package.width.value,
        dimHeight=package.height.value,
        dimUnit=package.dimension_unit.value,
        productCode=getattr(service, "value", None) or "*",
    )

    return lib.Serializable(request, lib.to_dict)
