"""Inbound carrier webhook events must authenticate their sender (fail closed).

The route is public by design: the carrier is the only caller, and a Teleship
event proves itself with an HMAC-SHA256 hex signature (x-teleship-signature)
made with the secret returned when the webhook was registered.
"""
import contextlib
import hashlib
import hmac
import json
from unittest.mock import patch

import karrio.lib as lib
from django.http.request import RawPostDataException
from django.urls import reverse
from karrio.server.core.logging import logger
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.manager.models import Tracking
from karrio.server.providers.models import CarrierConnection
from karrio.server.providers.serializers.base import WebhookEventSerializer

SECRET = "whsec_connection_secret"
OTHER_SECRET = "whsec_someone_elses_secret"
NUMBER = "TELESHIP-SIG-NUMBER"
DESCRIPTION = "FORGED"
# The one body every rejection answers with: it must not tell a caller whether
# a secret is configured. The specific reason is in the server log.
REJECTION = {
    "operation": "Webhook event",
    "success": False,
    "messages": [
        {
            "code": "webhook_signature_verification_failed",
            "message": "webhook signature verification failed",
        }
    ],
}


def sign(raw: bytes, secret: str = SECRET) -> str:
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


def event_body(description: str = DESCRIPTION) -> dict:
    # Not in sorted key order on purpose: JSON.stringify keeps the sender's order.
    return {
        "eventName": "shipment.updated",
        "objectType": "shipment",
        "objectId": "test-shipment",
        "data": {
            "trackingNumber": NUMBER,
            "shipmentId": "test-shipment",
            "firstMile": {"carrier": "test"},
            "lastMile": {"carrier": "test"},
            "shipTo": {"address": {"city": "Test", "country": "US"}},
            "shipFrom": {"address": {"country": "GB"}},
            "events": [
                {
                    "timestamp": "2026-11-15T12:00:00Z",
                    "code": "in_transit",
                    "description": description,
                }
            ],
        },
    }


def compact(body: dict) -> bytes:
    """What JSON.stringify(payload) produces."""
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode()


class WebhookSignatureCase(APITestCase):
    def make_connection(self, secret=SECRET, carrier_id="s17-connection"):
        connection = CarrierConnection.objects.create(
            carrier_code="teleship",
            carrier_id=carrier_id,
            test_mode=True,
            created_by=self.user,
            credentials={"client_id": "test-client", "client_secret": "test-secret"},
            config={"webhook_secret": secret} if secret else {},
        )
        tracker = Tracking.objects.create(
            tracking_number=NUMBER,
            test_mode=True,
            created_by=self.user,
            carrier=create_carrier_snapshot(connection),
            status="pending",
            events=[],
        )
        return connection, tracker

    def post(self, connection, raw: bytes, signature=None, header="HTTP_X_TELESHIP_SIGNATURE"):
        url = reverse(
            "karrio.server.providers:connection-webhook-event",
            kwargs=dict(pk=connection.pk),
        )
        extra = {header: signature} if signature is not None else {}
        return self.client_class().post(
            url, data=raw, content_type="application/json", **extra
        )

    def codes(self, response):
        return [_["code"] for _ in json.loads(response.content)["messages"]]

    @contextlib.contextmanager
    def warnings(self):
        """The WARNING records the server logged (loguru), as a list."""
        records = []
        handler = logger.add(lambda _: records.append(_.record), level="WARNING")
        try:
            yield records
        finally:
            logger.remove(handler)

    def assert_applied(self, tracker, applied: bool):
        tracker.refresh_from_db()
        self.assertEqual(tracker.status, "in_transit" if applied else "pending")
        self.assertEqual(
            [_["description"] for _ in tracker.events],
            [DESCRIPTION] if applied else [],
        )


