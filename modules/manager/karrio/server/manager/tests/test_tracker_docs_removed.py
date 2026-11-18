from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.manager.models import Tracking


class TestTrackerDocsRemoved(APITestCase):
    def test_dead_download_route_is_not_registered(self):
        with self.assertRaises(NoReverseMatch):
            reverse("karrio.server.manager:tracker-docs", kwargs={"pk": "trk_test", "doc": "delivery_image"})
        # These spellings reached the dead view anonymously (the unanchored
        # pattern matched a prefix). The two-segment form that the model used
        # to advertise resolves to the carrier/number route instead.
        for path in [
            "/v1/trackers/trk_test/image/extra",
            "/v1/trackers/trk_test/delivery_image/",
        ]:
            with self.subTest(path=path), self.assertRaises(Resolver404):
                resolve(path)

    def test_image_urls_are_null_and_full_tracker_still_serializes(self):
        tracker = Tracking.objects.create(
            tracking_number="TEST-IMAGE", test_mode=True, created_by=self.user,
            carrier=create_carrier_snapshot(self.dhl_carrier),
            delivery_image="test-image", signature_image="test-signature",
        )
        response = self.client.get(reverse(
            "karrio.server.manager:tracker-details", kwargs={"identifier": tracker.pk}
        ))
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["id"], tracker.pk)
        self.assertIsNone(response.data["delivery_image_url"])
        self.assertIsNone(response.data["signature_image_url"])
