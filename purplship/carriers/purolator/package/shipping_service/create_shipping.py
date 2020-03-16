from typing import List, Tuple, cast, Union, Type, Dict
from datetime import datetime
from pysoap.envelope import Envelope
from pypurolator.shipping_service import (
    CreateShipmentRequest, Shipment, SenderInformation, ReceiverInformation, PackageInformation,
    TrackingReferenceInformation, Address, InternationalInformation, PickupInformation, PickupType,
    ArrayOfPiece, Piece, Weight as PurolatorWeight, WeightUnit as PurolatorWeightUnit, RequestContext,
    Dimension as PurolatorDimension, DimensionUnit as PurolatorDimensionUnit, TotalWeight, PhoneNumber,
    PrinterType as PurolatorPrinterType, CreateShipmentResponse, PIN, ValidateShipmentRequest, ResponseInformation,
    Error as PurolatorError, ArrayOfError
)
from purplship.core.models import ShipmentRequest, ShipmentDetails, Error
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, PrinterType
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.soap import create_envelope
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.units import Product
from purplship.carriers.purolator.error import parse_error_response

ShipmentRequestType = Type[Union[ValidateShipmentRequest, CreateShipmentRequest]]


def parse_shipment_creation_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    details = response.xpath(".//*[local-name() = $name]", name="CreateShipmentResponse")
    shipment = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(node: Element, settings: Settings) -> ShipmentDetails:
    shipment = CreateShipmentResponse()
    shipment.build(node)
    return ShipmentDetails(
        carrier=settings.carrier_name,
        service=None,
        tracking_number=cast(PIN, shipment.ShipmentPIN).Value,
        total_charge=None,
        charges=[],
        shipment_date=str(datetime.today().strftime("%Y-%m-%d")),
        documents=[],
        reference=None
    )


def create_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Dict[str, Envelope]]:
    requests = dict(
        validate=_shipment_request(payload, settings, validate=True),
        create=_shipment_request(payload, settings),
        error=_validation_error(settings)
    )
    return Serializable(requests, _request_serializer)


def _shipment_request(payload: ShipmentRequest, settings: Settings, validate: bool = False) -> Envelope:
    RequestType: ShipmentRequestType = ValidateShipmentRequest if validate else CreateShipmentRequest
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    dimension_unit: DimensionUnit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    service = next((svc for svc in payload.parcel.services if svc in Product.__members__), None)
    is_international = payload.shipper.country_code != payload.recipient.country_code
    printing = PrinterType[payload.parcel.options.get('printing', "regular")]
    request = create_envelope(
        header_content=RequestContext(
            Version='2.1',
            Language=settings.language,
            GroupID=None,
            RequestReference=None,
            UserToken=settings.user_token
        ),
        body_content=RequestType(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=payload.shipper.person_name,
                        Company=payload.shipper.company_name,
                        Department=None,
                        StreetNumber=None,
                        StreetSuffix=None,
                        StreetName=concat_str(payload.shipper.address_line_1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=concat_str(payload.shipper.address_line_2, join=True),
                        StreetAddress3=None,
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
                        StreetName=concat_str(payload.recipient.address_line_1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=concat_str(payload.recipient.address_line_2, join=True),
                        StreetAddress3=None,
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
                    ServiceID=Product[service or "purolator_express"].value,
                    Description=payload.parcel.description,
                    TotalWeight=TotalWeight(
                        Value=Weight(payload.parcel.weight, weight_unit).value,
                        WeightUnit=PurolatorWeightUnit[weight_unit.value].value
                    ) if payload.parcel.weight else None,
                    TotalPieces=1,
                    PiecesInformation=ArrayOfPiece(
                        Piece=[
                            Piece(
                                Weight=PurolatorWeight(
                                    Value=Weight(payload.parcel.weight, weight_unit).value,
                                    WeightUnit=PurolatorWeightUnit[weight_unit.value].value
                                ) if payload.parcel.weight else None,
                                Length=PurolatorDimension(
                                    Value=Dimension(payload.parcel.length, dimension_unit).value,
                                    DimensionUnit=PurolatorDimensionUnit[dimension_unit.value].value
                                ) if payload.parcel.length else None,
                                Width=PurolatorDimension(
                                    Value=Dimension(payload.parcel.width, dimension_unit).value,
                                    DimensionUnit=PurolatorDimensionUnit[dimension_unit.value].value
                                ) if payload.parcel.width else None,
                                Height=PurolatorDimension(
                                    Value=Dimension(payload.parcel.height, dimension_unit).value,
                                    DimensionUnit=PurolatorDimensionUnit[dimension_unit.value].value
                                ) if payload.parcel.height else None,
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
                ) if is_international else None,
                ReturnShipmentInformation=None,
                PaymentInformation=None,
                PickupInformation=PickupInformation(PickupType=PickupType.DROP_OFF.value),
                NotificationInformation=None,
                TrackingReferenceInformation=TrackingReferenceInformation(
                    Reference1=payload.parcel.reference
                ),
                OtherInformation=None,
                ProactiveNotification=None
            ),
            PrinterType=PurolatorPrinterType(printing.value).value
        )
    )
    return request


def _request_serializer(requests: Dict[str, Envelope]) -> Dict[str, str]:
    namespacedef_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'

    def serialize(envelope):
        envelope.ns_prefix_ = "SOAP-ENV"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_
        envelope.Body.anytypeobjs_[0].ns_prefix_ = "ns1"
        envelope.Header.anytypeobjs_[0].ns_prefix_ = "ns1"
        return export(envelope, namespacedef_=namespacedef_)

    return {request: serialize(envelope) for request, envelope in requests.items()}


def _validation_error(settings: Settings):
    return create_envelope(
        header_content=RequestContext(
            Version='2.1',
            Language=settings.language,
            GroupID=None,
            RequestReference=None,
            UserToken=settings.user_token
        ),
        body_content=ResponseInformation(
            Errors=ArrayOfError(
                Error=[
                    PurolatorError(
                        Description="Invalid Shipment Request",
                        Code='000000'
                    )
                ]
            )
        )
    )
