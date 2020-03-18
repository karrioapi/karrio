import time
from base64 import b64decode
from functools import reduce
from typing import List, Tuple, Optional
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
    DocImage,
    DocImages,
    Dutiable,
    MetaData,
    Notification,
    SpecialService
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import (
    ShipmentRequest,
    Error,
    ShipmentDetails,
    ReferenceDetails,
    ChargeDetails,
    Option,
)
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit
from purplship.carriers.dhl.units import (
    PackageType,
    ProductCode,
    PayorType,
    Dimension as DHLDimensionUnit,
    WeightUnit as DHLWeightUnit,
    CountryRegion,
    ServiceCode
)
from purplship.carriers.dhl.utils import Settings
from purplship.carriers.dhl.error import parse_error_response


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Error]]:
    return (
        _extract_shipment(response, settings),
        parse_error_response(response, settings),
    )


def _extract_shipment(
    shipment_response_node, settings: Settings
) -> Optional[ShipmentDetails]:
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
    barcodes = [
        child.text
        for child in shipment_response_node.xpath("//Barcodes")[0].getchildren()
    ]
    documents: List[str] = reduce(
        lambda r, i: (r + [i] if i else r), [get("AWBBarCode")] + plates + barcodes, []
    )
    reference = (
        ReferenceDetails(value=get("ReferenceID"), type=get("ReferenceType"))
        if len(shipment_response_node.xpath("//Reference")) > 0
        else None
    )
    currency_ = get("CurrencyCode")
    service = next(
        (p.name for p in ProductCode if p.value == get("ProductShortName")),
        get("ProductShortName")
    )

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_date=get("ShipmentDate"),
        service=service,
        charges=[
            ChargeDetails(
                name="PackageCharge",
                amount=float(get("PackageCharge")),
                currency=currency_,
            )
        ],
        documents=documents,
        reference=reference,
        total_charge=ChargeDetails(
            name="Shipment charge", amount=get("ShippingCharge"), currency=currency_
        ),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[DHLShipmentRequest]:
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    default_product_code = (
        ProductCode.express_worldwide_doc
        if payload.parcel.is_document
        else ProductCode.express_worldwide_nondoc
    )
    product = next(
        (ProductCode[svc] for svc in payload.parcel.services if svc in ProductCode.__members__),
        default_product_code
    )
    options: dict = {}
    requested_options = []
    for name, value in payload.parcel.options.items():
        if name in Option.__members__:
            options.update({
                name: (
                    Option[name].value(**value) if isinstance(value, dict) else Option[name].value(value)
                )
            })
        if name in ServiceCode.__members__:
            requested_options.append(ServiceCode[name].value)

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
            BillingAccountNumber=payload.payment.account_number,
            ShippingPaymentType=(
                PayorType[payload.payment.paid_by].value
                if payload.payment.paid_by is not None
                else None
            )
            if payload.payment is not None
            else None,
            DutyAccountNumber=payload.customs.duty.account_number,
            DutyPaymentType=(
                PayorType[payload.customs.duty.paid_by].value
                if payload.customs.duty.paid_by is not None
                else None
            )
            if all([payload.customs, payload.customs.duty])
            else None,
        ),
        Consignee=Consignee(
            CompanyName=payload.recipient.company_name,
            SuiteDepartmentName=None,
            AddressLine=concat_str(payload.recipient.address_line_1, payload.recipient.address_line_2),
            City=payload.recipient.city,
            Division=None,
            DivisionCode=payload.recipient.state_code,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            CountryName=None,
            FederalTaxId=payload.shipper.federal_tax_id,
            StateTaxId=payload.shipper.state_tax_id,
            Contact=(
                Contact(
                    PersonName=payload.recipient.person_name,
                    PhoneNumber=payload.recipient.phone_number,
                    Email=payload.recipient.email,
                    FaxNumber=None,
                    Telex=None,
                    PhoneExtension=None,
                    MobilePhoneNumber=None,
                )
                if any(
                    [
                        payload.recipient.person_name,
                        payload.recipient.phone_number,
                        payload.recipient.email,
                    ]
                )
                else None
            ),
            Suburb=None,
        ),
        Commodity=[
            Commodity(CommodityCode=c.sku, CommodityName=c.description)
            for c in payload.customs.commodities
        ],
        NewShipper=None,
        Shipper=Shipper(
            ShipperID=None,
            RegisteredAccount=settings.account_number,
            AddressLine=concat_str(payload.shipper.address_line_1, payload.shipper.address_line_2),
            CompanyName=payload.shipper.company_name,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=None,
            Division=None,
            DivisionCode=payload.shipper.state_code,
            Contact=(
                Contact(
                    PersonName=payload.shipper.person_name,
                    PhoneNumber=payload.shipper.phone_number,
                    Email=payload.shipper.email,
                    FaxNumber=None,
                    Telex=None,
                    PhoneExtension=None,
                    MobilePhoneNumber=None,
                )
                if any(
                    [
                        payload.shipper.person_name,
                        payload.shipper.phone_number,
                        payload.shipper.email,
                    ]
                )
                else None
            ),
        ),
        ShipmentDetails=DHLShipmentDetails(
            NumberOfPieces=None,
            Pieces=Pieces(
                Piece=[
                    Piece(
                        PieceID=payload.parcel.id,
                        PackageType=PackageType[
                            payload.parcel.packaging_type or "box"
                        ].value,
                        Depth=Dimension(payload.parcel.length, dimension_unit).value,
                        Width=Dimension(payload.parcel.width, dimension_unit).value,
                        Height=Dimension(payload.parcel.height, dimension_unit).value,
                        Weight=Weight(payload.parcel.weight, weight_unit).value,
                        DimWeight=None,
                        PieceContents=payload.parcel.description,
                    )
                ]
            ),
            Weight=Weight(payload.parcel.weight, weight_unit).value,
            CurrencyCode=options.get("currency", "USD"),
            WeightUnit=DHLWeightUnit[weight_unit.name].value,
            DimensionUnit=DHLDimensionUnit[dimension_unit.name].value,
            Date=time.strftime("%Y-%m-%d"),
            PackageType=PackageType[payload.parcel.packaging_type or "box"].value,
            IsDutiable="Y" if payload.customs is not None else "N",
            InsuredAmount=None,
            DoorTo=options.get("DoorTo"),
            GlobalProductCode=product.value,
            LocalProductCode=product.value,
            Contents="...",
        ),
        EProcShip=None,
        Dutiable=Dutiable(
            DeclaredCurrency=payload.customs.duty.currency or "USD",
            DeclaredValue=payload.customs.duty.amount,
            TermsOfTrade=payload.customs.terms_of_trade,
            ScheduleB=None,
            ExportLicense=None,
            ShipperEIN=None,
            ShipperIDType=None,
            ImportLicense=None,
            ConsigneeEIN=None,
        )
        if payload.customs is not None and payload.customs.duty is not None
        else None,
        ExportDeclaration=None,
        Reference=[Reference(ReferenceID=payload.parcel.reference)],
        SpecialService=[
            SpecialService(
                SpecialServiceType=service,
                SpecialServiceDesc=None,
                CommunicationAddress=None,
                CommunicationType=None,
                ChargeValue=None,
                CurrencyCode=None,
                IsWaived=None
            )
            for service in requested_options
        ],
        Notification=Notification(
            EmailAddress=options['notification'].email or payload.shipper.email,
            Message=None
        ) if 'notification' in options else None,
        LabelImageFormat=(payload.label.format if payload.label is not None else None),
        DocImages=DocImages(
            DocImage=[
                DocImage(
                    Type=doc.type,
                    ImageFormat=doc.format,
                    Image=b64decode(doc.image + "=" * (-len(doc.image) % 4)),
                )
                for doc in payload.doc_images
            ]
        )
        if len(payload.doc_images) > 0
        else None,
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
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd"',
        )
        .replace("<Image>b'", "<Image>")
        .replace("'</Image>", "</Image>")
    )
    return xml_str
