"""Karrio GLS Group shipment creation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls.error as error
import karrio.providers.gls.utils as provider_utils
import karrio.providers.gls.units as provider_units
import karrio.schemas.gls.shipment_request as gls_request
import karrio.schemas.gls.shipment_response as gls_response


def parse_shipment_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    """Parse GLS Group shipment response."""
    response = lib.failsafe(lambda: _response.deserialize()) or {}
    messages = error.parse_error_response(response, settings)

    shipment = (
        _extract_details(response, settings, _response.ctx)
        if not any(messages) and response.get("shipmentId")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from GLS Group response."""
    shipment = lib.to_object(gls_response.ShipmentResponseType, data)

    tracking_numbers = shipment.trackingNumbers or []

    # Get the first label data if available
    label_data = None
    if shipment.labels and len(shipment.labels) > 0:
        label_data = shipment.labels[0].labelData

    # Extract validated fields directly from schema
    shipment_identifier = shipment.shipmentId
    tracking_number = tracking_numbers[0]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_identifier,
        label_type="PDF",
        docs=models.Documents(label=label_data or ""),
        meta=dict(
            shipment_id=shipment_identifier,
            tracking_numbers=tracking_numbers,
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

    label_format = payload.label_type or "PDF"
    contact_id = settings.connection_config.contact_id.state

    # Build the shipment request matching vendor spec (PascalCase)
    request = gls_request.ShipmentRequestType(
        Shipment=gls_request.ShipmentType(
            Product=service.value_or_key if service else "PARCEL",
            Shipper=gls_request.ShipperType(
                ContactID=contact_id,
                Address=gls_request.AddressType(
                    Name1=shipper.company_name or shipper.person_name or "",
                    Name2=shipper.person_name if shipper.company_name else None,
                    Street=shipper.address_line1 or "",
                    StreetNumber=shipper.address_line2 or "",
                    ZIPCode=shipper.postal_code or "",
                    City=shipper.city or "",
                    CountryCode=shipper.country_code or "",
                    ContactPerson=shipper.person_name,
                    FixedLinePhonenumber=shipper.phone_number,
                ),
            ),
            Consignee=gls_request.ConsigneeType(
                Address=gls_request.AddressType(
                    Name1=recipient.company_name or recipient.person_name or "",
                    Name2=recipient.person_name if recipient.company_name else None,
                    Street=recipient.address_line1 or "",
                    StreetNumber=recipient.address_line2 or "",
                    ZIPCode=recipient.postal_code or "",
                    City=recipient.city or "",
                    CountryCode=recipient.country_code or "",
                    ContactPerson=recipient.person_name,
                    FixedLinePhonenumber=recipient.phone_number,
                ),
            ),
            ShipmentUnit=[
                gls_request.ShipmentUnitType(
                    Weight=package.weight.KG,
                    Volume=gls_request.VolumeType(
                        Width=str(package.width.CM) if package.width.value else None,
                        Height=str(package.height.CM) if package.height.value else None,
                        Length=str(package.length.CM) if package.length.value else None,
                    ) if any([package.width.value, package.height.value, package.length.value]) else None,
                    ShipmentUnitReference=(
                        [payload.reference] if payload.reference else None
                    ),
                )
                for package in packages
            ],
            ShipmentReference=(
                [payload.reference] if payload.reference else None
            ),
            ShippingDate=lib.fdate(
                options.shipment_date.state
            ) if options.shipment_date.state else None,
        ),
        PrintingOptions=gls_request.PrintingOptionsType(
            ReturnLabels=gls_request.ReturnLabelsType(
                TemplateSet=settings.connection_config.template_name.state or "NONE",
                LabelFormat=label_format,
            ),
        ),
    )

    return lib.Serializable(request, lib.to_dict)
