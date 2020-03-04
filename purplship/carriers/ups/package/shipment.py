from typing import List
from functools import partial
from pyups import common
from pyups.package_ship import (
    ShipmentRequest as UPSShipmentRequest, ShipmentResponse, ShipmentType, ShipperType,
    ShipPhoneType, ShipToType, ShipAddressType, AlternateDeliveryAddressType, ShipFromType,
    PaymentInfoType, ShipmentChargeType, BillShipperType, BillReceiverType, CreditCardType,
    BillReceiverAddressType, BillThirdPartyChargeType, ServiceType, PackageType, PackagingType,
    DimensionsType, PackageWeightType, ShipUnitOfMeasurementType, LabelSpecificationType, LabelImageFormatType
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.units import DimensionUnit
from purplship.core.utils.xml import Element
from purplship.core.models import (
    ShipmentRequest, ChargeDetails, ShipmentDetails, Error, ReferenceDetails, Party
)
from purplship.carriers.ups.units import ShippingPackagingType, ShippingServiceCode, WeightUnit
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_shipment_response(response: Element, settings: Settings) -> (ShipmentDetails, List[Error]):
    details = response.xpath(".//*[local-name() = $name]", name="FreightShipResponse")
    shipment = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_node: Element, settings: Settings) -> ShipmentDetails:
    shipmentResponse = ShipmentResponse()
    shipmentResponse.build(shipment_node)
    shipment = shipmentResponse.ShipmentResults

    if not shipment.NegotiatedRateCharges:
        total_charge = (
            shipment.ShipmentCharges.TotalChargesWithTaxes
            or shipment.ShipmentCharges.TotalCharges
        )
    else:
        total_charge = (
            shipment.NegotiatedRateCharges.TotalChargesWithTaxes
            or shipment.NegotiatedRateCharges.TotalCharge
        )

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=[pkg.TrackingNumber for pkg in shipment.PackageResults],
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
            pkg.ShippingLabel.GraphicImage
            for pkg in (shipment.PackageResults or [])
        ],
        reference=ReferenceDetails(
            value=shipmentResponse.Response.TransactionReference.CustomerContext,
            type="CustomerContext",
        ),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[UPSShipmentRequest]:
    services = [ShippingServiceCode[svc] for svc in payload.shipment.services if svc in ShippingServiceCode.__members__]
    request = UPSShipmentRequest(
        Request=common.RequestType(
            RequestOption=payload.shipment.extra.get("RequestOption")
            or ["validate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=", ".join(payload.shipment.references),
                TransactionIdentifier=payload.shipment.extra.get(
                    "TransactionIdentifier"
                ),
            ),
        ),
        Shipment=ShipmentType(
            Description=payload.shipment.extra.get("Description"),
            ReturnService=None,
            DocumentsOnlyIndicator="" if payload.shipment.is_document else None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                AttentionName=payload.shipper.person_name,
                CompanyDisplayableName=payload.shipper.extra.get(
                    "CompanyDisplayableName"
                ),
                TaxIdentificationNumber=payload.shipper.tax_id,
                TaxIDType=None,
                Phone=ShipPhoneType(
                    Number=payload.shipper.phone_number,
                    Extension=payload.shipper.extra.get("Extension"),
                )
                if payload.shipper.phone_number is not None
                else None,
                ShipperNumber=payload.shipper.account_number,
                FaxNumber=payload.shipper.extra.get("FaxNumber"),
                EMailAddress=payload.shipper.email_address,
                Address=ShipAddressType(
                    AddressLine=payload.shipper.address_lines,
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                AttentionName=payload.recipient.person_name,
                CompanyDisplayableName=payload.recipient.extra.get(
                    "CompanyDisplayableName"
                ),
                TaxIdentificationNumber=payload.recipient.tax_id,
                TaxIDType=None,
                Phone=ShipPhoneType(
                    Number=payload.recipient.phone_number,
                    Extension=payload.recipient.extra.get("Extension"),
                )
                if payload.recipient.phone_number is not None
                else None,
                FaxNumber=payload.recipient.extra.get("FaxNumber"),
                EMailAddress=payload.recipient.email_address,
                Address=ShipAddressType(
                    AddressLine=payload.recipient.address_lines,
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
                LocationID=None,
            ),
            AlternateDeliveryAddress=(
                lambda alternate: AlternateDeliveryAddressType(
                    Name=alternate.company_name,
                    AttentionName=alternate.person_name,
                    UPSAccessPointID=alternate.extra.get("UPSAccessPointID"),
                    Address=ShipAddressType(
                        AddressLine=alternate.address_lines,
                        City=alternate.city,
                        StateProvinceCode=alternate.state_code,
                        PostalCode=alternate.postal_code,
                        CountryCode=alternate.country_code,
                    ),
                )
            )(Party(payload.shipment.extra.get("AlternateDeliveryAddress")))
            if "AlternateDeliveryAddress" in payload.shipment.extra
            else None,
            ShipFrom=(
                lambda ship_from: ShipFromType(
                    Name=ship_from.company_name,
                    AttentionName=ship_from.person_name,
                    CompanyDisplayableName=ship_from.extra.get(
                        "CompanyDisplayableName"
                    ),
                    TaxIdentificationNumber=ship_from.tax_id,
                    TaxIDType=None,
                    Phone=ShipPhoneType(
                        Number=ship_from.phone_number,
                        Extension=ship_from.extra.get("Extension"),
                    )
                    if ship_from.phone_number is not None
                    else None,
                    FaxNumber=ship_from.extra.get("FaxNumber"),
                    EMailAddress=ship_from.email_address,
                    Address=ShipAddressType(
                        AddressLine=ship_from.address_lines,
                        City=ship_from.city,
                        StateProvinceCode=ship_from.state_code,
                        PostalCode=ship_from.postal_code,
                        CountryCode=ship_from.country_code,
                    ),
                )
            )(Party(**payload.shipment.extra.get("ShipFrom")))
            if "ShipFrom" in payload.shipment.extra
            else None,
            PaymentInformation=PaymentInfoType(
                ShipmentCharge=[
                    ShipmentChargeType(
                        Type=payload.shipment.extra.get("ShipmentCharge").get(
                            "Type"
                        )
                        if "ShipmentCharge" in payload.shipment.extra
                        else None,
                        BillShipper=BillShipperType(
                            AccountNumber=payload.shipment.payment_account_number
                            or payload.shipper.account_number,
                            CreditCard=(
                                lambda card: CreditCardType(
                                    Type=card.get("Type"),
                                    Number=card.get("Number"),
                                    ExpirationDate=card.get("ExpirationDate"),
                                    SecurityCode=card.get("Type"),
                                    Address=(
                                        lambda address: ShipAddressType(
                                            AddressLine=address.address_lines,
                                            City=address.city,
                                            StateProvinceCode=address.state_code,
                                            PostalCode=address.postal_code,
                                            CountryCode=address.country_code,
                                        )
                                    )(Party(**card.get("Address")))
                                    if "Address" in card
                                    else None,
                                )
                            )(payload.shipment.extra.get("CreditCard"))
                            if "CreditCard" in payload.shipment.extra
                            else None,
                            AlternatePaymentMethod=payload.shipment.payment_type,
                        )
                        if payload.shipment.paid_by == "SENDER"
                        else None,
                        BillReceiver=BillReceiverType(
                            AccountNumber=payload.recipient.account_number,
                            Address=BillReceiverAddressType(
                                PostalCode=payload.recipient.postal_code
                            ),
                        )
                        if not payload.shipment.paid_by
                        else None,
                        BillThirdParty=BillThirdPartyChargeType(
                            AccountNumber=payload.shipment.payment_account_number,
                            Address=BillReceiverAddressType(
                                PostalCode=payload.shipment.extra.get(
                                    "payor_postal_code"
                                )
                            ),
                        )
                        if payload.shipment.paid_by == "THIRD_PARTY"
                        else None,
                        ConsigneeBilledIndicator=None,
                    )
                ],
                SplitDutyVATIndicator=None,
            ),
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            ShipmentRatingOptions=None,
            MovementReferenceNumber=None,
            ReferenceNumber=None,
            Service=ServiceType(Code=services[0].value)
            if len(services) > 0
            else None,
            InvoiceLineTotal=None,
            NumOfPiecesInShipment=payload.shipment.total_items,
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
            ShipmentServiceOptions=None,
            Package=[
                PackageType(
                    Description=pkg.description,
                    Packaging=PackagingType(
                        Code=ShippingPackagingType[pkg.packaging_type].value,
                        Description=None,
                    )
                    if pkg.packaging_type != None
                    else None,
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
                            Code=DimensionUnit[
                                payload.shipment.dimension_unit
                            ].value,
                            Description=None,
                        ),
                        Length=pkg.length,
                        Width=pkg.width,
                        Height=pkg.height,
                    ),
                    DimWeight=pkg.extra.get("DimWeight"),
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=ShipUnitOfMeasurementType(
                            Code=WeightUnit[payload.shipment.weight_unit].value,
                            Description=None,
                        ),
                        Weight=pkg.weight,
                    ),
                    LargePackageIndicator=pkg.extra.get("LargePackageIndicator"),
                    ReferenceNumber=None,
                    AdditionalHandlingIndicator=None,
                    PackageServiceOptions=None,
                    Commodity=None,
                    HazMatPackageInformation=None,
                )
                for pkg in payload.shipment.items
            ],
        ),
        LabelSpecification=LabelSpecificationType(
            LabelImageFormat=LabelImageFormatType(
                Code=payload.shipment.label.format,
                Description=payload.shipment.label.format,
            ),
            HTTPUserAgent=payload.shipment.label.extra.get("HTTPUserAgent"),
            LabelStockSize=None,
            Instruction=payload.shipment.label.extra.get("Instruction"),
        )
        if payload.shipment.label is not None
        else None,
        ReceiptSpecification=None,
    )
    return Serializable(request, lambda _: partial(_request_serializer, settings=settings)(_))


def _request_serializer(request: UPSShipmentRequest, settings: Settings) -> str:
    namespace_ = """
                    xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" 
                    xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" 
                    xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"
                """.replace(" ", "").replace("\n", " ")
    return clean_namespaces(
        export(
            create_envelope(
                header_content=settings.Security,
                body_content=request
            ),
            namespacedef_=namespace_,
        ),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        body_child_prefix="ship:",
        header_child_name="UPSSecurity",
        body_child_name="Shipment",
    )
