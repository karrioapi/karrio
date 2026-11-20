"""Teleship carrier hooks tests (OAuth and webhook events)."""

import hmac
import json
import hashlib
import unittest
from .fixture import gateway, gateway_with_webhook_secret, webhook_secret

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.hooks.oauth as oauth_hooks
import karrio.providers.teleship.hooks.event as event_hooks
import karrio.providers.teleship.units as provider_units


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


def sign(raw: bytes, secret: str = webhook_secret) -> str:
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


def compact(body: dict) -> bytes:
    """What JSON.stringify(payload) produces."""
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode()


class TestTeleshipWebhookEventHooks(unittest.TestCase):
    """Inbound events fail closed: no stored secret, no header or a wrong
    signature are each rejected with their own message, nothing is applied."""

    def setUp(self):
        self.maxDiff = None

    def payload(self, body=None, headers=None, raw_body=None):
        return models.RequestPayload(
            query={},
            body=WebhookEventPayload if body is None else body,
            headers=headers or {},
            raw_body=raw_body,
            url="https://api.karrio.io/v1/connections/webhook/teleship-123/events",
        )

    def assert_rejected(self, payload, settings, code, text):
        details, messages = event_hooks.on_webhook_event(payload, settings)

        self.assertIsNone(details)
        self.assertEqual([_.code for _ in messages], [code])
        self.assertIn(text, messages[0].message)

    # negative: each rejection has its own message, nothing applied

    def test_on_webhook_event_rejects_a_missing_signature_header(self):
        raw = compact(WebhookEventPayload)

        self.assert_rejected(
            self.payload(raw_body=raw),
            gateway_with_webhook_secret.settings,
            "webhook_signature_missing",
            "x-teleship-signature",
        )

    def test_on_webhook_event_rejects_a_wrong_signature(self):
        raw = compact(WebhookEventPayload)

        for signature in ["deadbeef", sign(raw, "another-secret"), sign(raw) + "0", "sïg"]:
            self.assert_rejected(
                self.payload(
                    raw_body=raw, headers={"x-teleship-signature": signature}
                ),
                gateway_with_webhook_secret.settings,
                "invalid_signature",
                "Invalid webhook signature",
            )

    def test_on_webhook_event_rejects_when_no_secret_is_stored(self):
        raw = compact(WebhookEventPayload)

        for headers in [{}, {"x-teleship-signature": sign(raw)}, {"x-teleship-signature": ""}]:
            self.assert_rejected(
                self.payload(raw_body=raw, headers=headers),
                gateway.settings,
                "webhook_secret_not_configured",
                "webhook secret",
            )

    def test_on_webhook_event_rejects_an_empty_stored_secret(self):
        settings = karrio.gateway["teleship"].create(
            dict(client_id="a", client_secret="b", test_mode=True, config=dict(webhook_secret="")),
        ).settings
        raw = compact(WebhookEventPayload)

        self.assert_rejected(
            self.payload(raw_body=raw, headers={"x-teleship-signature": sign(raw, "")}),
            settings,
            "webhook_secret_not_configured",
            "webhook secret",
        )

    # positive

    def test_on_webhook_event_shipment_updated(self):
        raw = compact(WebhookEventPayload)
        payload = self.payload(raw_body=raw, headers={"x-teleship-signature": sign(raw)})

        details, messages = event_hooks.on_webhook_event(
            payload, gateway_with_webhook_secret.settings
        )

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
        body = {
            "eventName": "label.generated",
            "objectType": "shipment",
            "objectId": "shp-abc123",
            "data": {
                "trackingNumber": "TELESHIP999888777",
                "shipmentId": "shp-abc123",
            },
        }
        raw = compact(body)

        details, messages = event_hooks.on_webhook_event(
            self.payload(body, {"x-teleship-signature": sign(raw)}, raw),
            gateway_with_webhook_secret.settings,
        )

        self.assertIsNotNone(details)
        self.assertEqual(details.tracking_number, "TELESHIP999888777")
        self.assertEqual(details.shipment_identifier, "shp-abc123")
        # No tracking details for label.generated event
        self.assertIsNone(details.tracking)

    # what is signed

    def test_signature_forms(self):
        body = {**WebhookEventPayload, "objectId": "Müller 東京"}
        settings = gateway_with_webhook_secret.settings
        indented = json.dumps(body, indent=4).encode()
        compact_utf8 = compact(body)
        old_form = lib.to_json(body).encode()  # indent=4, sorted keys, ASCII escapes
        self.assertEqual(len({indented, compact_utf8, old_form}), 3)

        def verified(raw, signed):
            return event_hooks.verify_webhook_signature(
                self.payload(body, {"X-Teleship-Signature": sign(signed)}, raw), settings
            )

        self.assertTrue(verified(compact_utf8, compact_utf8))  # raw bytes as sent
        self.assertTrue(verified(indented, indented))  # raw bytes as sent
        self.assertTrue(verified(indented, compact_utf8))  # JSON.stringify of the parsed body
        self.assertFalse(verified(compact_utf8, old_form))  # never the indented, sorted form
        self.assertFalse(verified(indented, old_form))
        self.assertFalse(verified(compact_utf8, indented))  # other formatting of the same data

    def test_compact_form_keeps_the_received_key_order(self):
        body = {"b": 1, "a": {"y": 2, "x": [3, 1]}, "eventName": "x"}
        raw = json.dumps(body, indent=2).encode()
        settings = gateway_with_webhook_secret.settings

        def verified(signed):
            return event_hooks.verify_webhook_signature(
                self.payload(body, {"x-teleship-signature": sign(signed)}, raw), settings
            )

        self.assertTrue(verified(b'{"b":1,"a":{"y":2,"x":[3,1]},"eventName":"x"}'))
        self.assertFalse(verified(b'{"a":{"x":[3,1],"y":2},"b":1,"eventName":"x"}'))

    def test_signature_header_name_is_case_insensitive(self):
        raw = compact(WebhookEventPayload)

        for name in ["x-teleship-signature", "X-Teleship-Signature", "X-TELESHIP-SIGNATURE"]:
            self.assertTrue(
                event_hooks.verify_webhook_signature(
                    self.payload(raw_body=raw, headers={name: sign(raw)}),
                    gateway_with_webhook_secret.settings,
                ),
                name,
            )

    def test_without_raw_body_only_the_parsed_body_can_match(self):
        body = {"eventName": "x", "objectId": "é"}
        settings = gateway_with_webhook_secret.settings

        self.assertTrue(
            event_hooks.verify_webhook_signature(
                self.payload(body, {"x-teleship-signature": sign(compact(body))}), settings
            )
        )
        self.assertFalse(
            event_hooks.verify_webhook_signature(
                self.payload(body, {"x-teleship-signature": sign(lib.to_json(body).encode())}),
                settings,
            )
        )

    def test_non_json_raw_body_is_rejected_not_an_error(self):
        raw = b"\xff\xfe not json"

        for headers in [{}, {"x-teleship-signature": "00"}]:
            details, messages = event_hooks.on_webhook_event(
                self.payload(raw_body=raw, headers=headers),
                gateway_with_webhook_secret.settings,
            )
            self.assertIsNone(details)
            self.assertEqual(len(messages), 1)

    # the compact candidate is optional: a body it cannot encode (an escaped lone
    # surrogate) must neither break nor decide the verification

    def surrogate_raw(self):
        raw = json.dumps({**WebhookEventPayload, "extension": "\ud800"}).encode()
        self.assertIn(b"\\ud800", raw)
        return raw

    def test_signed_event_with_an_unencodable_compact_form_is_accepted(self):
        raw = self.surrogate_raw()
        body = json.loads(raw)
        settings = gateway_with_webhook_secret.settings

        self.assertEqual(event_hooks.signed_payloads(self.payload(body, raw_body=raw)), [raw])
        details, messages = event_hooks.on_webhook_event(
            self.payload(body, {"x-teleship-signature": sign(raw)}, raw), settings
        )
        self.assertEqual(messages, [])
        self.assertIsNotNone(details)

    def test_wrongly_signed_event_with_an_unencodable_compact_form_is_rejected(self):
        raw = self.surrogate_raw()
        body = json.loads(raw)

        for signature in ["deadbeef", sign(raw, "other-secret")]:
            self.assert_rejected(
                self.payload(body, {"x-teleship-signature": signature}, raw),
                gateway_with_webhook_secret.settings,
                "invalid_signature",
                "Invalid webhook signature",
            )

    def test_webhook_secret_is_a_declared_connection_option(self):
        self.assertIn(
            "webhook_secret", [_.name for _ in provider_units.ConnectionConfig]
        )
        self.assertEqual(
            gateway_with_webhook_secret.settings.connection_config.webhook_secret.state,
            webhook_secret,
        )
        self.assertIsNone(gateway.settings.connection_config.webhook_secret.state)


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
