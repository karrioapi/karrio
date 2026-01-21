import json
from time import sleep
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, ANY
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
import karrio.server.manager.models as models
import karrio.server.manager.serializers as serializers


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

            self.assertResponseNoErrors(response)
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
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

        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertDictEqual(response_data, TRACKING_RESPONSE)
        self.assertEqual(len(self.user.tracking_set.all()), 1)


class TestTrackersUpdate(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tracker = models.Tracking.objects.create(
            **{
                "tracking_number": "00340434292135100124",
                "test_mode": True,
                "delivered": False,
                "events": [
                    {
                        "date": "2021-01-11",
                        "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
                        "location": "BONN",
                        "code": "pre-transit",
                        "time": "20:34",
                    }
                ],
                "status": "in_transit",
                "created_by": self.user,
                "carrier": create_carrier_snapshot(self.dhl_carrier),
                "info": {
                    "carrier_tracking_link": "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=00340434292135100124",
                    "package_weight": 0.74,
                    "package_weight_unit": "KG",
                    "shipping_date": "2021-01-11",
                },
            }
        )

    def test_update_tracker_info(self):
        url = reverse(
            "karrio.server.manager:tracker-details",
            kwargs=dict(id_or_tracking_number=self.tracker.pk),
        )
        data = dict(info=TRACKING_INFO)

        response = self.client.put(url, data)
        response_data = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, UPDATE_TRACKING_RESPONSE)


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
    "estimated_delivery": ANY,
    "delivery_image_url": None,
    "signature_image_url": None,
    "events": [
        {
            "code": "KB",
            "date": "2010-08-30",
            "description": "UPS INTERNAL ACTIVITY CODE",
            "location": "BONN",
            "time": "10:39",
            "latitude": None,
            "longitude": None,
            "reason": None,
            "status": None,
            "timestamp": None,
        }
    ],
    "messages": [],
    "meta": {
        "ext": "ups",
        "carrier": "ups",
    },
    "metadata": {},
    "info": {
        "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z12345E6205277936/trackdetails",
        "customer_name": None,
        "expected_delivery": None,
        "note": None,
        "order_date": None,
        "order_id": None,
        "package_weight": None,
        "package_weight_unit": None,
        "shipment_delivery_date": None,
        "shipment_destination_country": None,
        "shipment_destination_postal_code": None,
        "shipment_origin_country": None,
        "shipment_origin_postal_code": None,
        "shipment_package_count": None,
        "shipment_pickup_date": None,
        "shipment_service": None,
        "shipping_date": None,
        "signed_by": None,
        "source": "api",
    },
}

TRACKING_INFO = {
    "shipment_service": "dhl_express_worldwide",
    "signed_by": "Jane Doe",
}

UPDATE_TRACKING_RESPONSE = {
    "id": ANY,
    "object_type": "tracker",
    "carrier_name": "dhl_express",
    "carrier_id": "dhl_express",
    "tracking_number": "00340434292135100124",
    "events": [
        {
            "date": "2021-01-11",
            "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
            "code": "pre-transit",
            "latitude": None,
            "location": "BONN",
            "longitude": None,
            "time": "20:34",
            "reason": None,
            "status": None,
            "timestamp": None,
        }
    ],
    "delivered": False,
    "test_mode": True,
    "status": "in_transit",
    "estimated_delivery": ANY,
    "delivery_image_url": None,
    "signature_image_url": None,
    "messages": [],
    "meta": {},
    "metadata": {},
    "info": {
        "carrier_tracking_link": "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=00340434292135100124",
        "customer_name": None,
        "expected_delivery": None,
        "note": None,
        "order_date": None,
        "order_id": None,
        "package_weight": "0.74",
        "package_weight_unit": "KG",
        "shipment_delivery_date": None,
        "shipment_destination_country": None,
        "shipment_destination_postal_code": None,
        "shipment_origin_country": None,
        "shipment_origin_postal_code": None,
        "shipment_package_count": None,
        "shipment_pickup_date": None,
        "shipment_service": "dhl_express_worldwide",
        "shipping_date": "2021-01-11",
        "signed_by": "Jane Doe",
        "source": None,
    },
}


class TestTrackerEstimatedDelivery(APITestCase):
    """Test estimated_delivery computation and sync."""

    def setUp(self) -> None:
        super().setUp()
        self.tracker = models.Tracking.objects.create(
            **{
                "tracking_number": "TEST123456789",
                "test_mode": True,
                "delivered": False,
                "events": [
                    {
                        "date": "2024-01-15",
                        "description": "Label created",
                        "code": "pending",
                        "time": "10:00",
                    }
                ],
                "status": "pending",
                "estimated_delivery": "2024-01-20",
                "created_by": self.user,
                "carrier": create_carrier_snapshot(self.dhl_carrier),
                "info": {
                    "shipping_date": "2024-01-15",
                    "expected_delivery": "2024-01-20",
                },
            }
        )

    def test_update_tracker_syncs_estimated_delivery_to_info(self):
        """Test that when estimated_delivery is updated, info.expected_delivery is also updated."""
        tracking_details = {
            "estimated_delivery": "2024-01-22",
        }

        serializers.tracking.update_tracker(self.tracker, tracking_details)
        self.tracker.refresh_from_db()

        self.assertEqual(self.tracker.estimated_delivery.isoformat(), "2024-01-22")
        self.assertEqual(self.tracker.info.get("expected_delivery"), "2024-01-22")

    def test_update_tracker_carrier_estimated_delivery_supersedes_info(self):
        """Test that carrier's estimated_delivery supersedes existing info.expected_delivery."""
        # First set a different expected_delivery in info
        self.tracker.info = {**self.tracker.info, "expected_delivery": "2024-01-18"}
        self.tracker.save()

        # Update with carrier's estimated_delivery
        tracking_details = {
            "estimated_delivery": "2024-01-25",
            "info": {"customer_name": "John Doe"},
        }

        serializers.tracking.update_tracker(self.tracker, tracking_details)
        self.tracker.refresh_from_db()

        # Carrier's estimated_delivery should supersede
        self.assertEqual(self.tracker.estimated_delivery.isoformat(), "2024-01-25")
        self.assertEqual(self.tracker.info.get("expected_delivery"), "2024-01-25")
        self.assertEqual(self.tracker.info.get("customer_name"), "John Doe")
