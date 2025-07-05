from typing import Tuple, List
import datetime
import karrio.schemas.dhl_ecommerce_europe.shipment_request as dhl_ecommerce_europe
import karrio.schemas.dhl_ecommerce_europe.shipment_response as shipping
from karrio.core.utils import Serializable, Deserializable, DF, SF
from karrio.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message,
)
from karrio.providers.dhl_ecommerce_europe.utils import Settings, request
from karrio.providers.dhl_ecommerce_europe.error import parse_error_response
import karrio.providers.dhl_ecommerce_europe.units as provider_units
import karrio.lib as lib


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ShipmentDetails, List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    
    shipment = (
        _extract_shipment_details(response, settings)
        if not messages
        else None
    )

    return shipment, messages


def _extract_shipment_details(data: dict, settings: Settings) -> ShipmentDetails:
    # Extract label from documents
    documents = data.get("documents", [])
    label_content = documents[0].get("content") if documents else None
    
    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.get("shipmentTrackingNumber"),
        shipment_identifier=data.get("shipmentTrackingNumber"),
        docs=lib.to_object(lib.models.Documents, {"label": label_content}) if label_content else None,
        meta=data,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable:
    """Create shipment request for DHL eCommerce Europe."""
    
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    request_data = {
        "plannedShippingDateAndTime": lib.fdatetime(
            options.shipment_date.state or datetime.datetime.now(),
            output_format="%Y-%m-%dT%H:%M:%S"
        ),
        "pickup": {
            "typeCode": "business",
            "accounts": [
                {
                    "typeCode": "shipper",
                    "number": settings.account_number,
                }
            ],
        },
        "productCode": payload.service or "U",
        "accounts": [
            {
                "typeCode": "shipper",
                "number": settings.account_number,
            }
        ],
        "customerDetails": {
            "shipperDetails": {
                "postalAddress": {
                    "postalCode": payload.shipper.postal_code,
                    "cityName": payload.shipper.city,
                    "countryCode": payload.shipper.country_code,
                    "addressLine1": payload.shipper.address_line1,
                },
                "contactInformation": {
                    "email": payload.shipper.email,
                    "phone": payload.shipper.phone_number,
                    "companyName": payload.shipper.company_name,
                    "fullName": payload.shipper.person_name,
                },
            },
            "receiverDetails": {
                "postalAddress": {
                    "postalCode": payload.recipient.postal_code,
                    "cityName": payload.recipient.city,
                    "countryCode": payload.recipient.country_code,
                    "addressLine1": payload.recipient.address_line1,
                },
                "contactInformation": {
                    "email": payload.recipient.email,
                    "phone": payload.recipient.phone_number,
                    "companyName": payload.recipient.company_name,
                    "fullName": payload.recipient.person_name,
                },
            },
        },
                    "packages": [
                {
                    "weight": package.weight.value,
                    "dimensions": {
                        "length": package.length.value,
                        "width": package.width.value,
                        "height": package.height.value,
                    },
                }
                for package in lib.to_packages(payload.parcels)
            ],
        "outputImageProperties": {
            "printerDPI": 300,
            "customerLogos": [],
            "customerBarcodes": [],
            "splitTransportAndWaybillDocLabels": False,
            "allDocumentsInOneImage": False,
            "splitDocumentsByPages": False,
            "splitInvoiceAndReceipt": True,
            "receiptAndLabelsInOneImage": False,
        },
    }

    return Serializable(request_data, lib.to_dict)


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    
    confirmation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=True,
        )
        if not messages
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable:
    """Create shipment cancellation request for DHL eCommerce Europe."""
    
    request_data = {
        "shipmentTrackingNumber": payload.shipment_identifier,
    }

    return Serializable(request_data, lib.to_dict)


def _shipment_request_serializer(data: dict) -> str:
    """Serialize shipment request to DHL eCommerce Europe API."""
    return lib.to_json(data)


def _shipment_cancel_request_serializer(data: dict) -> str:
    """Serialize shipment cancel request to DHL eCommerce Europe API."""
    return lib.to_json(data) 
