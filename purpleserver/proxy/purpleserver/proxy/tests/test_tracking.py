import json
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from purplship.core.models import TrackingDetails, TrackingEvent
from purpleserver.core.tests import APITestCase


class TestTracking(APITestCase):

    def test_tracking_shipment(self):
        url = reverse(
            'purpleserver.proxy:shipment-tracking',
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_name="ups")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.get(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, TRACKING_RESPONSE)


RETURNED_VALUE = (
    [
        TrackingDetails(
            carrier_id="ups",
            carrier_name="ups",
            tracking_number="1Z12345E6205277936",
            events=[
                TrackingEvent(
                    code="KB",
                    date="2010-08-30",
                    description="UPS INTERNAL ACTIVITY CODE",
                    location="BONN",
                    time="10:39"
                )
            ]
        )
    ],
    [],
)

TRACKING_RESPONSE = {
  "trackingDetails": {
    "carrierId": "ups",
    "carrierName": "ups",
    "events": [
      {
        "code": "KB",
        "date": "2010-08-30",
        "description": "UPS INTERNAL ACTIVITY CODE",
        "location": "BONN",
        "time": "10:39"
      }
    ],
    "trackingNumber": "1Z12345E6205277936"
  }
}
