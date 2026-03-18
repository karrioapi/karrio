"""Karrio SmartKargo rate API implementation."""

import karrio.schemas.smartkargo.rate_request as smartkargo_req
import karrio.schemas.smartkargo.rate_response as smartkargo_res

import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils
import karrio.providers.smartkargo.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = [
        (
            f"{idx}",
            [
                _extract_details(detail, settings)
                for detail in (response.get("details") or [])
            ],
        )
        for idx, response in enumerate(responses, start=1)
        if response.get("status", "").upper() == "QUOTED"
    ]

    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from SmartKargo quotation response."""
    detail = lib.to_object(smartkargo_res.DetailType, data)

    # Map service type to ShippingService enum
    service = provider_units.ShippingService.map(detail.serviceType)
    transit_days = detail.slaInDays

    # Build charges list with raw values (easyship pattern)
    charges = [
        ("Base Rate", detail.total),
        ("Tax", detail.totalTax),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(detail.total or 0)
        + lib.to_money(detail.totalTax or 0),
        currency=settings.connection_config.currency.state or "USD",
        transit_days=transit_days,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency=settings.connection_config.currency.state or "USD",
            )
            for name, amount in charges
            if amount is not None and amount > 0
        ],
        meta=dict(
            service_name=service.name_or_key,
            service_type=detail.serviceType,
            estimated_delivery=detail.deliveryDateBasedOnShipment,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for SmartKargo quotation API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    customs = lib.to_customs_info(payload.customs) if payload.customs else None
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Determine weight and dimension units
    # SmartKargo uses KG/LBR for weight and CMQ/CFT for volume
    # Typically KG correlates with CM dimensions, LB with IN
    is_metric = packages.weight_unit == "KG"
    weight_unit = (
        provider_units.WeightUnit.KG.value
        if is_metric
        else provider_units.WeightUnit.LBR.value
    )
    dimension_unit = (
        provider_units.DimensionUnit.CMQ.value
        if is_metric
        else provider_units.DimensionUnit.CFT.value
    )

    # Resolve common request fields
    primary_id = settings.connection_config.primary_id.state or settings.account_number
    additional_id = settings.connection_config.additional_id.state or primary_id
    origin = settings.connection_config.origin.state or ""
    destination = settings.connection_config.destination.state or ""
    reference = lib.text(
        payload.reference or settings.tracer.get_context("request_id"),
        trim=True,
        max=35,
    )
    shipment_date = lib.fdatetime(
        options.shipment_date.state
        or lib.to_next_business_datetime(datetime.datetime.now()),
        current_format="%Y-%m-%d",
        output_format="%Y-%m-%d %H:%M",
    )

    # Build one request per package (SmartKargo API only accepts one package per request)
    request = [
        smartkargo_req.RateRequestType(
            reference=reference,
            issueDate=shipment_date,
            packages=[
                smartkargo_req.PackageType(
                    reference=lib.text(package.parcel.reference_number or f"PKG-{index}", max=36),
                    commodityType=options.smartkargo_commodity_type.state or "9999",
                    serviceType=getattr(service, "value", None),
                    paymentMode=provider_units.PaymentMode.PX.value,
                    origin=origin,
                    destination=destination,
                    packageDescription=lib.text(package.parcel.description or "General Shipment", max=100),
                    totalPackages=1,
                    totalPieces=1,
                    grossVolumeUnityMeasure=dimension_unit,
                    totalGrossWeight=package.weight.value,
                    grossWeightUnityMeasure=weight_unit,
                    hasInsurance=options.smartkargo_declared_value.state is not None,
                    insuranceAmmount=lib.to_money(
                        options.smartkargo_declared_value.state or 0
                    ),
                    specialHandlingType=options.smartkargo_special_handling.state,
                    dimensions=[
                        smartkargo_req.DimensionType(
                            pieces=1,
                            height=package.height.value,
                            width=package.width.value,
                            length=package.length.value,
                            grossWeight=package.weight.value,
                        )
                    ],
                    participants=[
                        smartkargo_req.ParticipantType(
                            type="Shipper",
                            primaryId=lib.text(primary_id, max=36),
                            additionalId=lib.text(additional_id, max=36),
                            account=lib.text(settings.account_number, max=120),
                            name=lib.text(shipper.company_name or shipper.person_name, max=120),
                            postCode=lib.text(shipper.postal_code, max=15),
                            street=lib.text(shipper.street, max=250),
                            street2=lib.text(shipper.address_line2, max=250),
                            city=lib.text(shipper.city, max=60),
                            state=lib.text(shipper.state_code, max=60),
                            countryId=shipper.country_code,
                            phoneNumber=lib.text(shipper.phone_number, max=25),
                            email=lib.text(shipper.email, max=120),
                            taxId=lib.text(shipper.tax_id, max=50),
                        ),
                        smartkargo_req.ParticipantType(
                            type="Consignee",
                            primaryId=None,
                            additionalId=None,
                            account=None,
                            name=lib.text(recipient.company_name or recipient.person_name, max=120),
                            postCode=lib.text(recipient.postal_code, max=15),
                            street=lib.text(recipient.street, max=250),
                            street2=lib.text(recipient.address_line2, max=250),
                            city=lib.text(recipient.city, max=60),
                            state=lib.text(recipient.state_code, max=60),
                            countryId=recipient.country_code,
                            phoneNumber=lib.text(recipient.phone_number, max=25),
                            email=lib.text(recipient.email, max=120),
                            taxId=lib.text(recipient.tax_id, max=50),
                        ),
                    ],
                    customItems=(
                        [
                            smartkargo_req.CustomItemType(
                                exportHsCode=item.hs_code or lib.identity(item.metadata or {}).get("export_hs_code") or "N/A",
                                importHsCode=lib.identity(item.metadata or {}).get("import_hs_code") or item.hs_code or "N/A",
                                description=lib.text(item.description or item.title, max=500),
                                quantity=item.quantity,
                                quantityUnit=item.weight_unit or "kg",
                                weight=item.weight,
                                commercialValue=item.value_amount,
                                commercialValueCurrency=item.value_currency,
                                manufactureCountryCode=item.origin_country,
                                sku=lib.text(item.sku, max=25),
                            )
                            for item in customs.commodities
                        ]
                        if customs is not None and any(customs.commodities)
                        else []
                    ),
                    commercialInvoice=(
                        smartkargo_req.CommercialInvoiceType(
                            termsOfSale=customs.incoterm or "DDU",
                        )
                        if customs is not None and any(customs.commodities)
                        else None
                    ),
                )
            ],
        )
        for index, package in enumerate(packages, start=1)
    ]

    return lib.Serializable(request, lib.to_dict)
