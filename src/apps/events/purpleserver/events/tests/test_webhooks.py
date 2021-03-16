import json
from unittest.mock import ANY
from django.urls import reverse
from rest_framework import status
from purpleserver.core.tests import APITestCase
from purpleserver.events.models import Webhook


class TestWebhooks(APITestCase):

    def test_create_address(self):
        url = reverse('purpleserver.events:webhook-list')
        data = WEBHOOK_DATA

        response = self.client.post(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, WEBHOOK_RESPONSE)


class TestWebhookDetails(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.webhook: Webhook = Webhook.objects.create(**{
            "url": "http://localhost:8080",
            "description": "Testing Hook",
            "enabled_events": ["all"],
            "test_mode": True,
            "disabled": False,
            "id": ANY,
            "last_event_at": None,
            "created_by": self.user
        })

    def test_update_address(self):
        url = reverse('purpleserver.events:webhook-details', kwargs=dict(pk=self.webhook.pk))
        data = WEBHOOK_UPDATE_DATA

        response = self.client.patch(url, data)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_UPDATE_RESPONSE)


WEBHOOK_DATA = {
  "url": "http://localhost:8080",
  "description": "Testing Hook",
  "enabled_events": ["all"],
  "test_mode": True
}

WEBHOOK_RESPONSE = {
  "url": "http://localhost:8080",
  "description": "Testing Hook",
  "enabled_events": [
    "all"
  ],
  "test_mode": True,
  "disabled": False,
  "id": ANY,
  "last_event_at": None
}

WEBHOOK_UPDATE_DATA = {
  "description": "Testing Hook Updated",
  "enabled_events": ["shipment.purchased", "shipment.cancelled"]
}

WEBHOOK_UPDATE_RESPONSE = {
  "url": "http://localhost:8080",
  "description": "Testing Hook Updated",
  "enabled_events": [
    "shipment.purchased",
    "shipment.cancelled"
  ],
  "test_mode": True,
  "disabled": False,
  "id": ANY,
  "last_event_at": None
}
