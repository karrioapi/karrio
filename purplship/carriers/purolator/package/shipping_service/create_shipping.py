from typing import List, Tuple, cast
from datetime import datetime
from pysoap.envelope import Envelope, Header, Body
from pypurolator.shipping_service import (
    CreateShipmentRequestContainer, Shipment, SenderInformation, ReceiverInformation, PackageInformation,
    TrackingReferenceInformation, Address, InternationalInformation, PickupInformation, PickupType,
    ArrayOfPiece, Piece, Weight as PurolatorWeight, WeightUnit as PurolatorWeightUnit, RequestContext,
    Dimension as PurolatorDimension, DimensionUnit as PurolatorDimensionUnit, TotalWeight, PhoneNumber,
    PrinterType, CreateShipmentResponseContainer, PIN
)
from purplship.core.models import ShipmentRequest, ShipmentDetails, Error
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.units import Product
from purplship.carriers.purolator.error import parse_error_response


def parse_shipment_creation_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    return (
        _extract_shipment(response, settings),
        parse_error_response(response, settings)
    )


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipment = CreateShipmentResponseContainer()
    shipment.build(node)
    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=(
            [cast(PIN, pin).Value for pin in shipment.PiecePINs] +
            [cast(PIN, pin).Value for pin in shipment.ReturnShipmentPINs]
        ),
        total_charge=None,
        charges=[],
        shipment_date=str(datetime.today().strftime("%Y-%m-%d")),
        services=None,
        documents=[],
        reference=None
    )


def create_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Element]:
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    dimension_unit: DimensionUnit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    service = next((svc for svc in payload.parcel.services if svc in Product.__members__), None)
    printer_type: PrinterType = PrinterType[payload.parcel.options.get('printing', "REGULAR")]
    request = Envelope(
        Header=Header(
            RequestContext(
                Version='2.1',
                Language=settings.language,
                GroupID=None,
                RequestReference=None,
                UserToken=settings.user_token
            )
        ),
        Body=Body(
            CreateShipmentRequestContainer(
                Shipment=Shipment(
                    SenderInformation=SenderInformation(
                        Address=Address(
                            Name=payload.shipper.person_name,
                            Company=payload.shipper.company_name,
                            Department=None,
                            StreetNumber=None,
                            StreetSuffix=None,
                            StreetName=None,
                            StreetType=None,
                            StreetDirection=None,
                            Suite=None,
                            Floor=None,
                            StreetAddress2=payload.shipper.address_line_1,
                            StreetAddress3=payload.shipper.address_line_2,
                            City=payload.shipper.city,
                            Province=payload.shipper.state_code,
                            Country=payload.shipper.country_code,
                            PostalCode=payload.shipper.postal_code,
                            PhoneNumber=PhoneNumber(Phone=payload.shipper.phone_number),
                            FaxNumber=None
                        ),
                        TaxNumber=payload.shipper.federal_tax_id or payload.shipper.state_tax_id
                    ),
                    ReceiverInformation=ReceiverInformation(
                        Address=Address(
                            Name=payload.recipient.person_name,
                            Company=payload.recipient.company_name,
                            Department=None,
                            StreetNumber=None,
                            StreetSuffix=None,
                            StreetName=None,
                            StreetType=None,
                            StreetDirection=None,
                            Suite=None,
                            Floor=None,
                            StreetAddress2=payload.recipient.address_line_1,
                            StreetAddress3=payload.recipient.address_line_2,
                            City=payload.recipient.city,
                            Province=payload.recipient.state_code,
                            Country=payload.recipient.country_code,
                            PostalCode=payload.recipient.postal_code,
                            PhoneNumber=PhoneNumber(Phone=payload.recipient.phone_number),
                            FaxNumber=None
                        ),
                        TaxNumber=payload.recipient.federal_tax_id or payload.recipient.state_tax_id
                    ),
                    FromOnLabelIndicator=None,
                    FromOnLabelInformation=None,
                    ShipmentDate=datetime.today().strftime("%Y-%m-%d"),
                    PackageInformation=PackageInformation(
                        ServiceID=Product[service].value if service is not None else None,
                        Description=payload.parcel.description,
                        TotalWeight=TotalWeight(
                            Value=Weight(payload.parcel.weight, weight_unit).value,
                            WeightUnit=PurolatorWeightUnit[weight_unit.value]
                        ),
                        TotalPieces=1,
                        PiecesInformation=ArrayOfPiece(
                            Piece=[
                                Piece(
                                    Weight=PurolatorWeight(
                                        Value=Weight(payload.parcel.weight, weight_unit).value,
                                        WeightUnit=PurolatorWeightUnit[weight_unit.value]
                                    ),
                                    Length=PurolatorDimension(
                                        Value=Dimension(payload.parcel.length, dimension_unit).value,
                                        DimensionUnit=PurolatorDimensionUnit[dimension_unit.value]
                                    ),
                                    Width=PurolatorDimension(
                                        Value=Dimension(payload.parcel.width, dimension_unit).value,
                                        DimensionUnit=PurolatorDimensionUnit[dimension_unit.value]
                                    ),
                                    Height=PurolatorDimension(
                                        Value=Dimension(payload.parcel.height, dimension_unit).value,
                                        DimensionUnit=PurolatorDimensionUnit[dimension_unit.value]
                                    ),
                                    Options=None
                                )
                            ]
                        ),
                        DangerousGoodsDeclarationDocumentIndicator=None,
                        OptionsInformation=None
                    ),
                    InternationalInformation=InternationalInformation(
                        DocumentsOnlyIndicator=payload.parcel.is_document,
                        ContentDetails=payload.parcel.description,
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=None,
                        ImportExportType=None,
                        CustomsInvoiceDocumentIndicator=None
                    ),
                    ReturnShipmentInformation=None,
                    PaymentInformation=None,
                    PickupInformation=PickupInformation(PickupType=PickupType.DROP_OFF),
                    NotificationInformation=None,
                    TrackingReferenceInformation=TrackingReferenceInformation(
                        Reference1=payload.parcel.reference
                    ),
                    OtherInformation=None,
                    ProactiveNotification=None
                ),
                PrinterType=printer_type
            )
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: Element) -> str:
    namespace_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    return export(request, namespacedef_=namespace_)
