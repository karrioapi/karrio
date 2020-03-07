from base64 import b64encode
from datetime import datetime
from typing import List, Tuple
from functools import reduce
from pyfedex.ship_service_v25 import (
    CompletedShipmentDetail, ShipmentRateDetail, CompletedPackageDetail, ProcessShipmentRequest,
    TransactionDetail, VersionId, RequestedShipment, RequestedPackageLineItem, Party,
    Contact, Address, TaxpayerIdentification, Weight as FedexWeight,
    LabelSpecification, Dimensions as FedexDimensions,
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import Weight, WeightUnit, DimensionUnit, Dimension
from purplship.core.models import ShipmentDetails, Error, ChargeDetails, ShipmentRequest
from purplship.carriers.fedex.error import parse_error_response
from purplship.carriers.fedex.utils import Settings
from purplship.carriers.fedex.units import (
    PackagingType, ServiceType,
)


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    details = response.xpath(".//*[local-name() = $name]", name="CompletedShipmentDetail")
    shipment: ShipmentDetails = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_detail_node: Element, settings: Settings) -> ShipmentDetails:
    detail = CompletedShipmentDetail()
    detail.build(shipment_detail_node)

    shipment_node = shipment_detail_node.xpath(".//*[local-name() = $name]", name="ShipmentRateDetails")[0]
    shipment = ShipmentRateDetail()
    shipment.build(shipment_node)

    items_nodes = shipment_detail_node.xpath(".//*[local-name() = $name]", name="CompletedPackageDetails")
    items: [CompletedPackageDetail] = []
    for node in items_nodes:
        item = CompletedPackageDetail()
        item.build(node)
        items.append(item)

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=reduce(
            lambda ids, pkg: ids + [_id.TrackingNumber for _id in pkg.TrackingIds],
            items, [],
        ),
        total_charge=ChargeDetails(
            name="Shipment charge",
            amount=shipment.TotalNetChargeWithDutiesAndTaxes.Amount,
            currency=shipment.TotalNetChargeWithDutiesAndTaxes.Currency,
        ),
        charges=[
            ChargeDetails(
                name="base_charge",
                amount=shipment.TotalBaseCharge.Amount,
                currency=shipment.TotalBaseCharge.Currency,
            ),
            ChargeDetails(
                name="discount",
                amount=detail.ShipmentRating.EffectiveNetDiscount.Amount,
                currency=detail.ShipmentRating.EffectiveNetDiscount.Currency,
            ),
        ]
        + [
            ChargeDetails(
                name=surcharge.SurchargeType,
                amount=surcharge.Amount.Amount,
                currency=surcharge.Amount.Currency,
            )
            for surcharge in shipment.Surcharges
        ]
        + [
            ChargeDetails(
                name=fee.Type,
                amount=fee.Amount.Amount,
                currency=fee.Amount.Currency,
            )
            for fee in shipment.AncillaryFeesAndTaxes
        ],
        services=[],
        documents=reduce(
            lambda labels, pkg: labels + [str(b64encode(part.Image), "utf-8") for part in pkg.Label.Parts],
            items, [],
        ),
    )


