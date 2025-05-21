from jinja2 import Template

PROVIDER_SHIPMENT_IMPORTS_TEMPLATE = Template(
    """
from karrio.providers.{{id}}.shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.{{id}}.shipment.cancel import (
    parse_shipment_cancel_response,
    shipment_cancel_request,
)

"""
)

PROVIDER_SHIPMENT_CANCEL_TEMPLATE = Template(
    '''"""Karrio {{name}} shipment cancellation API implementation."""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """
    Parse shipment cancellation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ConfirmationDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract success state from the response
    success = _extract_cancellation_status(response)

    # Create confirmation details if successful
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def _extract_cancellation_status(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %}
) -> bool:
    """
    Extract cancellation success status from the carrier response

    response: The deserialized carrier response

    Returns True if cancellation was successful, False otherwise
    """
    {% if is_xml_api %}
    # Example implementation for XML response:
    # status_node = lib.find_element("shipment-status", response, first=True)
    # return status_node is not None and status_node.text.lower() == "cancelled"

    # For development, always return success
    return True
    {% else %}
    # Example implementation for JSON response:
    # return response.get("success", False)

    # For development, always return success
    return True
    {% endif %}


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment cancellation request for the carrier API

    payload: The standardized ShipmentCancelRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    {% if is_xml_api %}
    # Create XML request for shipment cancellation
    # Example implementation:
    # import karrio.schemas.{{id}}.shipment_cancel_request as {{id}}_req
    #
    # request = {{id}}_req.ShipmentCancelRequest(
    #     AccountNumber=settings.account_number,
    #     ShipmentReference=payload.shipment_identifier,
    #     # Add any other required fields
    # )
    #
    # return lib.Serializable(
    #     request,
    #     lambda _: lib.to_xml(
    #         _,
    #         name_="ShipmentCancelRequest",
    #         namespacedef_=(
    #             'xmlns="http://{{id}}.com/schema/shipment/cancel"'
    #         ),
    #     )
    # )

    # For development, return a simple XML request
    request = f"""<?xml version="1.0"?>
<shipment-cancel-request>
  <shipment-reference>{payload.shipment_identifier}</shipment-reference>
</shipment-cancel-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Create JSON request for shipment cancellation
    # Example implementation:
    # import karrio.schemas.{{id}}.shipment_cancel_request as {{id}}_req
    #
    # request = {{id}}_req.ShipmentCancelRequestType(
    #     shipmentId=payload.shipment_identifier,
    #     accountNumber=settings.account_number,
    #     # Add any other required fields
    # )
    #
    # return lib.Serializable(request, lib.to_dict)

    # For development, return a simple JSON request
    request = {
        "shipmentId": payload.shipment_identifier
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}

'''
)

