"""Karrio Teleship shipment API implementation."""

import karrio.schemas.teleship.shipment_request as teleship_req
import karrio.schemas.teleship.shipment_response as teleship_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract shipment details if present (work with raw dict)
    shipment = lib.identity(
        _extract_details(response, settings)
        if response.get("shipment")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response data"""
    # Convert to typed object for safe attribute access
    shipment_data = data.get("shipment") or {}
    shipment = lib.to_object(teleship_res.ShipmentType, shipment_data)

    # Extract charges using functional pattern (work with raw dicts)
    charges = [
        lib.to_object(teleship_res.ChargeType, charge)
        for charge in (shipment_data.get("charges") or [])
    ]

    # Calculate selected rate if charges are present
    selected_rate = lib.identity(
        models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=shipment.serviceCode or "",
            total_charge=lib.to_money(shipment.totalCharge.amount if shipment.totalCharge else 0),
            currency=shipment.totalCharge.currency if shipment.totalCharge else "USD",
            extra_charges=[
                models.ChargeDetails(
                    name=charge.name or "",
                    amount=lib.to_money(charge.amount),
                    currency=charge.currency or (shipment.totalCharge.currency if shipment.totalCharge else "USD"),
                )
                for charge in charges
            ] if any(charges) else [],
            meta=dict(
                service_name=shipment.serviceName or "",
            ),
        )
        if shipment.totalCharge and shipment.totalCharge.amount
        else None
    )

    # Extract label document from documents array
    label_doc = lib.identity(
        next(
            (doc for doc in (shipment.documents or []) if doc.type == "LABEL"),
            None
        )
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber or "",
        shipment_identifier=shipment.shipmentId or "",
        label_type=label_doc.format if label_doc else "PDF",
        docs=models.Documents(label=label_doc.base64String if label_doc else ""),
        selected_rate=selected_rate,
        meta=dict(
            service_code=shipment.serviceCode,
            service_name=shipment.serviceName,
            customer_reference=shipment.customerReference,
            ship_date=shipment.shipDate,
            estimated_delivery=shipment.estimatedDelivery,
            package_type=shipment.packageType,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API"""
    # Convert karrio models using functional lib utilities
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.KG.name,
    )

    # Use functional pattern to select first package
    package = packages[0] if any(packages) else None

    # Build request using typed schema classes
    request = teleship_req.ShipmentRequestType(
        serviceCode=options.teleship_service_code.state or service,
        customerReference=payload.reference or options.teleship_customer_reference.state,
        packageType=lib.identity(
            provider_units.PackagingType.map(
                package.packaging_type or "your_packaging"
            ).value if package else "parcel"
        ),
        shipTo=teleship_req.ShipToType(
            name=recipient.person_name or recipient.company_name,
            email=recipient.email,
            phone=recipient.phone_number,
            address=teleship_req.AddressType(
                line1=recipient.address_line1,
                city=recipient.city,
                state=recipient.state_code,
                postcode=recipient.postal_code,
                country=recipient.country_code,
            ),
        ),
        shipFrom=teleship_req.ShipFromType(
            name=shipper.person_name or shipper.company_name,
            company=shipper.company_name,
            address=teleship_req.AddressType(
                line1=shipper.address_line1,
                city=shipper.city,
                state=shipper.state_code,
                postcode=shipper.postal_code,
                country=shipper.country_code,
            ),
        ),
        weight=lib.identity(
            teleship_req.WeightType(
                value=package.weight.value,
                unit=package.weight.unit.lower(),
            ) if package else None
        ),
        dimensions=lib.identity(
            teleship_req.DimensionsType(
                unit=package.dimension_unit.lower(),
                length=package.length.value,
                width=package.width.value,
                height=package.height.value,
            ) if package and all([package.length.value, package.width.value, package.height.value]) else None
        ),
        commodities=[
            teleship_req.CommodityType(
                sku=commodity.sku,
                title=commodity.title or commodity.description,
                value=teleship_req.ValueType(
                    amount=int(commodity.value_amount or 0),
                    currency=commodity.value_currency or "USD",
                ),
                quantity=commodity.quantity,
                unitWeight=teleship_req.WeightType(
                    value=commodity.weight,
                    unit=(commodity.weight_unit).lower(),
                ),
                description=commodity.description,
                countryOfOrigin=commodity.origin_country,
            )
            for commodity in (customs.commodities or [])
        ] if payload.customs and any(customs.commodities or []) else [],
        customs=lib.identity(
            teleship_req.CustomsType(
                EORI=lib.failsafe(lambda: customs.options.eori_number.state),
                contentType=provider_units.CustomsContentType.map(customs.content_type or "other").value,
                invoiceDate=customs.invoice_date,
                invoiceNumber=customs.invoice,
            ) if payload.customs else None
        ),
        metadata=lib.identity(
            teleship_req.MetadataType(
                fulfillmentOrderId=options.teleship_order_tracking_reference.state,
            ) if options.teleship_order_tracking_reference.state else None
        ),
    )

    return lib.Serializable(request, lib.to_dict)
