"""Tests for the installed-vs-enabled carrier decoupling: live toggle, admin/tenant split, and no N+1."""

import karrio.server.core.dataunits as dataunits
from constance import config
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.exceptions import ValidationError

# A carrier whose connector is always installed in the test image.
CARRIER = "fedex"


class TestCarrierPluginVisibility(TestCase):
    def setUp(self):
        self.maxDiff = None
        # Always restore the flag so a failing assert can't leak into siblings.
        self.addCleanup(setattr, config, f"{CARRIER.upper()}_ENABLED", True)
        setattr(config, f"{CARRIER.upper()}_ENABLED", True)

    def test_installed_catalog_includes_carrier_regardless_of_enabled(self):
        # The cached catalog is the full installed set — independent of the flag.
        setattr(config, f"{CARRIER.upper()}_ENABLED", False)
        self.assertIn(CARRIER, dataunits.REFERENCE_MODELS["carriers"])
        self.assertIn(CARRIER, dataunits.CARRIER_NAMES)

    def test_enabled_set_reflects_toggle_live(self):
        # Enabled by default ...
        self.assertIn(CARRIER, dataunits.get_enabled_carrier_ids())
        # ... disabling takes effect immediately, same process, no rebuild ...
        setattr(config, f"{CARRIER.upper()}_ENABLED", False)
        self.assertNotIn(CARRIER, dataunits.get_enabled_carrier_ids())
        # ... and re-enabling too.
        setattr(config, f"{CARRIER.upper()}_ENABLED", True)
        self.assertIn(CARRIER, dataunits.get_enabled_carrier_ids())

    def test_contextual_reference_hides_disabled_from_tenant_keeps_for_admin(self):
        setattr(config, f"{CARRIER.upper()}_ENABLED", False)

        tenant_view = dataunits.contextual_reference(reduced=False)
        self.assertNotIn(CARRIER, tenant_view["carriers"])
        self.assertNotIn(CARRIER, tenant_view["services"])

        admin_view = dataunits.contextual_reference(reduced=False, include_disabled=True)
        self.assertIn(CARRIER, admin_view["carriers"])

    def test_ensure_carrier_enabled_blocks_tenant_allows_admin(self):
        setattr(config, f"{CARRIER.upper()}_ENABLED", False)

        # Non-admin (no admin path) → rejected.
        with self.assertRaises(ValidationError):
            dataunits.ensure_carrier_enabled(CARRIER, request=None)

        # Admin surface → exempt.
        admin_request = type("Req", (), {"path": "/admin/graphql"})()
        self.assertIsNone(dataunits.ensure_carrier_enabled(CARRIER, request=admin_request))

        # Enabled carrier is always allowed.
        setattr(config, f"{CARRIER.upper()}_ENABLED", True)
        self.assertIsNone(dataunits.ensure_carrier_enabled(CARRIER, request=None))

    def test_enabled_set_is_a_single_constance_query_not_n_plus_1(self):
        # Reading the enabled set for every installed carrier + LSP must be ONE
        # batched constance query, not a per-plugin loop. Guards against
        # reintroducing the constance N+1 on the hot /v1/references path.
        with CaptureQueriesContext(connection) as ctx:
            carriers, _lsp = dataunits.get_enabled_plugin_ids()

        self.assertIn(CARRIER, carriers)
        constance_queries = [q for q in ctx.captured_queries if "constance_constance" in q["sql"]]
        # At most one constance query total (single-tenant: one batched IN; under
        # MULTI_TENANTS it reads tenant flags with zero queries). Never one-per-plugin.
        self.assertLessEqual(
            len(constance_queries),
            1,
            f"enabled set must not fan out into per-plugin queries, got {len(constance_queries)}",
        )
        if constance_queries:
            self.assertIn(
                " IN (",
                constance_queries[0]["sql"],
                "enabled flags must be read with a single IN (...) query",
            )
