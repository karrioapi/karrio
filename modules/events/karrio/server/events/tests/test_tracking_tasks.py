import json
import datetime
from time import sleep
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.manager import models
from karrio.server.events.task_definitions.base import tracking


class TestTrackersBackgroundUpdate(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        # Note: Events are stored without None fields (latitude, longitude, reason)
        # because lib.to_dict() with clear_empty=True strips None values when
        # processing mock events, and we need JSON hashes to match for deduplication
        trackers = [
            {
                "tracking_number": "1Z12345E6205277936",
                "test_mode": True,
                "delivered": False,
                "events": [
                    {
                        "date": "2012-10-04",
                        "description": "Order Processed: Ready for UPS",
                        "location": "FR",
                        "code": "MP",
                        "time": "13:58",
                    }
                ],
                "status": "in_transit",
                "created_by": self.user,
                "carrier": create_carrier_snapshot(self.ups_carrier),
                "info": {
                    "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z12345E6205277936/trackdetails",
                    "shipment_service": "UPS Ground",
                },
            },
            {
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
            },
        ]
        [models.Tracking.objects.create(**t) for t in trackers]

    def test_get_trackers(self):
        url = reverse("karrio.server.manager:trackers-list")

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TRACKERS_LIST, response_data)

    def test_dispatcher_groups_by_carrier(self):
        """update_trackers groups trackers by carrier_id and dispatches per-carrier tasks."""
        with patch(
            "karrio.server.events.task_definitions.base.process_carrier_tracking_batch"
        ) as mock_task:
            sleep(0.1)
            tracking.update_trackers(delta=datetime.timedelta(seconds=0.1))

            # 2 carriers (ups + dhl) → 2 dispatched tasks
            self.assertEqual(mock_task.call_count, 2)

            # Each call should have tracker_ids and schema kwargs
            for call_args in mock_task.call_args_list:
                self.assertIn("tracker_ids", call_args.kwargs)
                self.assertIn("schema", call_args.kwargs)
                self.assertIsInstance(call_args.kwargs["tracker_ids"], list)
                self.assertTrue(len(call_args.kwargs["tracker_ids"]) > 0)

    def test_dispatcher_passes_schema(self):
        """update_trackers forwards the schema kwarg to dispatched tasks."""
        with patch(
            "karrio.server.events.task_definitions.base.process_carrier_tracking_batch"
        ) as mock_task:
            sleep(0.1)
            tracking.update_trackers(
                delta=datetime.timedelta(seconds=0.1), schema="test_schema"
            )

            for call_args in mock_task.call_args_list:
                self.assertEqual(call_args.kwargs["schema"], "test_schema")

    def test_process_carrier_trackers_incremental_save(self):
        """process_carrier_trackers fetches and saves each batch immediately."""
        dhl_tracker = models.Tracking.objects.get(
            tracking_number="00340434292135100124"
        )

        with patch(
            "karrio.server.events.task_definitions.base.tracking.karrio"
        ) as mock_karrio:
            mock_karrio.Tracking.fetch.return_value.from_.return_value.parse.return_value = (
                RETURNED_UPDATED_VALUE
            )

            tracking.process_carrier_trackers(tracker_ids=[dhl_tracker.id])

        dhl_tracker.refresh_from_db()
        # RETURNED_UPDATED_VALUE has 2 events for DHL
        self.assertEqual(len(dhl_tracker.events), 2)

    def test_process_carrier_trackers_flat_delay(self):
        """process_carrier_trackers uses flat delays between batches (not progressive)."""
        # Create 15 additional UPS trackers → 16 total UPS → 2 batches
        for i in range(15):
            models.Tracking.objects.create(
                tracking_number=f"1Z12345E00{i:08d}",
                test_mode=True,
                delivered=False,
                events=[],
                status="in_transit",
                created_by=self.user,
                carrier=create_carrier_snapshot(self.ups_carrier),
            )

        ups_ids = list(
            models.Tracking.objects.filter(
                tracking_number__startswith="1Z12345E"
            ).values_list("id", flat=True)
        )

        with patch(
            "karrio.server.events.task_definitions.base.tracking.karrio"
        ) as mock_karrio, patch(
            "karrio.server.events.task_definitions.base.tracking.time.sleep"
        ) as mock_sleep:
            mock_karrio.Tracking.fetch.return_value.from_.return_value.parse.return_value = (
                [], []
            )

            tracking.process_carrier_trackers(tracker_ids=ups_ids)

        # 16 trackers / 10 per batch = 2 batches → 1 sleep between batches
        self.assertEqual(mock_sleep.call_count, 1)
        # Flat delay (not progressive)
        mock_sleep.assert_called_with(tracking.TRACKER_BATCH_DELAY)

    def test_get_updated_trackers(self):
        """End-to-end: process_carrier_trackers updates trackers visible via API."""
        url = reverse("karrio.server.manager:trackers-list")

        dhl_ids = list(
            models.Tracking.objects.filter(
                tracking_number="00340434292135100124"
            ).values_list("id", flat=True)
        )

        with patch(
            "karrio.server.events.task_definitions.base.tracking.karrio"
        ) as mock_karrio:
            mock_karrio.Tracking.fetch.return_value.from_.return_value.parse.return_value = (
                RETURNED_UPDATED_VALUE
            )
            sleep(0.1)

            tracking.process_carrier_trackers(tracker_ids=dhl_ids)

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UPDATED_TRACKERS_LIST, response_data)


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
            status="in_transit",
            info={
                "carrier_tracking_link": "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum=1Z12345E6205277936/trackdetails",
                "shipment_service": "UPS Ground",
            },
        )
    ],
    [],
)

