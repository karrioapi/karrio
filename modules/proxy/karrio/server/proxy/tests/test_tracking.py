import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase


class TestTracking(APITestCase):
    def test_tracking_shipment(self):
        url = reverse("karrio.server.proxy:get-tracking")
        data = dict(tracking_number="1Z12345E6205277936", carrier_name="ups")

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, TRACKING_RESPONSE)


RETURNED_VALUE = [
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
]

TRACKING_RESPONSE = {
    "messages": [],
    "tracking": {
        "id": ANY,
        "carrier_name": "ups",
        "carrier_id": "ups_package",
        "tracking_number": "1Z12345E6205277936",
        "images": None,
        "info": {
            "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z12345E6205277936/trackdetails",
            "customer_name": None,
            "expected_delivery": None,
            "note": None,
            "order_date": None,
            "order_id": None,
            "package_weight": None,
            "package_weight_unit": None,
            "shipment_package_count": None,
            "shipment_pickup_date": None,
            "shipment_delivery_date": None,
            "shipment_service": None,
            "shipment_origin_country": None,
            "shipment_origin_postal_code": None,
            "shipment_destination_country": None,
            "shipment_destination_postal_code": None,
            "shipping_date": None,
            "signed_by": None,
            "source": "api",
        },
        "events": [
            {
                "date": "2010-08-30",
                "description": "UPS INTERNAL ACTIVITY CODE",
                "location": "BONN",
                "code": "KB",
                "time": "10:39",
                "latitude": None,
                "longitude": None,
            }
        ],
        "delivered": None,
        "test_mode": True,
        "status": "in_transit",
        "estimated_delivery": ANY,
        "meta": {"ext": "ups", "carrier": "ups"},
        "object_type": "tracker",
        "metadata": {},
        "messages": [],
    },
}
