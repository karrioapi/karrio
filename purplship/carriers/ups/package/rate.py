from functools import reduce
from typing import Callable, List, Tuple
from pyups import common
from pyups.rate_web_service_schema import (
    RateRequest as UPSRateRequest,
    PickupType,
    RatedShipmentType,
    ShipmentRatingOptionsType,
    ShipToType,
    ShipmentType,
    ShipperType,
    ShipAddressType,
    ShipToAddressType,
    PackageType,
    PackageWeightType,
    UOMCodeDescriptionType,
    DimensionsType,
)
from purplship.core.utils import export, concat_str, Serializable, format_date
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import Package
from purplship.core.models import RateDetails, ChargeDetails, Message, RateRequest
from purplship.core.errors import RequiredFieldError
from purplship.carriers.ups.units import (
    RatingServiceCode,
    RatingPackagingType,
    WeightUnit as UPSWeightUnit,
    ShippingServiceCode,
    PackagePresets
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    rate_reply = response.xpath(".//*[local-name() = $name]", name="RatedShipment")
    rates: List[RateDetails] = reduce(_extract_package_rate(settings), rate_reply, [])
    return rates, parse_error_response(response, settings)


def _extract_package_rate(
    settings: Settings
) -> Callable[[List[RateDetails], Element], List[RateDetails]]:
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
            arrival.build(arrival)
            for arrival in detail_node.xpath(
                ".//*[local-name() = $name]", name="Arrival"
            )
        ]
        currency_ = next(
            c.text
            for c in detail_node.xpath(
                ".//*[local-name() = $name]", name="CurrencyCode"
            )
        )
        service = ShippingServiceCode(rate.Service.Code).name
        return rates + [
            RateDetails(
                carrier=settings.carrier_name,
                currency=currency_,
                service=service,
                base_charge=float(rate.TransportationCharges.MonetaryValue),
                total_charge=float(total_charges.MonetaryValue),
                duties_and_taxes=reduce(
                    lambda total, charge: total + float(charge.MonetaryValue),
                    taxes or [],
                    0.0,
                ),
                extra_charges=reduce(
                    lambda total, charge: (
                        total
                        + [
                            ChargeDetails(
                                name=charge.Code,
                                amount=float(charge.MonetaryValue),
                                currency=charge.CurrencyCode,
                            )
                        ]
                    ),
                    [charge for charge in extra_charges if charge is not None],
                    [],
                ),
                estimated_delivery=format_date(arrival.Date),
            )
        ]

    return extract


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[UPSRateRequest]:
    parcel_preset = PackagePresets[payload.parcel.package_preset].value if payload.parcel.package_preset else None
    package = Package(payload.parcel, parcel_preset)
    service: str = next(
        (RatingServiceCode[s].value for s in payload.parcel.services if s in RatingServiceCode.__members__),
        RatingServiceCode.ups_express.value
    )

    if (("freight" in service) or ("ground" in service)) and (package.weight.value is None):
        raise RequiredFieldError("parcel.weight")

    request = UPSRateRequest(
        Request=common.RequestType(
            RequestOption=["Rate"],
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.parcel.reference, TransactionIdentifier=None
            ),
        ),
        PickupType=None,
        CustomerClassification=None,
        Shipment=ShipmentType(
            OriginRecordTransactionTimestamp=None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                ShipperNumber=settings.account_number,
                Address=ShipAddressType(
                    AddressLine=concat_str(
                        payload.recipient.address_line_1,
                        payload.recipient.address_line_2,
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                Address=ShipToAddressType(
                    AddressLine=concat_str(
                        payload.recipient.address_line_1,
                        payload.recipient.address_line_2,
                    ),
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
            PaymentDetails=None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            Service=UOMCodeDescriptionType(Code=service, Description=None),
            NumOfPieces=None,  # Only required for Freight
            ShipmentTotalWeight=None,  # Only required for "timeintransit" requests
            DocumentsOnlyIndicator="" if payload.parcel.is_document else None,
            Package=[
                PackageType(
                    PackagingType=UOMCodeDescriptionType(
                        Code=RatingPackagingType[
                            payload.parcel.packaging_type or "small_box"
                        ].value,
                        Description=None,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=package.dimension_unit.value, Description=None
                        ),
                        Length=package.length.value,
                        Width=package.width.value,
                        Height=package.height.value,
                    ) if any([package.length.value, package.height.value, package.width.value]) else None,
                    DimWeight=None,
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=UPSWeightUnit[package.weight_unit.name].value, Description=None
                        ),
                        Weight=package.weight.value,
                    ) if package.weight.value else None,
                    Commodity=None,
                    PackageServiceOptions=None,
                    AdditionalHandlingIndicator=None,
                )
            ],
            ShipmentServiceOptions=None,
            ShipmentRatingOptions=ShipmentRatingOptionsType(
                NegotiatedRatesIndicator=""
            ),
            InvoiceLineTotal=None,
            RatingMethodRequestedIndicator=None,
            TaxInformationIndicator=None,
            PromotionalDiscountInformation=None,
            DeliveryTimeInformation=None,
        ),
    )
    return Serializable(
        create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(request: Element) -> str:
    namespace_ = """
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    return clean_namespaces(
        export(request, namespacedef_=namespace_),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        body_child_prefix="rate:",
        header_child_name="UPSSecurity",
        body_child_name="RateRequest",
    )
