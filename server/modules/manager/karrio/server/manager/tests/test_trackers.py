import json
from time import sleep
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase


class TestTrackers(APITestCase):
    def test_shipment_tracking(self):
        url = reverse(
            "karrio.server.manager:shipment-tracker",
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_name="ups"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.get(f"{url}")
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, TRACKING_RESPONSE)

    def test_shipment_tracking_retry(self):
        url = reverse(
            "karrio.server.manager:shipment-tracker",
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_name="ups"),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            self.client.get(f"{url}")
            sleep(0.1)
            response = self.client.get(f"{url}")
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, TRACKING_RESPONSE)
        self.assertEqual(len(self.user.tracking_set.all()), 1)


RETURNED_VALUE = (
    [
        TrackingDetails(
            carrier_id="ups_package",
            carrier_name="ups",
            tracking_number="1Z12345E6205277936",
            delivered=False,
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
    "id": ANY,
    "object_type": "tracker",
    "carrier_id": "ups_package",
    "carrier_name": "ups",
    "tracking_number": "1Z12345E6205277936",
    "test_mode": True,
    "delivered": False,
    "status": "in_transit",
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
    "meta": {},
    "metadata": {},
}
