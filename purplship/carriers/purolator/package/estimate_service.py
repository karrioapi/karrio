from typing import List, Tuple, cast
from datetime import datetime
from pysoap.envelope import Envelope
from pypurolator.estimate_service import (
    GetFullEstimateRequest, Shipment, SenderInformation, Address, ReceiverInformation,
    PackageInformation, TrackingReferenceInformation, PickupInformation,
    ArrayOfPiece, Piece, Weight as PurolatorWeight, WeightUnit as PurolatorWeightUnit, RequestContext,
    Dimension as PurolatorDimension, DimensionUnit as PurolatorDimensionUnit, TotalWeight,
    ShipmentEstimate, Tax, Surcharge, OptionPrice, PickupType, PhoneNumber
)
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Currency
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.soap import create_envelope
from purplship.core.models import RateRequest, RateDetails, Error, ChargeDetails
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.error import parse_error_response
from purplship.carriers.purolator.units import Product


def parse_full_estimate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    estimates = response.xpath(".//*[local-name() = $name]", name="ShipmentEstimate")
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings)
    )


def _extract_rate(estimate_node: Element, settings: Settings) -> RateDetails:
    estimate = ShipmentEstimate()
    estimate.build(estimate_node)
    currency = Currency.CAD.name
    duties_and_taxes = [
        ChargeDetails(
            name=cast(Tax, tax).Description,
            amount=float(cast(Tax, tax).Amount),
            currency=currency
        ) for tax in estimate.Taxes.Tax
    ]
    surcharges = [
        ChargeDetails(
            name=cast(Surcharge, charge).Description,
            amount=float(cast(Surcharge, charge).Amount),
            currency=currency
        ) for charge in estimate.Surcharges.Surcharge
    ]
    option_charges = [
        ChargeDetails(
            name=cast(OptionPrice, charge).Description,
            amount=float(cast(OptionPrice, charge).Amount),
            currency=currency
        ) for charge in estimate.OptionPrices.OptionPrice
    ]
    service = next((p.name for p in Product if p.value in estimate.ServiceID), estimate.ServiceID)
    return RateDetails(
        carrier=settings.carrier_name,
        service_name=service,
        currency=currency,
        base_charge=float(estimate.BasePrice),
        delivery_date=str(estimate.ExpectedDeliveryDate),
        total_charge=float(estimate.TotalPrice),
        duties_and_taxes=sum(c.amount for c in duties_and_taxes),
        extra_charges=(duties_and_taxes + surcharges + option_charges)
    )


def get_full_estimate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    weight_unit: WeightUnit = WeightUnit[payload.parcel.weight_unit or "LB"]
    dimension_unit: DimensionUnit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    service = next((svc for svc in payload.parcel.services if svc in Product.__members__), None)
    request = create_envelope(
        envelope_prefix="SOAP-ENV",
        header_prefix="ns1",
        header_content=RequestContext(
            Version='2.1',
            Language=settings.language,
            GroupID=None,
            RequestReference=None,
            UserToken=settings.user_token
        ),
        body_prefix="ns1",
        body_content=GetFullEstimateRequest(
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
                InternationalInformation=None,
                ReturnShipmentInformation=None,
                PaymentInformation=None,
                PickupInformation=PickupInformation(PickupType=PickupType.DROP_OFF.value),
                NotificationInformation=None,
                TrackingReferenceInformation=TrackingReferenceInformation(
                    Reference1=payload.parcel.reference,
                ),
                OtherInformation=None,
                ProactiveNotification=None
            ),
            ShowAlternativeServicesIndicator=True
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespacedef_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    envelope.ns_prefix_ = "SOAP-ENV"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    envelope.Body.anytypeobjs_[0].ns_prefix_ = "ns1"
    envelope.Header.anytypeobjs_[0].ns_prefix_ = "ns1"
    return export(envelope, namespacedef_=namespacedef_)