class TestWebhookSignatureMatrix(WebhookSignatureCase):
    """The proven probe: 8 combinations, all accepted at the tag."""

    def test_only_the_signed_event_with_a_stored_secret_is_accepted(self):
        raw = compact(event_body())
        results = {}
        for stored in (SECRET, None):
            for label, signature in (
                ("no header", None),
                ("wrong signature", "deadbeef"),
                ("other secret", sign(raw, OTHER_SECRET)),
                ("correct signature", sign(raw)),
            ):
                connection, tracker = self.make_connection(
                    stored, carrier_id=f"s17-{stored}-{label}".replace(" ", "-")
                )
                response = self.post(connection, raw, signature)
                results[(bool(stored), label)] = (response.status_code, json.loads(response.content))
                self.assert_applied(tracker, response.status_code == 200)

        accepted = [k for k, (code, _) in results.items() if code == 200]
        rejected = [k for k, (code, _) in results.items() if code == 401]
        self.assertEqual(accepted, [(True, "correct signature")])
        self.assertEqual(len(rejected), 7, results)
        self.assertEqual(results[(True, "correct signature")][1]["messages"], [])
        # One body for every rejection: no hint whether a secret is configured.
        for key in rejected:
            self.assertEqual(results[key][1], REJECTION, key)

    def test_the_specific_reason_is_logged_not_answered(self):
        raw = compact(event_body())
        cases = (
            (SECRET, None, "webhook_signature_missing"),
            (SECRET, "deadbeef", "invalid_signature"),
            (SECRET, sign(raw, OTHER_SECRET), "invalid_signature"),
            (None, sign(raw), "webhook_secret_not_configured"),
        )
        for stored, signature, reason in cases:
            connection, _ = self.make_connection(
                stored, carrier_id=f"s17-log-{reason}-{signature}"
            )
            with self.warnings() as records:
                response = self.post(connection, raw, signature)

            self.assertEqual(response.status_code, 401, reason)
            self.assertEqual(json.loads(response.content), REJECTION, reason)
            ours = [_ for _ in records if _["extra"].get("reason")]
            self.assertEqual(len(ours), 1, (reason, records))
            self.assertEqual(ours[0]["level"].name, "WARNING")
            self.assertEqual(ours[0]["extra"]["reason"], reason)
            self.assertEqual(ours[0]["extra"]["connection_id"], str(connection.pk))
            # connection id and reason only: never the header value, the secret or the body
            logged = f"{ours[0]['message']} {ours[0]['extra']}"
            for secret_text in (signature, SECRET, NUMBER, DESCRIPTION):
                if secret_text:
                    self.assertNotIn(secret_text, logged, reason)

    def test_an_accepted_event_logs_no_rejection(self):
        connection, _ = self.make_connection()
        raw = compact(event_body())
        with self.warnings() as records:
            self.assertEqual(self.post(connection, raw, sign(raw)).status_code, 200)
        self.assertEqual([_ for _ in records if _["extra"].get("reason")], [])

    def test_rejection_does_not_leak_the_secret(self):
        connection, _ = self.make_connection()
        response = self.post(connection, compact(event_body()), "deadbeef")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["success"])
        self.assertNotIn(SECRET, response.content.decode())

    def test_unknown_connection_is_still_404(self):
        connection, _ = self.make_connection()
        connection.delete()
        self.assertEqual(self.post(connection, compact(event_body())).status_code, 404)


