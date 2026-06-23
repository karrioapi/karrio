from unittest import mock

from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.events.models as events
from karrio.server.events.task_definitions.base import archiving


class TestArchivingBatching(GraphTestCase):
    def test_batched_delete_spans_multiple_batches(self):
        """_batched_delete must loop until the queryset is drained (GH #1125).

        A small BATCH_SIZE forces several iterations so a regression that only
        deletes the first page (or loops forever) is caught.
        """
        events.Event.objects.bulk_create(
            [
                events.Event(type="test_event", test_mode=False, created_by=self.user)
                for _ in range(5)
            ]
        )
        seeded = events.Event.objects.count()
        self.assertGreaterEqual(seeded, 5)

        with mock.patch.object(archiving, "BATCH_SIZE", 2):
            deleted = archiving._batched_delete(events.Event.objects.all())

        self.assertEqual(deleted, seeded)
        self.assertEqual(events.Event.objects.count(), 0)

    def test_batched_delete_with_links_drains_queryset(self):
        """The link-aware variant must also drain across batches (GH #1125)."""
        events.Event.objects.bulk_create(
            [
                events.Event(type="test_event", test_mode=False, created_by=self.user)
                for _ in range(3)
            ]
        )
        seeded = events.Event.objects.count()

        with mock.patch.object(archiving, "BATCH_SIZE", 1):
            # link_model=None exercises the no-orgs path without extra fixtures.
            deleted = archiving._batched_delete_with_links(
                events.Event.objects.all(), None
            )

        self.assertEqual(deleted, seeded)
        self.assertEqual(events.Event.objects.count(), 0)
