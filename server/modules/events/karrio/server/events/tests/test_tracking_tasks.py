import json
import datetime
from time import sleep
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import TrackingDetails, TrackingEvent
from karrio.server.core.tests import APITestCase
from karrio.server.manager import models
from karrio.server.events.task_definitions.base import tracking


class TestTrackersBackgroundUpdate(APITestCase):
    def setUp(self) -> None:
        super().setUp()
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
                "tracking_carrier": self.ups_carrier,
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
                "tracking_carrier": self.dhl_carrier,
            },
        ]
        [models.Tracking.objects.create(**t) for t in trackers]

    def test_get_trackers(self):
        url = reverse("karrio.server.manager:trackers-list")

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, TRACKERS_LIST)

    def test_get_updated_trackers(self):
        url = reverse("karrio.server.manager:trackers-list")

        with patch(
            "karrio.server.events.task_definitions.base.tracking.utils.identity"
        ) as mocks:
            mocks.return_value = RETURNED_UPDATED_VALUE
            sleep(0.1)
            tracking.update_trackers(delta=datetime.timedelta(seconds=0.1))

            response = self.client.get(url)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, UPDATED_TRACKERS_LIST)


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
            "object_type": "tracker",
            "carrier_name": "dhl_universal",
            "carrier_id": "dhl_universal",
            "tracking_number": "00340434292135100124",
            "estimated_delivery": None,
            "events": [
                {
                    "date": "2021-01-11",
                    "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
                    "location": "BONN",
                    "code": "pre-transit",
                    "time": "20:34",
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
            "object_type": "tracker",
            "carrier_name": "ups",
            "carrier_id": "ups_package",
            "tracking_number": "1Z12345E6205277936",
            "estimated_delivery": None,
            "events": [
                {
                    "date": "2012-10-04",
                    "description": "Order Processed: Ready for UPS",
                    "location": "FR",
                    "code": "MP",
                    "time": "13:58",
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
            carrier_id="dhl_universal",
            carrier_name="dhl_universal",
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
        )
    ],
    [],
)

UPDATED_TRACKERS_LIST = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": ANY,
            "object_type": "tracker",
            "carrier_name": "dhl_universal",
            "carrier_id": "dhl_universal",
            "tracking_number": "00340434292135100124",
            "events": [
                {
                    "date": "2021-03-02",
                    "description": "JESSICA",
                    "location": "Oderweg 2, AMSTERDAM",
                    "code": "pre-transit",
                    "time": "07:53",
                },
                {
                    "date": "2021-01-11",
                    "description": "The instruction data for this shipment have been provided by the sender to DHL electronically",
                    "location": "BONN",
                    "code": "pre-transit",
                    "time": "20:34",
                },
            ],
            "delivered": False,
            "test_mode": True,
            "status": "in_transit",
            "estimated_delivery": None,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
        {
            "id": ANY,
            "object_type": "tracker",
            "carrier_name": "ups",
            "carrier_id": "ups_package",
            "tracking_number": "1Z12345E6205277936",
            "events": [
                {
                    "date": "2012-10-04",
                    "description": "Order Processed: Ready for UPS",
                    "location": "FR",
                    "code": "MP",
                    "time": "13:58",
                }
            ],
            "delivered": False,
            "test_mode": True,
            "status": "in_transit",
            "estimated_delivery": None,
            "messages": [],
            "meta": {},
            "metadata": {},
        },
    ],
}
