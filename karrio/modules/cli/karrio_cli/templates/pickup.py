from jinja2 import Template

PROVIDER_PICKUP_CREATE_TEMPLATE = Template(
    '''"""Karrio {{name}} pickup API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract pickup details
    pickup = _extract_details(response, settings)

    return pickup, messages


def _extract_details(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from carrier response data

    data: The carrier-specific pickup response data
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    {% if is_xml_api %}
    # Example implementation for XML response:
    # Extract pickup details from the XML response
    # confirmation_number = lib.find_element("confirmation-number", response, first=True).text
    # pickup_date = lib.find_element("pickup-date", response, first=True).text
    # ready_time = lib.find_element("ready-time", response, first=True).text
    # closing_time = lib.find_element("closing-time", response, first=True).text

    # For development, return sample data
    confirmation_number = "PICKUP123"
    pickup_date = lib.today_str()
    ready_time = "09:00"
    closing_time = "17:00"
    {% else %}
    # Example implementation for JSON response:
    # Extract pickup details from the JSON response
    # confirmation_number = response.get("confirmationNumber")
    # pickup_date = response.get("pickupDate")
    # ready_time = response.get("readyTime")
    # closing_time = response.get("closingTime")

    # For development, return sample data
    confirmation_number = "PICKUP123"
    pickup_date = lib.today_str()
    ready_time = "09:00"
    closing_time = "17:00"
    {% endif %}

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup_date),
        ready_time=ready_time,
        closing_time=closing_time,
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a pickup request for the carrier API

    payload: The standardized PickupRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract pickup details
    address = lib.to_address(payload.address)
    pickup_date = payload.pickup_date or lib.today_str()
    ready_time = payload.ready_time or "09:00"
    closing_time = payload.closing_time or "17:00"

    {% if is_xml_api %}
    # Example implementation for XML request:
    request = f"""<?xml version="1.0"?>
<pickup-request>
    <pickup-date>{pickup_date}</pickup-date>
    <ready-time>{ready_time}</ready-time>
    <closing-time>{closing_time}</closing-time>
    <address>
        <address-line1>{address.address_line1}</address-line1>
        <city>{address.city}</city>
        <postal-code>{address.postal_code}</postal-code>
        <country-code>{address.country_code}</country-code>
        <state-code>{address.state_code}</state-code>
        <person-name>{address.person_name}</person-name>
        <company-name>{address.company_name}</company-name>
        <phone-number>{address.phone_number}</phone-number>
        <email>{address.email}</email>
    </address>
</pickup-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Example implementation for JSON request:
    request = {
        "pickupDate": pickup_date,
        "readyTime": ready_time,
        "closingTime": closing_time,
        "address": {
            "addressLine1": address.address_line1,
            "city": address.city,
            "postalCode": address.postal_code,
            "countryCode": address.country_code,
            "stateCode": address.state_code,
            "personName": address.person_name,
            "companyName": address.company_name,
            "phoneNumber": address.phone_number,
            "email": address.email,
        }
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}
'''
)

