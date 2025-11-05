"""Karrio GLS Group shipment creation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_group.error as error
import karrio.providers.gls_group.utils as provider_utils
import karrio.providers.gls_group.units as provider_units
import karrio.schemas.gls_group.shipment_request as gls_request
import karrio.schemas.gls_group.shipment_response as gls_response


def parse_shipment_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse GLS Group shipment response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment = (
        _extract_details(response, settings, _response.ctx)
        if not any(messages)
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from GLS Group response."""
    shipment = lib.to_object(gls_response.ShipmentType, data)

    # Get the first label data if available
    label_data = None
    if shipment.labels and len(shipment.labels) > 0:
        label_data = shipment.labels[0].labelData

    # Get the first tracking number
    tracking_number = (
        shipment.trackingNumbers[0]
        if shipment.trackingNumbers and len(shipment.trackingNumbers) > 0
        else shipment.shipmentId
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment.shipmentId,
        label_type="PDF",
        docs=models.Documents(label=label_data) if label_data else None,
        meta=dict(
            shipment_id=shipment.shipmentId,
            tracking_numbers=shipment.trackingNumbers or [],
            created_at=shipment.createdAt,
            shipping_date=shipment.shippingDate,
            status=shipment.status,
            parcels=[
                dict(
                    parcel_id=parcel.parcelId,
                    tracking_number=parcel.trackingNumber,
                    weight=parcel.weight,
                )
                for parcel in (shipment.parcels or [])
            ],
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for GLS Group API."""

    # Convert karrio models to GLS-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Get label format from options or use default
    label_format = payload.label_type or "PDF"

    # Build services array from options
    services = []
    for key, value in options.items():
        if value and key != "insurance":
            services.append({"type": key, "details": {}})

    # Build parcel references
    references = []
    if payload.reference:
        references.append({
            "type": "CUSTOMER_REFERENCE",
            "value": payload.reference,
        })

    # Create the shipment request
    request = gls_request.ShipmentRequestType(
        shipment=gls_request.ShipmentType(
            product=service.value_or_key if service else "PARCEL",
            sender=gls_request.ReceiverType(
                name1=shipper.company_name or shipper.person_name or "",
                name2=shipper.person_name if shipper.company_name else None,
                name3=None,
                street=shipper.address_line1 or "",
                houseNumber=shipper.address_line2 or "",
                zipCode=shipper.postal_code or "",
                city=shipper.city or "",
                country=shipper.country_code or "",
                contactPerson=shipper.person_name,
                phone=shipper.phone_number,
                email=shipper.email,
            ),
            receiver=gls_request.ReceiverType(
                name1=recipient.company_name or recipient.person_name or "",
                name2=recipient.person_name if recipient.company_name else None,
                name3=None,
                street=recipient.address_line1 or "",
                houseNumber=recipient.address_line2 or "",
                zipCode=recipient.postal_code or "",
                city=recipient.city or "",
                country=recipient.country_code or "",
                contactPerson=recipient.person_name,
                phone=recipient.phone_number,
                email=recipient.email,
            ),
            parcels=[
                gls_request.ParcelType(
                    weight=package.weight.KG,
                    length=int(package.length.CM) if package.length else None,
                    width=int(package.width.CM) if package.width else None,
                    height=int(package.height.CM) if package.height else None,
                    references=[
                        gls_request.ReferenceType(
                            type="CUSTOMER_REFERENCE",
                            value=getattr(package, 'parcel_id', None) or f"parcel_{idx+1}",
                        )
                    ] if getattr(package, 'parcel_id', None) else None,
                )
                for idx, package in enumerate(packages)
            ],
            services=[
                gls_request.ServiceType(type=svc["type"], details=gls_request.DetailsType())
                for svc in services
            ] if services else None,
            shippingDate=lib.fdate(getattr(payload, 'shipment_date', None)) if getattr(payload, 'shipment_date', None) else None,
            references=[
                gls_request.ReferenceType(type=ref["type"], value=ref["value"])
                for ref in references
            ] if references else None,
            labelFormat=label_format,
            printingOptions=gls_request.PrintingOptionsType(
                templateName=settings.connection_config.template_name.state or "STANDARD",
                printerLanguage=settings.connection_config.printer_language.state or label_format,
            ),
        )
    )

    return lib.Serializable(request, lib.to_dict)
