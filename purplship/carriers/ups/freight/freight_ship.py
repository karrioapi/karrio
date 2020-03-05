from typing import List, Tuple
from functools import partial
from pyups import common
from pyups.freight_ship_web_service_schema import (
    FreightShipRequest, FreightShipResponse, ShipToType, ShipFromType, ShipmentType,
    FreightShipAddressType, FreightShipPhoneType, PhoneType, PayerType, CommodityType,
    PaymentInformationType, ShipCodeDescriptionType,
    CommodityValueType, FreightShipUnitOfMeasurementType, WeightType, DimensionsType
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.utils.xml import Element
from purplship.core.units import DimensionUnit
from purplship.core.models import (
    ShipmentRequest, ShipmentDetails, ChargeDetails, ReferenceDetails, Error
)
from purplship.carriers.ups.units import ShippingServiceCode, WeightUnit, PackagingType
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
    services = [
        ShippingServiceCode[svc]
        for svc in payload.shipment.services
        if svc in ShippingServiceCode.__members__
    ]
    payer = None
    request = FreightShipRequest(
        Request=common.RequestType(
            RequestOption="1",
            SubVersion=None,
            TransactionReference=common.TransactionReferenceType(
                CustomerContext=", ".join(payload.shipment.references),
                TransactionIdentifier=None,
            ),
        ),
        Shipment=ShipmentType(
            ShipFrom=ShipFromType(
                Name=payload.shipper.company_name,
                TaxIdentificationNumber=payload.shipper.tax_id,
                TaxIDType=None,
                TariffPoint=None,
                Address=FreightShipAddressType(
                    AddressLine=payload.shipper.address_lines,
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
                TaxIdentificationNumber=payload.recipient.tax_id,
                Address=FreightShipAddressType(
                    AddressLine=payload.recipient.address_lines,
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
            PaymentInformation=PaymentInformationType(
                Payer=PayerType(
                    Name=payer.company_name,
                    Address=FreightShipAddressType(
                        AddressLine=payer.address_lines,
                        City=payer.city,
                        StateProvinceCode=payer.state_code,
                        Town=None,
                        PostalCode=payer.postal_code,
                        CountryCode=payer.country_code,
                    ),
                    ShipperNumber=payer.account_number
                    or payload.shipment.payment_account_number,
                    AttentionName=payer.person_name,
                    Phone=FreightShipPhoneType(
                        Number=payer.phone_number,
                        Extension=None,
                    )
                    if payer.phone_number is not None
                    else None,
                    FaxNumber=None,
                    EMailAddress=payer.email_address,
                )
                if payer is not None
                else None,
                ShipmentBillingOption=None,
            ),
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
                    CommodityID=pkg.id,
                    Description=pkg.description,
                    Weight=WeightType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(
                            Code=WeightUnit[payload.shipment.weight_unit].value,
                            Description=None,
                        ),
                        Value=pkg.weight,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=FreightShipUnitOfMeasurementType(
                            Code=DimensionUnit[
                                payload.shipment.dimension_unit
                            ].value,
                            Description=None,
                        ),
                        Length=pkg.length,
                        Width=pkg.width,
                        Height=pkg.height,
                    )
                    if any((pkg.length, pkg.width, pkg.height))
                    else None,
                    NumberOfPieces=pkg.quantity,
                    PackagingType=ShipCodeDescriptionType(
                        Code=PackagingType[pkg.packaging_type].value,
                        Description=None,
                    )
                    if pkg.packaging_type is not None
                    else None,
                    DangerousGoodsIndicator=None,
                    CommodityValue=CommodityValueType(
                        CurrencyCode=pkg.value_amount,
                        MonetaryValue=pkg.value_currency,
                    )
                    if any((pkg.value_amount, pkg.value_currency))
                    else None,
                    FreightClass=None,
                    NMFCCommodityCode=None,
                    NMFCCommodity=None,
                )
                for pkg in payload.shipment.items
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
    return Serializable(request, lambda _: partial(_request_serializer, settings=settings)(_))


def _request_serializer(request: FreightShipRequest, settings: Settings) -> str:
    namespace_ = """
                    xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                    xmlns:wsf="http://www.ups.com/schema/wsf" 
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                    xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" 
                    xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"
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
        body_child_prefix="fsp:",
        header_child_name="UPSSecurity",
        body_child_name="FreightShipRequest",
    )
