import time
from base64 import encodebytes
from typing import List, Tuple, Optional, cast
from pydhl.ship_val_global_req_6_2 import (
    ShipmentRequest as DHLShipmentRequest,
    Billing,
    Consignee,
    Contact,
    Commodity,
    Shipper,
    ShipmentDetails as DHLShipmentDetails,
    Pieces,
    Piece,
    Reference,
    Dutiable,
    MetaData,
    Notification,
    SpecialService,
    WeightUnit,
    DimensionUnit,
    Label,
)
from pydhl.ship_val_global_res_6_2 import ShipmentResponse, LabelImage
from purplship.core.utils import Serializable, SF, XP
from purplship.core.utils.xml import Element
from purplship.core.models import (
    ShipmentRequest,
    Message,
    ShipmentDetails,
)
from purplship.core.units import Options, Packages, Country
from purplship.providers.dhl_express.units import (
    PackageType,
    ProductCode,
    PaymentType,
    CountryRegion,
    SpecialServiceCode,
    DeliveryType,
    PackagePresets,
    LabelType,
)
from purplship.providers.dhl_express.utils import Settings
from purplship.providers.dhl_express.error import parse_error_response


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    air_way_bill = next(
        iter(response.xpath(".//*[local-name() = $name]", name="AirwayBillNumber")),
        None,
    )
    return (
        _extract_shipment(response, settings) if air_way_bill is not None else None,
        parse_error_response(response, settings),
    )


def _extract_shipment(shipment_node, settings: Settings) -> Optional[ShipmentDetails]:
    shipment = ShipmentResponse()
    shipment.build(shipment_node)
    label_image = next(iter(shipment.LabelImage), None)
    label = encodebytes(cast(LabelImage, label_image).OutputImage).decode("utf-8")

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.AirwayBillNumber,
        shipment_identifier=shipment.AirwayBillNumber,
        label=label,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[DHLShipmentRequest]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    options = Options(payload.options)
    product = ProductCode[payload.service].value
    package_type = (
        PackageType[packages[0].packaging_type or "your_packaging"].value
        if len(packages) == 1
        else None
    )
    delivery_type = next(
        (d for d in DeliveryType if d.name in payload.options.keys()), None
    )
    special_services = [
        SpecialServiceCode[s].value
        for s in payload.options.keys()
        if s in SpecialServiceCode
    ]
    has_payment_config = payload.payment is not None
    has_customs_config = payload.customs is not None
    label_format, label_template = LabelType[payload.label_type or 'PDF_6x4'].value

    request = DHLShipmentRequest(
        schemaVersion=6.2,
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=6.2)
        ),
        RegionCode=CountryRegion[payload.shipper.country_code].value,
        RequestedPickupTime="Y",
        LanguageCode="en",
        PiecesEnabled="Y",
        LatinResponseInd=None,
        Billing=Billing(
            ShipperAccountNumber=settings.account_number,
            BillingAccountNumber=payload.payment.account_number
            if has_payment_config
            else None,
            ShippingPaymentType=PaymentType[payload.payment.paid_by].value
            if has_payment_config
            else None,
            DutyAccountNumber=payload.customs.duty.account_number
            if has_customs_config
            else None,
            DutyPaymentType=PaymentType[payload.customs.duty.paid_by].value
            if has_customs_config
            else None,
        ),
        Consignee=Consignee(
            CompanyName=payload.recipient.company_name or "  ",
            SuiteDepartmentName=None,
            AddressLine=SF.concat_str(
                payload.recipient.address_line1, payload.recipient.address_line2
            ),
            City=payload.recipient.city,
            Division=None,
            DivisionCode=payload.recipient.state_code,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            CountryName=Country[payload.recipient.country_code].value,
            FederalTaxId=payload.shipper.federal_tax_id,
            StateTaxId=payload.shipper.state_tax_id,
            Contact=(
                Contact(
                    PersonName=payload.recipient.person_name,
                    PhoneNumber=payload.recipient.phone_number or "0000",
                    Email=payload.recipient.email,
                )
            ),
            Suburb=None,
        ),
        Commodity=[
            Commodity(CommodityCode=c.sku, CommodityName=c.description)
            for c in payload.customs.commodities
        ]
        if payload.customs is not None
        else None,
        NewShipper=None,
        Shipper=Shipper(
            ShipperID=settings.account_number or "  ",
            RegisteredAccount=settings.account_number,
            AddressLine=SF.concat_str(
                payload.shipper.address_line1, payload.shipper.address_line2
            ),
            CompanyName=payload.shipper.company_name or "  ",
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=Country[payload.shipper.country_code].value,
            Division=None,
            DivisionCode=payload.shipper.state_code,
            Contact=(
                Contact(
                    PersonName=payload.shipper.person_name,
                    PhoneNumber=payload.shipper.phone_number or "0000",
                    Email=payload.shipper.email,
                )
            ),
        ),
        ShipmentDetails=DHLShipmentDetails(
            NumberOfPieces=len(packages),
            Pieces=Pieces(
                Piece=[
                    Piece(
                        PieceID=payload.parcels[index].id,
                        PackageType=(
                            package_type
                            or PackageType[
                                package.packaging_type or "your_packaging"
                            ].value
                        ),
                        Depth=package.length.IN,
                        Width=package.width.IN,
                        Height=package.height.IN,
                        Weight=package.weight.LB,
                        DimWeight=None,
                        PieceContents=payload.parcels[index].description,
                    )
                    for index, package in enumerate(packages)
                ]
            ),
            Weight=packages.weight.LB,
            CurrencyCode=options.currency or "USD",
            WeightUnit=WeightUnit.L.value,
            DimensionUnit=DimensionUnit.I.value,
            Date=(options.shipment_date or time.strftime("%Y-%m-%d")),
            PackageType=package_type,
            IsDutiable=("Y" if payload.customs is not None else "N"),
            InsuredAmount=options.insurance,
            ShipmentCharges=(options.cash_on_delivery if options.cash_on_delivery else None),
            DoorTo=delivery_type,
            GlobalProductCode=product,
            LocalProductCode=product,
            Contents="  ",
        ),
        EProcShip=None,
        Dutiable=Dutiable(
            DeclaredCurrency=payload.customs.duty.currency or "USD",
            DeclaredValue=payload.customs.duty.amount,
            TermsOfTrade=payload.customs.incoterm,
        )
        if payload.customs is not None and payload.customs.duty is not None
        else None,
        ExportDeclaration=None,
        Reference=[Reference(ReferenceID=payload.reference)],
        SpecialService=[
            SpecialService(SpecialServiceType=service) for service in special_services
        ],
        Notification=(
            Notification(EmailAddress=options.notification_email or payload.recipient.email)
            if options.notification_email is None else None
        ),
        DocImages=None,
        RequestArchiveDoc=None,
        NumberOfArchiveDoc=None,
        LabelImageFormat=label_format,
        Label=Label(LabelTemplate=label_template),
        ODDLinkReq=None,
        DGs=None,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: DHLShipmentRequest) -> str:
    xml_str = (
        XP.export(
            request,
            name_="req:ShipmentRequest",
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd"',
        )
        .replace("<Image>b'", "<Image>")
        .replace("'</Image>", "</Image>")
    )
    return xml_str
