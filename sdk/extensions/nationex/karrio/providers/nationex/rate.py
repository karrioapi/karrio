import karrio.schemas.nationex.rate_request as nationex
import karrio.schemas.nationex.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.nationex.error as error
import karrio.providers.nationex.utils as provider_utils
import karrio.providers.nationex.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(response, settings)] if not any(messages) else []

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.RateResponseType, data)
    service = provider_units.ShippingService.nationex_delivery
    charges = [
        ("Base Charge", rate.BasePrice),
        ("Fuel Surcharge", rate.FuelCharge),
        ("NCVCharge", rate.NCVCharge),
        *[
            (_.NameFr if settings.language == "fr" else _.NameEn, _.Charge)
            for _ in rate.AccessoryCharges
            if _.Charge > 0
        ],
        *[
            (_.NameFr if settings.language == "fr" else _.NameEn, _.Charge)
            for _ in rate.SurchargeCharges
            if _.Charge > 0
        ],
        *[
            (_.NameFr if settings.language == "fr" else _.NameEn, _.Charge)
            for _ in rate.TaxCharges
            if _.Charge > 0
        ],
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name,
        total_charge=lib.to_money(rate.Total),
        currency="CAD",
        transit_days=rate.DelayTransitDays,
        estimated_delivery=lib.fdate(rate.EstimatedDeliveryDate, "%Y-%m-%d"),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                currency="CAD",
                amount=lib.to_money(amount),
            )
            for name, amount in charges
            if amount > 0
        ],
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    packages = lib.to_packages(
        payload.parcels,
        max_weight=units.Weight(99, "LB"),
    )
    service = lib.to_services(
        payload.services,
        initializer=provider_units.shipping_services_initializer,
    ).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    unit = provider_units.MeasurementUnit.map(packages.weight_unit).value

    request = nationex.RateRequestType(
        CustomerId=lib.to_int(settings.customer_id),
        ExpeditionDate=lib.fdate(options.shipment_date.state, "%Y-%m-%d"),
        ShipmentType=service.value,
        SourcePostalCode=payload.shipper.postal_code,
        DestinationPostalCode=payload.recipient.postal_code,
        TotalWeight=packages.weight.value,
        TotalParcels=len(packages),
        UnitsOfMeasurement=unit,
        Accessory=nationex.AccessoryType(
            InsuranceAmount=options.nationex_insurance_amount.state,
            FrozenProtection=options.nationex_frozen_protection.state,
            DangerousGoods=options.nationex_dangerous_goods.state,
            SNR=(
                options.nationex_snr.state
                if options.nationex_snr.state is not None
                else True
            ),
        ),
        Parcels=[
            nationex.ParcelType(
                NCV=(
                    True
                    if (
                        package.length.IN > 36
                        or package.width.IN > 36
                        or package.height.IN > 36
                        or package.weight.LB > 70
                    )
                    else False
                ),
                Weight=package.weight.map(provider_units.MeasurementOptions).value,
                Dimensions=(
                    nationex.DimensionsType(
                        Length=package.length.value,
                        Width=package.width.value,
                        Height=package.height.value,
                        Cubing=lib.to_decimal(
                            (package.length.IN * package.width.IN * package.height.IN)
                            / 1728
                        ),
                    )
                    if any(
                        [
                            package.length.value,
                            package.width.value,
                            package.height.value,
                        ]
                    )
                    else None
                ),
            )
            for package in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
