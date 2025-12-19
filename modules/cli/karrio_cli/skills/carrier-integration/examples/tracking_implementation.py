"""Example: Tracking Implementation Pattern

This example demonstrates the canonical pattern for implementing tracking functionality
in a Karrio carrier integration.
"""

# === FILE: karrio/providers/[carrier]/tracking.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].tracking_response as carrier_res


def parse_tracking_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    """Parse carrier tracking response into Karrio models.
    
    Handles multiple tracking numbers with concurrent responses.
    """
    responses = _response.deserialize()
    
    # Aggregate messages from all tracking responses (functional sum pattern)
    messages = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )
    
    # Extract tracking details for successful responses
    tracking_details = [
        _extract_details(tracking_number, response, settings)
        for tracking_number, response in responses
        if response and not _has_errors(response)
    ]
    
    return tracking_details, messages


def _has_errors(response: dict) -> bool:
    """Check if response contains errors."""
    return bool(response.get("errors", []))


def _extract_details(
    tracking_number: str,
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response.
    
    Use generated schema types for type-safe attribute access.
    """
    # Convert to typed object
    tracking = lib.to_object(carrier_res.TrackingResponseType, data)
    
    # Extract events using functional list comprehension
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.date, "%Y-%m-%dT%H:%M:%SZ"),
            time=lib.ftime(event.time, "%H:%M:%S") if hasattr(event, 'time') and event.time else None,
            description=lib.text(event.description),
            code=event.code if hasattr(event, 'code') else None,
            # Functional: join location parts, filter out None values
            location=", ".join(filter(None, [
                event.city if hasattr(event, 'city') else None,
                event.state if hasattr(event, 'state') else None,
                event.country if hasattr(event, 'country') else None,
            ])),
        )
        for event in (tracking.events or [])
    ]
    
    # Map carrier status to Karrio unified status
    status = provider_units.TrackingStatus.map(tracking.status).value
    
    # Determine if delivered
    delivered = status == models.TrackingStatus.delivered.value
    
    # Extract estimated delivery if available
    estimated_delivery = lib.fdate(
        tracking.estimatedDelivery, "%Y-%m-%dT%H:%M:%SZ"
    ) if hasattr(tracking, 'estimatedDelivery') and tracking.estimatedDelivery else None
    
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        status=status,
        events=events,
        delivered=delivered,
        estimated_delivery=estimated_delivery,
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(tracking_number) if hasattr(settings, 'tracking_url') else None,
            package_weight=tracking.weight if hasattr(tracking, 'weight') else None,
            shipping_date=lib.fdate(tracking.shipDate) if hasattr(tracking, 'shipDate') else None,
        ) if any([
            hasattr(settings, 'tracking_url'),
            hasattr(tracking, 'weight'),
            hasattr(tracking, 'shipDate'),
        ]) else None,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking request.
    
    For most carriers, tracking is a simple list of tracking numbers
    that will be processed concurrently by the proxy.
    """
    # Simply return the list of tracking numbers
    # The proxy will handle concurrent requests
    return lib.Serializable(payload.tracking_numbers)


# === FILE: karrio/mappers/[carrier]/proxy.py (tracking portion) ===

def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
    """Fetch tracking information for multiple tracking numbers.
    
    Uses lib.run_concurently for parallel API calls.
    """
    def _get_tracking(tracking_number: str):
        """Fetch single tracking number."""
        return tracking_number, lib.request(
            url=f"{self.settings.server_url}/tracking/{tracking_number}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Accept": "application/json",
            },
        )
    
    # Concurrent execution for all tracking numbers
    responses = lib.run_concurently(_get_tracking, request.serialize())
    
    return lib.Deserializable(
        responses,
        # Parse each response to dict, filter out empty responses
        lambda res: [
            (tracking_number, lib.to_dict(response))
            for tracking_number, response in res
            if any(response.strip())
        ],
    )


# === FILE: tests/[carrier]/test_tracking.py ===

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        print(f"Generated request: {request.serialize()}")
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertIn("/tracking/", mock.call_args[1]["url"])

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# Test Data Constants
TrackingPayload = {
    "tracking_numbers": ["1Z999AA10123456784"],
}

TrackingRequest = ["1Z999AA10123456784"]

TrackingResponse = """{
    "status": "IN_TRANSIT",
    "estimatedDelivery": "2024-01-20T14:00:00Z",
    "events": [
        {
            "date": "2024-01-18T10:30:00Z",
            "description": "Package arrived at distribution center",
            "code": "AR",
            "city": "Chicago",
            "state": "IL",
            "country": "US"
        },
        {
            "date": "2024-01-17T08:15:00Z",
            "description": "Package picked up",
            "code": "PU",
            "city": "New York",
            "state": "NY",
            "country": "US"
        }
    ]
}"""

ErrorResponse = """{
    "errors": [
        {
            "code": "TRACKING_NOT_FOUND",
            "message": "No tracking information found for this number"
        }
    ]
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "tracking_number": "1Z999AA10123456784",
            "status": "in_transit",
            "delivered": False,
            "estimated_delivery": "2024-01-20",
            "events": [
                {
                    "date": "2024-01-18",
                    "time": "10:30",
                    "description": "Package arrived at distribution center",
                    "code": "AR",
                    "location": "Chicago, IL, US",
                },
                {
                    "date": "2024-01-17",
                    "time": "08:15",
                    "description": "Package picked up",
                    "code": "PU",
                    "location": "New York, NY, US",
                },
            ],
        }
    ],
    [],  # Empty errors
]

ParsedErrorResponse = [
    [],  # Empty tracking details
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "code": "TRACKING_NOT_FOUND",
            "message": "No tracking information found for this number",
        }
    ],
]
