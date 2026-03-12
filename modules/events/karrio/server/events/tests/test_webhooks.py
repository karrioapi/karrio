import json
from unittest.mock import ANY, patch
from requests import Response

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from karrio.server.core.tests import APITestCase
from karrio.server.events.models import Webhook
from karrio.server.events.task_definitions.base.webhook import (
    notify_webhook_subscribers,
)

NOTIFICATION_DATETIME = timezone.now()


class TestWebhooks(APITestCase):
    def test_create_webhook(self):
        url = reverse("karrio.server.events:webhook-list")
        data = WEBHOOK_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, WEBHOOK_RESPONSE)


class TestWebhookDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.webhook: Webhook = Webhook.objects.create(
            **{
                "url": "https://api.karrio.io",
                "description": "Testing Hook",
                "enabled_events": ["all"],
                "test_mode": True,
                "disabled": False,
                "id": ANY,
                "last_event_at": None,
                "created_by": self.user,
            }
        )

    def test_update_webhook(self):
        url = reverse(
            "karrio.server.events:webhook-details", kwargs=dict(pk=self.webhook.pk)
        )
        data = WEBHOOK_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_UPDATED_RESPONSE)

    def test_webhook_notify(self):
        url = reverse(
            "karrio.server.events:webhook-details", kwargs=dict(pk=self.webhook.pk)
        )

        with patch(
            "karrio.server.events.task_definitions.base.webhook.identity"
        ) as mocks:
            response = Response()
            response.status_code = 200
            mocks.return_value = response

            notify_webhook_subscribers(
                event="shipment.purchased",
                data={"shipment": "content"},
                event_at=NOTIFICATION_DATETIME,
                ctx=dict(
                    user_id=self.user.id,
                    test_mode=True,
                ),
            )

        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_NOTIFIED_RESPONSE)

    def test_webhook_failure_streak_increments_and_auto_disables_after_threshold(self):
        """Failed deliveries increment failure_streak_count and eventually disable."""
        with patch("karrio.server.events.task_definitions.base.webhook.identity") as mocks:
            failed = Response()
            failed.status_code = 500
            mocks.return_value = failed

            # Trigger 6 failed notifications (disable when > 5)
            for _ in range(6):
                notify_webhook_subscribers(
                    event="shipment.purchased",
                    data={"shipment": "content"},
                    event_at=NOTIFICATION_DATETIME,
                    ctx=dict(user_id=self.user.id, test_mode=True),
                )

        self.webhook.refresh_from_db()
        self.assertEqual(self.webhook.failure_streak_count, 6)
        self.assertTrue(self.webhook.disabled)
        self.assertIsNone(self.webhook.last_event_at)


WEBHOOK_DATA = {
    "url": "https://api.karrio.io",
    "description": "Testing Hook",
    "enabled_events": ["all"],
    "test_mode": True,
}

WEBHOOK_RESPONSE = {
    "url": "https://api.karrio.io",
    "description": "Testing Hook",
    "enabled_events": ["all"],
    "test_mode": True,
    "disabled": False,
    "id": ANY,
    "object_type": "webhook",
    "secret": ANY,
    "last_event_at": None,
}

WEBHOOK_UPDATE_DATA = {
    "description": "Testing Hook Updated",
    "enabled_events": ["shipment_purchased", "shipment_cancelled"],
}

WEBHOOK_UPDATED_RESPONSE = {
    "url": "https://api.karrio.io",
    "description": "Testing Hook Updated",
    "enabled_events": ["shipment_purchased", "shipment_cancelled"],
    "test_mode": True,
    "disabled": False,
    "id": ANY,
    "object_type": "webhook",
    "secret": ANY,
    "last_event_at": None,
}

WEBHOOK_NOTIFIED_RESPONSE = {
    "url": "https://api.karrio.io",
    "description": "Testing Hook",
    "enabled_events": ["all"],
    "test_mode": True,
    "disabled": False,
    "id": ANY,
    "object_type": "webhook",
    "secret": ANY,
    "last_event_at": NOTIFICATION_DATETIME.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
}
