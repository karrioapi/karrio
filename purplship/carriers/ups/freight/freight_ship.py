from typing import List, Tuple
from pyups import common
from pyups.freight_ship_web_service_schema import (
    FreightShipRequest, FreightShipResponse, ShipToType, ShipFromType, ShipmentType,
    FreightShipAddressType, FreightShipPhoneType, PhoneType, CommodityType,
    ShipCodeDescriptionType, FreightShipUnitOfMeasurementType, WeightType, DimensionsType
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import DimensionUnit, Dimension, Weight, WeightUnit
from purplship.core.models import (
    ShipmentRequest, ShipmentDetails, ChargeDetails, ReferenceDetails, Error
)
from purplship.carriers.ups.units import ShippingServiceCode, WeightUnit as UPSWeightUnit, FreightClass
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_freight_ship_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    details = response.xpath(".//*[local-name() = $name]", name="FreightShipResponse")
    shipment = _extract_shipment(details[0], settings) if len(details) > 0 else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(shipment_node: Element, settings: Settings) -> ShipmentDetails:
    shipmentResponse = FreightShipResponse()
    shipmentResponse.build(shipment_node)
    shipment = shipmentResponse.ShipmentResults

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=[shipment.ShipmentNumber],
        total_charge=ChargeDetails(
            name="Shipment charge",
            amount=shipment.TotalShipmentCharge.MonetaryValue,
            currency=shipment.TotalShipmentCharge.CurrencyCode,
        ),
        charges=[
            ChargeDetails(
                name=rate.Type.Code,
                amount=rate.Factor.Value,
                currency=rate.Factor.UnitOfMeasurement.Code,
            )
            for rate in shipment.Rate
        ],
        shipment_date=None,
        services=[shipment.Service.Code],
        documents=[image.GraphicImage for image in (shipment.Documents or [])],
        reference=ReferenceDetails(
            value=shipmentResponse.Response.TransactionReference.CustomerContext,
            type="CustomerContext",
        ),
    )


def freight_ship_request(payload: ShipmentRequest, settings: Settings) -> Serializable[FreightShipRequest]:
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    services = [
        ShippingServiceCode[svc]
        for svc in payload.parcel.services
        if svc in ShippingServiceCode.__members__
    ]
    request = FreightShipRequest(
        Request=common.RequestType(
            RequestOption="1",
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=payload.parcel.reference,
                TransactionIdentifier=None,
            ),
        ),
        Shipment=ShipmentType(
            ShipFrom=ShipFromType(
                Name=payload.shipper.company_name,
                TaxIdentificationNumber=payload.shipper.federal_tax_id,
                TaxIDType=None,
                TariffPoint=None,
                Address=FreightShipAddressType(
                    AddressLine=concat_str(payload.shipper.address_line_1, payload.shipper.address_line_2),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    Town=None,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
                AttentionName=payload.shipper.person_name,
                Phone=FreightShipPhoneType(
                    Number=payload.shipper.phone_number,
                    Extension=None,
                )
                if payload.shipper.phone_number is not None
                else None,
                FaxNumber=None,
                EMailAddress=payload.shipper.email_address,
            ),
            ShipperNumber=payload.shipper.account_number,
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                TaxIdentificationNumber=payload.recipient.federal_tax_id,
                Address=FreightShipAddressType(
                    AddressLine=concat_str(payload.recipient.address_line_1, payload.recipient.address_line_2),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    Town=None,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                ),
                TariffPoint=None,
                AttentionName=payload.recipient.person_name,
                Phone=PhoneType(
                    Number=payload.recipient.phone_number,
                    Extension=None,
                )
                if payload.recipient.phone_number is not None
                else None,
                FaxNumber=None,
                EMailAddress=payload.recipient.email_address,
            ),
            PaymentInformation=None,
            ManufactureInformation=None,
            Service=ShipCodeDescriptionType(Code=services[0].value)
            if len(services) > 0
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
                    CommodityID=payload.parcel.id,
                    Description=payload.parcel.description,
                    Weight=WeightType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(Code=UPSWeightUnit[weight_unit.name].value),
                        Value=Weight(payload.parcel.weight, weight_unit).value,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(Code=dimension_unit.value),
                        Width=Dimension(payload.parcel.width, dimension_unit).value,
                        Height=Dimension(payload.parcel.height, dimension_unit).value,
                        Length=Dimension(payload.parcel.length, dimension_unit).value,
                    ) if any([payload.parcel.width, payload.parcel.height, payload.parcel.length]) else None,
                    NumberOfPieces=None,
                    PackagingType=None,
                    DangerousGoodsIndicator=None,
                    CommodityValue=None,
                    FreightClass=FreightClass[payload.parcel.options.get('ups_freight_class')].value,
                    NMFCCommodityCode=None,
                    NMFCCommodity=None,
                )
            ],
            Reference=None,
            ShipmentServiceOptions=None,
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
        _request_serializer
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
    """.replace(" ", "").replace("\n", " ")
    return clean_namespaces(
        export(request, namespacedef_=namespace_),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        body_child_prefix="fsp:",
        header_child_name="UPSSecurity",
        body_child_name="FreightShipRequest",
    )
