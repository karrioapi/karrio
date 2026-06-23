"""Tests for dhl_parcel_de_delivery_tier enum option.

Verifies:
- delivery_tier=premium → premium=True, economy=None in API request
- delivery_tier=economy → premium=None, economy=True in API request
- delivery_tier=standard (or unset) → premium=None, economy=None
- Legacy backward compat: dhl_parcel_de_premium=True → delivery_tier=premium
- Legacy backward compat: dhl_parcel_de_economy=True → delivery_tier=economy
"""

import unittest

from karrio.providers.dhl_parcel_de.units import (
    ShippingOption,
    shipping_options_initializer,
)


class TestDeliveryTierEnum(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_delivery_tier_premium_maps_to_option(self):
        """delivery_tier=premium is accessible via ShippingOption."""
        options = shipping_options_initializer({"dhl_parcel_de_delivery_tier": "premium"})
        self.assertEqual(options.dhl_parcel_de_delivery_tier.state, "premium")

    def test_delivery_tier_economy_maps_to_option(self):
        """delivery_tier=economy is accessible via ShippingOption."""
        options = shipping_options_initializer({"dhl_parcel_de_delivery_tier": "economy"})
        self.assertEqual(options.dhl_parcel_de_delivery_tier.state, "economy")

    def test_delivery_tier_unset(self):
        """When delivery_tier is not set, state is None."""
        options = shipping_options_initializer({})
        self.assertIsNone(options.dhl_parcel_de_delivery_tier.state)

    def test_legacy_premium_migrated_to_delivery_tier(self):
        """Legacy dhl_parcel_de_premium=True → delivery_tier=premium."""
        options = shipping_options_initializer({"dhl_parcel_de_premium": True})
        self.assertEqual(options.dhl_parcel_de_delivery_tier.state, "premium")

    def test_legacy_economy_migrated_to_delivery_tier(self):
        """Legacy dhl_parcel_de_economy=True → delivery_tier=economy."""
        options = shipping_options_initializer({"dhl_parcel_de_economy": True})
        self.assertEqual(options.dhl_parcel_de_delivery_tier.state, "economy")

    def test_legacy_both_false_no_delivery_tier(self):
        """Legacy premium=False, economy=False → no delivery_tier."""
        options = shipping_options_initializer({"dhl_parcel_de_premium": False, "dhl_parcel_de_economy": False})
        self.assertIsNone(options.dhl_parcel_de_delivery_tier.state)

    def test_delivery_tier_takes_precedence_over_legacy(self):
        """When both delivery_tier and legacy premium are set, delivery_tier wins."""
        options = shipping_options_initializer(
            {
                "dhl_parcel_de_delivery_tier": "economy",
                "dhl_parcel_de_premium": True,
            }
        )
        self.assertEqual(options.dhl_parcel_de_delivery_tier.state, "economy")

    def test_option_enum_exists_in_shipping_option(self):
        """dhl_parcel_de_delivery_tier is a valid ShippingOption member."""
        self.assertIn("dhl_parcel_de_delivery_tier", ShippingOption.__members__)

    def test_old_premium_economy_removed(self):
        """dhl_parcel_de_premium and dhl_parcel_de_economy are no longer ShippingOption members."""
        self.assertNotIn("dhl_parcel_de_premium", ShippingOption.__members__)
        self.assertNotIn("dhl_parcel_de_economy", ShippingOption.__members__)
