import json
from unittest.mock import ANY, patch
from requests import Response

from django.urls import reverse
from rest_framework import status

from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.events.models import Webhook
from karrio.server.manager import models


class TestBatchWebhookResend(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tracker = models.Tracking.objects.create(
            tracking_number="1Z12345E6205277936",
            test_mode=True,
            delivered=False,
            events=[
                {
                    "date": "2012-10-04",
                    "description": "Order Processed: Ready for UPS",
                    "location": "FR",
                    "code": "MP",
                    "time": "13:58",
                }
            ],
            status="in_transit",
            created_by=self.user,
            carrier=create_carrier_snapshot(self.ups_carrier),
        )
        self.webhook = Webhook.objects.create(
            url="https://hooks.example.com/webhook",
            description="Test Hook",
            enabled_events=["all"],
            test_mode=True,
            disabled=False,
            created_by=self.user,
        )

    def test_batch_resend_to_all_webhooks(self):
        url = reverse("karrio.server.events:batch-webhook-resend")
        data = BATCH_RESEND_DATA(self)

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, BATCH_RESEND_RESPONSE(self))

    def test_batch_resend_to_specific_webhook(self):
        url = reverse("karrio.server.events:batch-webhook-resend")
        data = BATCH_RESEND_TARGETED_DATA(self)

        with patch(
            "karrio.server.events.task_definitions.base.webhook.identity"
        ) as mock_notify:
            mock_response = Response()
            mock_response.status_code = 200
            mock_notify.return_value = mock_response

            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, BATCH_RESEND_TARGETED_RESPONSE(self))

    def test_batch_resend_with_not_found_entity(self):
        url = reverse("karrio.server.events:batch-webhook-resend")
        data = BATCH_RESEND_NOT_FOUND_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, BATCH_RESEND_NOT_FOUND_RESPONSE)

    def test_batch_resend_empty_entity_ids(self):
        url = reverse("karrio.server.events:batch-webhook-resend")
        data = {"entity_ids": [], "object_type": "tracker"}

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, BATCH_RESEND_EMPTY_RESPONSE)


def BATCH_RESEND_DATA(test_case):
    return {
        "entity_ids": [test_case.tracker.pk],
        "object_type": "tracker",
    }


def BATCH_RESEND_TARGETED_DATA(test_case):
    return {
        "entity_ids": [test_case.tracker.pk],
        "object_type": "tracker",
        "webhook_id": test_case.webhook.pk,
    }


def BATCH_RESEND_RESPONSE(test_case):
    return {
        "object_type": "tracker",
        "resources": [
            {
                "id": test_case.tracker.pk,
                "status": "queued",
                "error": None,
            }
        ],
        "count": 1,
        "test_mode": True,
        "created_at": ANY,
    }


def BATCH_RESEND_TARGETED_RESPONSE(test_case):
    return {
        "object_type": "tracker",
        "resources": [
            {
                "id": test_case.tracker.pk,
                "status": "queued",
                "error": None,
            }
        ],
        "count": 1,
        "test_mode": True,
        "created_at": ANY,
    }


BATCH_RESEND_NOT_FOUND_DATA = {
    "entity_ids": ["trk_nonexistent_id"],
    "object_type": "tracker",
}

BATCH_RESEND_NOT_FOUND_RESPONSE = {
    "object_type": "tracker",
    "resources": [
        {
            "id": "trk_nonexistent_id",
            "status": "failed",
            "error": "Not found",
        }
    ],
    "count": 0,
    "test_mode": True,
    "created_at": ANY,
}

BATCH_RESEND_EMPTY_RESPONSE = {
    "object_type": "tracker",
    "resources": [],
    "count": 0,
    "test_mode": True,
    "created_at": ANY,
}
