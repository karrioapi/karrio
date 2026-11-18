from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.core.tests import APITestCase
from karrio.server.core.middleware import CreatorAccess
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.manager.models import Tracking


class TestTrackerAccess(APITestCase):
    def setUp(self):
        super().setUp()
        scope = patch(
            "karrio.server.core.models.base.get_access_filter", CreatorAccess()
        )
        scope.start()
        self.addCleanup(scope.stop)
        self.other = get_user_model().objects.create_user("other@example.com", "test")
        self.own = Tracking.objects.create(
            tracking_number="OWNER-TRACK",
            test_mode=True,
            created_by=self.user,
            carrier=create_carrier_snapshot(self.dhl_carrier),
        )
        self.foreign = Tracking.objects.create(
            tracking_number="FOREIGN-TRACK",
            test_mode=True,
            created_by=self.other,
            carrier=create_carrier_snapshot(self.dhl_carrier),
        )

    def lookup(self, identifier):
        return self.client.get(
            reverse(
                "karrio.server.manager:tracker-details",
                kwargs=dict(identifier=identifier),
            )
        )

    def test_owner_id_and_tracking_number(self):
        for identifier in [self.own.pk, self.own.tracking_number]:
            with self.subTest(identifier=identifier):
                response = self.lookup(identifier)
                self.assertResponseNoErrors(response)
                self.assertEqual(response.data["id"], self.own.pk)

    def test_other_owner_id_and_tracking_number(self):
        response = self.lookup(self.foreign.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lookup(self.foreign.tracking_number).status_code, 404)
        self.client.credentials()
        self.assertDictEqual(response.data, self.lookup(self.foreign.pk).data)
        self.assertNotIn("id", response.data)

    def test_anonymous_public_shape(self):
        self.own.info = {"recipient_name": "PRIVATE", "account_number": "PRIVATE"}
        self.own.delivery_image = "PRIVATE-IMAGE"
        self.own.signature_image = "PRIVATE-SIGNATURE"
        self.own.options = {"private": "PRIVATE"}
        self.own.metadata = {"private": "PRIVATE"}
        self.own.reference = "PRIVATE"
        self.own.account_number = "PRIVATE"
        self.own.meta = {"secret": "PRIVATE"}
        self.own.messages = [{"message": "PRIVATE"}]
        self.own.events = [
            {
                "date": "2026-11-15",
                "time": "12:00",
                "location": "Depot",
                "description": "In transit",
                "code": "PRIVATE",
                "extra": "PRIVATE",
            }
        ]
        self.own.save()
        self.client.credentials()
        response = self.lookup(self.own.pk)
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            response.data,
            {
                "carrier_name": self.own.carrier_name,
                "tracking_number": "OWNER-TRACK",
                "status": self.own.status,
                "delivered": False,
                "estimated_delivery": None,
                "events": [
                    {
                        "date": "2026-11-15",
                        "time": "12:00",
                        "location": "Depot",
                        "description": "In transit",
                    }
                ],
            },
        )

    def test_anonymous_misses_are_identical(self):
        self.client.credentials()
        responses = [
            self.lookup(identifier)
            for identifier in [
                self.own.tracking_number,
                self.foreign.tracking_number,
                "trk_" + "0" * 32,
                "trk_missing",
                self.own.pk.upper(),
            ]
        ]
        self.assertListEqual(
            [response.status_code for response in responses], [404] * len(responses)
        )
        for response in responses:
            self.assertDictEqual(response.data, responses[0].data)

    def test_missing_identifier(self):
        self.assertEqual(self.lookup("trk_missing").status_code, 404)

    def test_public_event_values_are_strings_or_null(self):
        self.client.credentials()
        for value in [{"secret": "PRIVATE"}, ["PRIVATE"], 123, True, None]:
            with self.subTest(value=value):
                self.own.events = [dict.fromkeys(
                    ["date", "time", "location", "description"], value
                )]
                self.own.save()
                response = self.lookup(self.own.pk)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["events"], [dict.fromkeys(
                    ["date", "time", "location", "description"]
                )])

    def test_archived_tracker_is_hidden_for_all_callers(self):
        self.own.is_archived = True
        self.own.save()
        self.assertEqual(self.lookup(self.own.pk).status_code, 404)
        self.client.credentials()
        self.assertEqual(self.lookup(self.own.pk).status_code, 404)

    def test_bad_credentials_do_not_fall_through(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid-test-token")
        self.assertEqual(self.lookup(self.own.pk).status_code, 401)
