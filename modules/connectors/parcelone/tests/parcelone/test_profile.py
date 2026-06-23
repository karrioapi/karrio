"""ParcelOne profile fetcher tests."""

import unittest
from unittest.mock import patch

import karrio.core.dynamic as core_dynamic
import karrio.providers.parcelone.units as units
import karrio.providers.parcelone.utils as utils

from .fixture import gateway


class TestParcelOneProfile(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # Bust the module-level cache between tests.
        utils._PROFILE_CACHE.clear()

    def test_get_profile_proxy_hits_correct_url(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = '{"results": []}'
            gateway.proxy.get_profile()

        self.assertEqual(
            mock.call_args[1]["url"],
            f"{gateway.settings.server_url}/shippingapi/v1/profile",
        )
        self.assertEqual(mock.call_args[1]["method"], "GET")

    def test_settings_profile_normalizes_response(self):
        with patch("karrio.providers.parcelone.utils.lib.request") as mock:
            mock.return_value = ProfileResponseJSON
            profile = gateway.settings.profile

        self.assertEqual(profile["mandator"], "1")
        self.assertIn("PA1", profile["ceps"])
        self.assertIn("plusZ", profile["ceps"]["PA1"]["products"])
        self.assertIn("LMC", profile["ceps"]["PA1"]["products"]["plusZ"]["services"])

    def test_settings_profile_caches_per_connection(self):
        with patch("karrio.providers.parcelone.utils.lib.request") as mock:
            mock.return_value = ProfileResponseJSON
            first = gateway.settings.profile
            second = gateway.settings.profile

        self.assertIs(first, second)
        self.assertEqual(mock.call_count, 1)

    def test_settings_profile_falls_back_to_static_on_failure(self):
        with patch("karrio.providers.parcelone.utils.lib.request") as mock:
            mock.side_effect = RuntimeError("boom")
            profile = gateway.settings.profile

        # Static fallback present and shaped correctly.
        self.assertIn("ceps", profile)
        self.assertIn("PA1", profile["ceps"])
        self.assertEqual(profile, units.STATIC_PROFILE)

    def test_services_for_product_resolves_from_static(self):
        services = units.services_for_product("PA1", "plusZ")
        self.assertIn("LMC", services)
        self.assertIn("SRL", services)
        self.assertIn("SRO", services)

    def test_services_for_product_returns_empty_for_unknown(self):
        self.assertEqual(units.services_for_product("UNKNOWN", "x"), [])


class TestParcelOneDynamicMetadata(unittest.TestCase):
    """`fetch_dynamic_metadata` projection of profile → DynamicMetadata."""

    def setUp(self) -> None:
        self.maxDiff = None
        utils._PROFILE_CACHE.clear()

    def _preload_profile(self, profile: dict) -> None:
        s = gateway.settings
        utils._PROFILE_CACHE[(s.id or s.username, s.mandator_id, s.consigner_id)] = profile

    def test_settings_mixes_in_dynamic_metadata_mixin(self):
        """Connector opts into PR #764 augmentation so ``has_dynamic_metadata=true``."""
        self.assertIsInstance(gateway.settings, core_dynamic.DynamicMetadataMixin)

    def test_projection_produces_one_service_per_product(self):
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()

        # Every (CEP, Product) pair becomes a ServiceLevel.
        expected_count = sum(
            len(cep.get("products") or {}) for cep in (units.STATIC_PROFILE.get("ceps") or {}).values()
        )
        self.assertEqual(len(dyn.services), expected_count)
        self.assertEqual(dyn.source, "profile")

        service_codes = {s.service_code for s in dyn.services}
        # Smoke-check a few well-known codes from the static catalog.
        self.assertIn("parcelone_pa1_basic", service_codes)
        self.assertIn("parcelone_dhl_101", service_codes)
        self.assertIn("parcelone_ups_07", service_codes)

    def test_projection_is_exclusive(self):
        """ParcelOne ``/profile`` is authoritative — the dynamic catalog must
        flag ``exclusive=True`` so the server-side merge fully replaces the
        static enum rather than unioning with it.
        """
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()
        self.assertTrue(dyn.exclusive)

    def test_projection_unions_unique_options_across_products(self):
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()

        unique_service_ids = {
            sid
            for cep in (units.STATIC_PROFILE.get("ceps") or {}).values()
            for product in (cep.get("products") or {}).values()
            for sid in (product.get("services") or [])
        }
        self.assertEqual({o.code for o in dyn.options}, unique_service_ids)

    def test_known_service_id_reuses_static_enum_metadata(self):
        """A ServiceID present in ShippingOption maps back to its canonical key."""
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()

        sro = next((o for o in dyn.options if o.code == "SRO"), None)
        self.assertIsNotNone(sro)
        self.assertEqual(sro.name, "parcelone_return_only")
        self.assertEqual(sro.meta.get("category"), "RETURN")

    def test_unknown_service_id_falls_through_as_bare_descriptor(self):
        """A ServiceID with no static enum entry still surfaces — keyed on the wire code."""
        profile = {
            "mandator": "1",
            "consigners": ["1"],
            "ceps": {
                "FAKE": {
                    "name": "Fake Carrier",
                    "products": {
                        "X": {"name": "Test Product", "services": ["BRAND_NEW_SVC"]},
                    },
                },
            },
        }
        self._preload_profile(profile)
        dyn = gateway.settings.fetch_dynamic_metadata()

        new = next((o for o in dyn.options if o.code == "BRAND_NEW_SVC"), None)
        self.assertIsNotNone(new)
        self.assertEqual(new.name, "BRAND_NEW_SVC")
        self.assertEqual(new.meta, {"category": "DYNAMIC"})

    def test_service_availability_lists_options_per_service(self):
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()

        # PA1 plusZ should advertise LMC (selectable, not auto-attached) and
        # the return-label trio.
        plus_z_options = dyn.service_availability.get("parcelone_pa1_plusz", [])
        self.assertIn("parcelone_last_mile_tracking", plus_z_options)
        self.assertIn("parcelone_return_label", plus_z_options)
        self.assertIn("parcelone_return_only", plus_z_options)

    def test_connection_config_defaults_prefer_pa1(self):
        self._preload_profile(units.STATIC_PROFILE)
        dyn = gateway.settings.fetch_dynamic_metadata()
        self.assertEqual(dyn.connection_config_defaults.get("cep_id"), "PA1")
        self.assertIn(dyn.connection_config_defaults.get("product_id"), units.STATIC_PROFILE["ceps"]["PA1"]["products"])

    def test_empty_live_profile_falls_back_to_static_catalog(self):
        """An empty / broken live profile still publishes the static catalog.

        Profile fetch never silently swallows the catalog — the connector
        keeps publishing the static snapshot so the shipping app doesn't lose
        the service/option list when the vendor API is flaky.
        """
        self._preload_profile({})  # _fetch_profile returned None → empty cache value.
        dyn = gateway.settings.fetch_dynamic_metadata()
        self.assertEqual(dyn.source, "profile")
        self.assertFalse(dyn.is_empty)
        self.assertGreater(len(dyn.services), 0)


class TestParcelOneDynamicConfig(unittest.TestCase):
    """Tuning knobs are env-var driven, NOT user-facing connection fields."""

    def test_tuning_knobs_are_not_connection_fields(self):
        """``dynamic_ttl_seconds`` & friends must not show up as attrs fields.

        Annotated fields on the Settings dataclass leak into the Django
        connection model + schema generation. The tuning knobs are
        operational, so we expose them via ``connection_system_config`` and
        a read-only ``@property`` — matching the DHL Parcel DE convention.
        """
        import attr
        from karrio.mappers.parcelone.settings import Settings as MapperSettings

        attrs_fields = {f.name for f in attr.fields(MapperSettings)}
        for knob in (
            "dynamic_ttl_seconds",
            "dynamic_timeout_seconds",
            "dynamic_negative_ttl_seconds",
        ):
            self.assertNotIn(knob, attrs_fields, f"{knob} must not be an attrs/connection field")

    def test_tuning_knobs_default_to_baseline(self):
        self.assertDictEqual(_dynamic_knobs(gateway.settings), DEFAULT_DYNAMIC_KNOBS)

    def test_tuning_knobs_read_from_system_config(self):
        """Env-var-style overrides flow through ``connection_system_config``."""

        class _FakeSystemConfig:
            def get(self, key, default=None):
                return {
                    "PARCELONE_DYNAMIC_TTL_SECONDS": "900",
                    "PARCELONE_DYNAMIC_TIMEOUT_SECONDS": "2.5",
                    "PARCELONE_DYNAMIC_NEGATIVE_TTL_SECONDS": "30",
                }.get(key, default)

        original = gateway.settings.system_config
        gateway.settings.system_config = _FakeSystemConfig()
        try:
            self.assertDictEqual(_dynamic_knobs(gateway.settings), OVERRIDDEN_DYNAMIC_KNOBS)
        finally:
            gateway.settings.system_config = original


def _dynamic_knobs(settings) -> dict:
    """Snapshot the three dynamic-metadata tuning knobs into a comparable dict."""
    return {
        "dynamic_ttl_seconds": settings.dynamic_ttl_seconds,
        "dynamic_timeout_seconds": settings.dynamic_timeout_seconds,
        "dynamic_negative_ttl_seconds": settings.dynamic_negative_ttl_seconds,
    }


DEFAULT_DYNAMIC_KNOBS = {
    "dynamic_ttl_seconds": 3600,
    "dynamic_timeout_seconds": 1.5,
    "dynamic_negative_ttl_seconds": 60,
}

OVERRIDDEN_DYNAMIC_KNOBS = {
    "dynamic_ttl_seconds": 900,
    "dynamic_timeout_seconds": 2.5,
    "dynamic_negative_ttl_seconds": 30,
}


ProfileResponseJSON = """{
    "status": 200,
    "results": [{
        "MandatorID": "1",
        "Consigners": [{"ConsignerID": "1"}],
        "CEPs": [
            {
                "CEPID": "PA1",
                "CEPLongname": "PARCEL.ONE",
                "Products": [
                    {
                        "ProductID": "plusZ",
                        "ProductName": "Parcel Plus Z",
                        "Services": [
                            {"ServiceID": "LMC"},
                            {"ServiceID": "SRL"},
                            {"ServiceID": "SRO"}
                        ]
                    }
                ]
            }
        ]
    }]
}"""


if __name__ == "__main__":
    unittest.main()