def process_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[ProcessShipmentRequest]:
    dimension_unit = payload.shipment.dimension_unit or "IN"
    weight_unit = payload.shipment.weight_unit or "LB"
    requested_services = [svc for svc in payload.shipment.services if svc in ServiceType.__members__]
    request = ProcessShipmentRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v18_Ship"),
        Version=VersionId(ServiceId="ship", Major=21, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType="REGULAR_PICKUP",
            ServiceType=(
                ServiceType[requested_services[0]].value if len(requested_services) > 0 else None
            ),
            PackagingType=PackagingType[
                payload.shipment.packaging_type or "YOUR_PACKAGING"
            ].value,
            ManifestDetail=None,
            TotalWeight=FedexWeight(
                Units=weight_unit,
                Value=Weight(
                    payload.shipment.total_weight or sum(p.weight for p in payload.shipment.items),
                    WeightUnit[weight_unit]
                ).value,
            ),
            TotalInsuredValue=payload.shipment.insured_amount,
            PreferredCurrency=payload.shipment.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=payload.shipper.account_number,
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=None,
                            Usage=None,
                            Number=payload.recipient.tax_id,
                            EffectiveDate=None,
                            ExpirationDate=None,
                        )
                    ]
                    if payload.shipper.tax_id is not None else None
                ),
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.shipper.person_name,
                    Title=None,
                    CompanyName=payload.shipper.company_name,
                    PhoneNumber=payload.shipper.phone_number,
                    PhoneExtension=None,
                    TollFreePhoneNumber=None,
                    PagerNumber=None,
                    FaxNumber=None,
                    EMailAddress=payload.shipper.email_address,
                )
                if any(
                    (
                        payload.shipper.company_name,
                        payload.shipper.phone_number,
                        payload.shipper.person_name,
                        payload.shipper.email_address,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=payload.shipper.address_lines,
                    City=payload.shipper.city,
                    StateOrProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    UrbanizationCode=None,
                    CountryCode=payload.shipper.country_code,
                    CountryName=None,
                    Residential=None,
                    GeographicCoordinates=None,
                ),
            ),
            Recipient=Party(
                AccountNumber=payload.recipient.account_number,
                Tins=(
                    [
                        TaxpayerIdentification(
                            TinType=None,
                            Usage=None,
                            Number=payload.recipient.tax_id,
                            EffectiveDate=None,
                            ExpirationDate=None,
                        )
                    ]
                    if payload.recipient.tax_id is not None else None
                ),
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.recipient.person_name,
                    Title=None,
                    CompanyName=payload.recipient.company_name,
                    PhoneNumber=payload.recipient.phone_number,
                    PhoneExtension=None,
                    TollFreePhoneNumber=None,
                    PagerNumber=None,
                    FaxNumber=None,
                    EMailAddress=payload.recipient.email_address,
                )
                if any(
                    (
                        payload.recipient.company_name,
                        payload.recipient.phone_number,
                        payload.recipient.person_name,
                        payload.recipient.email_address,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=payload.recipient.address_lines,
                    City=payload.recipient.city,
                    StateOrProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    UrbanizationCode=None,
                    CountryCode=payload.recipient.country_code,
                    CountryName=None,
                    Residential=None,
                    GeographicCoordinates=None,
                ),
            ),
            RecipientLocationNumber=None,
            Origin=None,
            SoldTo=None,
            ShippingChargesPayment=None,
            SpecialServicesRequested=None,
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=LabelSpecification(
                Dispositions=None,
                LabelFormatType=payload.shipment.label.format,
                ImageType=payload.shipment.label.type,
                LabelStockType="PAPER_7X4.75",
                LabelPrintingOrientation=None,
                LabelOrder=None,
                PrintedLabelOrigin=None,
                CustomerSpecifiedDetail=None,
            ) if payload.shipment.label is not None else None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=["LIST"] + ([] if not payload.shipment.currency else ["PREFERRED"]),
            EdtRequestType=None,
            MasterTrackingId=None,
            PackageCount=len(payload.shipment.items),
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=index,
                    GroupNumber=None,
                    GroupPackageCount=index,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=FedexWeight(
                        Units=weight_unit,
                        Value=Weight(pkg.weight, WeightUnit[weight_unit]).value,
                    ),
                    Dimensions=FedexDimensions(
                        Length=Dimension(pkg.length, DimensionUnit[dimension_unit]).value,
                        Width=Dimension(pkg.width, DimensionUnit[dimension_unit]).value,
                        Height=Dimension(pkg.height, DimensionUnit[dimension_unit]).value,
                        Units=dimension_unit,
                    ),
                    PhysicalPackaging=None,
                    ItemDescription=pkg.content,
                    ItemDescriptionForClearance=pkg.description,
                    CustomerReferences=None,
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, pkg in enumerate(payload.shipment.items, 1)
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ProcessShipmentRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v25"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="ProcessShipmentRequest",
    )
