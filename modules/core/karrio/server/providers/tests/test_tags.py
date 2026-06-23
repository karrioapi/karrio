"""Unit tests for the service-level tag registry.

Covers ``validate_tags`` (kind coercion + warnings), ``derive_badges``
(precedence semantics), and ``column_to_tag_key`` (importer dispatch).
"""

import unittest

from karrio.server.providers.tags import (
    TAG_COLUMN_SUFFIX,
    TAG_REGISTRY,
    coerce_tag_value,
    column_to_tag_key,
    derive_badges,
    validate_tags,
)


class TestValidateTags(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_bool_kind_accepts_true_and_false(self):
        cleaned, warnings = validate_tags({"recommended": True})
        self.assertDictEqual(cleaned, {"recommended": True})
        self.assertListEqual(warnings, [])

        cleaned, warnings = validate_tags({"recommended": False})
        self.assertDictEqual(cleaned, {"recommended": False})
        self.assertListEqual(warnings, [])

    def test_bool_kind_coerces_truthy_strings(self):
        for raw in ("true", "TRUE", "1", "yes", "on"):
            cleaned, warnings = validate_tags({"recommended": raw})
            self.assertDictEqual(cleaned, {"recommended": True}, msg=raw)
            self.assertListEqual(warnings, [], msg=raw)

    def test_bool_kind_coerces_falsy_strings(self):
        for raw in ("false", "0", "no", "off"):
            cleaned, warnings = validate_tags({"recommended": raw})
            self.assertDictEqual(cleaned, {"recommended": False}, msg=raw)
            self.assertListEqual(warnings, [], msg=raw)

    def test_bool_kind_rejects_garbage(self):
        cleaned, warnings = validate_tags({"recommended": "maybe"})
        self.assertDictEqual(cleaned, {})
        self.assertEqual(len(warnings), 1)
        self.assertIn("recommended", warnings[0])

    def test_enum_kind_accepts_known_values(self):
        cleaned, warnings = validate_tags({"recommendation_category": "home_delivery"})
        self.assertDictEqual(cleaned, {"recommendation_category": "home_delivery"})
        self.assertListEqual(warnings, [])

    def test_enum_kind_rejects_unknown_value(self):
        cleaned, warnings = validate_tags({"recommendation_category": "frooz"})
        self.assertDictEqual(cleaned, {})
        self.assertEqual(len(warnings), 1)
        self.assertIn("recommendation_category", warnings[0])

    def test_enum_kind_normalises_case_and_whitespace(self):
        cleaned, warnings = validate_tags({"recommendation_category": "  Home_Delivery  "})
        self.assertDictEqual(cleaned, {"recommendation_category": "home_delivery"})
        self.assertListEqual(warnings, [])

    def test_int_kind_accepts_in_range(self):
        cleaned, warnings = validate_tags({"display_priority": 50})
        self.assertDictEqual(cleaned, {"display_priority": 50})
        self.assertListEqual(warnings, [])

    def test_int_kind_accepts_string_integer(self):
        cleaned, warnings = validate_tags({"display_priority": "80"})
        self.assertDictEqual(cleaned, {"display_priority": 80})
        self.assertListEqual(warnings, [])

    def test_int_kind_rejects_out_of_range(self):
        cleaned, warnings = validate_tags({"display_priority": 999})
        self.assertDictEqual(cleaned, {})
        self.assertEqual(len(warnings), 1)
        self.assertIn("display_priority", warnings[0])

    def test_int_kind_rejects_non_integer(self):
        cleaned, warnings = validate_tags({"display_priority": "not-a-number"})
        self.assertDictEqual(cleaned, {})
        self.assertEqual(len(warnings), 1)

    def test_unknown_key_rejected_with_warning(self):
        cleaned, warnings = validate_tags({"definitely_not_a_tag": "x"})
        self.assertDictEqual(cleaned, {})
        self.assertEqual(len(warnings), 1)
        self.assertIn("unknown tag key", warnings[0])

    def test_empty_input_is_a_noop(self):
        self.assertEqual(validate_tags({}), ({}, []))
        self.assertEqual(validate_tags(None), ({}, []))

    def test_multiple_valid_keys_pass_together(self):
        cleaned, warnings = validate_tags(
            {
                "recommended": "true",
                "recommendation_category": "most_popular",
                "recommendation_type": "best_price",
                "display_priority": 80,
                "surface_visibility": "default",
            }
        )
        self.assertDictEqual(
            cleaned,
            {
                "recommended": True,
                "recommendation_category": "most_popular",
                "recommendation_type": "best_price",
                "display_priority": 80,
                "surface_visibility": "default",
            },
        )
        self.assertListEqual(warnings, [])


class TestDeriveBadges(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_no_tags_returns_empty(self):
        self.assertListEqual(derive_badges({}), [])
        self.assertListEqual(derive_badges(None), [])

    def test_recommended_badge(self):
        self.assertListEqual(
            derive_badges({"recommendation_type": "recommended"}),
            [{"label_key": "tags.badge.recommended", "style": "yellow", "priority": 50}],
        )

    def test_best_price_wins_over_recommended(self):
        # Higher priority wins; only one badge is returned today.
        self.assertListEqual(
            derive_badges({"recommendation_type": "best_price"}),
            [{"label_key": "tags.badge.best_price", "style": "green", "priority": 60}],
        )

    def test_unrecognised_value_yields_no_badge(self):
        self.assertListEqual(
            derive_badges({"recommendation_type": "completely_made_up"}),
            [],
        )


class TestColumnDispatch(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_known_tag_column_returns_key(self):
        self.assertEqual(column_to_tag_key("recommended_tag"), "recommended")
        self.assertEqual(
            column_to_tag_key("recommendation_category_tag"),
            "recommendation_category",
        )
        self.assertEqual(column_to_tag_key("display_priority_tag"), "display_priority")

    def test_unknown_tag_column_returns_none(self):
        self.assertIsNone(column_to_tag_key("bogus_tag"))

    def test_non_tag_column_returns_none(self):
        self.assertIsNone(column_to_tag_key("fuel_surcharge"))
        self.assertIsNone(column_to_tag_key("first_mile"))
        self.assertIsNone(column_to_tag_key(""))
        self.assertIsNone(column_to_tag_key(TAG_COLUMN_SUFFIX))


class TestCoerceTagValue(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_unknown_key_surfaces_explicit_error(self):
        value, error = coerce_tag_value("absolutely_not_a_tag", "x")
        self.assertIsNone(value)
        self.assertIn("unknown tag key", error or "")

    def test_int_range_optional(self):
        # All declared int tags currently have a range; sanity-check the
        # registry-driven path so a future un-ranged int tag won't crash.
        for key, spec in TAG_REGISTRY.items():
            if spec.kind != "int":
                continue
            in_range = spec.range[0] if spec.range else 0
            value, error = coerce_tag_value(key, in_range)
            self.assertEqual(value, in_range, msg=key)
            self.assertIsNone(error, msg=key)


if __name__ == "__main__":
    unittest.main()
