"""Karrio ParcelOne rating implementation."""

import typing
import karrio.schemas.parcelone.shipping_wcf as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse rate response from ParcelOne API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    charges_results: typing.List[parcelone.ChargesResult] = lib.find_element(
        "ChargesResult", response, parcelone.ChargesResult
    )

    rates = [
        _extract_rate(result, settings, _response.ctx)
        for result in charges_results
        if (result.ActionResult is not None and result.ActionResult.Success == 1)
        or result.TotalCharges is not None
    ]

    return [rate for rate in rates if rate is not None], messages


def _extract_rate(
    result: parcelone.ChargesResult,
    settings: provider_utils.Settings,
    ctx: typing.Dict[str, typing.Any] = {},
) -> models.RateDetails:
    """Extract rate details from ChargesResult element."""
    service_code = ctx.get("service_code", "parcelone_standard")
    service = provider_units.ShippingService.map(service_code)

    total_charge = (
        lib.to_money(result.TotalCharges.Value) if result.TotalCharges else 0.0
    )
    currency = result.TotalCharges.Currency if result.TotalCharges else "EUR"

    extra_charges = [
        models.ChargeDetails(
            name=charge.Description or "Shipping Charge",
            amount=lib.to_money(charge.Value),
            currency=charge.Currency or currency,
        )
        for charge in (result.ShipmentCharges.Amount if result.ShipmentCharges else [])
        if charge.Value
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        total_charge=total_charge,
        currency=currency or "EUR",
        extra_charges=extra_charges,
        meta=dict(
            service_name=service.name_or_key,
            remarks=result.Remarks,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne rate request."""
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    services = lib.to_services(
        payload.services,
        initializer=provider_units.shipping_services_initializer,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get first service or use default
    service = next(
        (svc for svc in services),
        provider_units.ShippingService.parcelone_dhl_paket,
    )

    # Parse service for CEP and product IDs
    service_code = service.value
    cep_id, product_id = provider_units.parse_service_code(service_code)
    cep_id = cep_id or settings.cep_id or "DHL"
    product_id = product_id or settings.product_id or "PAKET"

    request = parcelone.Charges(
        MandatorID=settings.mandator_id,
        ConsignerID=settings.consigner_id,
        CEPID=cep_id,
        ProductID=product_id,
        ShipToAddress=parcelone.Address(
            PostalCode=recipient.postal_code,
            City=recipient.city,
            Country=recipient.country_code,
            State=recipient.state_code,
        ),
        Packages=parcelone.ArrayOfShipmentPackage(
            ShipmentPackage=[
                parcelone.ShipmentPackage(
                    PackageWeight=parcelone.Measurement(
                        Value=str(pkg.weight.KG) if pkg.weight else "0",
                        Unit="KG",
                    ),
                    PackageDimensions=(
                        parcelone.Dimensions(
                            Length=str(pkg.length.CM) if pkg.length else None,
                            Width=str(pkg.width.CM) if pkg.width else None,
                            Height=str(pkg.height.CM) if pkg.height else None,
                            Measurement="CM",
                        )
                        if pkg.length and pkg.width and pkg.height
                        else None
                    ),
                )
                for pkg in packages
            ]
        ),
        PrivateAddressIndicator=1 if recipient.residential else 0,
    )

    return lib.Serializable(
        request,
        lambda req: _request_serializer(req, settings),
        dict(service_code=service.name),
    )


def _request_serializer(
    request: parcelone.Charges,
    settings: provider_utils.Settings,
) -> str:
    """Serialize rate request to SOAP envelope."""
    charges_xml = lib.to_xml(
        request,
        name_="wcf:Charges",
        namespacedef_='xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"',
    )

    body = f"""<tns:getCharges>
            <tns:ChargesData>
                {charges_xml}
            </tns:ChargesData>
        </tns:getCharges>"""

    return provider_utils.create_envelope(body, settings)
