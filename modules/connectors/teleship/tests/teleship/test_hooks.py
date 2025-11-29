"""Teleship carrier hooks tests (OAuth and webhook events)."""

import unittest
from .fixture import gateway

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.hooks.oauth as oauth_hooks
import karrio.providers.teleship.hooks.event as event_hooks


class TestTeleshipOAuthHooks(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_on_oauth_authorize(self):
        payload = models.OAuthAuthorizePayload(
            redirect_uri="https://api.karrio.io/v1/connections/oauth/teleship/callback",
            state="base64encodedstate",
            options={"scope": "read_accounts write_shipments"},
        )

        output, messages = oauth_hooks.on_oauth_authorize(payload, gateway.settings)

        self.assertIsNotNone(output)
        self.assertEqual(output.carrier_name, "teleship")
        self.assertIn("/oauth/authorize?", output.authorization_url)
        self.assertIn("redirectUri=", output.authorization_url)
        self.assertIn("state=base64encodedstate", output.authorization_url)
        self.assertEqual(output.meta, {"scope": "read_accounts write_shipments"})
        # Without system config, OAUTH_CLIENT_ID will be None and generate an error
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "OAUTH_CONFIG_ERROR")

    def test_on_oauth_authorize_missing_client_id(self):
        """Test OAuth authorize with missing client ID generates error.

        Since oauth_client_id is a property that reads from system config,
        we test that it correctly generates an error when the system config
        doesn't have TELESHIP_OAUTH_CLIENT_ID set (which is the default test case).
        """
        # gateway.settings already has no oauth_client_id because no system config
        payload = models.OAuthAuthorizePayload(
            redirect_uri="https://api.karrio.io/v1/connections/oauth/teleship/callback",
            state="test_state",
            options={},
        )

        output, messages = oauth_hooks.on_oauth_authorize(payload, gateway.settings)

        self.assertIsNotNone(output)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "OAUTH_CONFIG_ERROR")
        self.assertIn("TELESHIP_OAUTH_CLIENT_ID", messages[0].message)

    def test_on_oauth_callback_success(self):
        payload = models.RequestPayload(
            query={
                "code": "auth_code_12345",
                "account_client_id": "user_client_id_abc",
                "account_client_secret": "user_client_secret_xyz",
                "state": "base64encodedstate",
            },
            body={},
            headers={},
            url="https://api.karrio.io/v1/connections/oauth/teleship/callback",
        )

        credentials, messages = oauth_hooks.on_oauth_callback(payload, gateway.settings)

        self.assertEqual(credentials, {
            "client_id": "user_client_id_abc",
            "client_secret": "user_client_secret_xyz",
        })
        self.assertEqual(messages, [])

    def test_on_oauth_callback_missing_code(self):
        payload = models.RequestPayload(
            query={
                "account_client_id": "user_client_id_abc",
                "account_client_secret": "user_client_secret_xyz",
            },
            body={},
            headers={},
            url="https://api.karrio.io/v1/connections/oauth/teleship/callback",
        )

        credentials, messages = oauth_hooks.on_oauth_callback(payload, gateway.settings)

        self.assertIsNone(credentials)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "OAUTH_CALLBACK_ERROR")
        self.assertIn("authorization code", messages[0].message)

    def test_on_oauth_callback_missing_credentials(self):
        payload = models.RequestPayload(
            query={
                "code": "auth_code_12345",
            },
            body={},
            headers={},
            url="https://api.karrio.io/v1/connections/oauth/teleship/callback",
        )

        credentials, messages = oauth_hooks.on_oauth_callback(payload, gateway.settings)

        self.assertIsNone(credentials)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "OAUTH_CALLBACK_ERROR")
        self.assertIn("account credentials", messages[0].message)


class TestTeleshipWebhookEventHooks(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_on_webhook_event_shipment_updated(self):
        payload = models.RequestPayload(
            query={},
            body=WebhookEventPayload,
            headers={"x-teleship-signature": ""},  # No secret configured, so no validation
            url="https://api.karrio.io/v1/connections/webhook/teleship-123/events",
        )

        details, messages = event_hooks.on_webhook_event(payload, gateway.settings)

        self.assertIsNotNone(details)
        self.assertEqual(details.carrier_name, "teleship")
        self.assertEqual(details.tracking_number, "TELESHIP12345678901")
        self.assertEqual(details.shipment_identifier, "6f384ad7-f8bf-40ce-8bf0-715248738f10")
        self.assertIsNotNone(details.tracking)
        self.assertEqual(details.tracking.tracking_number, "TELESHIP12345678901")
        self.assertEqual(len(details.tracking.events), 2)
        self.assertEqual(messages, [])

    def test_on_webhook_event_label_generated(self):
        """Test webhook event without tracking data (label generated event)."""
        payload = models.RequestPayload(
            query={},
            body={
                "eventName": "label.generated",
                "objectType": "shipment",
                "objectId": "shp-abc123",
                "data": {
                    "trackingNumber": "TELESHIP999888777",
                    "shipmentId": "shp-abc123",
                },
            },
            headers={},
            url="https://api.karrio.io/v1/connections/webhook/teleship-123/events",
        )

        details, messages = event_hooks.on_webhook_event(payload, gateway.settings)

        self.assertIsNotNone(details)
        self.assertEqual(details.tracking_number, "TELESHIP999888777")
        self.assertEqual(details.shipment_identifier, "shp-abc123")
        # No tracking details for label.generated event
        self.assertIsNone(details.tracking)


if __name__ == "__main__":
    unittest.main()


WebhookEventPayload = {
    "eventName": "shipment.updated",
    "objectType": "shipment",
    "objectId": "6f384ad7-f8bf-40ce-8bf0-715248738f10",
    "data": {
        "shipmentId": "6f384ad7-f8bf-40ce-8bf0-715248738f10",
        "trackingNumber": "TELESHIP12345678901",
        "customerReference": "ORDER-2025-001",
        "shipDate": "2025-01-15T00:00:00.000Z",
        "estimatedDelivery": "2025-01-20T00:00:00.000Z",
        "shipTo": {
            "name": "Jane Doe",
            "company": "US Imports Inc",
            "address": {
                "city": "Los Angeles",
                "state": "CA",
                "postcode": "90001",
                "country": "US",
            },
        },
        "shipFrom": {
            "name": "John Smith",
            "company": "UK Exports Ltd",
            "address": {
                "city": "London",
                "state": "LDN",
                "postcode": "SW1A 1AA",
                "country": "GB",
            },
        },
        "firstMile": {
            "carrier": "Teleship",
            "trackingNumber": "TELESHIP12345678901",
        },
        "lastMile": {
            "carrier": "USPS",
            "trackingNumber": "9400111899223033019889",
        },
        "events": [
            {
                "timestamp": "2025-01-17T14:30:00.000Z",
                "code": "IN_TRANSIT",
                "description": "Package in transit to destination",
                "location": "Chicago, IL",
            },
            {
                "timestamp": "2025-01-15T10:00:00.000Z",
                "code": "PICKED_UP",
                "description": "Package picked up from sender",
                "location": "London, UK",
            },
        ],
    },
}