TRACKING_RESPONSE = {
    "id": ANY,
    "carrier_id": "ups_package",
    "carrier_name": "ups",
    "tracking_number": "1Z12345E6205277936",
    "test_mode": True,
    "delivered": False,
    "events": [
        {
            "code": "KB",
            "date": "2010-08-30",
            "description": "UPS INTERNAL ACTIVITY CODE",
            "location": "BONN",
            "time": "10:39",
            "reason": None,
        }
    ],
}

TRACKERS_LIST = {
    "count": 2,
    "next": ANY,
    "previous": ANY,
    "results": [
        {
            "id": ANY,
            "info": ANY,
            "object_type": "tracker",
            "carrier_name": "dhl_express",
            "carrier_id": "dhl_express",
            "tracking_number": "00340434292135100124",
            "delivery_image_url": None,
            "signature_image_url": None,
            "estimated_delivery": ANY,
            "events": [
                {
                    "date": "2021-01-11",
                    "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
                    "location": "BONN",
                    "code": "pre-transit",
                    "time": "20:34",
                    "latitude": None,
                    "longitude": None,
                    "reason": None,
                    "status": None,
                    "timestamp": None,
                }
            ],
            "delivered": False,
            "status": "in_transit",
            "test_mode": True,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
        {
            "id": ANY,
            "info": ANY,
            "object_type": "tracker",
            "carrier_name": "ups",
            "carrier_id": "ups_package",
            "tracking_number": "1Z12345E6205277936",
            "delivery_image_url": None,
            "signature_image_url": None,
            "estimated_delivery": ANY,
            "events": [
                {
                    "date": "2012-10-04",
                    "description": "Order Processed: Ready for UPS",
                    "location": "FR",
                    "code": "MP",
                    "time": "13:58",
                    "latitude": None,
                    "longitude": None,
                    "reason": None,
                    "status": None,
                    "timestamp": None,
                }
            ],
            "delivered": False,
            "status": "in_transit",
            "test_mode": True,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
    ],
}

RETURNED_UPDATED_VALUE = (
    [
        TrackingDetails(
            carrier_id="dhl_express",
            carrier_name="dhl_express",
            tracking_number="00340434292135100124",
            delivered=False,
            events=[
                TrackingEvent(
                    code="pre-transit",
                    date="2021-03-02",
                    description="JESSICA",
                    location="Oderweg 2, AMSTERDAM",
                    time="07:53",
                ),
                TrackingEvent(
                    code="pre-transit",
                    date="2021-01-11",
                    description="The instruction data for this shipment have been provided by the sender to DHL electronically",
                    location="BONN",
                    time="20:34",
                ),
            ],
            info={
                "carrier_tracking_link": "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=00340434292135100124",
                "package_weight": "0.74",
                "package_weight_unit": "KG",
                "shipment_service": "dhl_express_worldwide",
                "shipping_date": "2021-01-11",
                "signed_by": "Jane Doe",
            },
        )
    ],
    [],
)

UPDATED_TRACKERS_LIST = {
    "count": 2,
    "next": ANY,
    "previous": ANY,
    "results": [
        {
            "id": ANY,
            "info": ANY,
            "object_type": "tracker",
            "carrier_name": "dhl_express",
            "carrier_id": "dhl_express",
            "tracking_number": "00340434292135100124",
            "delivery_image_url": None,
            "signature_image_url": None,
            "estimated_delivery": ANY,
            "events": [
                {
                    "date": "2021-03-02",
                    "description": "JESSICA",
                    "location": "Oderweg 2, AMSTERDAM",
                    "code": "pre-transit",
                    "time": "07:53",
                    "latitude": None,
                    "longitude": None,
                    "reason": None,
                    "status": None,
                    "timestamp": None,
                },
                {
                    "date": "2021-01-11",
                    "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
                    "location": "BONN",
                    "code": "pre-transit",
                    "time": "20:34",
                    "latitude": None,
                    "longitude": None,
                    "reason": None,
                    "status": None,
                    "timestamp": None,
                },
            ],
            "delivered": False,
            "status": "in_transit",
            "test_mode": True,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
        {
            "id": ANY,
            "info": ANY,
            "object_type": "tracker",
            "carrier_name": "ups",
            "carrier_id": "ups_package",
            "tracking_number": "1Z12345E6205277936",
            "delivery_image_url": None,
            "signature_image_url": None,
            "estimated_delivery": ANY,
            "events": [
                {
                    "date": "2012-10-04",
                    "description": "Order Processed: Ready for UPS",
                    "location": "FR",
                    "code": "MP",
                    "time": "13:58",
                    "latitude": None,
                    "longitude": None,
                    "reason": None,
                    "status": None,
                    "timestamp": None,
                }
            ],
            "delivered": False,
            "status": "in_transit",
            "test_mode": True,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
    ],
}
