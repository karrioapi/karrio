from typing import List, Tuple
from pyups import common
from pyups.ship_web_service_schema import (
    ShipmentRequest as UPSShipmentRequest,
    ShipmentResponse,
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
    LabelSpecificationType,
    LabelImageFormatType,
    ShipmentResultsType,
    ShipmentServiceOptionsType,
    NotificationType
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import DimensionUnit, Weight, WeightUnit, Dimension
from purplship.core.models import (
    ShipmentRequest,
    ChargeDetails,
    ShipmentDetails,
    Error,
    ReferenceDetails,
    Option,
)
from purplship.carriers.ups.units import (
    ShippingPackagingType,
    ShippingServiceCode,
    WeightUnit as UPSWeightUnit,
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Error]]:
    details = response.xpath(".//*[local-name() = $name]", name="ShipmentResponse")
    shipment = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_node: Element, settings: Settings) -> ShipmentDetails:
    shipmentResponse = ShipmentResponse()
    shipmentResponse.build(shipment_node)
    shipment: ShipmentResultsType = shipmentResponse.ShipmentResults

    if shipment.NegotiatedRateCharges is None:
        total_charge = shipment.ShipmentCharges.TotalCharges
    else:
        total_charge = shipment.NegotiatedRateCharges.TotalCharge

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_number=shipment.ShipmentIdentificationNumber,
        total_charge=ChargeDetails(
            name="Shipment charge",
            amount=total_charge.MonetaryValue,
            currency=total_charge.CurrencyCode,
        ),
        charges=[
            ChargeDetails(
                name=charge.Code,
                amount=charge.MonetaryValue,
                currency=charge.CurrencyCode,
            )
            for charge in [
                shipment.ShipmentCharges.TransportationCharges,
                shipment.ShipmentCharges.ServiceOptionsCharges,
                shipment.ShipmentCharges.BaseServiceCharge,
            ]
            if charge is not None
        ],
        documents=[
            pkg.ShippingLabel.GraphicImage for pkg in (shipment.PackageResults or [])
        ],
        reference=ReferenceDetails(
            value=shipmentResponse.Response.TransactionReference.CustomerContext,
            type="CustomerContext",
        ),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[UPSShipmentRequest]:
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    service = next(
        (ShippingServiceCode[s].value for s in payload.parcel.services if s in ShippingServiceCode.__members__),
        None
    )
    options: dict = {}
    for name, value in payload.parcel.options.items():
        if name in Option.__members__:
            options.update({
                name: Option[name].value(**value if isinstance(value, dict) else value)
            })

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
            ReturnService=None,
            DocumentsOnlyIndicator="" if payload.parcel.is_document else None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                AttentionName=payload.shipper.person_name,
                CompanyDisplayableName=None,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                Phone=ShipPhoneType(Number=payload.shipper.phone_number, Extension=None)
                if payload.shipper.phone_number is not None
                else None,
                ShipperNumber=settings.account_number,
                FaxNumber=None,
                EMailAddress=payload.shipper.email,
                Address=ShipAddressType(
                    AddressLine=concat_str(
                        payload.shipper.address_line_1, payload.shipper.address_line_2
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
                Phone=ShipPhoneType(
                    Number=payload.recipient.phone_number, Extension=None
                )
                if payload.recipient.phone_number is not None
                else None,
                FaxNumber=None,
                EMailAddress=payload.recipient.email,
                Address=ShipAddressType(
                    AddressLine=concat_str(
                        payload.recipient.address_line_1,
                        payload.recipient.address_line_2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
                LocationID=None,
            ),
            AlternateDeliveryAddress=None,
            ShipFrom=None,
            PaymentInformation=None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            ShipmentRatingOptions=None,
            MovementReferenceNumber=None,
            ReferenceNumber=None,
            Service=ServiceType(Code=service) if service is not None else None,
            InvoiceLineTotal=None,
            NumOfPiecesInShipment=None,
            USPSEndorsement=None,
            MILabelCN22Indicator=None,
            SubClassification=None,
            CostCenter=None,
            PackageID=None,
            IrregularIndicator=None,
            ShipmentIndicationType=None,
            MIDualReturnShipmentKey=None,
            MIDualReturnShipmentIndicator=None,
            RatingMethodRequestedIndicator=None,
            TaxInformationIndicator=None,
            PromotionalDiscountInformation=None,
            ShipmentServiceOptions=ShipmentServiceOptionsType(
                SaturdayDeliveryIndicator=None,
                SaturdayPickupIndicator=None,
                COD=None,
                AccessPointCOD=None,
                DeliverToAddresseeOnlyIndicator=None,
                DirectDeliveryOnlyIndicator=None,
                Notification=[
                    NotificationType(
                        NotificationCode=event,
                        EMail=options['notification'].email or payload.shipper.email,
                        VoiceMessage=None,
                        TextMessage=None,
                        Locale=None
                    ) for event in [8]
                ] if 'notification' in options else None,
                LabelDelivery=None,
                InternationalForms=None,
                DeliveryConfirmation=None,
                ReturnOfDocumentIndicator=None,
                ImportControlIndicator=None,
                LabelMethod=None,
                CommercialInvoiceRemovalIndicator=None,
                UPScarbonneutralIndicator=None,
                PreAlertNotification=None,
                ExchangeForwardIndicator=None,
                HoldForPickupIndicator=None,
                DropoffAtUPSFacilityIndicator=None,
                LiftGateForPickUpIndicator=None,
                LiftGateForDeliveryIndicator=None,
                SDLShipmentIndicator=None,
                EPRAReleaseCode=None,
                RestrictedArticles=None,
                InsideDelivery=None,
                ItemDisposal=None
            ) if options != {} else None,
            Package=[
                PackageType(
                    Description=payload.parcel.description,
                    Packaging=PackagingType(
                        Code=ShippingPackagingType[payload.parcel.packaging_type].value,
                        Description=None,
                    )
                    if payload.parcel.packaging_type is not None
                    else None,
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
                            Code=dimension_unit.value, Description=None
                        ),
                        Length=Dimension(payload.parcel.length, dimension_unit).value,
                        Width=Dimension(payload.parcel.width, dimension_unit).value,
                        Height=Dimension(payload.parcel.height, dimension_unit).value,
                    ),
                    DimWeight=None,
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
                            Code=UPSWeightUnit[weight_unit.name].value, Description=None
                        ),
                        Weight=Weight(payload.parcel.weight, weight_unit).value,
                    ),
                    LargePackageIndicator=None,
                    ReferenceNumber=None,
                    AdditionalHandlingIndicator=None,
                    PackageServiceOptions=None,
                    Commodity=None,
                    HazMatPackageInformation=None,
                )
            ],
        ),
        LabelSpecification=LabelSpecificationType(
            LabelImageFormat=LabelImageFormatType(
                Code=payload.label.format, Description=payload.label.format
            ),
            HTTPUserAgent=None,
            LabelStockSize=None,
            Instruction=None,
        )
        if payload.label is not None
        else None,
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