PROVIDER_PICKUP_UPDATE_TEMPLATE = Template('''"""Karrio {{name}} pickup update API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_pickup_update_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup update response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract updated pickup details
    pickup = _extract_details(response, settings)

    return pickup, messages


def _extract_details(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from carrier response data

    data: The carrier-specific pickup response data
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    {% if is_xml_api %}
    # Example implementation for XML response:
    # Extract pickup details from the XML response
    # confirmation_number = lib.find_element("confirmation-number", response, first=True).text
    # pickup_date = lib.find_element("pickup-date", response, first=True).text
    # ready_time = lib.find_element("ready-time", response, first=True).text
    # closing_time = lib.find_element("closing-time", response, first=True).text

    # For development, return sample data
    confirmation_number = "PICKUP123"
    pickup_date = lib.today_str()
    ready_time = "10:00"
    closing_time = "18:00"
    {% else %}
    # Example implementation for JSON response:
    # Extract pickup details from the JSON response
    # confirmation_number = response.get("confirmationNumber")
    # pickup_date = response.get("pickupDate")
    # ready_time = response.get("readyTime")
    # closing_time = response.get("closingTime")

    # For development, return sample data
    confirmation_number = "PICKUP123"
    pickup_date = lib.today_str()
    ready_time = "10:00"
    closing_time = "18:00"
    {% endif %}

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup_date),
        ready_time=ready_time,
        closing_time=closing_time,
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a pickup update request for the carrier API

    payload: The standardized PickupUpdateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract pickup update details
    confirmation_number = payload.confirmation_number
    address = lib.to_address(payload.address)
    pickup_date = payload.pickup_date or lib.today_str()
    ready_time = payload.ready_time or "10:00"
    closing_time = payload.closing_time or "18:00"

    {% if is_xml_api %}
    # Example implementation for XML request:
    request = f"""<?xml version="1.0"?>
<pickup-update-request>
    <confirmation-number>{confirmation_number}</confirmation-number>
    <pickup-date>{pickup_date}</pickup-date>
    <ready-time>{ready_time}</ready-time>
    <closing-time>{closing_time}</closing-time>
    <address>
        <address-line1>{address.address_line1}</address-line1>
        <city>{address.city}</city>
        <postal-code>{address.postal_code}</postal-code>
        <country-code>{address.country_code}</country-code>
        <state-code>{address.state_code}</state-code>
        <person-name>{address.person_name}</person-name>
        <company-name>{address.company_name}</company-name>
        <phone-number>{address.phone_number}</phone-number>
        <email>{address.email}</email>
    </address>
</pickup-update-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Example implementation for JSON request:
    request = {
        "confirmationNumber": confirmation_number,
        "pickupDate": pickup_date,
        "readyTime": ready_time,
        "closingTime": closing_time,
        "address": {
            "addressLine1": address.address_line1,
            "city": address.city,
            "postalCode": address.postal_code,
            "countryCode": address.country_code,
            "stateCode": address.state_code,
            "personName": address.person_name,
            "companyName": address.company_name,
            "phoneNumber": address.phone_number,
            "email": address.email,
        }
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}
'''
)

PROVIDER_PICKUP_CANCEL_TEMPLATE = Template('''"""Karrio {{name}} pickup cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[{% if is_xml_api %}lib.Element{% else %}dict{% endif %}],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse pickup cancellation response from carrier API"""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if cancellation was successful
    success = _extract_cancellation_status(response)
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Pickup",
        ) if success else None
    )

    return confirmation, messages


def _extract_cancellation_status(
    response: {% if is_xml_api %}lib.Element{% else %}dict{% endif %}
) -> bool:
    """Extract cancellation success status from carrier response"""
    {% if is_xml_api %}
    # Example implementation for XML response:
    # status_node = lib.find_element("status", response, first=True)
    # return status_node is not None and status_node.text.lower() == "cancelled"

    # For development, always return success
    return True
    {% else %}
    # Example implementation for JSON response:
    # return response.get("status", "").lower() == "cancelled"

    # For development, always return success
    return True
    {% endif %}


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup cancellation request for carrier API"""
    # Extract cancellation details
    confirmation_number = payload.confirmation_number

    {% if is_xml_api %}
    # Example implementation for XML request:
    request = f"""<?xml version="1.0"?>
<pickup-cancel-request>
    <confirmation-number>{confirmation_number}</confirmation-number>
</pickup-cancel-request>"""

    return lib.Serializable(request, lambda r: r)
    {% else %}
    # Example implementation for JSON request:
    request = {
        "confirmationNumber": confirmation_number
    }

    return lib.Serializable(request, lib.to_dict)
    {% endif %}
'''
)

PROVIDER_PICKUP_IMPORTS_TEMPLATE = Template(
    '''"""Karrio {{name}} pickup API imports."""

from karrio.providers.{{id}}.pickup.create import (
    parse_pickup_response,
    pickup_request,
)
from karrio.providers.{{id}}.pickup.update import (
    parse_pickup_update_response,
    pickup_update_request,
)
from karrio.providers.{{id}}.pickup.cancel import (
    parse_pickup_cancel_response,
    pickup_cancel_request,
)
'''
)


