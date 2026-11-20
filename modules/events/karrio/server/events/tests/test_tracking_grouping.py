import datetime
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model

import karrio.server.providers.models as providers
from karrio.server.core.tests import APITestCase
from karrio.server.core.utils import create_carrier_snapshot
from karrio.server.events.task_definitions.base import tracking
from karrio.server.manager import models

STALE = datetime.timedelta(seconds=0.1)
SHARED_LABEL = "shared-label"


class TestTrackerPollingGroups(APITestCase):
    """The tracker sweep must poll every tracker with its own connection.

    The carrier_id label is free text chosen by each owner, so two owners can
    use the same label for different connections (and even for different
    carriers). Grouping by that label must never decide which credentials a
    tracker is polled with.
    """

    def setUp(self) -> None:
        super().setUp()
        users = get_user_model().objects
        self.user_a = users.create_user("poll-a@example.com", "test")
        self.user_b = users.create_user("poll-b@example.com", "test")
        self.past = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)

    # ── fixtures ────────────────────────────────────────────────────────────

    def _own(self, user, account, carrier_id=SHARED_LABEL):
        return providers.CarrierConnection.objects.create(
            carrier_code="ups",
            carrier_id=carrier_id,
            test_mode=True,
            active=True,
            created_by=user,
            credentials=dict(
                client_id=f"client-{account}",
                client_secret="secret",
                account_number=account,
            ),
        )

    def _tracker(self, user, connection, number, snapshot=None):
        tracker = models.Tracking.objects.create(
            tracking_number=number,
            test_mode=True,
            delivered=False,
            status="in_transit",
            created_by=user,
            carrier=(
                create_carrier_snapshot(connection) if snapshot is None else snapshot
            ),
        )
        models.Tracking.objects.filter(pk=tracker.pk).update(updated_at=self.past)
        return tracker

    # ── harness ─────────────────────────────────────────────────────────────

    def _sweep(self):
        """Run the real dispatcher and the real per-group processing.

        Only the carrier HTTP layer (karrio.Tracking.fetch) and the Huey
        enqueue are replaced. Returns the dispatched groups, the account
        number each tracking number was polled with, and the context each
        tracing record was saved under.
        """
        groups, polled, traced = [], {}, []

        def _fetch(request):
            numbers = list(request.tracking_numbers)

            def _from(gateway):
                for number in numbers:
                    polled[number] = gateway.settings.account_number
                return MagicMock(parse=MagicMock(return_value=([], [])))

            return MagicMock(from_=_from)

        def _dispatch(tracker_ids, **kwargs):
            groups.append(sorted(tracker_ids))
            tracking.process_carrier_trackers(tracker_ids=tracker_ids)

        with patch.object(
            tracking, "karrio"
        ) as mock_karrio, patch(
            "karrio.server.events.task_definitions.base.process_carrier_tracking_batch",
            side_effect=_dispatch,
        ), patch.object(
            tracking.tracing,
            "bulk_save_tracing_records",
            side_effect=lambda tracer, context=None: traced.append(context),
        ):
            mock_karrio.Tracking.fetch.side_effect = _fetch
            tracking.update_trackers(delta=STALE)

        return groups, polled, traced

    # ── (1) two owners, same label, own connections ────────────────────────

    def test_same_label_two_owners_poll_with_their_own_connection(self):
        conn_a = self._own(self.user_a, "AAAAAA")
        conn_b = self._own(self.user_b, "BBBBBB")
        tracker_a = self._tracker(self.user_a, conn_a, "1ZPOLL0000000001")
        tracker_b = self._tracker(self.user_b, conn_b, "1ZPOLL0000000002")

        groups, polled, _ = self._sweep()

        self.assertEqual(
            sorted(groups), sorted([[tracker_a.id], [tracker_b.id]]), "two groups"
        )
        self.assertEqual(polled["1ZPOLL0000000001"], "AAAAAA")
        self.assertEqual(polled["1ZPOLL0000000002"], "BBBBBB")

    def test_same_label_two_owners_is_safe_when_processed_in_one_task(self):
        """A task queued before the change may still carry a mixed group."""
        conn_a = self._own(self.user_a, "AAAAAA")
        conn_b = self._own(self.user_b, "BBBBBB")
        tracker_a = self._tracker(self.user_a, conn_a, "1ZPOLL0000000011")
        tracker_b = self._tracker(self.user_b, conn_b, "1ZPOLL0000000012")
        polled = {}

        def _fetch(request):
            numbers = list(request.tracking_numbers)

            def _from(gateway):
                for number in numbers:
                    polled[number] = gateway.settings.account_number
                return MagicMock(parse=MagicMock(return_value=([], [])))

            return MagicMock(from_=_from)

        with patch.object(tracking, "karrio") as mock_karrio, patch.object(
            tracking.time, "sleep"
        ):
            mock_karrio.Tracking.fetch.side_effect = _fetch
            tracking.process_carrier_trackers(
                tracker_ids=[tracker_a.id, tracker_b.id]
            )

        self.assertEqual(polled["1ZPOLL0000000011"], "AAAAAA")
        self.assertEqual(polled["1ZPOLL0000000012"], "BBBBBB")

    # ── (2) a brokered (platform) connection whose label equals an own one ─

    def test_brokered_tracker_is_not_polled_with_an_own_connection_of_the_same_label(
        self,
    ):
        system = providers.SystemConnection.objects.create(
            carrier_code="ups",
            carrier_id=SHARED_LABEL,
            test_mode=True,
            active=True,
            credentials=dict(
                client_id="client-system",
                client_secret="secret",
                account_number="SYSSYS",
            ),
        )
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_a
        )
        conn_b = self._own(self.user_b, "BBBBBB")
        tracker_a = self._tracker(self.user_a, brokered, "1ZPOLL0000000021")
        tracker_b = self._tracker(self.user_b, conn_b, "1ZPOLL0000000022")

        self.assertEqual(tracker_a.carrier["connection_type"], "brokered")

        groups, polled, _ = self._sweep()

        self.assertEqual(
            sorted(groups), sorted([[tracker_a.id], [tracker_b.id]]), "two groups"
        )
        # the brokered tracker uses the platform credentials, never the own account
        self.assertEqual(polled["1ZPOLL0000000021"], "SYSSYS")
        self.assertEqual(polled["1ZPOLL0000000022"], "BBBBBB")

    # ── (3) snapshots without a connection id ──────────────────────────────

    def test_legacy_snapshot_with_carrier_connection_id_is_polled_with_it(self):
        conn_a = self._own(self.user_a, "AAAAAA")
        conn_b = self._own(self.user_b, "BBBBBB")
        self._tracker(
            self.user_a,
            None,
            "1ZPOLL0000000031",
            snapshot={"carrier_id": SHARED_LABEL, "carrier_connection_id": conn_a.id},
        )
        self._tracker(
            self.user_b,
            None,
            "1ZPOLL0000000032",
            snapshot={"carrier_id": SHARED_LABEL, "carrier_connection_id": conn_b.id},
        )

        groups, polled, _ = self._sweep()

        self.assertEqual(len(groups), 2)
        self.assertEqual(polled["1ZPOLL0000000031"], "AAAAAA")
        self.assertEqual(polled["1ZPOLL0000000032"], "BBBBBB")

    def test_snapshot_without_connection_id_falls_back_to_the_label(self):
        """No connection id: grouped by label as before, never dropped or merged."""
        label_only = [
            self._tracker(
                self.user_a,
                None,
                f"1ZPOLL00000000{i}",
                snapshot={"carrier_id": "legacy-label"},
            )
            for i in (41, 42)
        ]
        conn_b = self._own(self.user_b, "BBBBBB", carrier_id="legacy-label")
        current = self._tracker(self.user_b, conn_b, "1ZPOLL0000000043")

        groups, polled, _ = self._sweep()

        self.assertEqual(
            sorted(groups),
            sorted([sorted(t.id for t in label_only), [current.id]]),
        )
        # the group that cannot be resolved (no connection id) is skipped with a
        # warning, as before, and does not stop the other group
        self.assertEqual(polled, {"1ZPOLL0000000043": "BBBBBB"})

    # ── (4) tracing is saved under each tracker's own context ──────────────

    def test_tracing_is_saved_under_each_trackers_own_context(self):
        conn_a = self._own(self.user_a, "AAAAAA")
        conn_b = self._own(self.user_b, "BBBBBB")
        self._tracker(self.user_a, conn_a, "1ZPOLL0000000051")
        self._tracker(self.user_b, conn_b, "1ZPOLL0000000052")

        _, _, traced = self._sweep()

        self.assertEqual(
            sorted(c.user.email for c in traced),
            ["poll-a@example.com", "poll-b@example.com"],
        )

    # ── (5) ordering and batch size are unchanged ──────────────────────────

    def test_single_connection_set_keeps_order_and_batch_size(self):
        conn = self._own(self.user_a, "AAAAAA")
        trackers = [
            self._tracker(self.user_a, conn, f"1ZPOLL00000001{i:02d}")
            for i in range(25)
        ]
        order = [t.id for t in models.Tracking.objects.filter(id__in=[t.id for t in trackers])]
        batches = []

        def _fetch(request):
            batches.append(list(request.tracking_numbers))
            return MagicMock(from_=MagicMock(return_value=MagicMock(parse=MagicMock(return_value=([], [])))))

        with patch.object(tracking, "karrio") as mock_karrio, patch.object(
            tracking.time, "sleep"
        ) as sleep, patch(
            "karrio.server.events.task_definitions.base.process_carrier_tracking_batch",
            side_effect=lambda tracker_ids, **kw: (
                dispatched.append(list(tracker_ids)),
                tracking.process_carrier_trackers(tracker_ids=tracker_ids),
            ),
        ):
            dispatched = []
            mock_karrio.Tracking.fetch.side_effect = _fetch
            tracking.update_trackers(delta=STALE)

        self.assertEqual(len(dispatched), 1)
        self.assertEqual(sorted(dispatched[0]), sorted(order))
        self.assertEqual([len(b) for b in batches], [10, 10, 5])
        # processing order follows the stored order of the group's trackers
        by_id = {t.id: t.tracking_number for t in trackers}
        expected = [by_id[i] for i in [t.id for t in models.Tracking.objects.filter(id__in=order)]]
        self.assertEqual([n for b in batches for n in b], expected)
        self.assertEqual(sleep.call_count, 2)

    # ── (6) one connection and one owner per group ─────────────────────────

    def _shared_system_connection(self):
        return providers.SystemConnection.objects.create(
            carrier_code="ups",
            carrier_id=SHARED_LABEL,
            test_mode=True,
            active=True,
            credentials=dict(
                client_id="client-system",
                client_secret="secret",
                account_number="SYSSYS",
            ),
        )

    def test_brokered_trackers_of_two_owners_on_one_system_connection_are_split(self):
        system = self._shared_system_connection()
        brokered_a = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_a
        )
        brokered_b = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_b
        )
        tracker_a = self._tracker(self.user_a, brokered_a, "1ZPOLL0000000061")
        tracker_b = self._tracker(self.user_b, brokered_b, "1ZPOLL0000000062")

        self.assertEqual(
            tracker_a.carrier["connection_id"], tracker_b.carrier["connection_id"]
        )

        groups, polled, traced = self._sweep()

        self.assertEqual(
            sorted(groups), sorted([[tracker_a.id], [tracker_b.id]]), "two groups"
        )
        # the platform credentials are used for both
        self.assertEqual(polled["1ZPOLL0000000061"], "SYSSYS")
        self.assertEqual(polled["1ZPOLL0000000062"], "SYSSYS")
        # each tracing record is saved under its own owner
        self.assertEqual(
            sorted(c.user.email for c in traced),
            ["poll-a@example.com", "poll-b@example.com"],
        )

    def test_brokered_trackers_of_two_owners_are_split_in_one_task(self):
        """A task queued before the change may still carry both owners."""
        system = self._shared_system_connection()
        brokered_a = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_a
        )
        brokered_b = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_b
        )
        tracker_a = self._tracker(self.user_a, brokered_a, "1ZPOLL0000000071")
        tracker_b = self._tracker(self.user_b, brokered_b, "1ZPOLL0000000072")
        traced = []

        with (
            patch.object(tracking, "karrio") as mock_karrio,
            patch.object(tracking.time, "sleep"),
            patch.object(
                tracking.tracing,
                "bulk_save_tracing_records",
                side_effect=lambda tracer, context=None: traced.append(context),
            ),
        ):
            mock_karrio.Tracking.fetch.return_value = MagicMock(
                from_=MagicMock(
                    return_value=MagicMock(parse=MagicMock(return_value=([], [])))
                )
            )
            tracking.process_carrier_trackers(tracker_ids=[tracker_a.id, tracker_b.id])

        self.assertEqual(
            sorted(c.user.email for c in traced),
            ["poll-a@example.com", "poll-b@example.com"],
        )

    def test_one_owners_trackers_on_a_system_connection_stay_one_group(self):
        system = self._shared_system_connection()
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=system, is_enabled=True, created_by=self.user_a
        )
        trackers = [
            self._tracker(self.user_a, brokered, f"1ZPOLL00000002{i:02d}")
            for i in range(25)
        ]
        batches, traced = [], []

        def _fetch(request):
            batches.append(list(request.tracking_numbers))
            return MagicMock(
                from_=MagicMock(
                    return_value=MagicMock(parse=MagicMock(return_value=([], [])))
                )
            )

        dispatched = []
        with (
            patch.object(tracking, "karrio") as mock_karrio,
            patch.object(tracking.time, "sleep") as sleep,
            patch.object(
                tracking.tracing,
                "bulk_save_tracing_records",
                side_effect=lambda tracer, context=None: traced.append(context),
            ),
            patch(
                "karrio.server.events.task_definitions.base.process_carrier_tracking_batch",
                side_effect=lambda tracker_ids, **kw: (
                    dispatched.append(list(tracker_ids)),
                    tracking.process_carrier_trackers(tracker_ids=tracker_ids),
                ),
            ),
        ):
            mock_karrio.Tracking.fetch.side_effect = _fetch
            tracking.update_trackers(delta=STALE)

        self.assertEqual(len(dispatched), 1)
        self.assertEqual(sorted(dispatched[0]), sorted(t.id for t in trackers))
        self.assertEqual([len(b) for b in batches], [10, 10, 5])
        self.assertEqual(sleep.call_count, 2)
        self.assertEqual({c.user.email for c in traced}, {"poll-a@example.com"})

    def test_groups_are_dispatched_in_label_order(self):
        for label, account in (("zeta", "ZZZZZZ"), ("alpha", "AAAAAA")):
            conn = self._own(self.user_a, account, carrier_id=label)
            self._tracker(self.user_a, conn, f"1ZPOLL{account}")

        with patch(
            "karrio.server.events.task_definitions.base.process_carrier_tracking_batch"
        ) as dispatch:
            tracking.update_trackers(delta=STALE)

        labels = [
            models.Tracking.objects.get(id=c.kwargs["tracker_ids"][0]).carrier[
                "carrier_id"
            ]
            for c in dispatch.call_args_list
        ]
        self.assertEqual(labels, ["alpha", "zeta"])
