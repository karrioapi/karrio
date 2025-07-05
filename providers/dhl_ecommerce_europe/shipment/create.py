import karrio.schemas.dhl_ecommerce_europe.shipment_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_europe.error as error
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils
import karrio.providers.dhl_ecommerce_europe.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.ShipmentDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    shipments = []
    if "shipmentTrackingNumber" in response:
        shipment_response = lib.to_object(shipping.ShipmentResponse, response)
        shipments = [_extract_details(shipment_response, settings)]

    return shipments, messages


def _extract_details(
    data: shipping.ShipmentResponse,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    # Get the label document
    label_doc = None
    if data.documents:
        label_doc = next(
            (doc.content for doc in data.documents if doc.typeCode == "waybill-doc"),
            None
        )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.shipmentTrackingNumber,
        shipment_identifier=data.shipmentTrackingNumber,
        label=label_doc,
        meta=dict(
            shipment_details=lib.to_dict(data.shipmentDetails) if data.shipmentDetails else None,
            documents=[lib.to_dict(doc) for doc in data.documents] if data.documents else None,
            charges=[lib.to_dict(charge) for charge in data.shipmentCharges] if data.shipmentCharges else None,
        ),
    )


def shipment_request(payload: models.ShipmentRequest, settings: provider_utils.Settings) -> lib.Serializable:
    """Create shipment request for DHL eCommerce Europe."""
    
    packages = payload.packages
    service = payload.service or "V01PAK"
    
    request_data = {
        "plannedShippingDateAndTime": lib.fdatetime(
            payload.shipment_date or lib.fnow(),
            "%Y-%m-%dT%H:%M:%S"
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
        "productCode": service,
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
                    "addressLine2": payload.shipper.address_line2,
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
                    "addressLine2": payload.recipient.address_line2,
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
                "customerReferences": [
                    {"value": package.parcel_id, "typeCode": "CU"}
                ] if package.parcel_id else [],
            }
            for package in packages
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

    return lib.Serializable(request_data) 