class TestWebhookSignatureBodyForms(WebhookSignatureCase):
    def setUp(self):
        super().setUp()
        self.connection, self.tracker = self.make_connection()

    def test_compact_body_signed_as_sent(self):
        raw = compact(event_body())
        self.assertEqual(self.post(self.connection, raw, sign(raw)).status_code, 200)
        self.assert_applied(self.tracker, True)

    def test_indented_body_signed_as_sent(self):
        raw = json.dumps(event_body(), indent=4).encode()
        self.assertEqual(self.post(self.connection, raw, sign(raw)).status_code, 200)
        self.assert_applied(self.tracker, True)

    def test_non_ascii_body_signed_as_sent(self):
        body = event_body("Zugestellt – Müller, 東京 ✓")
        raw = compact(body)
        self.assertIn("東京".encode(), raw)
        response = self.post(self.connection, raw, sign(raw))
        self.assertEqual(response.status_code, 200, response.content)
        self.tracker.refresh_from_db()
        self.assertEqual(self.tracker.events[0]["description"], "Zugestellt – Müller, 東京 ✓")

    def test_signature_of_the_compact_form_of_a_differently_formatted_body(self):
        """JSON.stringify(payload) signed, body re-indented in transit."""
        body = event_body()
        raw = json.dumps(body, indent=2).encode()
        self.assertEqual(
            self.post(self.connection, raw, sign(compact(body))).status_code, 200
        )
        self.assert_applied(self.tracker, True)

    def test_compact_form_keeps_the_received_key_order(self):
        body = event_body()
        sorted_signature = sign(compact(json.loads(json.dumps(body, sort_keys=True))))
        raw = json.dumps(body, indent=2).encode()
        response = self.post(self.connection, raw, sorted_signature)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), REJECTION)
        self.assert_applied(self.tracker, False)

    def test_non_ascii_compact_form_is_not_ascii_escaped(self):
        body = event_body("Müller 東京")
        raw = json.dumps(body, indent=2, ensure_ascii=False).encode()
        self.assertEqual(
            self.post(self.connection, raw, sign(compact(body))).status_code, 200
        )

    def test_the_old_indented_sorted_form_is_never_accepted(self):
        body = event_body("Müller")
        old_form = lib.to_json(body).encode()  # indent=4, sorted keys, ASCII escapes
        raw = compact(body)
        self.assertNotEqual(old_form, raw)
        response = self.post(self.connection, raw, sign(old_form))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), REJECTION)
        self.assert_applied(self.tracker, False)

    def test_a_tampered_body_is_rejected(self):
        raw = compact(event_body())
        tampered = compact(event_body("TAMPERED"))
        response = self.post(self.connection, tampered, sign(raw))
        self.assertEqual(response.status_code, 401)
        self.tracker.refresh_from_db()
        self.assertEqual(self.tracker.events, [])

    def test_signature_header_name_is_case_insensitive(self):
        """Django hands the headers over as 'X-Teleship-Signature'."""
        raw = compact(event_body())
        captured = {}
        original = WebhookEventSerializer.process_event

        def spy(request, pk):
            captured["headers"] = dict(request.headers)
            return original(request, pk)

        with patch.object(WebhookEventSerializer, "process_event", staticmethod(spy)):
            response = self.post(self.connection, raw, sign(raw))
        self.assertIn("X-Teleship-Signature", captured["headers"])
        self.assertEqual(response.status_code, 200)

    def test_signature_with_non_ascii_header_value_is_rejected_not_an_error(self):
        response = self.post(self.connection, compact(event_body()), "sïgnature")
        self.assertEqual(response.status_code, 401)


class TestWebhookUnencodableCompactForm(WebhookSignatureCase):
    """An escaped lone surrogate ("\\ud800") parses but has no UTF-8 form: the
    compact candidate cannot be built and must simply be absent, not break or
    decide the verification of the raw body."""

    def setUp(self):
        super().setUp()
        self.connection, self.tracker = self.make_connection()
        self.raw = json.dumps({**event_body(), "extension": "\ud800"}).encode()
        self.assertIn(b"\\ud800", self.raw)

    def test_raw_signed_event_is_accepted_and_applied(self):
        response = self.post(self.connection, self.raw, sign(self.raw))
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.codes(response), [])
        self.assert_applied(self.tracker, True)

    def test_wrong_signature_is_a_401_and_nothing_is_applied(self):
        for signature in ("deadbeef", sign(self.raw, OTHER_SECRET)):
            response = self.post(self.connection, self.raw, signature)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(json.loads(response.content), REJECTION)
            self.assert_applied(self.tracker, False)

    def test_missing_signature_is_a_401_and_nothing_is_applied(self):
        response = self.post(self.connection, self.raw)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), REJECTION)
        self.assert_applied(self.tracker, False)


class TestWebhookRawBodyCapture(WebhookSignatureCase):
    def test_raw_bytes_reach_the_hook_and_the_request_still_parses(self):
        connection, _ = self.make_connection()
        body = event_body("Müller")
        raw = json.dumps(body, indent=3, ensure_ascii=False).encode()
        captured = {}

        def fake(payload, carrier=None, **kwargs):
            captured.update(payload)
            return None, []

        with patch("karrio.server.core.gateway.Hooks.on_webhook_event", side_effect=fake):
            response = self.post(connection, raw, "anything")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(captured["raw_body"], raw)
        self.assertEqual(captured["body"], body)  # DRF parsed it after the raw read
        self.assertEqual(
            list(captured["body"]["data"]), list(body["data"])
        )

    def test_unreadable_raw_body_is_not_an_error_and_still_fails_closed(self):
        connection, tracker = self.make_connection()
        parsed = event_body()

        class Request:
            data = parsed
            query_params = {}
            headers = {"x-teleship-signature": "deadbeef"}

            @property
            def body(self):
                raise RawPostDataException("stream already read")

            def build_absolute_uri(self):
                return "http://testserver/webhook"

        data, status = WebhookEventSerializer.process_event(Request(), connection.pk)
        self.assertEqual(status, 401)
        self.assertEqual(data, REJECTION)
        self.assert_applied(tracker, False)
