from functools import reduce
from datetime import datetime
from typing import Tuple, List, Optional
from pyfedex.rate_service_v26 import (
    RateReplyDetail,
    RateRequest as FedexRateRequest,
    TransactionDetail,
    VersionId,
    RequestedShipment,
    TaxpayerIdentification,
    Party,
    Contact,
    Address,
    RatedShipmentDetail,
    Weight as FedexWeight,
)
from purplship.core.utils import export, concat_str, Serializable, format_date
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.units import Currency, Package, Options
from purplship.core.utils.xml import Element
from purplship.core.errors import RequiredFieldError
from purplship.core.models import RateDetails, RateRequest, Error, ChargeDetails
from purplship.carriers.fedex.units import PackagingType, ServiceType, PackagePresets
from purplship.carriers.fedex.error import parse_error_response
from purplship.carriers.fedex.utils import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    rate_reply = response.xpath(".//*[local-name() = $name]", name="RateReplyDetails")
    rate_details: List[RateDetails] = [
        _extract_quote(detail_node, settings) for detail_node in rate_reply
    ]
    return (
        [details for details in rate_details if details is not None],
        parse_error_response(response, settings),
    )


def _extract_quote(detail_node: Element, settings: Settings) -> Optional[RateDetails]:
    detail = RateReplyDetail()
    detail.build(detail_node)
    if not detail.RatedShipmentDetails:
        return None
    shipmentDetail: RatedShipmentDetail = detail.RatedShipmentDetails[
        0
    ].ShipmentRateDetail
    delivery_ = reduce(
        lambda v, c: c.text,
        detail_node.xpath(".//*[local-name() = $name]", name="DeliveryTimestamp"),
        None,
    )
    currency_ = reduce(
        lambda v, c: c.text,
        detail_node.xpath(".//*[local-name() = $name]", name="Currency"),
        Currency.USD.name,
    )
    Discounts_ = map(
        lambda d: ChargeDetails(
            name=d.RateDiscountType, amount=float(d.Amount.Amount), currency=currency_
        ),
        shipmentDetail.FreightDiscounts,
    )
    Surcharges_ = map(
        lambda s: ChargeDetails(
            name=s.SurchargeType, amount=float(s.Amount.Amount), currency=currency_
        ),
        shipmentDetail.Surcharges,
    )
    Taxes_ = map(
        lambda t: ChargeDetails(
            name=t.TaxType, amount=float(t.Amount.Amount), currency=currency_
        ),
        shipmentDetail.Taxes,
    )
    return RateDetails(
        carrier=settings.carrier_name,
        service=ServiceType(detail.ServiceType).name,
        currency=currency_,
        estimated_delivery=(
            format_date(delivery_, "%Y-%m-%dT%H:%M:%S") if delivery_ is not None else None
        ),
        base_charge=float(shipmentDetail.TotalBaseCharge.Amount),
        total_charge=float(shipmentDetail.TotalNetChargeWithDutiesAndTaxes.Amount),
        duties_and_taxes=float(shipmentDetail.TotalTaxes.Amount),
        discount=float(shipmentDetail.TotalFreightDiscounts.Amount),
        extra_charges=list(Discounts_) + list(Surcharges_) + list(Taxes_),
    )


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[FedexRateRequest]:
    parcel_preset = PackagePresets[payload.parcel.package_preset].value if payload.parcel.package_preset else None
    package = Package(payload.parcel, parcel_preset)

    if package.weight.value is None:
        raise RequiredFieldError("parcel.weight")

    service = next(
        (ServiceType[s].value for s in payload.parcel.services if s in ServiceType.__members__),
        None
    )
    options = Options(payload.options)

    request = FedexRateRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="crs", Major=26, Intermediate=0, Minor=0),
        ReturnTransitAndCommit=True,
        CarrierCodes=None,
        VariableOptions=None,
        ConsolidationKey=None,
        RequestedShipment=RequestedShipment(
            ShipTimestamp=datetime.now(),
            DropoffType="REGULAR_PICKUP",
            ServiceType=service,
            PackagingType=PackagingType[package.packaging_type or "your_packaging"].value,
            VariationOptions=None,
            TotalWeight=FedexWeight(
                Units=package.weight_unit.value,
                Value=package.weight.value,
            ),
            TotalInsuredValue=None,
            PreferredCurrency=options.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=settings.account_number,
                Tins=[
                    TaxpayerIdentification(TinType=None, Number=tax)
                    for tax in [
                        payload.shipper.federal_tax_id,
                        payload.shipper.state_tax_id,
                    ]
                ]
                if any([payload.shipper.federal_tax_id, payload.shipper.state_tax_id])
                else None,
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
                    EMailAddress=payload.shipper.email,
                )
                if any(
                    (
                        payload.shipper.company_name,
                        payload.shipper.person_name,
                        payload.shipper.phone_number,
                        payload.shipper.email,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=concat_str(
                        payload.shipper.address_line_1, payload.shipper.address_line_2
                    ),
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
                AccountNumber=None,
                Tins=[
                    TaxpayerIdentification(TinType=None, Number=tax)
                    for tax in [
                        payload.recipient.federal_tax_id,
                        payload.recipient.state_tax_id,
                    ]
                ]
                if any(
                    [payload.recipient.federal_tax_id, payload.recipient.state_tax_id]
                )
                else None,
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
                    EMailAddress=payload.recipient.email,
                )
                if any(
                    (
                        payload.recipient.company_name,
                        payload.recipient.person_name,
                        payload.recipient.phone_number,
                        payload.recipient.email,
                    )
                )
                else None,
                Address=Address(
                    StreetLines=concat_str(
                        payload.recipient.address_line_1,
                        payload.recipient.address_line_2,
                    ),
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
            LabelSpecification=None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=["LIST"]
            + ([] if "currency" not in payload.options else ["PREFERRED"]),
            EdtRequestType=None,
            PackageCount=None,
            ShipmentOnlyFields=None,
            ConfigurationData=None,
            RequestedPackageLineItems=None,
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: FedexRateRequest) -> str:
    return clean_namespaces(
        export(
            create_envelope(body_content=request),
            namespacedef_='tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v26"',
        ),
        envelope_prefix="tns:",
        body_child_prefix="ns:",
        body_child_name="RateRequest",
    )
