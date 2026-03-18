"""Karrio SmartKargo shipment API implementation."""

import karrio.schemas.smartkargo.rate_request as smartkargo_req
import karrio.schemas.smartkargo.shipment_response as smartkargo_res

import typing
import datetime
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils
import karrio.providers.smartkargo.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[dict, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    responses = _response.deserialize()
    label_type = _response.ctx.get("label_type", "PDF") if _response.ctx else "PDF"

    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response, _ in responses],
        start=[],
    )

    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{idx}",
                _extract_details(response, label, label_type, settings),
            )
            for idx, (response, label) in enumerate(responses, start=1)
            if _is_valid_booking(response)
        ]
    )

    return shipment, messages


def _is_valid_booking(response: dict) -> bool:
    """Check if a booking response contains a valid shipment."""
    shipments = response.get("shipments") or []
    return (
        response.get("status") == "Processed"
        and response.get("valid") == "Yes"
        and any(s.get("status") == "Booked" for s in shipments)
    )


def _extract_details(
    response: dict,
    label_data: dict,
    label_type: str,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from SmartKargo booking response envelope."""
    # Each response is a full booking envelope; extract the first (only) shipment
    data = (response.get("shipments") or [{}])[0]
    shipment = lib.to_object(smartkargo_res.ShipmentType, data)

    # Build tracking number from prefix + airWaybill
    tracking_number = f"{shipment.prefix}{shipment.airWaybill}"

    # Extract label from label response
    label_content = label_data.get("base64Content", "")
    # Remove data URI prefix if present (e.g., "data:application/pdf;base64,")
    if label_content and ";base64," in label_content:
        label_content = label_content.split(";base64,")[1].strip()

    # Map service type to service name
    service = provider_units.ShippingService.map(shipment.serviceType)

    # Build charges breakdown
    charges = [
        ("Shipping Fee", shipment.shippingFee),
        ("Insurance", shipment.insurance),
        ("Tax", shipment.totalTax),
    ]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment.packageReference,
        label_type=label_type,
        docs=models.Documents(label=label_content),
        selected_rate=lib.identity(
            models.RateDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                service=service.name_or_key,
                total_charge=lib.to_money(shipment.total or 0),
                currency=shipment.currency or settings.connection_config.currency.state or "USD",
                extra_charges=[
                    models.ChargeDetails(
                        name=name,
                        amount=lib.to_money(amount),
                        currency=shipment.currency or settings.connection_config.currency.state or "USD",
                    )
                    for name, amount in charges
                    if amount is not None and amount > 0
                ],
            )
            if shipment.total is not None
            else None
        ),
        meta=lib.to_dict(
            dict(
                service_name=service.name_or_key,
                last_mile_tracking_number=shipment.barCode,
                estimated_delivery=shipment.estimatedDeliveryDate,
                carrier_tracking_link=settings.tracking_url.format(tracking_number),
                smartkargo_service_type=shipment.serviceType,
                smartkargo_prefix=shipment.prefix,
                smartkargo_air_waybill=shipment.airWaybill,
                smartkargo_header_reference=shipment.headerReference,
                smartkargo_package_reference=shipment.packageReference,
                smartkargo_origin=shipment.origin,
                smartkargo_destination=shipment.destination,
                smartkargo_label_url=shipment.labelUrl,
            )
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for SmartKargo booking API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Determine weight and dimension units based on package collection
    # SmartKargo uses KG/LBR for weight and CMQ/CFT for volume
    # Typically KG correlates with CM dimensions, LB with IN
    is_metric = packages.weight_unit == "KG"
    weight_unit = (
        provider_units.WeightUnit.KG
        if is_metric
        else provider_units.WeightUnit.LBR
    )
    dimension_unit = (
        provider_units.DimensionUnit.CMQ
        if is_metric
        else provider_units.DimensionUnit.CFT
    )
    customs = lib.to_customs_info(payload.customs)

    # Get label type from payload or connection config
    label_type = lib.identity(
        payload.label_type or settings.connection_config.label_type.state or "PDF"
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
    shipment_date = lib.identity(
        options.shipment_date.state
        or lib.to_next_business_datetime(datetime.datetime.now())
    )

    # Build one request per package (SmartKargo API only accepts one package per booking)
    request = [
        smartkargo_req.RateRequestType(
            reference=reference,
            issueDate=lib.fdatetime(
                shipment_date,
                current_format="%Y-%m-%d",
                output_format="%Y-%m-%d %H:%M",
            ),
            packages=[
                smartkargo_req.PackageType(
                    reference=lib.text(package.parcel.reference_number or f"PKG-{index}", max=36),
                    commodityType=options.smartkargo_commodity_type.state or "9999",
                    serviceType=service,
                    paymentMode=provider_units.PaymentMode.PX.value,
                    origin=origin,
                    destination=destination,
                    packageDescription=lib.text(
                        package.parcel.description or packages.description, max=100
                    ),
                    totalPackages=1,
                    totalPieces=1,
                    grossVolumeUnityMeasure=dimension_unit.value,
                    totalGrossWeight=package.weight.value,
                    grossWeightUnityMeasure=weight_unit.value,
                    hasInsurance=options.smartkargo_declared_value.state is not None,
                    insuranceAmmount=lib.to_money(
                        options.smartkargo_declared_value.state or 0
                    ),
                    specialHandlingType=options.smartkargo_special_handling.state,
                    deliveryType=options.smartkargo_delivery_type.state or "DoorToDoor",
                    channel=lib.text(options.smartkargo_channel.state or "Direct", max=15),
                    labelRef2=lib.text(options.smartkargo_label_ref2.state, max=20),
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

    return lib.Serializable(request, lib.to_dict, ctx=dict(label_type=label_type))
