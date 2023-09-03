import karrio.schemas.boxknight.rate_request as boxknight
import karrio.schemas.boxknight.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.boxknight.error as error
import karrio.providers.boxknight.utils as provider_utils
import karrio.providers.boxknight.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[typing.Union[dict, typing.List[dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings)
        for rate in response
        if isinstance(response, list)
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.Rate, data)
    service = provider_units.ShippingService.map(rate.service)
    transit_days = (
        lib.to_date(rate.estimateTo, "%Y-%m-%d")
        - lib.to_date(rate.estimateFrom, "%Y-%m-%d")
    ).days

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.price),
        currency=units.Currency.CAD.name,
        transit_days=transit_days if transit_days > 0 else 1,
        meta=dict(service_name=rate.name),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    if (
        payload.shipper.country_code is not None
        and payload.shipper.country_code != units.Country.CA.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    if (
        payload.recipient.country_code is not None
        and payload.recipient.country_code != units.Country.CA.name
    ):
        raise errors.DestinationNotServicedError(payload.recipient.country_code)

    packages = lib.to_packages(payload.parcels)

    request = boxknight.RateRequest(
        postalCode=payload.recipient.postal_code,
        originPostalCode=payload.shipper.postal_code,
        packages=[
            boxknight.Package(
                refNumber=package.parcel.reference_number or str(idx),
                weightOptions=boxknight.WeightOptions(
                    weight=package.weight.value,
                    unit=package.weight_unit.value.lower(),
                ),
                sizeOptions=boxknight.SizeOptions(
                    length=package.length.value,
                    width=package.width.value,
                    height=package.height.value,
                    unit=provider_units.DimensionUnit.map(
                        package.dimension_unit.name
                    ).value,
                ),
            )
            for idx, package in enumerate(packages, start=1)
        ],
    )

    return lib.Serializable(request, lib.to_dict)