# XML schema templates for pickup operations
XML_SCHEMA_PICKUP_CREATE_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-request" xmlns="http://{{id}}.com/ws/pickup-request" elementFormDefault="qualified">
    <xsd:element name="pickup-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="account-number" type="xsd:string" minOccurs="0" />
                <xsd:element name="pickup-date" type="xsd:date" />
                <xsd:element name="ready-time" type="xsd:string" />
                <xsd:element name="closing-time" type="xsd:string" />
                <xsd:element name="instruction" type="xsd:string" minOccurs="0" />
                <xsd:element name="address">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" />
                            <xsd:element name="street" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="state" type="xsd:string" minOccurs="0" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country" type="xsd:string" />
                            <xsd:element name="phone" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="parcel-count" type="xsd:integer" minOccurs="0" />
                <xsd:element name="weight" type="xsd:decimal" minOccurs="0" />
                <xsd:element name="weight-unit" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_PICKUP_CREATE_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-response" xmlns="http://{{id}}.com/ws/pickup-response" elementFormDefault="qualified">
    <xsd:element name="pickup-response">
                    <xsd:complexType>
                        <xsd:all>
                <xsd:element name="confirmation-number" type="xsd:string" />
                <xsd:element name="pickup-date" type="xsd:date" />
                <xsd:element name="ready-time" type="xsd:string" minOccurs="0" />
                <xsd:element name="closing-time" type="xsd:string" minOccurs="0" />
                <xsd:element name="status" type="xsd:string" minOccurs="0" />
                <xsd:element name="request-id" type="xsd:string" minOccurs="0" />
                        </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_PICKUP_UPDATE_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-update-request" xmlns="http://{{id}}.com/ws/pickup-update-request" elementFormDefault="qualified">
    <xsd:element name="pickup-update-request">
                    <xsd:complexType>
                        <xsd:all>
                <xsd:element name="confirmation-number" type="xsd:string" />
                <xsd:element name="account-number" type="xsd:string" minOccurs="0" />
                <xsd:element name="pickup-date" type="xsd:date" />
                <xsd:element name="ready-time" type="xsd:string" />
                <xsd:element name="closing-time" type="xsd:string" />
                <xsd:element name="instruction" type="xsd:string" minOccurs="0" />
                <xsd:element name="address">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="company-name" type="xsd:string" minOccurs="0" />
                            <xsd:element name="person-name" type="xsd:string" />
                            <xsd:element name="street" type="xsd:string" />
                            <xsd:element name="city" type="xsd:string" />
                            <xsd:element name="state" type="xsd:string" minOccurs="0" />
                            <xsd:element name="postal-code" type="xsd:string" />
                            <xsd:element name="country" type="xsd:string" />
                            <xsd:element name="phone" type="xsd:string" minOccurs="0" />
                            <xsd:element name="email" type="xsd:string" minOccurs="0" />
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="parcel-count" type="xsd:integer" minOccurs="0" />
                <xsd:element name="weight" type="xsd:decimal" minOccurs="0" />
                <xsd:element name="weight-unit" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_PICKUP_UPDATE_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-update-response" xmlns="http://{{id}}.com/ws/pickup-update-response" elementFormDefault="qualified">
    <xsd:element name="pickup-update-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="confirmation-number" type="xsd:string" />
                <xsd:element name="pickup-date" type="xsd:date" />
                <xsd:element name="ready-time" type="xsd:string" minOccurs="0" />
                <xsd:element name="closing-time" type="xsd:string" minOccurs="0" />
                <xsd:element name="status" type="xsd:string" minOccurs="0" />
                <xsd:element name="request-id" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_PICKUP_CANCEL_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-cancel-request" xmlns="http://{{id}}.com/ws/pickup-cancel-request" elementFormDefault="qualified">
    <xsd:element name="pickup-cancel-request">
                    <xsd:complexType>
                        <xsd:all>
                <xsd:element name="confirmation-number" type="xsd:string" />
                <xsd:element name="pickup-date" type="xsd:date" minOccurs="0" />
                <xsd:element name="reason" type="xsd:string" minOccurs="0" />
                <xsd:element name="account-number" type="xsd:string" minOccurs="0" />
                        </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

XML_SCHEMA_PICKUP_CANCEL_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/pickup-cancel-response" xmlns="http://{{id}}.com/ws/pickup-cancel-response" elementFormDefault="qualified">
    <xsd:element name="pickup-cancel-response">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="status" type="xsd:string" />
                <xsd:element name="confirmation-number" type="xsd:string" minOccurs="0" />
                <xsd:element name="status-message" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
