"""Tests for ?connection_id= driven dynamic metadata hydration."""

import datetime
import json
from unittest.mock import patch

import karrio.core.dynamic as core_dynamic
import karrio.core.models as core_models
from django.urls import reverse
from karrio.server.core.tests import APITestCase
from rest_framework import status


def _profile_metadata() -> core_dynamic.DynamicMetadata:
    """A minimal DynamicMetadata payload used across the tests."""
    return core_dynamic.DynamicMetadata(
        services=[
            core_models.ServiceLevel(
                service_code="canadapost_priority_dynamic",
                service_name="Priority (live)",
                currency="CAD",
                domicile=True,
            )
        ],
        options=[
            core_dynamic.OptionDescriptor(
                code="LIVE_OPT",
                name="canadapost_live_opt",
                value_type="bool",
                meta={"category": "DYNAMIC"},
            )
        ],
        service_availability={
            "canadapost_priority_dynamic": ["canadapost_live_opt"],
        },
        connection_config_defaults={"some_default": "live-value"},
        source="profile",
        fetched_at=datetime.datetime.now(datetime.UTC),
        ttl_seconds=3600,
    )


class TestCarrierDetailsDynamicMetadata(APITestCase):
    """`GET /v1/carriers/<name>` dynamic-metadata merge behaviour."""

    def test_no_connection_id_returns_static(self):
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        # Static-only — no dynamic-metadata marker.
        self.assertNotIn("_dynamic_metadata_sources", data)

    def test_connection_id_for_non_dynamic_carrier_no_ops(self):
        """canadapost Settings doesn't mix in DynamicMetadataMixin — response stays static."""
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_connection_id_unknown_returns_404(self):
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url, {"connection_id": "00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_connection_id_carrier_mismatch_returns_400(self):
        """connection belongs to canadapost, URL asks for ups → 400."""
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "ups"},
        )
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_merge_dynamic_metadata_called_when_connection_id_present(self):
        """With ?connection_id=, the view delegates to merge_dynamic_metadata."""
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        with patch(
            "karrio.server.core.dynamic.merge_dynamic_metadata",
            side_effect=lambda ref, **_: ref,
        ) as mock_merge:
            response = self.client.get(url, {"connection_id": str(self.carrier.pk)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_merge.call_count, 1)
        kwargs = mock_merge.call_args.kwargs
        self.assertEqual(kwargs["connection_id"], str(self.carrier.pk))
        self.assertEqual(kwargs["carrier_name"], "canadapost")


class TestCarrierServicesDynamicMetadata(APITestCase):
    def test_carrier_services_static(self):
        url = reverse(
            "karrio.server.providers:carrier-services",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCarrierOptionsDynamicMetadata(APITestCase):
    def test_carrier_options_static(self):
        url = reverse(
            "karrio.server.providers:carrier-options",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCarrierListSkipsDynamicMetadata(APITestCase):
    """`GET /v1/carriers` (list) must stay static even with a connection_id."""

    def test_list_ignores_connection_id(self):
        url = reverse("karrio.server.providers:carrier-list")
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        # No dynamic-metadata marker in any carrier block.
        for entry in data:
            self.assertNotIn("_dynamic_metadata_sources", entry)


class TestHasDynamicMetadataFlag(APITestCase):
    """The shipping app gates ?connection_id= calls on this flag."""

    def test_references_publishes_carriers_with_dynamic_metadata(self):
        """The references payload includes the (possibly empty) opted-in carrier list."""
        from karrio.server.core import dataunits

        references = dataunits.contextual_reference(self._request_with_user(), reduced=False)
        self.assertIn("carriers_with_dynamic_metadata", references)
        self.assertIsInstance(references["carriers_with_dynamic_metadata"], list)

    def test_carrier_details_exposes_has_dynamic_metadata(self):
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertIn("has_dynamic_metadata", data)
        # canadapost Settings does not mix in DynamicMetadataMixin.
        self.assertFalse(data["has_dynamic_metadata"])

    def test_carrier_list_exposes_has_dynamic_metadata(self):
        url = reverse("karrio.server.providers:carrier-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertTrue(data, "carrier list must not be empty in tests")
        for entry in data:
            self.assertIn("has_dynamic_metadata", entry)

    def test_flag_true_for_carrier_with_dynamic_mixin(self):
        """If we publish 'parcelone' as dynamic, the per-carrier flag flips on."""
        from karrio.server.core import dataunits

        with patch(
            "karrio.server.core.dynamic.carriers_with_dynamic_metadata",
            return_value={"canadapost"},
        ):
            references = dataunits.contextual_reference(self._request_with_user(), reduced=False)
            details = dataunits.get_carrier_details("canadapost", contextual_reference=references)

        self.assertTrue(details["has_dynamic_metadata"])
        self.assertIn("canadapost", references["carriers_with_dynamic_metadata"])

    def _request_with_user(self):
        from rest_framework.test import APIRequestFactory

        request = APIRequestFactory().get("/")
        request.user = self.user
        return request


class TestMergeRules(APITestCase):
    """Direct unit tests on the merge function — no HTTP, no DB."""

    def test_merge_unions_services_dynamic_wins_on_collision(self):
        from karrio.server.core.dynamic import _merge

        static = {
            "services": {"canadapost": {"canadapost_priority": "canadapost_priority"}},
            "service_names": {"canadapost": {"canadapost_priority": "Priority"}},
            "options": {"canadapost": {"canadapost_signature": {"type": "bool"}}},
            "connection_configs": {"canadapost": {"some_default": {"default": "static"}}},
        }
        merged = _merge(static, _profile_metadata(), "canadapost")

        self.assertDictEqual(
            merged["services"]["canadapost"],
            {
                "canadapost_priority": "canadapost_priority",
                "canadapost_priority_dynamic": "canadapost_priority_dynamic",
            },
        )
        self.assertEqual(
            merged["service_names"]["canadapost"]["canadapost_priority_dynamic"],
            "Priority (live)",
        )
        self.assertIn("canadapost_live_opt", merged["options"]["canadapost"])
        self.assertEqual(
            merged["connection_configs"]["canadapost"]["some_default"]["default"],
            "live-value",
        )
        self.assertEqual(
            merged["service_availability"]["canadapost"]["canadapost_priority_dynamic"],
            ["canadapost_live_opt"],
        )
        self.assertEqual(merged["_dynamic_metadata_sources"]["canadapost"], "profile")

    def test_merge_does_not_mutate_input(self):
        from karrio.server.core.dynamic import _merge

        static = {"services": {"canadapost": {}}, "service_names": {"canadapost": {}}}
        before = json.dumps(static, sort_keys=True)
        _merge(static, _profile_metadata(), "canadapost")
        self.assertEqual(json.dumps(static, sort_keys=True), before)

    def test_merge_exclusive_replaces_static_catalog(self):
        """``DynamicMetadata.exclusive=True`` makes the dynamic catalog fully
        supersede the static one for that carrier.

        Used by connectors whose live catalog is authoritative — e.g.
        ParcelOne ``/profile`` — so the picker never offers a service
        the vendor API would actually reject.
        """
        from karrio.server.core.dynamic import _merge

        static_only_service = "canadapost_legacy_only_in_static"
        static_only_option = "canadapost_legacy_signature"
        static = {
            "services": {"canadapost": {static_only_service: static_only_service}},
            "service_names": {"canadapost": {static_only_service: "Legacy"}},
            "options": {"canadapost": {static_only_option: {"type": "bool"}}},
        }
        dyn = _profile_metadata()
        dyn.exclusive = True

        merged = _merge(static, dyn, "canadapost")

        self.assertDictEqual(
            merged["services"]["canadapost"],
            {"canadapost_priority_dynamic": "canadapost_priority_dynamic"},
        )
        self.assertDictEqual(
            merged["service_names"]["canadapost"],
            {"canadapost_priority_dynamic": "Priority (live)"},
        )
        # Only the live option survives; the static one is dropped.
        self.assertNotIn(static_only_option, merged["options"]["canadapost"])
        self.assertIn("canadapost_live_opt", merged["options"]["canadapost"])


class TestSignalInvalidation(APITestCase):
    """post_save / post_delete on CarrierConnection trigger cache invalidation."""

    def test_post_save_calls_invalidate(self):
        with patch("karrio.server.core.dynamic.invalidate") as mock_invalidate:
            self.carrier.test_mode = not self.carrier.test_mode
            self.carrier.save()
        mock_invalidate.assert_called_with(str(self.carrier.pk))

    def test_post_delete_calls_invalidate(self):
        # Create a throwaway connection so we can delete without affecting fixtures.
        import karrio.server.providers.models as providers

        connection = providers.CarrierConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost_to_delete",
            test_mode=True,
            active=True,
            created_by=self.user,
            credentials={"username": "x", "customer_number": "1", "contract_id": "1", "password": "p"},
        )
        pk = str(connection.pk)
        with patch("karrio.server.core.dynamic.invalidate") as mock_invalidate:
            connection.delete()
        mock_invalidate.assert_called_with(pk)


class TestAnonymousConnectionIdRejected(APITestCase):
    """Public catalog endpoints stay public for the static path, but ?connection_id= requires auth.

    The dynamic path resolves a real connection and may use stored credentials
    to fetch per-account catalogs — exposing it to anonymous callers would
    leak per-tenant metadata to anyone who guesses a connection id.
    """

    def setUp(self) -> None:
        super().setUp()
        # Drop the auto-applied auth token so requests go out anonymous.
        self.client.credentials()

    def test_carrier_details_anonymous_with_connection_id_returns_401(self):
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_carrier_services_anonymous_with_connection_id_returns_401(self):
        url = reverse(
            "karrio.server.providers:carrier-services",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_carrier_options_anonymous_with_connection_id_returns_401(self):
        url = reverse(
            "karrio.server.providers:carrier-options",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url, {"connection_id": str(self.carrier.pk)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_carrier_details_anonymous_static_path_still_public(self):
        """No ?connection_id= → public static catalog stays reachable without auth."""
        url = reverse(
            "karrio.server.providers:carrier-details",
            kwargs={"carrier_name": "canadapost"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDynamicMixinDiscovery(APITestCase):
    """`carriers_with_dynamic_metadata()` must look at the right attribute."""

    def test_discovery_uses_capital_S_settings_attribute(self):
        """PluginMetadata exposes the settings class as `Settings` — not `settings`.

        Regression test for the typo that left has_dynamic_metadata always
        false. We register a fake provider whose `Settings` mixes in
        :class:`DynamicMetadataMixin` and assert the discovery picks it up.
        """
        from karrio.server.core import dynamic as core_dynamic_server

        class _FakeSettings(core_dynamic.DynamicMetadataMixin):
            pass

        class _FakeProvider:
            Settings = _FakeSettings
            settings = None  # the typo path: must NOT be what we read.

        fake_providers = {"_fake_dynamic_carrier": _FakeProvider}
        with patch("karrio.sdk.gateway") as mock_gateway:
            mock_gateway.providers = fake_providers
            discovered = core_dynamic_server.carriers_with_dynamic_metadata()

        self.assertIn("_fake_dynamic_carrier", discovered)

    def test_discovery_skips_providers_without_settings(self):
        from karrio.server.core import dynamic as core_dynamic_server

        class _FakeProvider:
            Settings = None

        with patch("karrio.sdk.gateway") as mock_gateway:
            mock_gateway.providers = {"_fake_no_settings": _FakeProvider}
            discovered = core_dynamic_server.carriers_with_dynamic_metadata()

        self.assertNotIn("_fake_no_settings", discovered)

    def test_discovery_skips_providers_without_mixin(self):
        from karrio.server.core import dynamic as core_dynamic_server

        class _PlainSettings:
            pass

        class _FakeProvider:
            Settings = _PlainSettings

        with patch("karrio.sdk.gateway") as mock_gateway:
            mock_gateway.providers = {"_fake_plain": _FakeProvider}
            discovered = core_dynamic_server.carriers_with_dynamic_metadata()

        self.assertNotIn("_fake_plain", discovered)


class TestBrokeredAndSystemInvalidation(APITestCase):
    """Cache busts cover brokered / system connections, not just CarrierConnection."""

    def _make_system_and_brokered(self):
        import karrio.server.providers.models as providers

        system = providers.SystemConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost_system",
            test_mode=True,
            active=True,
            credentials={
                "username": "sys",
                "customer_number": "1",
                "contract_id": "1",
                "password": "p",
            },
        )
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=system,
            is_enabled=True,
            created_by=self.user,
        )
        return system, brokered

    def test_brokered_post_save_busts_brokered_cache(self):
        _, brokered = self._make_system_and_brokered()
        with patch("karrio.server.core.dynamic.invalidate") as mock_invalidate:
            brokered.is_enabled = not brokered.is_enabled
            brokered.save()
        mock_invalidate.assert_called_with(str(brokered.pk))

    def test_brokered_post_delete_busts_brokered_cache(self):
        _, brokered = self._make_system_and_brokered()
        pk = str(brokered.pk)
        with patch("karrio.server.core.dynamic.invalidate") as mock_invalidate:
            brokered.delete()
        mock_invalidate.assert_called_with(pk)

    def test_system_post_save_busts_each_brokered(self):
        system, brokered = self._make_system_and_brokered()
        with patch("karrio.server.core.dynamic.invalidate_for_system_connection") as mock_invalidate_for_system:
            system.test_mode = not system.test_mode
            system.save()
        mock_invalidate_for_system.assert_called_with(str(system.pk))

    def test_invalidate_for_system_iterates_all_linked_brokered(self):
        """The helper drops the per-brokered cache for every brokered tied to the system connection."""
        import karrio.server.providers.models as providers
        from karrio.server.core import dynamic as core_dynamic_server

        system, brokered_a = self._make_system_and_brokered()
        brokered_b = providers.BrokeredConnection.objects.create(
            system_connection=system,
            is_enabled=True,
            created_by=self.user,
        )

        with patch.object(core_dynamic_server, "_invalidate_connection") as mock_each:
            core_dynamic_server.invalidate_for_system_connection(str(system.pk))

        invalidated_pks = {call.args[0].pk for call in mock_each.call_args_list}
        self.assertEqual(invalidated_pks, {brokered_a.pk, brokered_b.pk})

    def test_invalidate_falls_back_to_brokered_lookup(self):
        """``invalidate(<brokered_pk>)`` resolves through BrokeredConnection too."""
        from karrio.server.core import dynamic as core_dynamic_server

        _, brokered = self._make_system_and_brokered()
        with patch.object(core_dynamic_server, "_invalidate_connection") as mock_each:
            core_dynamic_server.invalidate(str(brokered.pk))
        self.assertEqual(mock_each.call_count, 1)
        self.assertEqual(mock_each.call_args.args[0].pk, brokered.pk)
