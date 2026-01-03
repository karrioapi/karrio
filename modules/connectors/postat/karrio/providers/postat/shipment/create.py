"""Karrio PostAT shipment API implementation."""

import karrio.schemas.postat.plc_types as postat

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.postat.error as error
import karrio.providers.postat.utils as provider_utils
import karrio.providers.postat.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    result = lib.find_element("ImportShipmentResult", response, first=True)
    shipment = (
        _extract_details(response, settings)
        if result is not None and not any(messages)
        else None
    )

    return shipment, messages


def _extract_details(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from ImportShipmentResponse."""
    result = lib.find_element("ImportShipmentResult", response, first=True)
    pdf_data = lib.find_element("pdfData", response, first=True)
    zpl_data = lib.find_element("zplLabelData", response, first=True)

    code_elements = lib.find_element("Code", result) or []
    tracking_numbers = [code.text for code in code_elements if code.text]
    tracking_number = tracking_numbers[0]

    label = lib.failsafe(lambda: zpl_data.text) or lib.failsafe(lambda: pdf_data.text)
    label_type = "ZPL" if zpl_data is not None and zpl_data.text else "PDF"

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            tracking_numbers=tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the PostAT SOAP API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Label configuration with fallbacks
    label_format = lib.identity(
        settings.connection_config.label_format.state or payload.label_type
    )
    label_size = lib.identity(
        settings.connection_config.label_size.state
        or options.postat_label_size.state
        or "SIZE_100x150"
    )
    paper_layout = lib.identity(
        settings.connection_config.paper_layout.state
        or options.postat_paper_layout.state
        or "LAYOUT_2xA5inA4"
    )

    # Build request using generated schema types
    request = lib.Envelope(
        Body=lib.Body(
            postat.ImportShipmentType(
                row=[
                    postat.ImportShipmentRowType(
                        ClientID=settings.client_id,
                        OrgUnitID=settings.org_unit_id,
                        OrgUnitGuid=settings.org_unit_guid,
                        DeliveryServiceThirdPartyID=service,
                        CustomDataBit1=False,
                        OUShipperReference1=payload.reference,
                        ColloList=postat.ColloListType(
                            ColloRow=[
                                postat.ColloRowType(
                                    Weight=package.weight.KG,
                                    Length=package.length.CM,
                                    Width=package.width.CM,
                                    Height=package.height.CM,
                                )
                                for package in packages
                            ]
                        ),
                        OURecipientAddress=postat.AddressType(
                            Name1=recipient.company_name or recipient.person_name,
                            Name2=(
                                recipient.person_name
                                if recipient.company_name
                                else None
                            ),
                            AddressLine1=recipient.street,
                            AddressLine2=recipient.address_line2,
                            HouseNumber=recipient.street_number,
                            PostalCode=recipient.postal_code,
                            City=recipient.city,
                            CountryID=recipient.country_code,
                            Email=recipient.email,
                            Tel1=recipient.phone_number,
                        ),
                        OUShipperAddress=postat.AddressType(
                            Name1=shipper.company_name or shipper.person_name,
                            Name2=shipper.person_name if shipper.company_name else None,
                            AddressLine1=shipper.street,
                            AddressLine2=shipper.address_line2,
                            PostalCode=shipper.postal_code,
                            City=shipper.city,
                            CountryID=shipper.country_code,
                        ),
                        PrinterObject=postat.PrinterObjectType(
                            LabelFormatID=label_size,
                            LanguageID=label_format,
                            PaperLayoutID=paper_layout,
                        ),
                    )
                ]
            )
        )
    )

    return lib.Serializable(request, lib.envelope_serializer)
