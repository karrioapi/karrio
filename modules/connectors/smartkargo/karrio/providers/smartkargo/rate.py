"""Karrio SmartKargo rate API implementation."""

import karrio.schemas.smartkargo.rate_request as smartkargo_req
import karrio.schemas.smartkargo.rate_response as smartkargo_res

import typing
import datetime
import uuid
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
        total_charge=lib.to_money(detail.total or 0) + lib.to_money(detail.totalTax or 0),
        currency="USD",
        transit_days=transit_days,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency="USD",
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

    # Get service type - API requires serviceType (errors if empty)
    # Default to EST (Standard) when none specified, like UPS defaults to ups_standard
    service_type = (
        service.value
        if service
        else provider_units.ShippingService.smartkargo_standard.value
    )

    # Get shipment date from options or use current date (issueDate is required by API)
    shipment_date = options.shipment_date.state or datetime.datetime.now()

    # Build one request per package (SmartKargo API only accepts one package per request)
    request = [
        smartkargo_req.RateRequestType(
            reference=payload.reference or str(uuid.uuid4().hex),
            issueDate=lib.fdatetime(
                shipment_date,
                current_format="%Y-%m-%d",
                output_format="%Y-%m-%d %H:%M",
            ),
            packages=[
                smartkargo_req.PackageType(
                    reference=package.parcel.reference_number or f"PKG-{index}",
                    commodityType=options.smartkargo_commodity_type.state or "9999",
                    serviceType=service_type,
                    paymentMode=provider_units.PaymentMode.PX.value,
                    packageDescription=package.parcel.description or "General Shipment",
                    totalPackages=1,
                    totalPieces=1,
                    grossVolumeUnitMeasure=dimension_unit,
                    totalGrossWeight=package.weight.value,
                    grossWeightUnitMeasure=weight_unit,
                    insuranceRequired=options.insurance.state is not None,
                    declaredValue=lib.to_money(options.declared_value.state or options.insurance.state or 0),
                    specialHandlingType=options.smartkargo_special_handling.state,
                    deliveryType=options.smartkargo_delivery_type.state or "DoorToDoor",
                    channel=options.smartkargo_channel.state or "Direct",
                    labelRef2=options.smartkargo_label_ref2.state,
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
                            primaryId=settings.account_id,
                            additionalId=None,
                            account=settings.account_number,
                            name=shipper.company_name or shipper.person_name,
                            postCode=shipper.postal_code,
                            street=shipper.street,
                            street2=shipper.address_line2,
                            city=shipper.city,
                            state=shipper.state_code,
                            countryId=shipper.country_code,
                            phoneNumber=shipper.phone_number,
                            email=shipper.email,
                        ),
                        smartkargo_req.ParticipantType(
                            type="Consignee",
                            primaryId=None,
                            additionalId=None,
                            account=None,
                            name=recipient.company_name or recipient.person_name,
                            postCode=recipient.postal_code,
                            street=recipient.street,
                            street2=recipient.address_line2,
                            city=recipient.city,
                            state=recipient.state_code,
                            countryId=recipient.country_code,
                            phoneNumber=recipient.phone_number,
                            email=recipient.email,
                        ),
                    ],
                )
            ],
        )
        for index, package in enumerate(packages, start=1)
    ]

    return lib.Serializable(request, lib.to_dict)