PROVIDER_SHIPMENT_CREATE_TEMPLATE = Template(
    '''"""Karrio {{name}} shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.{{id}}.shipment_request as {{id}}_req
import karrio.schemas.{{id}}.shipment_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data
    {% if is_xml_api %}
    has_shipment = response.xpath(".//shipment") if hasattr(response, 'xpath') else False
    {% else %}
    has_shipment = "shipment" in response if hasattr(response, 'get') else False
    {% endif %}

    shipment = _extract_details(response, settings) if has_shipment else None

    return shipment, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """
    Extract shipment details from carrier response data

    data: The carrier-specific shipment data structure
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Convert the carrier data to a proper object for easy attribute access
    {% if is_xml_api %}
    # For XML APIs, convert Element to proper response object
    shipment = lib.to_object({{id}}_res.ShipmentResponse, data)

    # Extract tracking info
    tracking_number = shipment.tracking_number if hasattr(shipment, 'tracking_number') else ""
    shipment_id = shipment.shipment_id if hasattr(shipment, 'shipment_id') else ""

    # Extract label info
    label_format = shipment.label_format if hasattr(shipment, 'label_format') else "PDF"
    label_base64 = shipment.label_image if hasattr(shipment, 'label_image') else ""

    # Extract optional invoice
    invoice_base64 = shipment.invoice_image if hasattr(shipment, 'invoice_image') else ""

    # Extract service code for metadata
    service_code = shipment.service_code if hasattr(shipment, 'service_code') else ""
    {% else %}
    # For JSON APIs, convert dict to proper response object
    response_obj = lib.to_object({{id}}_res.ShipmentResponseType, data)

    # Access the shipment data
    shipment = response_obj.shipment if hasattr(response_obj, 'shipment') else None

    if shipment:
        # Extract tracking info
        tracking_number = shipment.trackingNumber if hasattr(shipment, 'trackingNumber') else ""
        shipment_id = shipment.shipmentId if hasattr(shipment, 'shipmentId') else ""

        # Extract label info
        label_data = shipment.labelData if hasattr(shipment, 'labelData') else None
        label_format = label_data.format if label_data and hasattr(label_data, 'format') else "PDF"
        label_base64 = label_data.image if label_data and hasattr(label_data, 'image') else ""

        # Extract optional invoice
        invoice_base64 = shipment.invoiceImage if hasattr(shipment, 'invoiceImage') else ""

        # Extract service code for metadata
        service_code = shipment.serviceCode if hasattr(shipment, 'serviceCode') else ""
    else:
        tracking_number = ""
        shipment_id = ""
        label_format = "PDF"
        label_base64 = ""
        invoice_base64 = ""
        service_code = ""
    {% endif %}

    documents = models.Documents(
        label=label_base64,
    )

    # Add invoice if present
    if invoice_base64:
        documents.invoice = invoice_base64

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type=label_format,
        docs=documents,
        meta=dict(
            service_code=service_code,
            # Add any other relevant metadata from the carrier's response
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for the carrier API

    payload: The standardized ShipmentRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.ShipmentRequest(
        # Map shipper details
        shipper={{id}}_req.Address(
            address_line1=shipper.address_line1,
            city=shipper.city,
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
            state_code=shipper.state_code,
            person_name=shipper.person_name,
            company_name=shipper.company_name,
            phone_number=shipper.phone_number,
            email=shipper.email,
        ),
        # Map recipient details
        recipient={{id}}_req.Address(
            address_line1=recipient.address_line1,
            city=recipient.city,
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
            state_code=recipient.state_code,
            person_name=recipient.person_name,
            company_name=recipient.company_name,
            phone_number=recipient.phone_number,
            email=recipient.email,
        ),
        # Map package details
        packages=[
            {{id}}_req.Package(
                weight=package.weight.value,
                weight_unit=provider_units.WeightUnit[package.weight.unit].value,
                length=package.length.value if package.length else None,
                width=package.width.value if package.width else None,
                height=package.height.value if package.height else None,
                dimension_unit=provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                packaging_type=provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            )
            for package in packages
        ],
        # Add service code
        service_code=service,
        # Add account information
        customer_number=settings.customer_number,
        # Add label details
        label_format=payload.label_type or "PDF",
        # Add any other required fields for the carrier API
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.ShipmentRequestType(
        # Map shipper details
        shipper={
            "addressLine1": shipper.address_line1,
            "city": shipper.city,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "stateCode": shipper.state_code,
            "personName": shipper.person_name,
            "companyName": shipper.company_name,
            "phoneNumber": shipper.phone_number,
            "email": shipper.email,
        },
        # Map recipient details
        recipient={
            "addressLine1": recipient.address_line1,
            "city": recipient.city,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "stateCode": recipient.state_code,
            "personName": recipient.person_name,
            "companyName": recipient.company_name,
            "phoneNumber": recipient.phone_number,
            "email": recipient.email,
        },
        # Map package details
        packages=[
            {
                "weight": package.weight.value,
                "weightUnit": provider_units.WeightUnit[package.weight.unit].value,
                "length": package.length.value if package.length else None,
                "width": package.width.value if package.width else None,
                "height": package.height.value if package.height else None,
                "dimensionUnit": provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                "packagingType": provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            }
            for package in packages
        ],
        # Add service code
        serviceCode=service,
        # Add account information
        customerNumber=settings.customer_number,
        # Add label details
        labelFormat=payload.label_type or "PDF",
        # Add any other required fields for this carrier's API
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})

'''
)


XML_SCHEMA_SHIPMENT_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/shipment" xmlns="http://{{id}}.com/ws/shipment" elementFormDefault="qualified">
    <xsd:element name="shipment-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="shipper">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="phone-number" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="recipient">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="address-line1" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country-code" type="xsd:string" />
                            <xsd:element name="state-code" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="phone-number" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="packages">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="package" maxOccurs="unbounded">
                                <xsd:complexType>
                                    <xsd:all>
                                        <xsd:element name="weight" type="xsd:decimal" />
                                        <xsd:element name="weight-unit" type="xsd:string" />
                                        <xsd:element name="length" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="width" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="height" type="xsd:decimal" minOccurs="0" />
                                        <xsd:element name="dimension-unit" type="xsd:string" minOccurs="0" />
                                        <xsd:element name="packaging-type" type="xsd:string" minOccurs="0" />
                                    </xsd:all>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="service" type="xsd:string" />
                <xsd:element name="options" type="xsd:string" minOccurs="0" />
                <xsd:element name="label-type" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_SHIPMENT_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/shipment" xmlns="http://{{id}}.com/ws/shipment" elementFormDefault="qualified">
    <xsd:element name="shipment-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="tracking-number" type="xsd:string" />
                <xsd:element name="shipment-identifier" type="xsd:string" />
                <xsd:element name="label-type" type="xsd:string" />
                <xsd:element name="label" type="xsd:base64Binary" />
                <xsd:element name="documents" minOccurs="0">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="invoice" type="xsd:base64Binary" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="meta" minOccurs="0">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="service-code" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

