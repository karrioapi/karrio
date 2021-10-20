from typing import List, Tuple
from ups_lib.freight_rate_web_service_schema import (
    FreightRateRequest,
    RequestType,
    TransactionReferenceType,
    ShipFromType,
    ShipToType,
    AddressType,
    PayerType,
    PaymentInformationType,
    RateCodeDescriptionType,
    CommodityType,
    WeightType,
    DimensionsType,
    UnitOfMeasurementType,
    ShipmentTotalWeightType,
    RateType,
    ShipmentServiceOptionsType,
)
from purplship.core.utils import (
    apply_namespaceprefix,
    create_envelope,
    Serializable,
    Envelope,
    Element,
    SF,
    NF,
    XP,
)
from purplship.core.units import Packages, Services, Options, CompleteAddress
from purplship.core.models import RateDetails, ChargeDetails, Message, RateRequest
from purplship.providers.ups_ground.units import (
    ServiceCode,
    PackagingType,
    WeightUnit as UPSWeightUnit,
    PackagePresets,
    ServiceOption,
)
from purplship.providers.ups_ground.error import parse_error_response
from purplship.providers.ups_ground.utils import Settings


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    rate_replys = XP.find("Rate", response, RateType)
    rates: List[RateDetails] = [
        _extract_package_rate(rate, settings) for rate in rate_replys
    ]
    return rates, parse_error_response(response, settings)


def _extract_package_rate(rate: RateType, settings: Settings) -> RateDetails:

    pass
    # return RateDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #     currency=currency,
    #     service=service.name_or_key,
    #     base_charge=NF.decimal(rate.TransportationCharges.MonetaryValue),
    #     total_charge=NF.decimal(total_charges.MonetaryValue),
    #     duties_and_taxes=0.0,
    #     extra_charges=[],
    #     transit_days=NF.integer(transit_days),
    #     meta=dict(service_name=service.name_or_key)
    # )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels, PackagePresets)
    packages.validate(required=["weight"])
    options = Options(payload.options, ServiceOption)
    service = Services(payload.services, ServiceCode).first
    ship_from = CompleteAddress.map(payload.shipper)
    ship_to = CompleteAddress.map(payload.shipper)

    mps_packaging = PackagingType.ups_freight_other.value if len(packages) > 1 else None

    request = create_envelope(
        header_content=settings.Security,
        body_content=FreightRateRequest(
            Request=RequestType(
                RequestOption=[1],
                SubVersion=1707,
                TransactionReference=TransactionReferenceType(
                    CustomerContext=payload.reference,
                    TransactionIdentifier=getattr(payload, "id", None),
                ),
            ),
            ShipFrom=ShipFromType(
                Name=ship_from.company_name,
                Address=AddressType(
                    AddressLine=[ship_from.address_line],
                    City=ship_from.city,
                    StateProvinceCode=ship_from.state_code,
                    Town=None,
                    CountryCode=ship_from.country_code,
                    ResidentialAddressIndicator=("" if ship_from.residential else None),
                ),
                AttentionName=ship_from.person_name,
                TariffPoint=None,
            ),
            ShipTo=ShipToType(
                Name=ship_to.company_name,
                Address=AddressType(
                    AddressLine=[ship_to.address_line],
                    City=ship_to.city,
                    StateProvinceCode=ship_to.state_code,
                    Town=None,
                    CountryCode=ship_to.country_code,
                    ResidentialAddressIndicator=("" if ship_to.residential else None),
                ),
                AttentionName=ship_to.person_name,
                TariffPoint=None,
            ),
            PaymentInformation=PaymentInformationType(
                Payer=PayerType(
                    Name=ship_from.company_name,
                    Address=AddressType(
                        AddressLine=[ship_from.address_line],
                        City=ship_from.city,
                        StateProvinceCode=ship_from.state_code,
                        Town=None,
                        CountryCode=ship_from.country_code,
                        ResidentialAddressIndicator=(
                            "" if ship_from.residential else None
                        ),
                    ),
                    AttentionName=ship_from.person_name,
                    ShipperNumber=settings.account_number,
                ),
                ShipmentBillingOption=RateCodeDescriptionType(
                    Code=40, Description="Freight Collect"
                ),
            ),
            Service=(
                RateCodeDescriptionType(Code=service, Description=None)
                if service is not None
                else None
            ),
            HandlingUnitOne=None,
            HandlingUnitTwo=None,
            Commodity=[
                CommodityType(
                    CommodityID=getattr(commodity, "id", None),
                    Description=commodity.parcel.description,
                    Weight=WeightType(
                        Value=commodity.weight.value,
                        UnitOfMeasurement=UnitOfMeasurementType(
                            Code=UPSWeightUnit[commodity.weight_unit.name].value,
                        ),
                    ),
                    AdjustedWeight=None,
                    Dimensions=(
                        DimensionsType(
                            UnitOfMeasurement=UnitOfMeasurementType(
                                Code=commodity.dimension_unit.value, Description=None
                            ),
                            Length=commodity.length.value,
                            Width=commodity.width.value,
                            Height=commodity.height.value,
                        )
                        if commodity.has_dimensions
                        else None
                    ),
                    NumberOfPieces=1,
                    PackagingType=RateCodeDescriptionType(
                        Code=(
                            mps_packaging
                            or PackagingType[
                                commodity.packaging_type or "small_box"
                            ].value,
                        )
                    ),
                    DangerousGoodsIndicator=None,
                    CommodityValue=None,
                    FreightClass=None,
                    NMFCCommodity=None,
                    NMFCCommodityCode=None,
                )
                for commodity in packages
            ],
            ShipmentServiceOptions=(
                ShipmentServiceOptionsType(
                    PickupOptions=None,
                    DeliveryOptions=None,
                    OverSeasLeg=None,
                    COD=None,
                    DangerousGoods=None,
                    SortingAndSegregating=None,
                    DeclaredValue=None,
                    ExcessDeclaredValue=None,
                    CustomsValue=None,
                    DeliveryDutiesPaidIndicator=None,
                    DeliveryDutiesUnpaidIndicator=None,
                    HandlingCharge=None,
                    CustomsClearanceIndicator=None,
                    FreezableProtectionIndicator=None,
                    ExtremeLengthIndicator=None,
                    LinearFeet=None,
                    AdjustedHeight=None,
                )
                if any(
                    [
                        options.cash_on_delivery,
                        options.email_notification,
                        options.dangerous_good,
                        options.declared_value,
                    ]
                )
                else None
            ),
            PickupRequest=None,
            AlternateRateOptions=RateCodeDescriptionType(Code=3),
            GFPOptions=None,
            AccountType=None,
            ShipmentTotalWeight=ShipmentTotalWeightType(
                Value=packages.weight.value,
                UnitOfMeasurement=UnitOfMeasurementType(
                    Code=UPSWeightUnit[packages.weight.unit].value,
                ),
            ),
            HandlingUnitWeight=None,
            AdjustedWeightIndicator=None,
            TimeInTransitIndicator="",
            HandlingUnits=None,
            AdjustedHeightIndicator=None,
            DensityEligibleIndicator=None,
            QuoteNumberIndicator="",
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(envelope: Envelope) -> str:
    namespace_ = (
        'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" '
        'xmlns:wsf="http://www.ups.com/schema/wsf" '
        'xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" '
        'xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"'
    )
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "rate")
    apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return XP.export(envelope, namespacedef_=namespace_)
