import time
from base64 import b64decode
from functools import reduce
from typing import List, Tuple, Optional
from pydhl.ship_val_global_req_6_2 import (
    ShipmentRequest as DHLShipmentRequest, Billing, Consignee, Contact, Commodity,
    Shipper, ShipmentDetails as DHLShipmentDetails, Pieces, Piece, Reference,
    SpecialService, DocImage, DocImages, Dutiable, MetaData
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import (
    ShipmentRequest, Error, ShipmentDetails, ReferenceDetails, ChargeDetails
)
from purplship.carriers.dhl.units import PackageType, Service, Product, PayorType, Dimension, WeightUnit, CountryRegion
from purplship.carriers.dhl.utils import Settings
from purplship.carriers.dhl.error import parse_error_response


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    return _extract_shipment(response, settings), parse_error_response(response, settings)


def _extract_shipment(shipment_response_node, settings: Settings) -> Optional[ShipmentDetails]:
    """
        Shipment extraction is implemented using lxml queries instead of generated ShipmentResponse type
        because the type construction fail during validation out of our control
    """
    def get_value(query):
        return query[0].text if len(query) > 0 else None

    def get(key: str):
        return get_value(shipment_response_node.xpath("//%s" % key))

    tracking_number = get("AirwayBillNumber")
    if not tracking_number:
        return None

    plates = [p.text for p in shipment_response_node.xpath("//LicensePlateBarCode")]
    barcodes = [child.text for child in shipment_response_node.xpath("//Barcodes")[0].getchildren()]
    documents: List[str] = reduce(
        lambda r, i: (r + [i] if i else r), [get("AWBBarCode")] + plates + barcodes, []
    )
    reference = (
        ReferenceDetails(value=get("ReferenceID"), type=get("ReferenceType"))
        if len(shipment_response_node.xpath("//Reference")) > 0 else None
    )
    currency_ = get("CurrencyCode")

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=[tracking_number],
        shipment_date=get("ShipmentDate"),
        services=(
            [get("ProductShortName")] +
            [service.text for service in shipment_response_node.xpath("//SpecialServiceDesc")] +
            [service.text for service in shipment_response_node.xpath("//InternalServiceCode")]
        ),
        charges=[
            ChargeDetails(name="PackageCharge", amount=float(get("PackageCharge")), currency=currency_)
        ],
        documents=documents,
        reference=reference,
        total_charge=ChargeDetails(name="Shipment charge", amount=get("ShippingCharge"), currency=currency_),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[DHLShipmentRequest]:
    is_dutiable = payload.shipment.declared_value is not None
    default_product_code = (
        Product.EXPRESS_WORLDWIDE_DOC if payload.shipment.is_document else Product.EXPRESS_WORLDWIDE
    )
    product = (
        [Product[svc] for svc in payload.shipment.services if svc in Product.__members__] + [default_product_code]
    )[0]
    default_packaging_type = (
        PackageType.Document if payload.shipment.is_document else PackageType.Your_packaging
    )
    options = dict(
        [(code, value) for code, value in payload.shipment.options.items() if code in Service.__members__] +
        ([] if not payload.shipment.insured_amount else [(Service.Shipment_Insurance.value, payload.shipment.insured_amount)])
    )

    request = DHLShipmentRequest(
        schemaVersion="6.1",
        Request=settings.Request(MetaData=MetaData(SoftwareName="3PV", SoftwareVersion="1.0")),
        RegionCode=CountryRegion[payload.shipper.country_code],
        RequestedPickupTime="Y",
        LanguageCode="en",
        PiecesEnabled="Y",
        LatinResponseInd=None,
        Billing=Billing(
            ShipperAccountNumber=payload.shipper.account_number,
            BillingAccountNumber=payload.shipment.payment_account_number,
            ShippingPaymentType=(
                PayorType[payload.shipment.paid_by].value if payload.shipment.paid_by is not None else None
            ),
            DutyAccountNumber=payload.shipment.duty_payment_account,
            DutyPaymentType=(
                PayorType[payload.shipment.duty_paid_by].value if payload.shipment.duty_paid_by is not None else None
            ),
        ),
        Consignee=Consignee(
            CompanyName=payload.recipient.company_name,
            SuiteDepartmentName=None,
            AddressLine=payload.recipient.address_lines,
            City=payload.recipient.city,
            Division=payload.recipient.state,
            DivisionCode=payload.recipient.state_code,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            CountryName=None,
            FederalTaxId=payload.shipper.tax_id,
            StateTaxId=None,
            Contact=(
                Contact(
                    PersonName=payload.recipient.person_name,
                    PhoneNumber=payload.recipient.phone_number,
                    Email=payload.recipient.email_address,
                    FaxNumber=None,
                    Telex=None,
                    PhoneExtension=None,
                    MobilePhoneNumber=None,
                )
                if any(
                    [payload.recipient.person_name, payload.recipient.phone_number, payload.recipient.email_address]
                ) else None
            ),
            Suburb=None,
        ),
        Commodity=[
            Commodity(CommodityCode=c.code, CommodityName=c.description) for c in payload.shipment.items
        ],
        NewShipper=None,
        Shipper=Shipper(
            ShipperID=payload.shipper.account_number,
            RegisteredAccount=payload.shipper.account_number,
            AddressLine=payload.shipper.address_lines,
            CompanyName=payload.shipper.company_name,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=None,
            Division=payload.shipper.state,
            DivisionCode=payload.shipper.state_code,
            Contact=(
                Contact(
                    PersonName=payload.shipper.person_name,
                    PhoneNumber=payload.shipper.phone_number,
                    Email=payload.shipper.email_address,
                    FaxNumber=None,
                    Telex=None,
                    PhoneExtension=None,
                    MobilePhoneNumber=None,
                )
                if any(
                    [payload.shipper.person_name, payload.shipper.phone_number, payload.shipper.email_address,]
                ) else None
            ),
        ),
        ShipmentDetails=DHLShipmentDetails(
            NumberOfPieces=len(payload.shipment.items),
            Pieces=Pieces(
                Piece=[
                    Piece(
                        PieceID=p.id,
                        PackageType=(
                            PackageType[p.packaging_type] if p.packaging_type is not None else default_packaging_type
                        ).value,
                        Weight=p.weight,
                        DimWeight=None,
                        Height=p.height,
                        Width=p.width,
                        Depth=p.length,
                        PieceContents=p.content,
                    )
                    for p in payload.shipment.items
                ]
            ),
            Weight=(
                payload.shipment.total_weight or sum(p.weight for p in payload.shipment.items)
            ),
            CurrencyCode=payload.shipment.currency or "USD",
            WeightUnit=WeightUnit[payload.shipment.weight_unit or "KG"].value,
            DimensionUnit=Dimension[payload.shipment.dimension_unit or "CM"].value,
            Date=payload.shipment.date or time.strftime("%Y-%m-%d"),
            PackageType=(
                PackageType[payload.shipment.packaging_type].value
                if payload.shipment.packaging_type is not None else None
            ),
            IsDutiable="Y" if is_dutiable else "N",
            InsuredAmount=payload.shipment.insured_amount,
            DoorTo=payload.options.get("DoorTo"),
            GlobalProductCode=product.value,
            LocalProductCode=product.value,
            Contents="...",
        ),
        EProcShip=None,
        Dutiable=Dutiable(
            DeclaredCurrency=payload.shipment.currency or "USD",
            DeclaredValue=payload.shipment.declared_value,
            TermsOfTrade=payload.shipment.customs.terms_of_trade,
            ScheduleB=None,
            ExportLicense=None,
            ShipperEIN=None,
            ShipperIDType=None,
            ImportLicense=None,
            ConsigneeEIN=None,
        )
        if is_dutiable
        else None,
        ExportDeclaration=None,
        Reference=[
            Reference(ReferenceID=r) for r in payload.shipment.references
        ],
        SpecialService=(
            [
                SpecialService(
                    SpecialServiceType=Service[code].value,
                    CommunicationAddress=None,
                    CommunicationType=None,
                    ChargeValue=value,
                    CurrencyCode=payload.shipment.currency,
                    IsWaived=None,
                )
                for code, value in options.items()
            ] if len(options) > 0 else None
        ),
        LabelImageFormat=(
            payload.shipment.label.format if payload.shipment.label is None else None
        ),
        DocImages=(
            DocImages(
                DocImage=[
                    DocImage(
                        Type=doc.type,
                        ImageFormat=doc.format,
                        Image=b64decode(doc.image + "=" * (-len(doc.image) % 4)),
                    )
                    for doc in payload.shipment.doc_images
                ]
            )
            if len(payload.shipment.doc_images) > 0 else None
        ),
        RequestArchiveDoc=None,
        NumberOfArchiveDoc=None,
        Label=None,
        ODDLinkReq=None,
        DGs=None,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: DHLShipmentRequest) -> str:
    xml_str = (
        export(
            request,
            name_="req:ShipmentRequest",
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" schemaVersion="6.1"',
        )
        .replace("<Image>b'", "<Image>")
        .replace("'</Image>", "</Image>")
    )
    return xml_str
