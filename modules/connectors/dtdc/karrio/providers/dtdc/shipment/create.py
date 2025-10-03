"""Karrio DTDC shipment creation implementation."""

import datetime
import karrio.schemas.dtdc.shipment_request as dtdc_req
import karrio.schemas.dtdc.shipment_response as dtdc_res
import karrio.schemas.dtdc.label_response as dtdc_label

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dtdc.error as error
import karrio.providers.dtdc.utils as provider_utils
import karrio.providers.dtdc.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[typing.Tuple[dict, dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    shipment_data, label_data = _response.deserialize()

    messages = error.parse_error_response(shipment_data, settings)
    shipment = lib.identity(
        _extract_details(
            (shipment_data["data"][0], label_data), settings, _response.ctx
        )
        if lib.failsafe(
            lambda: shipment_data["data"][0]["success"]
            and shipment_data["data"][0]["reference_number"]
        )
        else None
    )

    return shipment, messages


def _extract_details(
    data: typing.Tuple[dict, dict],
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from DTDC response data."""
    # fmt: on
    shipment_data, label_data = data
    service = provider_units.ShippingService.map(ctx.get("service"))

    shipment = lib.to_object(dtdc_res.DatumType, shipment_data)
    label = lib.to_object(dtdc_label.LabelResponseType, label_data)
    tracking_numbers = [piece.reference_number for piece in shipment.pieces or []]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.reference_number,
        shipment_identifier=shipment.reference_number,
        label_type="PDF",
        docs=models.Documents(label=label.label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(
                shipment.reference_number
            ),
            service_name=service.value_or_key,
            tracking_numbers=tracking_numbers,
            dtdc_courier_partner=shipment.courier_partner,
            dtdc_courier_account=shipment.courier_account,
            dtdc_chargeable_weight=shipment.chargeable_weight,
            dtdc_self_pickup_enabled=shipment.self_pickup_enabled,
            dtdc_customer_reference_number=shipment.customer_reference_number,
            dtdc_courier_partner_reference_number=shipment.courier_partner_reference_number,
        ),
    )
    # fmt: off


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for DTDC API."""

    # Parse address and package data
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address or payload.shipper)
    service = provider_units.ShippingService.map(payload.service)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages,
        option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(payload.customs)

    load_type = lib.identity(
        provider_units.PackagingType.map(
            packages.package_type or "your_packaging"
        ).value
    )
    label_type = lib.identity(
        settings.connection_config.label_type.state
        or provider_units.LabelType.map(payload.label_type or "PDF").value
        or "SHIP_LABEL_4X6"
    )

    invoice_date = lib.fdatetime(
        lib.to_date(
            options.dtdc_invoice_date.state
            or customs.invoice_date
            or options.shipping_date.state
            or datetime.datetime.now(),
            try_formats=["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"],
        ),
        output_format="%d %b %Y",
    )

    # Build request
    request = dtdc_req.ShipmentRequestType(
        consignments=[
            dtdc_req.ConsignmentType(
                customer_code=settings.customer_code,
                description=packages.description,
                service_type_id=service.value,
                load_type=load_type,
                dimension_unit="cm",
                length=str(packages[0].length.CM),
                width=str(packages[0].width.CM),
                height=str(packages[0].height.CM),
                weight_unit="kg",
                weight=str(packages[0].weight.KG),
                declared_value=str(
                    lib.to_money(options.declared_value.state) or 1
                ),
                num_pieces=len(packages),
                # Origin details
                origin_details=dtdc_req.NDetailsType(
                    name=shipper.person_name or shipper.company_name,
                    phone=shipper.phone_number,
                    alternate_phone=shipper.phone_number,
                    address_line_1=shipper.address_line1,
                    address_line_2=shipper.address_line2,
                    pincode=lib.to_int(shipper.postal_code),
                    city=shipper.city,
                    state=shipper.state_code,
                    email=shipper.email,
                    city_name=None,
                    state_name=None,
                ),
                # Destination details
                destination_details=dtdc_req.NDetailsType(
                    name=(recipient.person_name or recipient.company_name),
                    phone=recipient.phone_number,
                    address_line_1=recipient.address_line1,
                    address_line_2=recipient.address_line2,
                    pincode=lib.to_int(recipient.postal_code),
                    city=recipient.city,
                    state=recipient.state_code,
                    email=recipient.email,
                    alternate_phone=None,
                    city_name=None,
                    state_name=None,
                ),
                # Return details (use shipper as return address by default)
                return_details=dtdc_req.NDetailsType(
                    name=return_address.person_name or return_address.company_name,
                    address_line_1=return_address.address_line1,
                    address_line_2=return_address.address_line2,
                    city=return_address.city,
                    phone=return_address.phone_number,
                    pincode=lib.to_int(return_address.postal_code),
                    email=return_address.email,
                    alternate_phone=None,
                    state_name=None,
                    city_name=None,
                ),
                # Reference and options
                customer_reference_number=payload.reference,
                cod_collection_mode=options.dtdc_cod_collection_mode.state,
                cod_amount=options.dtdc_cod_amount.state,
                commodity_id=lib.to_int(options.dtdc_commodity_id.state),
                eway_bill=options.dtdc_eway_bill.state,
                is_risk_surcharge_applicable=options.dtdc_is_risk_surcharge_applicable.state,
                invoice_number=lib.identity(
                    options.dtdc_invoice_number.state or customs.invoice
                ),
                invoice_date=invoice_date,
                reference_number=None,
                pieces_detail=lib.identity(
                    [
                        dtdc_req.PiecesDetailType(
                            description=package.description,
                            declared_value=package.total_value,
                            weight=package.weight.KG,
                            height=package.height.CM,
                            length=package.length.CM,
                            width=package.width.CM,
                        )
                        for package in packages
                    ]
                    if len(packages) > 1
                    else []
                ),
            )
        ]
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            label_format="base64",
            label_type=label_type,
            service=service.name_or_key,
        ),
    )
