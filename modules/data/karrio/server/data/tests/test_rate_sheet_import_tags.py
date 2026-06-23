"""Importer tests for the ``<key>_tag`` column convention.

Covers:
1. ``_resolve_service_tags`` — direct dispatch unit tests
2. End-to-end: a flat workbook with tag columns appended produces a service
   dict whose ``tags`` field carries the validated registry values.
3. Unknown keys / invalid values are silently dropped (importer is permissive
   — the live rates surface is what enforces correctness).

Run:
    LOG_LEVEL=30 python -m unittest karrio.server.data.tests.test_rate_sheet_import_tags -v
"""

import io
import unittest

import karrio.server.data.resources.rate_sheets as rs
import openpyxl

_BASE_HEADERS = [
    "carrier_name",
    "service_code",
    "carrier_service_code",
    "service_name",
    "shipment_type",
    "origin_country",
    "zone_label",
    "country_codes",
    "min_weight",
    "max_weight",
    "weight_unit",
    "currency",
    "base_rate",
    "cost",
    "transit_days",
]

_TAG_HEADERS = [
    "recommended_tag",
    "recommendation_category_tag",
    "recommendation_type_tag",
    "display_priority_tag",
    "surface_visibility_tag",
    "bogus_tag",  # not in registry — must be ignored
]

_HEADERS = _BASE_HEADERS + _TAG_HEADERS


def _row(**overrides) -> list:
    base = {
        "carrier_name": "DHL Parcel DE",
        "service_code": "dhl_paket",
        "carrier_service_code": "V01PAK",
        "service_name": "DHL Paket",
        "shipment_type": "outbound",
        "origin_country": "DE",
        "zone_label": "Germany",
        "country_codes": "DE",
        "min_weight": 0,
        "max_weight": 2.0,
        "weight_unit": "KG",
        "currency": "EUR",
        "base_rate": 7.50,
        "cost": 4.80,
        "transit_days": 2,
        # tag columns default to empty
        "recommended_tag": "",
        "recommendation_category_tag": "",
        "recommendation_type_tag": "",
        "display_priority_tag": "",
        "surface_visibility_tag": "",
        "bogus_tag": "",
    }
    base.update(overrides)
    return [base.get(h) for h in _HEADERS]


def _make_xlsx(rows: list) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "service_rates"
    ws.append(_HEADERS)
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


class TestResolveServiceTags(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_extracts_registered_tag_columns(self):
        row = {
            "recommended_tag": "true",
            "recommendation_category_tag": "most_popular",
            "recommendation_type_tag": "best_price",
            "display_priority_tag": "80",
            "surface_visibility_tag": "default",
        }
        self.assertDictEqual(
            rs._resolve_service_tags(row),
            {
                "recommended": True,
                "recommendation_category": "most_popular",
                "recommendation_type": "best_price",
                "display_priority": 80,
                "surface_visibility": "default",
            },
        )

    def test_unknown_tag_columns_are_ignored(self):
        self.assertDictEqual(rs._resolve_service_tags({"bogus_tag": "x"}), {})

    def test_blank_values_are_ignored(self):
        self.assertDictEqual(
            rs._resolve_service_tags({"recommended_tag": "", "recommendation_category_tag": None}),
            {},
        )

    def test_invalid_enum_value_is_dropped(self):
        self.assertDictEqual(
            rs._resolve_service_tags(
                {
                    "recommendation_category_tag": "frooz",
                    "recommendation_type_tag": "best_price",
                }
            ),
            {"recommendation_type": "best_price"},
        )

    def test_out_of_range_int_is_dropped(self):
        self.assertDictEqual(
            rs._resolve_service_tags({"display_priority_tag": "999"}),
            {},
        )

    def test_non_tag_columns_are_untouched(self):
        # No false positives on unrelated columns — surcharges, features.
        self.assertDictEqual(
            rs._resolve_service_tags(
                {
                    "fuel_surcharge": 1.5,
                    "first_mile": "dropoff",
                    "tracked": True,
                }
            ),
            {},
        )


class TestImporterEndToEndTags(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_flat_workbook_tag_columns_land_on_service(self):
        data = _make_xlsx(
            [
                _row(
                    recommended_tag="true",
                    recommendation_category_tag="most_popular",
                    recommendation_type_tag="best_price",
                    display_priority_tag="80",
                    surface_visibility_tag="default",
                    bogus_tag="should be ignored",
                ),
            ]
        )
        rows, _ = rs.parse_flat_workbook(data)
        carrier_inputs = rs.build_rate_sheet_input_from_flat(rows)
        services = carrier_inputs["DHL Parcel DE"]["services"]
        self.assertEqual(len(services), 1)
        self.assertDictEqual(
            services[0]["tags"],
            {
                "recommended": True,
                "recommendation_category": "most_popular",
                "recommendation_type": "best_price",
                "display_priority": 80,
                "surface_visibility": "default",
            },
        )

    def test_flat_workbook_without_tag_columns_yields_empty_tags(self):
        data = _make_xlsx([_row()])
        rows, _ = rs.parse_flat_workbook(data)
        carrier_inputs = rs.build_rate_sheet_input_from_flat(rows)
        services = carrier_inputs["DHL Parcel DE"]["services"]
        self.assertDictEqual(services[0]["tags"], {})


if __name__ == "__main__":
    unittest.main()
