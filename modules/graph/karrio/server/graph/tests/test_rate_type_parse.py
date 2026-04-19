"""Regression tests for RateType.parse — must tolerate partial/legacy
selected_rate JSON blobs that lack id/carrier_name/carrier_id/test_mode.

Before this change, such rows generated 1287+ Sentry events per hour via
`GetShipments` admin query with:

    GraphQLError: RateType.__init__() missing 4 required keyword-only
    arguments: 'id', 'carrier_name', 'carrier_id', and 'test_mode'
"""

import unittest

from karrio.server.graph.schemas.base.types import RateType


class TestRateTypeParse(unittest.TestCase):
    def test_empty_dict_yields_defaults(self):
        rt = RateType.parse({})
        self.assertEqual(rt.id, "")
        self.assertEqual(rt.carrier_name, "")
        self.assertEqual(rt.carrier_id, "")
        self.assertFalse(rt.test_mode)
        self.assertEqual(rt.total_charge, 0.0)
        self.assertEqual(rt.extra_charges, [])

    def test_partial_legacy_rate(self):
        """A legacy selected_rate with only service + total_charge must still parse."""
        rt = RateType.parse({"service": "dhl_parcel_de_paket", "total_charge": 8.62})
        self.assertEqual(rt.service, "dhl_parcel_de_paket")
        self.assertEqual(rt.total_charge, 8.62)
        self.assertEqual(rt.id, "")  # filled in with default

    def test_full_rate_passes_through(self):
        rt = RateType.parse(
            {
                "id": "rat_abc",
                "carrier_name": "dhl_parcel_de",
                "carrier_id": "DHL Live",
                "service": "dhl_parcel_de_paket",
                "test_mode": False,
                "total_charge": 8.62,
                "currency": "EUR",
                "extra_charges": [{"name": "Fuel", "amount": 0.5, "currency": "EUR"}],
            }
        )
        self.assertEqual(rt.id, "rat_abc")
        self.assertEqual(rt.carrier_name, "dhl_parcel_de")
        self.assertEqual(len(rt.extra_charges), 1)
