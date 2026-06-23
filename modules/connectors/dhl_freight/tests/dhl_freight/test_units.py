"""Carrier units — enums, mappings, services CSV."""

import unittest

import karrio.providers.dhl_freight.units as units


class TestShippingService(unittest.TestCase):
    def test_eurapid_maps_to_ECI(self):
        self.assertEqual(
            units.ShippingService.map("dhl_freight_eurapid").value,
            "ECI",
        )

    def test_euroconnect_maps_to_ECX(self):
        self.assertEqual(
            units.ShippingService.map("dhl_freight_euroconnect").value,
            "ECX",
        )

    def test_dom_resolves_by_value(self):
        """Mapping by DHL on-wire code returns the karrio service name."""
        self.assertEqual(
            units.ShippingService.map("DOM").name,
            "dhl_freight_domestic",
        )

    def test_unknown_service_falls_back(self):
        """Unknown codes go through the value_or_key shim, not raise."""
        result = units.ShippingService.map("UNKNOWN").value_or_key
        self.assertEqual(result, "UNKNOWN")


class TestPackagingType(unittest.TestCase):
    def test_pallet_maps_to_PAL(self):
        self.assertEqual(units.PackagingType.map("pallet").value, "PAL")
        self.assertEqual(units.PackagingType.map("PAL").value, "PAL")

    def test_box_maps_to_BOX(self):
        self.assertEqual(units.PackagingType.map("small_box").value, "BOX")
        self.assertEqual(units.PackagingType.map("medium_box").value, "BOX")
        self.assertEqual(units.PackagingType.map("large_box").value, "BOX")

    def test_your_packaging_defaults_to_pallet(self):
        self.assertEqual(units.PackagingType.map("your_packaging").value, "PAL")


class TestIncoterm(unittest.TestCase):
    def test_supported_terms(self):
        self.assertEqual(units.Incoterm.DAP.value, "DAP")
        self.assertEqual(units.Incoterm.DDP.value, "DDP")
        self.assertEqual(units.Incoterm.CPT.value, "CPT")
        self.assertEqual(units.Incoterm.CIP.value, "CIP")
        self.assertEqual(units.Incoterm.DPU.value, "DPU")


class TestPartyType(unittest.TestCase):
    def test_four_distinct_party_types(self):
        types = {t.value for t in units.PartyType}
        self.assertEqual(types, {"Consignor", "Consignee", "Pickup", "Delivery"})


class TestDefaultServices(unittest.TestCase):
    def test_services_csv_loaded(self):
        codes = {s.service_code for s in units.DEFAULT_SERVICES}
        # All five product codes from PRD §5.1 must be present.
        self.assertEqual(
            codes,
            {
                "dhl_freight_eurapid",
                "dhl_freight_euroconnect",
                "dhl_freight_euroconnect_plus",
                "dhl_freight_domestic",
                "dhl_freight_ftl",
            },
        )

    def test_domestic_service_is_domicile(self):
        dom = next(s for s in units.DEFAULT_SERVICES if s.service_code == "dhl_freight_domestic")
        self.assertTrue(dom.domicile)
        self.assertFalse(dom.international)

    def test_international_services_have_eu_country_codes(self):
        eurapid = next(s for s in units.DEFAULT_SERVICES if s.service_code == "dhl_freight_eurapid")
        self.assertTrue(eurapid.international)
        zone_countries = set(eurapid.zones[0].country_codes or [])
        # Sanity check — a few major EU countries should be in the zone.
        for country in {"DE", "FR", "IT", "ES", "NL"}:
            self.assertIn(country, zone_countries)

    def test_ftl_weight_band(self):
        """FTL is heavy freight — min 2500 kg, max 24t."""
        ftl = next(s for s in units.DEFAULT_SERVICES if s.service_code == "dhl_freight_ftl")
        self.assertEqual(ftl.min_weight, 2500.0)
        self.assertEqual(ftl.max_weight, 24000.0)


class TestShippingOption(unittest.TestCase):
    def test_loading_options_present(self):
        """LOADING category must include the four dock-service flags."""
        names = {o.name for o in units.ShippingOption}
        self.assertIn("dhl_freight_tail_lift_loading", names)
        self.assertIn("dhl_freight_tail_lift_unloading", names)
        self.assertIn("dhl_freight_side_loading_pickup", names)
        self.assertIn("dhl_freight_side_unloading_delivery", names)

    def test_country_specific_tax_options_present(self):
        names = {o.name for o in units.ShippingOption}
        self.assertIn("dhl_freight_uit_number", names)  # Romania
        self.assertIn("dhl_freight_ekaer_number", names)  # Hungary
        self.assertIn("dhl_freight_sent_number", names)  # Poland

    def test_unified_options_map_to_dhl_freight_options(self):
        """`cash_on_delivery` / `insurance` unified options route to DHL options."""
        self.assertEqual(
            units.ShippingOption.cash_on_delivery,
            units.ShippingOption.dhl_freight_cash_on_delivery,
        )
        self.assertEqual(
            units.ShippingOption.insurance,
            units.ShippingOption.dhl_freight_insurance,
        )


class TestSystemConfig(unittest.TestCase):
    def test_system_config_keys(self):
        expected = {
            "DHL_FREIGHT_CLIENT_ID",
            "DHL_FREIGHT_CLIENT_SECRET",
            "DHL_FREIGHT_SANDBOX_CLIENT_ID",
            "DHL_FREIGHT_SANDBOX_CLIENT_SECRET",
            "DHL_FREIGHT_ACCOUNT_NUMBER",
            "DHL_FREIGHT_SANDBOX_ACCOUNT_NUMBER",
        }
        self.assertEqual(set(units.SYSTEM_CONFIG.keys()), expected)


if __name__ == "__main__":
    unittest.main()
