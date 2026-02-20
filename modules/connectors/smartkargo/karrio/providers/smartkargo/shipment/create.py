"""Karrio SmartKargo shipment API implementation."""

import karrio.schemas.smartkargo.rate_request as smartkargo_req
import karrio.schemas.smartkargo.shipment_response as smartkargo_res

import typing
import uuid
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
        label_content = label_content.split(";base64,")[1]

    # Map service type to service name
    service = provider_units.ShippingService.map(shipment.serviceType)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment.packageReference,
        label_type=label_type,
        docs=models.Documents(label=label_content),
        meta=dict(
            service_name=service.name_or_key,
            service_type=shipment.serviceType,
            prefix=shipment.prefix,
            air_waybill=shipment.airWaybill,
            header_reference=shipment.headerReference,
            package_reference=shipment.packageReference,
            estimated_delivery=shipment.estimatedDeliveryDate,
            origin=shipment.origin,
            label_url=shipment.labelUrl,
            total_charge=shipment.total,
            currency=shipment.currency,
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
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
        provider_units.WeightUnit.KG.value
        if is_metric
        else provider_units.WeightUnit.LBR.value
    )
    dimension_unit = (
        provider_units.DimensionUnit.CMQ.value
        if is_metric
        else provider_units.DimensionUnit.CFT.value
    )

    # Get label type from payload or connection config
    label_type = (
        payload.label_type
        or settings.connection_config.label_type.state
        or "PDF"
    )

    # Get shipment date from options or use current date (issueDate is required by API)
    shipment_date = options.shipment_date.state or datetime.datetime.now()

    # Build one request per package (SmartKargo API only accepts one package per booking)
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
                    serviceType=service,
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

    return lib.Serializable(request, lib.to_dict, ctx=dict(label_type=label_type))
