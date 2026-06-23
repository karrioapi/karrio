"""Localization coverage — every service/option has an i18n label."""

import unittest

import karrio.providers.dhl_freight.i18n as i18n
import karrio.providers.dhl_freight.units as units


class TestDHLFreightI18n(unittest.TestCase):
    def test_every_service_has_a_translation(self):
        missing = [s.name for s in units.ShippingService if s.name not in i18n.SERVICE_NAME_TRANSLATIONS]
        self.assertEqual(missing, [], f"services missing i18n labels: {missing}")

    def test_every_option_has_a_translation(self):
        # Unified aliases (cash_on_delivery, insurance) point at dhl_freight_*
        # members and don't need their own label.
        aliases = {"cash_on_delivery", "insurance"}
        missing = [
            o.name
            for o in units.ShippingOption
            if o.name.startswith("dhl_freight_")
            and o.name not in aliases
            and o.name not in i18n.OPTION_NAME_TRANSLATIONS
        ]
        self.assertEqual(missing, [], f"options missing i18n labels: {missing}")

    def test_every_customs_option_has_a_translation(self):
        missing = [o.name for o in units.CustomsOption if o.name not in i18n.OPTION_NAME_TRANSLATIONS]
        self.assertEqual(missing, [], f"customs options missing i18n labels: {missing}")


if __name__ == "__main__":
    unittest.main()