"""
)

# JSON schema templates for pickup operations
JSON_SCHEMA_PICKUP_CREATE_REQUEST_TEMPLATE = Template(
    """{
  "pickupRequest": {
    "accountNumber": "123456",
    "pickupDate": "2023-06-01",
    "readyTime": "09:00",
    "closingTime": "17:00",
    "instruction": "Please knock loudly",
    "address": {
      "companyName": "ACME Corp",
      "personName": "John Doe",
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postalCode": "12345",
      "country": "US",
      "phone": "555-123-4567",
      "email": "john@example.com"
    },
    "parcelCount": 3,
    "weight": 10.5,
    "weightUnit": "KG"
  }
}
"""
)

JSON_SCHEMA_PICKUP_CREATE_RESPONSE_TEMPLATE = Template(
    """{
  "pickupResponse": {
    "confirmationNumber": "PICKUP123456",
    "pickupDate": "2023-06-01",
    "readyTime": "09:00",
    "closingTime": "17:00",
    "status": "scheduled",
    "requestId": "REQ123456"
  }
}
"""
)

JSON_SCHEMA_PICKUP_UPDATE_REQUEST_TEMPLATE = Template(
    """{
  "pickupUpdateRequest": {
    "confirmationNumber": "PICKUP123456",
    "accountNumber": "123456",
    "pickupDate": "2023-06-01",
    "readyTime": "10:00",
    "closingTime": "18:00",
    "instruction": "Please knock loudly and call before arrival",
    "address": {
      "companyName": "ACME Corp",
      "personName": "John Doe",
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postalCode": "12345",
      "country": "US",
      "phone": "555-123-4567",
      "email": "john@example.com"
    },
    "parcelCount": 5,
    "weight": 15.5,
    "weightUnit": "KG"
  }
}
"""
)

JSON_SCHEMA_PICKUP_UPDATE_RESPONSE_TEMPLATE = Template(
    """{
  "pickupUpdateResponse": {
    "confirmationNumber": "PICKUP123456",
    "pickupDate": "2023-06-01",
    "readyTime": "10:00",
    "closingTime": "18:00",
    "status": "modified",
    "requestId": "REQ123456"
  }
}
"""
)

JSON_SCHEMA_PICKUP_CANCEL_REQUEST_TEMPLATE = Template(
    """{
  "pickupCancelRequest": {
    "confirmationNumber": "PICKUP123456",
    "accountNumber": "123456",
    "pickupDate": "2023-06-01",
    "reason": "No longer needed"
  }
}
"""
)

JSON_SCHEMA_PICKUP_CANCEL_RESPONSE_TEMPLATE = Template(
    """{
  "pickupCancelResponse": {
    "status": "cancelled",
    "confirmationNumber": "PICKUP123456",
    "statusMessage": "Pickup successfully cancelled"
  }
}
"""
)


TEST_PICKUP_TEMPLATE = Template('''"""{{name}} carrier pickup tests."""

import unittest
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from unittest.mock import patch
from .fixture import gateway


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Pickup.update(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/123/update"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Pickup.cancel(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/123/cancel"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
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
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "confirmation_number": "123"
}

PickupRequest = {% if is_xml_api %}{
    "address": {
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
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00"
}{% else %}{
    "address": {
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
    "pickupDate": "2024-01-01",
    "readyTime": "09:00",
    "closingTime": "17:00"
}{% endif %}

PickupResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<pickup-response>
    <confirmation-number>PICKUP123</confirmation-number>
    <pickup-date>2024-01-01</pickup-date>
    <ready-time>09:00</ready-time>
    <closing-time>17:00</closing-time>
    <status>scheduled</status>
</pickup-response>"""{% else %}"""{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-01",
  "readyTime": "09:00",
  "closingTime": "17:00",
  "status": "scheduled"
}"""{% endif %}

PickupUpdateResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<pickup-update-response>
    <confirmation-number>PICKUP123</confirmation-number>
    <pickup-date>2024-01-02</pickup-date>
    <ready-time>10:00</ready-time>
    <closing-time>18:00</closing-time>
    <status>updated</status>
</pickup-update-response>"""{% else %}"""{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-02",
  "readyTime": "10:00",
  "closingTime": "18:00",
  "status": "updated"
}"""{% endif %}

PickupCancelResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<pickup-cancel-response>
    <success>true</success>
    <message>Pickup successfully cancelled</message>
</pickup-cancel-response>"""{% else %}"""{
  "success": true,
  "message": "Pickup successfully cancelled"
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>pickup_error</code>
        <message>Unable to schedule pickup</message>
        <details>Invalid pickup date provided</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "pickup_error",
    "message": "Unable to schedule pickup",
    "details": "Invalid pickup date provided"
  }
}"""{% endif %}

ParsedPickupResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "confirmation_number": "PICKUP123",
        "pickup_date": "2024-01-01",
        "ready_time": "09:00",
        "closing_time": "17:00",
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "pickup_error",
            "message": "Unable to schedule pickup",
            "details": {
                "details": "Invalid pickup date provided"
            }
        }
    ]
]
'''
)
