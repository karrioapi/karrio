from jinja2 import Template

PROVIDER_TRACKING_TEMPLATE = Template('''"""Karrio {{name}} tracking API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract tracking details and events from the response to populate TrackingDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., TrackingRequestType),
# while XML schema types don't have this suffix (e.g., TrackingRequest).

import karrio.schemas.{{id}}.tracking_request as {{id}}_req
import karrio.schemas.{{id}}.tracking_response as {{id}}_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils
import karrio.providers.{{id}}.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, {% if is_xml_api %}lib.Element{% else %}dict{% endif %}]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
    ]

    return tracking_details, messages


def _extract_details(
    data: {% if is_xml_api %}lib.Element{% else %}dict{% endif %},
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """
    Extract tracking details from carrier response data

    data: The carrier-specific tracking data structure
    settings: The carrier connection settings
    tracking_number: The tracking number being tracked

    Returns a TrackingDetails object with extracted tracking information
    """
    # Convert the carrier data to a proper object for easy attribute access
    {% if is_xml_api %}
    # For XML APIs, convert Element to proper response object
    tracking_details = lib.to_object({{id}}_res.TrackingDetails, data)

    # Extract tracking status and information
    status_code = tracking_details.status_code if hasattr(tracking_details, 'status_code') else ""
    status_detail = tracking_details.status_description if hasattr(tracking_details, 'status_description') else ""
    est_delivery = tracking_details.estimated_delivery_date if hasattr(tracking_details, 'estimated_delivery_date') else None

    # Extract events
    events = []
    if hasattr(tracking_details, 'events') and tracking_details.events:
        for event in tracking_details.events.event:
            events.append({
                "date": event.date if hasattr(event, 'date') else "",
                "time": event.time if hasattr(event, 'time') else "",
                "code": event.code if hasattr(event, 'code') else "",
                "description": event.description if hasattr(event, 'description') else "",
                "location": event.location if hasattr(event, 'location') else ""
            })
    {% else %}
    # For JSON APIs, convert dict to proper response object
    tracking_details = lib.to_object({{id}}_res.TrackingResponseType, data)

    # Extract tracking status and information
    status_code = tracking_details.statusCode if hasattr(tracking_details, 'statusCode') else ""
    status_detail = tracking_details.statusDescription if hasattr(tracking_details, 'statusDescription') else ""
    est_delivery = tracking_details.estimatedDeliveryDate if hasattr(tracking_details, 'estimatedDeliveryDate') else None

    # Extract events
    events = []
    if hasattr(tracking_details, 'events') and tracking_details.events:
        for event in tracking_details.events:
            events.append({
                "date": event.date if hasattr(event, 'date') else "",
                "time": event.time if hasattr(event, 'time') else "",
                "code": event.code if hasattr(event, 'code') else "",
                "description": event.description if hasattr(event, 'description') else "",
                "location": event.location if hasattr(event, 'location') else ""
            })
    {% endif %}

    # Map carrier status to karrio standard tracking status
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if status_code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event["date"]),
                description=event["description"],
                code=event["code"],
                time=lib.flocaltime(event["time"]),
                location=event["location"],
            )
            for event in events
        ],
        estimated_delivery=lib.fdate(est_delivery) if est_delivery else None,
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a tracking request for the carrier API

    payload: The standardized TrackingRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract the tracking number(s) from payload
    tracking_numbers = payload.tracking_numbers
    reference = payload.reference

    {% if is_xml_api %}
    # For XML API request
    request = {{id}}_req.TrackingRequest(
        tracking_numbers=tracking_numbers,
        # Add required tracking request details
        reference=reference,
        language=payload.language_code or "en",
        # Add account credentials
        account_number=settings.account_number,
    )
    {% else %}
    # For JSON API request
    request = {{id}}_req.TrackingRequestType(
        trackingInfo={
            "trackingNumbers": tracking_numbers,
            "reference": reference,
            "language": payload.language_code or "en",
        },
        # Add account credentials
        accountNumber=settings.account_number,
    )
    {% endif %}

    return lib.Serializable(request, {% if is_xml_api %}lib.to_xml{% else %}lib.to_dict{% endif %})

'''
)

