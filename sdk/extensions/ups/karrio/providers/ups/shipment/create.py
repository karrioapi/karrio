from ups_lib import common
from ups_lib.ship_web_service_schema import (
    ShipmentRequest as UPSShipmentRequest,
    ShipmentType,
    ShipperType,
    ShipPhoneType,
    ShipToType,
    ShipAddressType,
    ServiceType,
    PackageType,
    PackagingType as UPSPackagingType,
    DimensionsType,
    PackageWeightType,
    ShipUnitOfMeasurementType,
    ShipmentResultsType,
    ShipmentServiceOptionsType,
    NotificationType,
    EmailDetailsType,
    CODType,
    CurrencyMonetaryType,
    PackageResultsType,
    LabelType,
    PaymentInfoType,
    ShipmentChargeType,
    BillShipperType,
    BillReceiverType,
    BillThirdPartyChargeType,
    BillReceiverAddressType,
    LabelSpecificationType,
    LabelImageFormatType,
    LabelStockSizeType,
    ImageFormatType,
    ReferenceNumberType,
)

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
    shipment = lib.to_object(ShipmentResultsType, node)
    package: PackageResultsType = next(iter(shipment.PackageResults), None)
    shipping_label = typing.cast(LabelType, package.ShippingLabel)

    label = (
        lib.image_to_pdf(shipping_label.GraphicImage)
        if typing.cast(ImageFormatType, shipping_label.ImageFormat).Code == "GIF"
        else shipping_label.GraphicImage
    )

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.ShipmentIdentificationNumber,
        shipment_identifier=shipment.ShipmentIdentificationNumber,
        docs=models.Documents(label=label),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[UPSShipmentRequest]:
    packages = lib.to_packages(payload.parcels, provider_units.PackagePresets)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    service = provider_units.ShippingService.map(payload.service).value_or_key

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
    label_format, label_height, label_width = provider_units.LabelType[
        payload.label_type or "PDF_6x4"
    ].value

    request = UPSShipmentRequest(
        Request=common.RequestType(
            RequestOption=["validate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.reference,
                TransactionIdentifier=getattr(payload, "id", None),
            ),
        ),
        Shipment=ShipmentType(
            Description=packages.description,
            DocumentsOnlyIndicator="" if packages.is_document else None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                AttentionName=payload.shipper.person_name,
                CompanyDisplayableName=None,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                Phone=(
                    ShipPhoneType(Number=payload.shipper.phone_number, Extension=None)
                    if payload.shipper.phone_number is not None
                    else None
                ),
                ShipperNumber=settings.account_number,
                FaxNumber=None,
                EMailAddress=payload.shipper.email,
                Address=ShipAddressType(
                    AddressLine=lib.join(
                        payload.shipper.address_line1, payload.shipper.address_line2
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                AttentionName=payload.recipient.person_name,
                CompanyDisplayableName=None,
                TaxIdentificationNumber=payload.recipient.federal_tax_id,
                TaxIDType=None,
                Phone=(
                    ShipPhoneType(Number=payload.recipient.phone_number, Extension=None)
                    if payload.recipient.phone_number is not None
                    else None
                ),
                FaxNumber=None,
                EMailAddress=payload.recipient.email,
                Address=ShipAddressType(
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
                PaymentInfoType(
                    ShipmentCharge=[
                        ShipmentChargeType(
                            Type=charge_type,
                            BillShipper=(
                                BillShipperType(
                                    AccountNumber=settings.account_number,
                                    CreditCard=None,
                                    AlternatePaymentMethod=None,
                                )
                                if payment.paid_by == units.PaymentType.sender.name
                                else None
                            ),
                            BillReceiver=(
                                BillReceiverType(
                                    AccountNumber=payment.account_number,
                                    Address=BillReceiverAddressType(
                                        PostalCode=payload.recipient.postal_code
                                    ),
                                )
                                if payment.paid_by == units.PaymentType.recipient.name
                                else None
                            ),
                            BillThirdParty=(
                                BillThirdPartyChargeType(
                                    AccountNumber=payment.account_number,
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
                    ReferenceNumberType(
                        BarCodeIndicator=None,
                        Code=payload.shipper.country_code,
                        Value=payload.reference,
                    )
                ]
                if (country_pair not in ["US/US", "PR/PR"])
                and any(payload.reference or "")
                else None
            ),
            Service=(ServiceType(Code=service) if service is not None else None),
            ShipmentServiceOptions=(
                ShipmentServiceOptionsType(
                    COD=(
                        CODType(
                            CODFundsCode=None,
                            CODAmount=CurrencyMonetaryType(
                                CurrencyCode=options.currency.state or "USD",
                                MonetaryValue=options.cash_on_delivery.state,
                            ),
                        )
                        if options.cash_on_delivery.state
                        else None
                    ),
                    Notification=(
                        [
                            NotificationType(
                                NotificationCode=event,
                                EMail=EmailDetailsType(
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
                )
                if any(
                    [options.cash_on_delivery.state, options.email_notification.state]
                )
                else None
            ),
            Package=[
                PackageType(
                    Description=package.parcel.description,
                    Packaging=UPSPackagingType(
                        Code=(
                            mps_packaging
                            or provider_units.PackagingType.map(package.packaging_type).value
                            or provider_units.PackagingType.ups_customer_supplied_package.value
                        ),
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
                            Code=package.dimension_unit.value,
                        ),
                        Length=package.length.value,
                        Width=package.width.value,
                        Height=package.height.value,
                    ),
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
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
        LabelSpecification=LabelSpecificationType(
            LabelImageFormat=LabelImageFormatType(Code=label_format, Description=None),
            HTTPUserAgent=None,
            LabelStockSize=LabelStockSizeType(Height=label_height, Width=label_width),
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
