import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase


class TestTracking(APITestCase):
    def test_tracking_shipment(self):
        url = reverse(
            "karrio.server.proxy:shipment-tracking",
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_name="ups"),
        )

        with patch("karrio.server.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.get(f"{url}?test")
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, TRACKING_RESPONSE)


RETURNED_VALUE = (
    [
        TrackingDetails(
            carrier_id="ups_package",
            carrier_name="ups",
            tracking_number="1Z12345E6205277936",
            events=[
                TrackingEvent(
                    code="KB",
                    date="2010-08-30",
                    description="UPS INTERNAL ACTIVITY CODE",
                    location="BONN",
                    time="10:39",
                )
            ],
        )
    ],
    [],
)

TRACKING_RESPONSE = {
    "messages": [],
    "tracking": {
        "id": ANY,
        "object_type": "tracker",
        "carrier_id": "ups_package",
        "carrier_name": "ups",
        "delivered": None,
        "estimated_delivery": None,
        "events": [
            {
                "code": "KB",
                "date": "2010-08-30",
                "description": "UPS INTERNAL ACTIVITY CODE",
                "location": "BONN",
                "time": "10:39",
            }
        ],
        "messages": [],
        "metadata": {},
        "status": "in_transit",
        "test_mode": True,
        "tracking_number": "1Z12345E6205277936",
    },
}
