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
        for identifier in [self.foreign.pk, self.foreign.tracking_number]:
            with self.subTest(identifier=identifier):
                self.assertEqual(self.lookup(identifier).status_code, 404)

    def test_anonymous_refused(self):
        self.client.credentials()
        for identifier in [self.own.pk, self.own.tracking_number]:
            with self.subTest(identifier=identifier):
                self.assertEqual(self.lookup(identifier).status_code, 401)

    def test_missing_identifier(self):
        self.assertEqual(self.lookup("trk_missing").status_code, 404)
