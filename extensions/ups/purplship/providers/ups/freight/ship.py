from typing import List, Tuple, cast
from pyups import common
from pyups.freight_ship_web_service_schema import (
    FreightShipRequest,
    FreightShipResponse,
    ShipToType,
    ShipFromType,
    ShipmentType,
    FreightShipAddressType,
    FreightShipPhoneType,
    PhoneType,
    CommodityType,
    ShipCodeDescriptionType,
    FreightShipUnitOfMeasurementType,
    WeightType,
    DimensionsType,
    ShipmentResultsType,
    ShipmentServiceOptionsType,
    EMailNotificationType,
    CODType,
    CODValueType,
    DocumentType,
    ImageFormsType,
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import Packages, Options
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message,
)
from purplship.providers.ups.units import (
    ShippingServiceCode,
    WeightUnit,
    FreightClass,
    PackagePresets,
)
from purplship.providers.ups.error import parse_error_response
from purplship.providers.ups.utils import Settings

NOTIFICATION_EVENT_TYPES = ["001", "002", "003", "004"]


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = response.xpath(".//*[local-name() = $name]", name="FreightShipResponse")
    shipment = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_node: Element, settings: Settings) -> ShipmentDetails:
    shipmentResponse = FreightShipResponse()
    shipmentResponse.build(shipment_node)
    shipment: ShipmentResultsType = shipmentResponse.ShipmentResults
    document = cast(DocumentType, shipment.Documents)
    label = (
        cast(ImageFormsType, document.Image).GraphicImage
        if document is not None
        else None
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=shipment.ShipmentNumber,
        shipment_identifier=shipment.ShipmentNumber,
        label=label,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[FreightShipRequest]:
    packages = Packages(payload.parcels, PackagePresets)
    options = Options(payload.options)
    service = ShippingServiceCode[payload.service].value
    freight_class = FreightClass[
        payload.options.get("ups_freight_class", "ups_freight_class_50")
    ].value

    request = FreightShipRequest(
        Request=common.RequestType(
            RequestOption="1",
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.reference, TransactionIdentifier=None
            ),
        ),
        Shipment=ShipmentType(
            ShipFrom=ShipFromType(
                Name=payload.shipper.company_name,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                TariffPoint=None,
                Address=FreightShipAddressType(
                    AddressLine=concat_str(
                        payload.shipper.address_line1, payload.shipper.address_line2
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    Town=None,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
                AttentionName=payload.shipper.person_name,
                Phone=FreightShipPhoneType(
                    Number=payload.shipper.phone_number, Extension=None
                )
                if payload.shipper.phone_number is not None
                else None,
                FaxNumber=None,
                EMailAddress=payload.shipper.email,
            ),
            ShipperNumber=settings.account_number,
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                TaxIdentificationNumber=payload.recipient.federal_tax_id,
                Address=FreightShipAddressType(
                    AddressLine=concat_str(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    Town=None,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
                TariffPoint=None,
                AttentionName=payload.recipient.person_name,
                Phone=PhoneType(Number=payload.recipient.phone_number, Extension=None)
                if payload.recipient.phone_number is not None
                else None,
                FaxNumber=None,
                EMailAddress=payload.recipient.email,
            ),
            PaymentInformation=None,
            ManufactureInformation=None,
            Service=ShipCodeDescriptionType(Code=service)
            if service is not None
            else None,
            HandlingUnitOne=None,
            HandlingUnitTwo=None,
            ExistingShipmentID=None,
            HandlingInstructions=None,
            DeliveryInstructions=None,
            PickupInstructions=None,
            SpecialInstructions=None,
            ShipmentTotalWeight=None,
            Commodity=[
                CommodityType(
                    CommodityID=package.parcel.id,
                    Description=package.parcel.description,
                    Weight=WeightType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(
                            Code=WeightUnit[package.weight_unit].value
                        ),
                        Value=package.weight.value,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(
                            Code=package.dimension_unit
                        ),
                        Width=package.width.value,
                        Height=package.height.value,
                        Length=package.length.value,
                    )
                    if any(
                        [
                            package.width.value,
                            package.height.value,
                            package.length.value,
                        ]
                    )
                    else None,
                    NumberOfPieces=None,
                    PackagingType=None,
                    DangerousGoodsIndicator=None,
                    CommodityValue=None,
                    FreightClass=freight_class,
                    NMFCCommodityCode=None,
                    NMFCCommodity=None,
                )
                for package in packages
            ],
            Reference=None,
            ShipmentServiceOptions=ShipmentServiceOptionsType(
                EMailInformation=[
                    EMailNotificationType(
                        EMailAddress=options.notification.email
                        or payload.shipper.email,
                        EventType=NOTIFICATION_EVENT_TYPES,
                    )
                ]
                if options.notification
                else None,
                PickupOptions=None,
                DeliveryOptions=None,
                OverSeasLeg=None,
                COD=CODType(
                    CODValue=CODValueType(
                        CurrencyCode=options.currency or "USD",
                        MonetaryValue=options.cash_on_delivery.amount,
                    ),
                    CODPaymentMethod=None,
                    CODBillingOption=None,
                    RemitTo=None,
                )
                if options.cash_on_delivery
                else None,
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
            )
            if options.has_content
            else None,
            PickupRequest=None,
            Documents=None,
            ITNNumber=None,
            TaxID=None,
            MovementReferenceNumber=None,
            EICNumberAndStatement=None,
            TimeInTransitIndicator=None,
            HandlingUnits=None,
            DensityEligibleIndicator=None,
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
        xmlns:wsf="http://www.ups.com/schema/wsf"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0"
        xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    return clean_namespaces(
        export(request, namespacedef_=namespace_),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        body_child_prefix="fsp:",
        header_child_name="UPSSecurity",
        body_child_name="FreightShipRequest",
    )
