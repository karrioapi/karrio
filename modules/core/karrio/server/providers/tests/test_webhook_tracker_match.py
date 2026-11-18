"""Signed carrier events must stay within their connection's tracker pool."""
import hashlib
import hmac
from types import SimpleNamespace

import karrio.lib as lib
from django.contrib.auth import get_user_model
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.manager.models import Tracking
from karrio.server.providers.models import CarrierConnection
from karrio.server.providers.serializers.base import WebhookEventSerializer


class TestWebhookTrackerMatch(APITestCase):
    def setUp(self):
        super().setUp()
        self.other = get_user_model().objects.create_user("other-match@example.com", "test")
        self.connection = CarrierConnection.objects.create(
            carrier_code="teleship", carrier_id="test-connection", test_mode=True,
            created_by=self.user, credentials={"client_id": "test-client", "client_secret": "test-secret"},
            config={"webhook_secret": "test-signing-secret"},
        )
        self.snapshot = create_carrier_snapshot(self.connection)
        self.own = self.tracker(self.user, self.snapshot)
        # Newest first: the old OR query chooses the foreign row.
        foreign_connection = CarrierConnection.objects.create(
            carrier_code="teleship", carrier_id="other-connection", test_mode=True,
            created_by=self.other,
            credentials={"client_id": "other-test-client", "client_secret": "other-test-secret"},
        )
        self.foreign = self.tracker(self.other, create_carrier_snapshot(foreign_connection))
        self.body = {
            "eventName": "shipment.updated", "objectType": "shipment",
            "objectId": "test-shipment", "data": {
                "trackingNumber": "SHARED-NUMBER",
                "firstMile": {"carrier": "test"}, "lastMile": {},
                "shipTo": {"address": {"city": "Test", "country": "US"}},
                "shipFrom": {"address": {"country": "GB"}},
                "events": [{"timestamp": "2026-11-15T12:00:00Z",
                            "code": "in_transit", "description": "Test event"}],
            },
        }

    def tracker(self, user, snapshot, number="SHARED-NUMBER"):
        return Tracking.objects.create(
            tracking_number=number, test_mode=True, created_by=user,
            carrier=snapshot, status="pending", events=[],
        )

    def event(self):
        signature = hmac.new(b"test-signing-secret", lib.to_json(self.body).encode(), hashlib.sha256).hexdigest()
        request = SimpleNamespace(
            data=self.body, query_params={},
            headers={"x-teleship-signature": signature},
            build_absolute_uri=lambda: "http://testserver/webhook",
        )
        return WebhookEventSerializer.process_event(request, self.connection.pk)

    def test_signed_event_isolates_two_tenants(self):
        result, status = self.event()
        self.assertEqual(status, 200)
        self.assertTrue(result["success"], result)
        self.foreign.refresh_from_db()
        self.own.refresh_from_db()
        self.assertEqual(self.foreign.events, [])
        self.assertEqual(self.foreign.status, "pending")
        self.assertEqual(self.own.events[0]["description"], "Test event")
        self.assertEqual(self.own.status, "in_transit")

    def test_ambiguous_match_is_noop(self):
        duplicate = self.tracker(self.user, self.snapshot)
        self.event()
        for tracker in [self.own, self.foreign, duplicate]:
            tracker.refresh_from_db()
            self.assertEqual(tracker.events, [])
            self.assertEqual(tracker.status, "pending")

    def test_number_must_match_as_well_as_connection(self):
        self.own.delete()
        unrelated = self.tracker(self.user, self.snapshot, "OTHER-NUMBER")
        self.event()
        for tracker in [unrelated, self.foreign]:
            tracker.refresh_from_db()
            self.assertEqual(tracker.events, [])
