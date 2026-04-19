"""Unit tests for Settings.get_billing_number: billing_id precedence,
service_code fallback, and stale id behavior."""

import unittest

import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import cached_auth, client_id, client_secret


def _gateway(service_billing_numbers):
    return karrio.gateway["dhl_parcel_de"].create(
        dict(
            username="u",
            password="p",
            client_id=client_id,
            client_secret=client_secret,
            test_mode=False,
            config={
                "label_type": "PDF",
                "service_billing_numbers": service_billing_numbers,
                "default_billing_number": "11111111110000",
            },
        ),
        cache=lib.Cache(**cached_auth),
    )


class TestBillingNumberResolution(unittest.TestCase):
    def test_single_entry_resolved_by_service_code(self):
        g = _gateway(
            [
                {"service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket"),
            "22222222220101",
        )

    def test_duplicate_entries_without_ids_return_first_match(self):
        """Backward-compat: legacy configs with two entries and no ids still
        resolve (first match wins). A warning-level concern but not an error."""
        g = _gateway(
            [
                {"service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
                {"service": "dhl_parcel_de_paket", "billing_number": "33333333330101"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket"),
            "22222222220101",
        )

    def test_service_code_fallback_uses_first_matching_row(self):
        g = _gateway(
            [
                {"service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
                {"service": "dhl_parcel_de_paket", "billing_number": "33333333330101"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket"),
            "22222222220101",
        )

    def test_billing_id_match_wins_over_service_code(self):
        g = _gateway(
            [
                {"id": "sbn_aaa", "service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
                {"id": "sbn_bbb", "service": "dhl_parcel_de_paket", "billing_number": "33333333330101"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket", billing_id="sbn_bbb"),
            "33333333330101",
        )

    def test_stale_billing_id_falls_back_to_service_code(self):
        """If the stored billing_id no longer exists in the config, the
        resolver falls back to service_code match rather than failing."""
        g = _gateway(
            [
                {"id": "sbn_aaa", "service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket", billing_id="sbn_missing"),
            "22222222220101",
        )

    def test_service_code_miss_falls_back_to_default(self):
        g = _gateway(
            [
                {"service": "dhl_parcel_de_kleinpaket", "billing_number": "22222222220300"},
            ]
        )
        self.assertEqual(
            g.settings.get_billing_number("dhl_parcel_de_paket"),
            "11111111110000",
        )
