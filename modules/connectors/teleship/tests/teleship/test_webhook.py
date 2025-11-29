"""Teleship carrier webhook registration tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTeleshipWebhook(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.WebhookRegistrationRequest = models.WebhookRegistrationRequest(
            **WebhookRegistrationPayload
        )
        self.WebhookDeregistrationRequest = models.WebhookDeregistrationRequest(
            **WebhookDeregistrationPayload
        )

    def test_create_webhook_registration_request(self):
        request = gateway.mapper.create_webhook_registration_request(
            self.WebhookRegistrationRequest
        )

        self.assertEqual(lib.to_dict(request.serialize()), WebhookRegistrationRequest)

    def test_register_webhook(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Webhook.register(self.WebhookRegistrationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/webhooks",
            )

    def test_parse_webhook_registration_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = WebhookRegistrationResponse
            parsed_response = (
                karrio.Webhook.register(self.WebhookRegistrationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedWebhookRegistrationResponse
            )

    def test_create_webhook_deregistration_request(self):
        request = gateway.mapper.create_webhook_deregistration_request(
            self.WebhookDeregistrationRequest
        )

        self.assertEqual(lib.to_dict(request.serialize()), WebhookDeregistrationRequest)

    def test_deregister_webhook(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ""
            karrio.Webhook.deregister(self.WebhookDeregistrationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/webhooks/WHK-12345",
            )

    def test_parse_webhook_deregistration_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Webhook.deregister(self.WebhookDeregistrationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedWebhookDeregistrationResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.teleship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Webhook.register(self.WebhookRegistrationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


WebhookRegistrationPayload = {
    "url": "https://example.com/webhooks/teleship",
    "description": "Teleship shipment tracking updates",
    "enabled_events": ["shipment.created", "shipment.updated", "shipment.delivered"],
}

WebhookDeregistrationPayload = {"webhook_id": "WHK-12345"}

WebhookRegistrationRequest = {
    "url": "https://example.com/webhooks/teleship",
    "description": "Teleship shipment tracking updates",
    "enabled": True,
    "enabledEvents": ["shipment.created", "shipment.updated", "shipment.delivered"],
}

WebhookDeregistrationRequest = {"webhookId": "WHK-12345"}

WebhookRegistrationResponse = """{
    "id": "WHK-12345",
    "url": "https://example.com/webhooks/teleship",
    "description": "Teleship shipment tracking updates",
    "enabled": true,
    "enabledEvents": ["shipment.created", "shipment.updated", "shipment.delivered"],
    "secret": "whsec_abc123xyz789"
}"""

ErrorResponse = """{
    "messages": [
        {
            "code": 400,
            "timestamp": "2025-01-15T10:30:45Z",
            "message": "Webhook registration failed",
            "details": [
                "Invalid URL format",
                "URL must use HTTPS protocol"
            ]
        }
    ]
}"""

ParsedWebhookRegistrationResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "webhook_identifier": "WHK-12345",
        "secret": "whsec_abc123xyz789",
        "meta": {
            "description": "Teleship shipment tracking updates",
            "enabled": True,
            "enabledEvents": [
                "shipment.created",
                "shipment.updated",
                "shipment.delivered",
            ],
            "id": "WHK-12345",
            "secret": "whsec_abc123xyz789",
            "url": "https://example.com/webhooks/teleship",
        },
    },
    [],
]

ParsedWebhookDeregistrationResponse = [
    {
        "carrier_id": "teleship",
        "carrier_name": "teleship",
        "success": True,
        "operation": "webhook_deregistration",
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "teleship",
            "carrier_name": "teleship",
            "code": "400",
            "message": "Webhook registration failed",
            "details": {
                "timestamp": "2025-01-15T10:30:45Z",
                "details": [
                    "Invalid URL format",
                    "URL must use HTTPS protocol",
                ],
            },
        }
    ],
]