JSON_SCHEMA_SHIPMENT_REQUEST_TEMPLATE = Template(
    """{
  "shipmentRequest": {
    "shipper": {
      "addressLine1": "123 Main St",
      "city": "Anytown",
      "postalCode": "12345",
      "countryCode": "US",
      "stateCode": "CA",
      "personName": "John Doe",
      "companyName": "ACME Corp",
      "phoneNumber": "555-123-4567",
      "email": "john@example.com"
    },
    "recipient": {
      "addressLine1": "456 Oak St",
      "city": "Somewhere",
      "postalCode": "67890",
      "countryCode": "US",
      "stateCode": "NY",
      "personName": "Jane Smith",
      "companyName": "XYZ Inc",
      "phoneNumber": "555-987-6543",
      "email": "jane@example.com"
    },
    "packages": [
      {
        "weight": 10.5,
        "weightUnit": "KG",
        "length": 20.0,
        "width": 15.0,
        "height": 10.0,
        "dimensionUnit": "CM",
        "packagingType": "BOX"
      }
    ],
    "service": "EXPRESS",
    "options": {
      "insurance": true,
      "signature_required": false
    },
    "labelType": "PDF"
  }
}
"""
)

JSON_SCHEMA_SHIPMENT_RESPONSE_TEMPLATE = Template(
    """{
  "shipmentResponse": {
    "trackingNumber": "1Z999999999999999",
    "shipmentIdentifier": "SHIP123456",
    "labelType": "PDF",
    "label": "base64_encoded_label_data",
    "documents": {
      "invoice": "base64_encoded_invoice_data"
    },
    "meta": {
      "serviceCode": "EXPRESS"
    }
  }
}
"""
)

XML_SCHEMA_SHIPMENT_CANCEL_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/shipment-cancel" xmlns="http://{{id}}.com/ws/shipment-cancel" elementFormDefault="qualified">
    <xsd:element name="shipment-cancel-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="shipment-identifier" type="xsd:string" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_SHIPMENT_CANCEL_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/shipment-cancel" xmlns="http://{{id}}.com/ws/shipment-cancel" elementFormDefault="qualified">
    <xsd:element name="shipment-cancel-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="success" type="xsd:boolean" />
                <xsd:element name="message" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

JSON_SCHEMA_SHIPMENT_CANCEL_REQUEST_TEMPLATE = Template(
    """{
  "shipmentCancelRequest": {
    "shipmentIdentifier": "SHIP123456"
  }
}
"""
)

JSON_SCHEMA_SHIPMENT_CANCEL_RESPONSE_TEMPLATE = Template(
    """{
  "shipmentCancelResponse": {
    "success": true,
    "message": "Shipment successfully cancelled"
  }
}
"""
)

TEST_SHIPMENT_TEMPLATE = Template('''"""{{name}} carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class Test{{compact_name}}Shipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_shipment_cancel_request(self.ShipmentCancelRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/SHIP123456/cancel"
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 10.0,
        "height": 10.0,
        "length": 10.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }],
    "service": "express"
}

ShipmentCancelPayload = {
    "shipment_identifier": "SHIP123456"
}

ShipmentRequest = {% if is_xml_api %}{
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weight_unit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimension_unit": "CM",
            "packaging_type": "BOX"
        }
    ],
    "service_code": "express",
    "label_format": "PDF"
}{% else %}{
    "shipper": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weightUnit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimensionUnit": "CM",
            "packagingType": "BOX"
        }
    ],
    "serviceCode": "express",
    "labelFormat": "PDF"
}{% endif %}

ShipmentCancelRequest = {% if is_xml_api %}{
    "shipment_identifier": "SHIP123456"
}{% else %}{
    "shipmentIdentifier": "SHIP123456"
}{% endif %}

ShipmentResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<shipment-response>
    <tracking-number>1Z999999999999999</tracking-number>
    <shipment-id>SHIP123456</shipment-id>
    <label-format>PDF</label-format>
    <label-image>base64_encoded_label_data</label-image>
    <invoice-image>base64_encoded_invoice_data</invoice-image>
    <service-code>express</service-code>
</shipment-response>"""{% else %}"""{
  "shipment": {
    "trackingNumber": "1Z999999999999999",
    "shipmentId": "SHIP123456",
    "labelData": {
      "format": "PDF",
      "image": "base64_encoded_label_data"
    },
    "invoiceImage": "base64_encoded_invoice_data",
    "serviceCode": "express"
  }
}"""{% endif %}

ShipmentCancelResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<shipment-cancel-response>
    <success>true</success>
    <message>Shipment successfully cancelled</message>
</shipment-cancel-response>"""{% else %}"""{
  "success": true,
  "message": "Shipment successfully cancelled"
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>shipment_error</code>
        <message>Unable to create shipment</message>
        <details>Invalid shipment information provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "shipment_error",
    "message": "Unable to create shipment",
    "details": "Invalid shipment information provided"
  }
}"""{% endif %}

ParsedShipmentResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "tracking_number": "1Z999999999999999",
        "shipment_identifier": "SHIP123456",
        "label_type": "PDF",
        "docs": {
            "label": "base64_encoded_label_data",
            "invoice": "base64_encoded_invoice_data"
        },
        "meta": {
            "service_code": "express"
        }
    },
    []
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "success": True,
        "operation": "Cancel Shipment"
    },
    []
]

ParsedErrorResponse = [
    {},
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "shipment_error",
            "message": "Unable to create shipment",
            "details": {
                "details": "Invalid shipment information provided"
            }
        }
    ]
]''')
