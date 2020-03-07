from functools import reduce, partial
from typing import Callable, List, Tuple
from pyups import common
from pyups.rate_web_service_schema import (
    RateRequest as UPSRateRequest, PickupType, RatedShipmentType,
    ShipToType, ShipmentType, ShipperType, ShipAddressType, ShipToAddressType,
    PaymentDetailsType, ShipmentChargeType, PackageType,
    BillShipperChargeType, BillReceiverAddressType, PackageWeightType, BillReceiverChargeType,
    ShipmentRatingOptionsType, UOMCodeDescriptionType,
    ShipmentServiceOptionsType, DimensionsType, BillThirdPartyChargeType,
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import DimensionUnit
from purplship.core.models import (
    RateDetails, ChargeDetails, Error, RateRequest
)
from purplship.carriers.ups.units import (
    RatingServiceCode, RatingPackagingType, WeightUnit, ServiceOption,
    RatingOption, ShippingServiceCode
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    rate_reply = response.xpath(".//*[local-name() = $name]", name="RatedShipment")
    rates: List[RateDetails] = reduce(_extract_package_rate(settings), rate_reply, [])
    return rates, parse_error_response(response, settings)


def _extract_package_rate(settings: Settings) -> Callable[[List[RateDetails], Element], List[RateDetails]]:
    def extract(rates: List[RateDetails], detail_node: Element) -> List[RateDetails]:
        rate = RatedShipmentType()
        rate.build(detail_node)
    
        if rate.NegotiatedRateCharges is not None:
            total_charges = (
                rate.NegotiatedRateCharges.TotalChargesWithTaxes
                or rate.NegotiatedRateCharges.TotalCharge
            )
            taxes = rate.NegotiatedRateCharges.TaxCharges
            itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
        else:
            total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
            taxes = rate.TaxCharges
            itemized_charges = rate.ItemizedCharges + taxes
    
        extra_charges = itemized_charges + [rate.ServiceOptionsCharges]
    
        arrival = PickupType()
        [
            arrival.build(arrival) for arrival in
            detail_node.xpath(".//*[local-name() = $name]", name="Arrival")
        ]
        currency_ = next(c.text for c in detail_node.xpath(
            ".//*[local-name() = $name]", name="CurrencyCode"
        ))
    
        return rates + [
            RateDetails(
                carrier=settings.carrier_name,
                currency=currency_,
                service_name=str(ShippingServiceCode(rate.Service.Code).name),
                service_type=rate.Service.Code,
                base_charge=float(rate.TransportationCharges.MonetaryValue),
                total_charge=float(total_charges.MonetaryValue),
                duties_and_taxes=reduce(
                    lambda total, charge: total + float(charge.MonetaryValue),
                    taxes or [],
                    0.0,
                ),
                discount=None,
                extra_charges=reduce(
                    lambda total, charge: (total + [
                      ChargeDetails(name=charge.Code, amount=float(charge.MonetaryValue), currency=charge.CurrencyCode)
                    ]),
                    [charge for charge in extra_charges if charge is not None],
                    [],
                ),
                delivery_date=str(arrival.Date)
            )
        ]
    
    return extract


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[UPSRateRequest]:
    service = (
        [
            RatingServiceCode[svc]
            for svc in payload.shipment.services
            if svc in RatingServiceCode.__members__
        ]
        + [RatingServiceCode.UPS_Worldwide_Express]
    )[0]
    payment_details_provided = (
        all((payload.shipment.paid_by, payload.shipment.payment_account_number))
        or (
            payload.shipment.paid_by == "SENDER"
            and payload.shipper.account_number is not None
        )
        or (
            payload.shipment.paid_by == "RECIPIENT"
            and payload.recipient.account_number is not None
        )
    )
    is_negotiated_rate = any(
        (payload.shipment.payment_account_number, payload.shipper.account_number)
    )
    service_options = [
        opt
        for opt in payload.options.keys()
        if opt in ServiceOption.__members__
    ]
    rating_options = [
        opt
        for opt in payload.options.keys()
        if opt in RatingOption.__members__
    ]
    request = UPSRateRequest(
        Request=common.RequestType(
            RequestOption=["Rate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=", ".join(payload.shipment.references),
                TransactionIdentifier=None,
            ),
        ),
        PickupType=None,
        CustomerClassification=None,
        Shipment=ShipmentType(
            OriginRecordTransactionTimestamp=None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                ShipperNumber=payload.shipper.account_number,
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
                Address=ShipToAddressType(
                    AddressLine=payload.recipient.address_lines,
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                    ResidentialAddressIndicator=None,
                ),
            ),
            ShipFrom=None,
            AlternateDeliveryAddress=None,
            ShipmentIndicationType=None,
            PaymentDetails=PaymentDetailsType(
                ShipmentCharge=[
                    ShipmentChargeType(
                        Type=None,
                        BillShipper=BillShipperChargeType(
                            AccountNumber=payload.shipment.payment_account_number
                            or payload.shipper.account_number
                        )
                        if payload.shipment.paid_by == "SENDER"
                        else None,
                        BillReceiver=BillReceiverChargeType(
                            AccountNumber=payload.shipment.payment_account_number
                            or payload.recipient.account_number,
                            Address=BillReceiverAddressType(
                                PostalCode=payload.recipient.postal_code
                            ),
                        )
                        if payload.shipment.paid_by == "RECIPIENT"
                        else None,
                        BillThirdParty=BillThirdPartyChargeType(
                            AccountNumber=payload.shipment.payment_account_number,
                            Address=None,
                        )
                        if payload.shipment.paid_by == "THIRD_PARTY"
                        else None,
                        ConsigneeBilledIndicator=None,
                    )
                ],
                SplitDutyVATIndicator=None,
            )
            if payment_details_provided
            else None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            Service=UOMCodeDescriptionType(
                Code=service.value, Description=None
            ),
            NumOfPieces=payload.shipment.total_items,
            ShipmentTotalWeight=payload.shipment.total_weight,
            DocumentsOnlyIndicator="" if payload.shipment.is_document else None,
            Package=[
                PackageType(
                    PackagingType=UOMCodeDescriptionType(
                        Code=RatingPackagingType[pkg.packaging_type or "BOX"].value,
                        Description=None,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=DimensionUnit[
                                payload.shipment.dimension_unit
                            ].value,
                            Description=None,
                        ),
                        Length=pkg.length,
                        Width=pkg.width,
                        Height=pkg.height,
                    ),
                    DimWeight=None,
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=WeightUnit[payload.shipment.weight_unit].value,
                            Description=None,
                        ),
                        Weight=pkg.weight,
                    ),
                    Commodity=None,
                    PackageServiceOptions=None,
                    AdditionalHandlingIndicator=None,
                )
                for pkg in payload.shipment.items
            ],
            ShipmentServiceOptions=ShipmentServiceOptionsType(
                SaturdayDeliveryIndicator=None,
                AccessPointCOD=None,
                DeliverToAddresseeOnlyIndicator=None,
                DirectDeliveryOnlyIndicator=None,
                COD=None,
                DeliveryConfirmation=None,
                ReturnOfDocumentIndicator=None,
                UPScarbonneutralIndicator=None,
                CertificateOfOriginIndicator=None,
                PickupOptions=None,
                DeliveryOptions=None,
                RestrictedArticles=None,
                ShipperExportDeclarationIndicator=None,
                CommercialInvoiceRemovalIndicator=None,
                ImportControl=None,
                ReturnService=None,
                SDLShipmentIndicator=None,
                EPRAIndicator=None,
            )
            if len(service_options) > 0
            else None,
            ShipmentRatingOptions=ShipmentRatingOptionsType(
                NegotiatedRatesIndicator="" if is_negotiated_rate else None,
                FRSShipmentIndicator=None,
                RateChartIndicator=None,
                UserLevelDiscountIndicator=None,
            )
            if len(rating_options) > 0 or is_negotiated_rate
            else None,
            InvoiceLineTotal=None,
            RatingMethodRequestedIndicator=None,
            TaxInformationIndicator=None,
            PromotionalDiscountInformation=None,
            DeliveryTimeInformation=None,
        ),
    )
    return Serializable(request, lambda _: partial(_request_serializer, settings=settings)(_))


def _request_serializer(request: UPSRateRequest, settings: Settings) -> str:
    namespace_ = """
                    xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"
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
        body_child_prefix="rate:",
        header_child_name="UPSSecurity",
        body_child_name="RateRequest",
    )