TEST_TRACKING_TEMPLATE = Template('''"""{{name}} carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Tracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["TRACK123"],
    "reference": "ORDER123"
}

TrackingRequest = {% if is_xml_api %}{
    "tracking_numbers": [
        "TRACK123"
    ],
    "reference": "ORDER123"
}{% else %}{
  "trackingNumbers": [
    "TRACK123"
  ],
  "reference": "ORDER123"
}{% endif %}

TrackingResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<tracking-response>
    <tracking-info>
        <tracking-number>TRACK123</tracking-number>
        <status>in_transit</status>
        <status-details>Package is in transit</status-details>
        <estimated-delivery>2024-04-15</estimated-delivery>
        <events>
            <event>
                <date>2024-04-12</date>
                <time>14:30:00</time>
                <code>PU</code>
                <description>Package picked up</description>
                <location>San Francisco, CA</location>
            </event>
        </events>
    </tracking-info>
</tracking-response>"""{% else %}"""{
  "trackingInfo": [
    {
      "trackingNumber": "TRACK123",
      "status": "in_transit",
      "statusDetails": "Package is in transit",
      "estimatedDelivery": "2024-04-15",
      "events": [
        {
          "date": "2024-04-12",
          "time": "14:30:00",
          "code": "PU",
          "description": "Package picked up",
          "location": "San Francisco, CA"
        }
      ]
    }
  ]
}"""{% endif %}

ErrorResponse = {% if is_xml_api %}"""<?xml version="1.0"?>
<error-response>
    <e>
        <code>tracking_error</code>
        <message>Unable to track shipment</message>
        <details>Invalid tracking number</details>
    </e>
</error-response>"""{% else %}"""{
  "error": {
    "code": "tracking_error",
    "message": "Unable to track shipment",
    "details": "Invalid tracking number"
  }
}"""{% endif %}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "tracking_number": "TRACK123",
            "events": [
                {
                    "date": "2024-04-12",
                    "time": "14:30:00",
                    "code": "PU",
                    "description": "Package picked up",
                    "location": "San Francisco, CA"
                }
            ],
            "estimated_delivery": "2024-04-15",
            "status": "in_transit"
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "tracking_error",
            "message": "Unable to track shipment",
            "details": {
                "details": "Invalid tracking number"
            }
        }
    ]
]'''
)

XML_SCHEMA_TRACKING_REQUEST_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/tracking" xmlns="http://{{id}}.com/ws/tracking" elementFormDefault="qualified">
    <xsd:element name="tracking-request">
        <xsd:complexType>
            <xsd:all>
                <xsd:element name="tracking-numbers">
                    <xsd:complexType>
                        <xsd:sequence>
                            <xsd:element name="tracking-number" type="xsd:string" maxOccurs="unbounded" />
                        </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
                <xsd:element name="language-code" type="xsd:string" minOccurs="0" />
                <xsd:element name="reference" type="xsd:string" minOccurs="0" />
            </xsd:all>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
""")

XML_SCHEMA_TRACKING_RESPONSE_TEMPLATE = Template("""<?xml version="1.0"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://{{id}}.com/ws/tracking" xmlns="http://{{id}}.com/ws/tracking" elementFormDefault="qualified">
    <xsd:element name="tracking-response">
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="tracking-info" maxOccurs="unbounded">
                    <xsd:complexType>
                        <xsd:all>
                            <xsd:element name="tracking-number" type="xsd:string" />
                            <xsd:element name="status" type="xsd:string" />
                            <xsd:element name="status-details" type="xsd:string" minOccurs="0" />
                            <xsd:element name="estimated-delivery" type="xsd:date" minOccurs="0" />
                            <xsd:element name="events">
                                <xsd:complexType>
                                    <xsd:sequence>
                                        <xsd:element name="event" maxOccurs="unbounded">
                                            <xsd:complexType>
                                                <xsd:all>
                                                    <xsd:element name="date" type="xsd:date" />
                                                    <xsd:element name="time" type="xsd:time" />
                                                    <xsd:element name="code" type="xsd:string" />
                                                    <xsd:element name="description" type="xsd:string" />
                                                    <xsd:element name="location" type="xsd:string" minOccurs="0" />
                                                </xsd:all>
                                            </xsd:complexType>
                                        </xsd:element>
                                    </xsd:sequence>
                                </xsd:complexType>
                            </xsd:element>
                        </xsd:all>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
""")

JSON_SCHEMA_TRACKING_REQUEST_TEMPLATE = Template(
    """{
  "trackingRequest": {
    "trackingNumbers": [
      "1Z999999999999999"
    ],
    "languageCode": "en",
    "reference": "ORDER123"
  }
}
"""
)

JSON_SCHEMA_TRACKING_RESPONSE_TEMPLATE = Template(
    """{
  "trackingResponse": {
    "trackingInfo": [
      {
        "trackingNumber": "1Z999999999999999",
        "status": "in_transit",
        "statusDetails": "Package is in transit",
        "estimatedDelivery": "2024-04-15",
        "events": [
          {
            "date": "2024-04-12",
            "time": "14:30:00",
            "code": "PU",
            "description": "Package picked up",
            "location": "San Francisco, CA"
          },
          {
            "date": "2024-04-13",
            "time": "09:15:00",
            "code": "IT",
            "description": "In transit",
            "location": "Los Angeles, CA"
          }
        ]
      }
    ]
  }
}
"""
)
