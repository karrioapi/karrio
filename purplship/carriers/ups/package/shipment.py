from typing import List, Tuple, Dict, cast
from pyups import common
from pyups.ship_web_service_schema import (
    ShipmentRequest as UPSShipmentRequest,
    ShipmentType,
    ShipperType,
    ShipPhoneType,
    ShipToType,
    ShipAddressType,
    ServiceType,
    PackageType,
    PackagingType,
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
    CreditCardType,
    CreditCardAddressType,
    BillReceiverAddressType,
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import Options, Package, PaymentType
from purplship.core.errors import RequiredFieldError
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message, Payment
from purplship.carriers.ups.units import (
    ShippingPackagingType,
    ShippingServiceCode,
    WeightUnit as UPSWeightUnit,
    PackagePresets,
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = next(
        iter(response.xpath(".//*[local-name() = $name]", name="ShipmentResults")), None
    )
    shipment = _extract_shipment(details, settings) if details is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipment = ShipmentResultsType()
    shipment.build(node)
    package: PackageResultsType = next(iter(shipment.PackageResults), None)

    return ShipmentDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.ShipmentIdentificationNumber,
        label=cast(LabelType, package.ShippingLabel).GraphicImage,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[UPSShipmentRequest]:
    parcel_preset = (
        PackagePresets[payload.parcel.package_preset].value
        if payload.parcel.package_preset
        else None
    )
    package = Package(payload.parcel, parcel_preset)
    options = Options(payload.options)
    service = ShippingServiceCode[payload.service].value

    if (("freight" in service) or ("ground" in service)) and (
        package.weight.value is None
    ):
        raise RequiredFieldError("parcel.weight")

    charges: Dict[str, Payment] = {
        "01": payload.payment,
        "02": payload.customs.duty if payload.customs is not None else None,
    }

    request = UPSShipmentRequest(
        Request=common.RequestType(
            RequestOption=["validate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.parcel.reference, TransactionIdentifier=None
            ),
        ),
        Shipment=ShipmentType(
            Description=payload.parcel.description,
            DocumentsOnlyIndicator="" if payload.parcel.is_document else None,
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
                    AddressLine=concat_str(
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
                    AddressLine=concat_str(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
            ),
            PaymentInformation=PaymentInfoType(
                ShipmentCharge=[
                    ShipmentChargeType(
                        Type=charge_type,
                        BillShipper=BillShipperType(
                            AccountNumber=settings.account_number,
                            CreditCard=CreditCardType(
                                Type=payment.credit_card.type,
                                Number=payment.credit_card.number,
                                ExpirationDate=(
                                    f"{payment.credit_card.expiry_year}{payment.credit_card.expiry_month}"
                                ),
                                SecurityCode=payment.credit_card.security_code,
                                Address=CreditCardAddressType(
                                    AddressLine=concat_str(
                                        payload.shipper.address_line1,
                                        payload.shipper.address_line2,
                                    ),
                                    City=payload.shipper.city,
                                    StateProvinceCode=payload.shipper.state_code,
                                    PostalCode=payload.payment.credit_card.postal_code
                                    or payload.shipper.postal_code,
                                    CountryCode=payload.shipper.country_code,
                                ),
                            )
                            if payment.credit_card is not None
                            else None,
                            AlternatePaymentMethod=None,
                        )
                        if payment.paid_by == PaymentType.sender.name
                        else None,
                        BillReceiver=BillReceiverType(
                            AccountNumber=payment.account_number,
                            Address=BillReceiverAddressType(
                                PostalCode=payload.recipient.postal_code
                            ),
                        )
                        if payment.paid_by == PaymentType.recipient.name
                        else None,
                        BillThirdParty=BillThirdPartyChargeType(
                            AccountNumber=payment.account_number,
                        )
                        if payment.paid_by == PaymentType.third_party.name
                        else None,
                        ConsigneeBilledIndicator=None,
                    )
                    for charge_type, payment in charges.items()
                    if payment is not None
                ],
                SplitDutyVATIndicator=None,
            )
            if any(charges.values())
            else None,
            Service=(ServiceType(Code=service) if service is not None else None),
            ShipmentServiceOptions=ShipmentServiceOptionsType(
                COD=CODType(
                    CODFundsCode=None,
                    CODAmount=CurrencyMonetaryType(
                        CurrencyCode=options.currency or "USD",
                        MonetaryValue=options.cash_on_delivery.amount,
                    ),
                )
                if options.cash_on_delivery
                else None,
                Notification=[
                    NotificationType(
                        NotificationCode=event,
                        EMail=EmailDetailsType(
                            EMailAddress=[
                                options.notification.email or payload.shipper.email
                            ],
                        ),
                        VoiceMessage=None,
                        TextMessage=None,
                        Locale=None,
                    )
                    for event in [8]
                ]
                if options.notification
                else None,
            )
            if any([options.cash_on_delivery, options.notification])
            else None,
            Package=[
                PackageType(
                    Description=payload.parcel.description,
                    Packaging=(
                        PackagingType(
                            Code=ShippingPackagingType[
                                payload.parcel.packaging_type
                            ].value,
                        )
                        if payload.parcel.packaging_type is not None
                        else None
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
                            Code=UPSWeightUnit[package.weight_unit.name].value,
                        ),
                        Weight=package.weight.value,
                    ),
                )
            ],
        ),
        LabelSpecification=None,
        ReceiptSpecification=None,
    )
    return Serializable(
        create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(request: Element) -> str:
    namespace_ = """
        xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth"
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"
        xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"
        xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    return clean_namespaces(
        export(request, namespacedef_=namespace_),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        body_child_prefix="ship:",
        header_child_name="UPSSecurity",
        body_child_name="Shipment",
    )
