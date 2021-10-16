from typing import List, Tuple, cast
from ups_lib.freight_ship_web_service_schema import (
    FreightShipRequest,
    RequestType,
    TransactionReferenceType,
    ShipmentType,
    ShipFromType,
    ShipToType,
    AddressType,
    ShipCodeDescriptionType,
    PayerType,
    PaymentInformationType,
    PhoneType,
    WeightType,
    UnitOfMeasurementType,
    DimensionsType,
    ReferenceType,
    ReferenceNumberType,
    ShipmentServiceOptionsType,
    EMailInformationType,
    CODType,
    CODValueType,
    RemitToType,
    FreightShipPhoneType,
    FreightShipAddressType,
    ShipmentTotalWeightType,
    DangerousGoodsType,
    DeclaredValueType,
    DocumentsType,
    ImageType,
    PrintSizeType,
    ShipmentResultsType,
    CommodityType,
)
from purplship.core.utils import (
    gif_to_pdf,
    apply_namespaceprefix,
    create_envelope,
    Serializable,
    Element,
    Envelope,
    XP,
    SF,
)
from purplship.core.units import Options, Packages, PaymentType, CompleteAddress
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message, Payment
from purplship.providers.ups_ground.units import (
    PackagingType,
    ServiceCode,
    ServiceOption,
    WeightUnit as UPSWeightUnit,
    PackagePresets,
    LabelType,
    FreightClass,
)
from purplship.providers.ups_ground.error import parse_error_response
from purplship.providers.ups_ground.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = XP.find("ShipmentResults", response, first=True)
    shipment = _extract_shipment(details, settings) if details is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.build(ShipmentResultsType, node)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.ShipmentIdentificationNumber,
        shipment_identifier=shipment.ShipmentIdentificationNumber,
        label=None,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[Envelope]:
    packages = Packages(payload.parcels, PackagePresets)
    packages.validate(required=["weight"])
    options = Options(payload.options, ServiceOption)
    service = ServiceCode.map(payload.service).value_or_key
    ship_from = CompleteAddress.map(payload.shipper)
    ship_to = CompleteAddress.map(payload.shipper)

    payment_account_number = getattr(
        payload.payment, "account_number", settings.account_number
    )
    payment_address = getattr(payload.payment, "address", None)
    mps_packaging = PackagingType.your_packaging.value if len(packages) > 1 else None
    payer = dict(
        sender=payment_address or ship_from,
        recipient=payment_address or ship_to,
        third_party=payment_address,
    )[getattr(payload.payment, "paid_by", "sender")]
    label_format, label_height, label_width = LabelType[
        payload.label_type or "PDF_6x4"
    ].value

    request = create_envelope(
        header_content=settings.Security,
        body_content=FreightShipRequest(
            Request=RequestType(
                RequestOption=1,
                SubVersion=1607,
                TransactionReference=TransactionReferenceType(
                    CustomerContext=payload.reference,
                    TransactionIdentifier=getattr(payload, "id", None),
                ),
            ),
            Shipment=ShipmentType(
                ShipFrom=ShipFromType(
                    Name=ship_from.company_name,
                    Address=AddressType(
                        AddressLine=ship_from.address_line,
                        City=ship_from.city,
                        StateProvinceCode=ship_from.state_code,
                        Town=None,
                        PostalCode=ship_from.postal_code,
                        CountryCode=ship_from.country_code,
                        ResidentialAddressIndicator=(
                            "" if ship_from.residential else None
                        ),
                    ),
                    TariffPoint=None,
                    AttentionName=ship_from.person_name,
                    Phone=PhoneType(Number=ship_from.phone_number),
                    FaxNumber=None,
                    EMailAddress=ship_from.email,
                ),
                ShipTo=ShipToType(
                    Name=ship_to.company_name,
                    TaxIdentificationNumber=None,
                    Address=AddressType(
                        AddressLine=ship_to.address_line,
                        City=ship_to.city,
                        StateProvinceCode=ship_to.state_code,
                        Town=None,
                        PostalCode=ship_to.postal_code,
                        CountryCode=ship_to.country_code,
                        ResidentialAddressIndicator=(
                            "" if ship_to.residential else None
                        ),
                    ),
                    TariffPoint=None,
                    AttentionName=ship_to.person_name,
                    Phone=PhoneType(Number=ship_to.phone_number),
                    FaxNumber=None,
                    EMailAddress=ship_to.email,
                ),
                PaymentInformation=PaymentInformationType(
                    Payer=PayerType(
                        Name=payer.company_name,
                        Address=AddressType(
                            AddressLine=payer.address_line,
                            City=payer.city,
                            StateProvinceCode=payer.state_code,
                            Town=None,
                            CountryCode=payer.country_code,
                            PostalCode=payer.postal_code,
                            ResidentialAddressIndicator=(
                                "" if payer.residential else None
                            ),
                        ),
                        ShipperNumber=payment_account_number,
                        AttentionName=payer.person_name,
                        Phone=PhoneType(Number=payer.phone_number),
                        FaxNumber=None,
                        EMailAddress=payer.email,
                    ),
                    ShipmentBillingOption=ShipCodeDescriptionType(
                        Code=40, Description="Freight Collect"
                    ),
                ),
                ManufactureInformation=None,
                Service=(
                    ShipCodeDescriptionType(Code=service, Description=None)
                    if service is not None
                    else None
                ),
                HandlingUnitOne=None,
                HandlingUnitTwo=None,
                ExistingShipmentID=None,
                HandlingInstructions=None,
                DeliveryInstructions=None,
                PickupInstructions=None,
                SpecialInstructions=None,
                ShipmentTotalWeight=ShipmentTotalWeightType(
                    Value=packages.weight.value,
                    UnitOfMeasurement=UPSWeightUnit[packages.weight.unit].value,
                ),
                Commodity=[
                    CommodityType(
                        CommodityID=getattr(commodity, "id", None),
                        Description=commodity.parcel.description,
                        Weight=WeightType(
                            Value=commodity.weight.value,
                            UnitOfMeasurement=UnitOfMeasurementType(
                                Code=UPSWeightUnit[commodity.weight_unit.name].value,
                            ),
                        ),
                        AdjustedWeight=None,
                        Dimensions=(
                            DimensionsType(
                                UnitOfMeasurement=UnitOfMeasurementType(
                                    Code=commodity.dimension_unit.value,
                                    Description=None,
                                ),
                                Length=commodity.length.value,
                                Width=commodity.width.value,
                                Height=commodity.height.value,
                            )
                            if commodity.has_dimensions
                            else None
                        ),
                        NumberOfPieces=1,
                        PackagingType=ShipCodeDescriptionType(
                            Code=(
                                mps_packaging
                                or PackagingType[
                                    commodity.packaging_type or "your_packaging"
                                ].value
                            ),
                        ),
                        DangerousGoodsIndicator=(
                            "" if options.dangerous_good else None
                        ),
                        CommodityValue=None,
                        FreightClass=FreightClass.map(
                            options.freight_class or 50
                        ).value,
                        NMFCCommodity=None,
                        NMFCCommodityCode=None,
                    )
                    for commodity in packages
                ],
                Reference=(
                    [
                        ReferenceType(
                            Number=ReferenceNumberType(
                                Code="OTHER", Value=payload.reference
                            )
                        )
                    ]
                    if any(payload.reference or "")
                    else None
                ),
                ShipmentServiceOptions=(
                    ShipmentServiceOptionsType(
                        EMailInformation=(
                            [
                                EMailInformationType(
                                    EMailType=f"000{email_type}",
                                    EMail=options.email_notification_to
                                    or payload.recipient.email,
                                )
                                for email_type in [1, 2, 3, 4]
                            ]
                            if any(
                                [options.email_notification_to, payload.recipient.email]
                            )
                            else None
                        ),
                        COD=(
                            CODType(
                                CODValue=CODValueType(
                                    CurrencyCode=options.currency or "USD",
                                    MonetaryValue=options.cash_on_delivery,
                                ),
                                CODPaymentMethod=ShipCodeDescriptionType(Code="M"),
                                CODBillingOption=ShipCodeDescriptionType(Code="02"),
                                RemitTo=RemitToType(
                                    Name=payer.company_name,
                                    Address=FreightShipAddressType(
                                        AddressLine=payer.address_line,
                                        City=payer.city,
                                        StateProvinceCode=payer.state_code,
                                        Town=payer.city,
                                        PostalCode=payer.postal_code,
                                        CountryCode=payer.country_code,
                                        ResidentialAddressIndicator=(
                                            "" if payer.residential else None
                                        ),
                                    ),
                                    AttentionName=payer.person_name,
                                    Phone=(
                                        FreightShipPhoneType(Number=payer.phone_number)
                                        if payer.phone_number
                                        else None
                                    ),
                                    FaxNumber=None,
                                    EMailAddress=payer.email,
                                ),
                            )
                            if options.cash_on_delivery
                            else None
                        ),
                        DangerousGoods=(
                            DangerousGoodsType(
                                Name=(ship_from.company_name or ship_from.person_name),
                                Phone=(
                                    FreightShipPhoneType(Number=payer.phone_number)
                                    if payer.phone_number
                                    else None
                                ),
                            )
                            if options.dangerous_good
                            else None
                        ),
                        DeclaredValue=(
                            DeclaredValueType(
                                CurrencyCode=options.currency or "USD",
                                MonetaryValue=options.declared_value,
                            )
                            if options.declared_value
                            else None
                        ),
                    )
                    if any(
                        [
                            options.cash_on_delivery,
                            options.email_notification,
                            options.dangerous_good,
                            options.declared_value,
                        ]
                    )
                    else None
                ),
                PickupRequest=None,
                Documents=DocumentsType(
                    Image=ImageType(
                        Type=ShipCodeDescriptionType(Code="30"),
                        LabelsPerPage=1,
                        Format=ShipCodeDescriptionType(Code="01"),
                        PrintFormat=ShipCodeDescriptionType(
                            Code="02" if "ZPL" in label_format else "01"
                        ),
                        PrintSize=PrintSizeType(Length=label_height, Width=label_width),
                    )
                ),
                ITNNumber=None,
                TaxID=None,
                MovementReferenceNumber=None,
                EICNumberAndStatement=None,
                TimeInTransitIndicator=None,
                HandlingUnits=None,
                DensityEligibleIndicator=None,
            ),
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespace_ = (
        'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" '
        'xmlns:wsf="http://www.ups.com/schema/wsf" '
        'xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" '
        'xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" '
        'xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"'
    )

    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "ship")
    apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return XP.export(envelope, namespacedef_=namespace_)
