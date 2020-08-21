import json
from time import sleep
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import TrackingDetails, TrackingEvent
from purpleserver.core.tests import APITestCase


class TestShipmentTracking(APITestCase):

    def test_shipment_tracking(self):
        url = reverse(
            'purpleserver.manager:shipment-tracking',
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_id="ups")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.get(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, TRACKING_RESPONSE)

    def test_shipment_tracking_retry(self):
        url = reverse(
            'purpleserver.manager:shipment-tracking',
            kwargs=dict(tracking_number="1Z12345E6205277936", carrier_id="ups")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            self.client.get(url)
            sleep(2)

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, TRACKING_RESPONSE)
        self.assertEqual(len(self.user.tracking_set.all()), 1)


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
    "id": ANY,
    "carrierId": "ups",
    "carrierName": "ups",
    "trackingNumber": "1Z12345E6205277936",
    "shipmentId": None,
    "events": [
        {
            "code": "KB",
            "date": "2010-08-30",
            "description": "UPS INTERNAL ACTIVITY CODE",
            "location": "BONN",
            "signatory": None,
            "time": "10:39"
        }
    ]
}
