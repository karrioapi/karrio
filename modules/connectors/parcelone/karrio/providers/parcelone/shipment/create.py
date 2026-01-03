"""Karrio ParcelOne shipment creation implementation."""

import typing
import karrio.schemas.parcelone.shipping_wcf as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.providers.parcelone.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse shipment creation response from ParcelOne API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment_results: typing.List[parcelone.ShipmentResult] = lib.find_element(
        "ShipmentResult", response, parcelone.ShipmentResult
    )

    shipment = _extract_details(shipment_results[0], settings) if shipment_results else None

    return shipment, messages


def _extract_details(
    result: parcelone.ShipmentResult,
    settings: provider_utils.Settings,
) -> typing.Optional[models.ShipmentDetails]:
    """Extract shipment details from ShipmentResult."""
    action = result.ActionResult
    if action is None or action.Success != 1:
        return None

    packages = lib.failsafe(lambda: result.PackageResults.ShipmentPackageResult) or []
    tracking_ids = [p.TrackingID for p in packages if p.TrackingID]

    # Bundle all labels for multi-piece shipments
    labels = [p.Label for p in packages if p.Label]
    label = lib.bundle_base64(labels, "PDF") if len(labels) > 1 else next(iter(labels), None)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=action.TrackingID or next(iter(tracking_ids), None),
        shipment_identifier=action.ShipmentID or action.TrackingID,
        label_type="PDF",
        docs=models.Documents(label=label),
        meta=dict(
            shipment_id=action.ShipmentID,
            tracking_numbers=tracking_ids,
            label_url=result.LabelURL,
            total_charge=lib.failsafe(lambda: lib.to_money(result.TotalCharges.Value)),
            currency=lib.failsafe(lambda: result.TotalCharges.Currency) or "EUR",
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne shipment request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, required=["weight"])
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = payload.customs
    is_international = shipper.country_code != recipient.country_code

    # Parse service to get CEP and product
    service = provider_units.ShippingService.map(payload.service)
    service_code = service.value_or_key
    cep_id, product_id = provider_units.parse_service_code(service_code)
    cep_id = cep_id or settings.cep_id or "DHL"
    product_id = product_id or settings.product_id or "PAKET"

    # Build services list from options
    services = []
    if options.cash_on_delivery.state:
        services.append(
            parcelone.ShipmentService(
                ServiceID="COD",
                Value=parcelone.Amount(
                    Value=str(options.cash_on_delivery.state),
                    Currency=options.parcelone_cod_currency.state or "EUR",
                ),
            )
        )
    if options.insurance.state:
        services.append(
            parcelone.ShipmentService(
                ServiceID="INS",
                Value=parcelone.Amount(
                    Value=str(options.insurance.state),
                    Currency=options.parcelone_insurance_currency.state or "EUR",
                ),
            )
        )
    if options.signature_required.state:
        services.append(parcelone.ShipmentService(ServiceID="SIG"))
    if options.saturday_delivery.state:
        services.append(parcelone.ShipmentService(ServiceID="SAT"))
    # Only add email notification if explicitly requested with an email address
    email_notification_value = options.parcelone_notification_email.state
    if email_notification_value and isinstance(email_notification_value, str):
        services.append(
            parcelone.ShipmentService(
                ServiceID="MAIL",
                Parameters=email_notification_value,
            )
        )

    request = parcelone.Shipment(
        MandatorID=settings.mandator_id,
        ConsignerID=settings.consigner_id,
        CEPID=cep_id,
        ProductID=product_id,
        Software="Karrio",
        ShipToData=parcelone.ShipTo(
            Name1=recipient.company_name or recipient.person_name,
            Name2=recipient.person_name if recipient.company_name else None,
            ShipmentAddress=parcelone.Address(
                Street=recipient.street,
                Streetno=recipient.street_number,
                PostalCode=recipient.postal_code,
                City=recipient.city,
                Country=recipient.country_code,
                State=recipient.state_code,
            ),
            ShipmentContact=parcelone.Contact(
                Email=recipient.email,
                Phone=recipient.phone_number,
                Company=recipient.company_name,
            ),
            PrivateAddressIndicator=1 if recipient.residential else 0,
        ),
        ShipFromData=parcelone.ShipFrom(
            Name1=shipper.company_name or shipper.person_name,
            Name2=shipper.person_name if shipper.company_name else None,
            ShipmentAddress=parcelone.Address(
                Street=shipper.street,
                Streetno=shipper.street_number,
                PostalCode=shipper.postal_code,
                City=shipper.city,
                Country=shipper.country_code,
                State=shipper.state_code,
            ),
            ShipmentContact=parcelone.Contact(
                Email=shipper.email,
                Phone=shipper.phone_number,
                Company=shipper.company_name,
            ),
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
                    PackageRef=pkg.parcel.id or str(index),
                    IntDocData=(
                        parcelone.IntDoc(
                            Currency=(
                                customs.duty.currency or "EUR"
                                if customs.duty
                                else "EUR"
                            ),
                            TotalValue=(
                                str(customs.duty.declared_value or 0)
                                if customs.duty
                                else None
                            ),
                            ItemCategory=1,
                            InvoiceNo=customs.invoice,
                            ContentsDesc=(
                                parcelone.ArrayOfIntDocContents(
                                    IntDocContents=[
                                        parcelone.IntDocContents(
                                            Contents=item.description or item.title,
                                            Quantity=item.quantity,
                                            ItemValue=str(item.value_amount),
                                            NetWeight=str(item.weight),
                                            Origin=item.origin_country,
                                            TariffNumber=item.hs_code,
                                        )
                                        for item in (customs.commodities or [])
                                    ]
                                )
                                if customs.commodities
                                else None
                            ),
                        )
                        if is_international and customs
                        else None
                    ),
                )
                for index, pkg in enumerate(packages, 1)
            ]
        ),
        LabelFormat=parcelone.Format(
            Type="PDF",
            Size="100x150",
        ),
        PrintLabel=1,
        ShipmentRef=payload.reference,
        ReturnShipmentIndicator=1 if options.is_return.state else None,
        Services=(
            parcelone.ArrayOfShipmentService(ShipmentService=services)
            if services
            else None
        ),
    )

    return lib.Serializable(
        request,
        lambda req: _request_serializer(req, settings),
    )


def _request_serializer(
    request: parcelone.Shipment,
    settings: provider_utils.Settings,
) -> str:
    """Serialize shipment request to SOAP envelope."""
    shipment_xml = lib.to_xml(
        request,
        name_="wcf:Shipment",
        namespacedef_='xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"',
    )

    body = f"""<tns:registerShipments>
            <tns:ShippingData>
                {shipment_xml}
            </tns:ShippingData>
        </tns:registerShipments>"""

    return provider_utils.create_envelope(body, settings)
