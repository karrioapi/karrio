"""Rating — DHL Freight uses the universal CSV-driven rate provider.

DHL Freight does not expose a live-rates endpoint in this booking API. Rates
are resolved from ``services.csv`` (zone × weight band × service code).
"""

import unittest

import karrio.core.models as models
import karrio.sdk as karrio

from .fixture import gateway


class TestDHLFreightRate(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RATE_PAYLOAD)

    def test_create_rate_request_uses_universal_provider(self):
        """The rate request must serialise — it goes through universal.rate_request."""
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertIsNotNone(request)

    def test_rate_resolves_from_csv(self):
        """Universal rating returns the configured services without errors.

        ``services.csv`` ships with rate=0 placeholders — the merchant uploads
        their negotiated rate card via the standard rate-sheet UI. The test
        only asserts the universal flow doesn't blow up.
        """
        _, messages = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
        non_route_errors = [m for m in messages if m.code != "SHIPPING_SDK_DESTINATION_NOT_SERVICED_ERROR"]
        self.assertEqual(non_route_errors, [])


if __name__ == "__main__":
    unittest.main()


RATE_PAYLOAD = dict(
    shipper=dict(
        company_name="Rower Gear NL",
        address_line1="Damrak Straat 1",
        city="Niemegen",
        postal_code="4651 SR",
        country_code="NL",
    ),
    recipient=dict(
        company_name="Ford Romania",
        address_line1="Esma Sultan Street",
        city="MANKALYA",
        postal_code="905500",
        country_code="RO",
    ),
    parcels=[
        dict(
            weight=550.0,
            weight_unit="KG",
            length=100.0,
            width=90.0,
            height=140.0,
            dimension_unit="CM",
            packaging_type="pallet",
        )
    ],
    services=["dhl_freight_eurapid"],
)
