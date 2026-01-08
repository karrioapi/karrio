"""Karrio ParcelOne rating implementation.

Note: ParcelOne REST API returns charges as part of the shipment creation response.
This implementation creates a rate request that can be used to get charges
by setting ReturnCharges=1 on the shipment request.
"""

import typing
import karrio.schemas.parcelone as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse rate response from ParcelOne REST API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    rates = lib.identity(
        [_extract_rate(response, settings, _response.ctx)]
        if response.get("success") == 1 and response.get("results")
        else []
    )

    return [rate for rate in rates if rate is not None], messages


def _extract_rate(
    data: dict,
    settings: provider_utils.Settings,
    ctx: typing.Dict[str, typing.Any] = None,
) -> typing.Optional[models.RateDetails]:
    """Extract rate details from API response."""
    ctx = ctx or {}
    result = lib.to_object(parcelone.ShipmentResultType, data.get("results") or {})

    # Check if we have charges in the response
    if result.TotalCharges is None and not result.Charges:
        return None

    service_code = ctx.get("service_code", "parcelone_pa1_eco")
    service = provider_units.ShippingService.map(service_code)

    total_charge = lib.failsafe(lambda: float(result.TotalCharges.Value)) if result.TotalCharges else 0.0
    currency = lib.failsafe(lambda: result.TotalCharges.Currency) or "EUR"

    extra_charges = [
        models.ChargeDetails(
            name=charge.Description or "Shipping Charge",
            amount=lib.to_money(charge.Value),
            currency=charge.Currency or currency,
        )
        for charge in (result.Charges or [])
        if charge.Value
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        extra_charges=extra_charges,
        meta=dict(
            service_name=service.name_or_key,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne rate request.

    Uses the shipment endpoint with ReturnCharges=1 to get rates.
    """
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    services = lib.to_services(payload.services, service_type=provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get first service or use default
    service = lib.identity(
        next(iter(services), None)
        or provider_units.ShippingService.parcelone_pa1_eco
    )

    # Parse service for CEP and product IDs
    service_code = service.value if hasattr(service, 'value') else str(service)
    cep_id, product_id = provider_units.parse_service_code(service_code)
    cep_id = cep_id or settings.connection_config.cep_id.state
    product_id = product_id or settings.connection_config.product_id.state

    request = parcelone.ShippingDataRequestType(
        ShippingData=parcelone.ShipmentType(
            CEPID=cep_id,
            ProductID=product_id,
            MandatorID=settings.mandator_id,
            ConsignerID=settings.consigner_id,
            ShipToData=parcelone.ShipToType(
                Name1=recipient.company_name or recipient.person_name,
                ShipmentAddress=parcelone.AddressType(
                    Street=recipient.street,
                    PostalCode=recipient.postal_code,
                    City=recipient.city,
                    Country=recipient.country_code,
                    State=recipient.state_code,
                ),
                PrivateAddressIndicator=1 if recipient.residential else 0,
            ),
            ShipFromData=parcelone.ShipFromType(
                Name1=shipper.company_name or shipper.person_name,
                ShipmentAddress=parcelone.AddressType(
                    Street=shipper.street,
                    PostalCode=shipper.postal_code,
                    City=shipper.city,
                    Country=shipper.country_code,
                    State=shipper.state_code,
                ),
            ) if shipper else None,
            ReturnCharges=1,  # Request charges only
            PrintLabel=0,  # Don't generate label for rate request
            Software="Karrio",
            Packages=[
                parcelone.ShipmentPackageType(
                    PackageRef=str(index),
                    PackageWeight=parcelone.MeasurementType(
                        Value=str(pkg.weight.KG),
                        Unit="kg",
                    ),
                    PackageDimensions=(
                        parcelone.DimensionsType(
                            Length=str(pkg.length.CM),
                            Width=str(pkg.width.CM),
                            Height=str(pkg.height.CM),
                        )
                        if pkg.length.CM and pkg.width.CM and pkg.height.CM
                        else None
                    ),
                )
                for index, pkg in enumerate(packages, 1)
            ],
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(service_code=service.name if hasattr(service, 'name') else str(service)),
    )
