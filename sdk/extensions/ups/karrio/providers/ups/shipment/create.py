import ups_lib.ship_web_service_schema as ups
import ups_lib.common as common
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    details = lib.find_element("ShipmentResults", response, first=True)
    shipment = _extract_shipment(details, settings) if details is not None else None

    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    node: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(ups.ShipmentResultsType, node)
    label = _process_label(shipment)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.ShipmentIdentificationNumber,
        shipment_identifier=shipment.ShipmentIdentificationNumber,
        docs=models.Documents(label=label),
    )


def _process_label(shipment: ups.ShipmentResultsType):
    label_type = (
        "ZPL"
        if "ZPL" in shipment.PackageResults[0].ShippingLabel.ImageFormat.Code
        else "PDF"
    )
    labels = [
        (
            lib.image_to_pdf(pkg.ShippingLabel.GraphicImage, rotate=-90)
            if label_type == "PDF"
            else pkg.ShippingLabel.GraphicImage
        )
        for pkg in shipment.PackageResults
    ]


    return (
        labels[0]
        if len(labels) == 1
        else lib.bundle_base64(labels, label_type)
    )



def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[ups.ShipmentRequest]:
    packages = lib.to_packages(payload.parcels, provider_units.PackagePresets)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    biling_address = lib.to_address(payload.billing_address or payload.shipper)

    if any(key in service for key in ["freight", "ground"]):
        packages.validate(required=["weight"])

    country_pair = f"{payload.shipper.country_code}/{payload.recipient.country_code}"
    charges: typing.Dict[str, models.Payment] = {
        "01": payload.payment,
        "02": payload.customs.duty if payload.customs is not None else None,
    }
    mps_packaging = (
        provider_units.PackagingType.your_packaging.value if len(packages) > 1 else None
    )
    label_format, label_height, label_width = (
        provider_units.LabelType.map(payload.label_type).value
        or provider_units.LabelType.PDF_6x4.value
    )

    request = ups.ShipmentRequest(
        Request=common.RequestType(
            RequestOption=["validate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.reference,
                TransactionIdentifier=getattr(payload, "id", None),
            ),
        ),
        Shipment=ups.ShipmentType(
            Description=packages.description,
            DocumentsOnlyIndicator=("" if packages.is_document else None),
            Shipper=ups.ShipperType(
                Name=(payload.shipper.company_name or payload.shipper.person_name),
                AttentionName=payload.shipper.person_name,
                CompanyDisplayableName=payload.shipper.company_name,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                Phone=ups.ShipPhoneType(Number=payload.shipper.phone_number or "000-000-0000"),
                ShipperNumber=settings.account_number,
                FaxNumber=None,
                EMailAddress=payload.shipper.email,
                Address=ups.ShipAddressType(
                    AddressLine=lib.join(
                        payload.shipper.address_line1, payload.shipper.address_line2
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipFrom=ups.ShipperType(
                Name=(payload.shipper.company_name or payload.shipper.person_name),
                AttentionName=payload.shipper.person_name,
                CompanyDisplayableName=payload.shipper.company_name,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                Phone=ups.ShipPhoneType(Number=payload.shipper.phone_number or "000-000-0000"),
                ShipperNumber=settings.account_number,
                FaxNumber=None,
                EMailAddress=payload.shipper.email,
                Address=ups.ShipAddressType(
                    AddressLine=lib.join(
                        payload.shipper.address_line1, payload.shipper.address_line2
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ups.ShipToType(
                Name=(payload.recipient.company_name or payload.recipient.person_name),
                AttentionName=payload.recipient.person_name,
                CompanyDisplayableName=payload.recipient.company_name,
                TaxIdentificationNumber=payload.recipient.federal_tax_id,
                TaxIDType=payload.recipient.federal_tax_id,
                Phone=ups.ShipPhoneType(Number=payload.recipient.phone_number or "000-000-0000"),
                FaxNumber=None,
                EMailAddress=payload.recipient.email,
                Address=ups.ShipAddressType(
                    AddressLine=lib.join(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
            ),
            PaymentInformation=(
                ups.PaymentInfoType(
                    ShipmentCharge=[
                        ups.ShipmentChargeType(
                            Type=charge_type,
                            BillShipper=(
                                ups.BillShipperType(
                                    AccountNumber=settings.account_number,
                                    CreditCard=None,
                                    AlternatePaymentMethod=None,
                                )
                                if payment.paid_by == units.PaymentType.sender.name
                                else None
                            ),
                            BillReceiver=(
                                ups.BillReceiverType(
                                    AccountNumber=payment.account_number,
                                    Address=ups.BillReceiverAddressType(
                                        PostalCode=payload.recipient.postal_code,
                                    ),
                                )
                                if payment.paid_by == units.PaymentType.recipient.name
                                else None
                            ),
                            BillThirdParty=(
                                ups.BillThirdPartyChargeType(
                                    AccountNumber=payment.account_number,
                                    Address=ups.AccountAddressType(
                                        PostalCode=biling_address.postal_code,
                                        CountryCode=biling_address.country_code,
                                    )
                                )
                                if payment.paid_by == units.PaymentType.third_party.name
                                else None
                            ),
                            ConsigneeBilledIndicator=None,
                        )
                        for charge_type, payment in charges.items()
                        if payment is not None
                    ],
                    SplitDutyVATIndicator=None,
                )
                if any(charges.values())
                else None
            ),
            MovementReferenceNumber=None,
            ReferenceNumber=(
                [
                    ups.ReferenceNumberType(
                        BarCodeIndicator=None,
                        Code=payload.shipper.country_code,
                        Value=payload.reference,
                    )
                ]
                if (country_pair not in ["US/US", "PR/PR"])
                and any(payload.reference or "")
                else None
            ),
            Service=(ups.ServiceType(Code=service) if service is not None else None),
            ShipmentServiceOptions=ups.ShipmentServiceOptionsType(
                SaturdayPickupIndicator=(
                    "" if options.ups_saturday_pickup_indicator.state else None
                ),
                SaturdayDeliveryIndicator=(
                    "" if options.ups_saturday_delivery_indicator.state else None
                ),
                COD=(
                    ups.CODType(
                        CODFundsCode=None,
                        CODAmount=ups.CurrencyMonetaryType(
                            CurrencyCode=options.currency.state or "USD",
                            MonetaryValue=options.cash_on_delivery.state,
                        ),
                    )
                    if options.cash_on_delivery.state
                    else None
                ),
                AccessPointCOD=(
                    ups.ShipmentServiceOptionsAccessPointCODType(
                        CurrencyCode=options.currency.state,
                        MonetaryValue=lib.to_money(options.ups_access_point_cod.state),
                    )
                    if options.ups_access_point_cod.state
                    else None
                ),
                DeliverToAddresseOnlyIndicator=(
                    ""
                    if options.ups_deliver_to_addressee_only_indicator.state
                    else None
                ),
                DirectDeliveryOnlyIndicator=(
                    "" if options.ups_direct_delivery_only_indicator.state else None
                ),
                Notification=(
                    [
                        ups.NotificationType(
                            NotificationCode=event,
                            EMail=ups.EmailDetailsType(
                                EMailAddress=[
                                    options.email_notification_to.state
                                    or payload.recipient.email
                                ]
                            ),
                            VoiceMessage=None,
                            TextMessage=None,
                            Locale=None,
                        )
                        for event in [8]
                    ]
                    if options.email_notification.state
                    and any(
                        [
                            options.email_notification_to.state,
                            payload.recipient.email,
                        ]
                    )
                    else None
                ),
                LabelDelivery=None,
                InternationalForms=None,
                DeliveryConfirmation=(
                    ups.DeliveryConfirmationType(
                        DCISType=options.ups_delivery_confirmation.state or "01"
                    )
                    if options.ups_delivery_confirmation.state
                    else None
                ),
                ReturnOfDocumentIndicator=(
                    "" if options.ups_return_of_document_indicator.state else None
                ),
                ImportControlIndicator=(
                    "" if options.ups_import_control_indicator.state else None
                ),
                LabelMethod=None,
                CommercialInvoiceRemovalIndicator=(
                    ""
                    if options.ups_commercial_invoice_removal_indicator.state
                    else None
                ),
                UPScarbonneutralIndicator=(
                    "" if options.ups_carbonneutral_indicator.state else None
                ),
                PreAlertNotification=None,
                ExchangeForwardIndicator=None,
                HoldForPickupIndicator=(
                    "" if options.ups_hold_for_pickup_indicator.state else None
                ),
                DropoffAtUPSFacilityIndicator=(
                    "" if options.ups_drop_off_at_ups_facility_indicator.state else None
                ),
                LiftGateForPickUpIndicator=(
                    "" if options.ups_lift_gate_at_pickup_indicator.state else None
                ),
                LiftGateForDeliveryIndicator=(
                    "" if options.ups_lift_gate_at_delivery_indicator.state else None
                ),
                SDLShipmentIndicator=(
                    "" if options.ups_sdl_shipment_indicator.state else None
                ),
                EPRAReleaseCode=("" if options.ups_epra_indicator.state else None),
                RestrictedArticles=None,
                InsideDelivery=None,
                ItemDisposal=None,
            ),
            Package=[
                ups.PackageType(
                    Description=package.parcel.description,
                    Packaging=ups.PackagingType(
                        Code=(
                            mps_packaging
                            or provider_units.PackagingType.map(
                                package.packaging_type
                            ).value
                            or provider_units.PackagingType.ups_customer_supplied_package.value
                        ),
                    ),
                    Dimensions=ups.DimensionsType(
                        UnitOfMeasurement=ups.ShipUnitOfMeasurementType(
                            Code=package.dimension_unit.value,
                        ),
                        Length=package.length.value,
                        Width=package.width.value,
                        Height=package.height.value,
                    ),
                    PackageWeight=ups.PackageWeightType(
                        UnitOfMeasurement=ups.ShipUnitOfMeasurementType(
                            Code=provider_units.WeightUnit[
                                package.weight_unit.name
                            ].value,
                        ),
                        Weight=package.weight.value,
                    ),
                )
                for package in packages
            ],
        ),
        LabelSpecification=ups.LabelSpecificationType(
            LabelImageFormat=ups.LabelImageFormatType(Code=label_format),
            HTTPUserAgent=None,
            LabelStockSize=ups.LabelStockSizeType(
                Height=label_height,
                Width=label_width,
            ),
            Instruction=None,
            CharacterSet=None,
        ),
        ReceiptSpecification=None,
    )

    return lib.Serializable(
        lib.create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(envelope: lib.Envelope) -> str:
    namespace_ = (
        'xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth"'
        ' xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"'
        ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
        ' xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"'
        ' xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"'
        ' xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"'
        ' xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"'
    )

    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "ship")
    lib.apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return lib.to_xml(envelope, namespacedef_=namespace_)
