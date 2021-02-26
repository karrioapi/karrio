import time
from base64 import encodebytes
from typing import List, Tuple, Optional
from dhl_express_lib.ship_val_global_req_6_2 import (
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
    Label
)
from dhl_express_lib.ship_val_global_res_6_2 import LabelImage
from purplship.core.utils import Serializable, SF, XP
from purplship.core.utils.xml import Element
from purplship.core.models import (
    ShipmentRequest,
    Message,
    ShipmentDetails,
    Payment,
    Customs,
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
    tracking_number = shipment_node.xpath(".//*[local-name() = $name]", name="AirwayBillNumber")[0].text
    label_node = shipment_node.xpath(".//*[local-name() = $name]", name="LabelImage")[0]
    label = encodebytes(XP.build(LabelImage, label_node).OutputImage).decode("utf-8")

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label=label,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[DHLShipmentRequest]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    options = Options(payload.options, SpecialServiceCode)
    product = next(
        (p.value for p in ProductCode if payload.service == p.name),
        payload.service
    )

    insurance = options['dhl_shipment_insurance'].value if 'dhl_shipment_insurance' in options else None
    package_type = (
        PackageType[packages[0].packaging_type or "your_packaging"].value
        if len(packages) == 1 else None
    )
    delivery_type = next(
        (d for d in DeliveryType if d.name in payload.options.keys()), None
    )
    label_format, label_template = LabelType[payload.label_type or 'PDF_6x4'].value
    payment = (payload.payment or Payment(paid_by="sender", account_number=settings.account_number))
    customs = (payload.customs or Customs())
    content = (packages[0].parcel.content or "N/A")

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
            BillingAccountNumber=payment.account_number,
            ShippingPaymentType=PaymentType[payment.paid_by].value,
            DutyAccountNumber=(customs.duty.account_number if customs.duty is not None else None),
            DutyPaymentType=(PaymentType[customs.duty.paid_by].value if customs.duty is not None else None),
        ),
        Consignee=Consignee(
            CompanyName=payload.recipient.company_name or "N/A",
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
        Commodity=(
            [
                Commodity(CommodityCode=c.sku, CommodityName=c.description)
                for c in payload.customs.commodities
            ]
            if any(customs.commodities) else None
        ),
        NewShipper=None,
        Shipper=Shipper(
            ShipperID=settings.account_number or "N/A",
            RegisteredAccount=settings.account_number,
            AddressLine=SF.concat_str(
                payload.shipper.address_line1, payload.shipper.address_line2
            ),
            CompanyName=payload.shipper.company_name or "N/A",
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
                        PieceID=package.parcel.id,
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
                        PieceContents=(
                            package.parcel.content or package.parcel.description
                        ),
                    )
                    for package in packages
                ]
            ),
            Weight=packages.weight.LB,
            CurrencyCode=options.currency or "USD",
            WeightUnit=WeightUnit.L.value,
            DimensionUnit=DimensionUnit.I.value,
            Date=(options.shipment_date or time.strftime("%Y-%m-%d")),
            PackageType=package_type,
            IsDutiable=("Y" if payload.customs is not None else "N"),
            InsuredAmount=insurance,
            ShipmentCharges=(options.cash_on_delivery if options.cash_on_delivery else None),
            DoorTo=delivery_type,
            GlobalProductCode=product,
            LocalProductCode=product,
            Contents=content,
        ),
        EProcShip=None,
        Dutiable=(
            Dutiable(
                DeclaredCurrency=customs.duty.currency or "USD",
                DeclaredValue=insurance or 1.0,
                TermsOfTrade=customs.incoterm,
            )
            if customs.duty is not None else None
        ),
        ExportDeclaration=None,
        Reference=[Reference(ReferenceID=payload.reference)],
        SpecialService=[
            SpecialService(SpecialServiceType=SpecialServiceCode[key].value.key)
            for key, svc in options if key in SpecialServiceCode
        ],
        Notification=(
            Notification(
                EmailAddress=options.notification_email or payload.recipient.email
            )
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
