import unittest
import karrio.lib as lib


class TestToStateCode(unittest.TestCase):
    def test_name_resolves_to_code(self):
        self.assertEqual(lib.to_state_code("California", "US"), "CA")

    def test_name_matching_ignores_case_and_accents(self):
        self.assertListEqual(
            [lib.to_state_code(value, "CA") for value in ["quebec", "Québec"]],
            ["QC", "QC"],
        )

    def test_name_matching_ignores_trailing_subdivision_word(self):
        self.assertListEqual(
            [
                lib.to_state_code("New York State", "US"),
                lib.to_state_code("Quebec Province", "CA"),
            ],
            ["NY", "QC"],
        )

    def test_known_and_prefixed_codes_resolve_to_code(self):
        self.assertListEqual(
            [lib.to_state_code(value, "US") for value in ["ny", "US-NY", " NY "]],
            ["NY", "NY", "NY"],
        )

    def test_country_without_published_subdivisions_is_unchanged(self):
        self.assertEqual(
            lib.to_state_code("Västra Götaland", "SE"),
            "Västra Götaland",
        )

    def test_unmatched_value_is_unchanged(self):
        self.assertEqual(lib.to_state_code("Atlantis", "US"), "Atlantis")

    def test_missing_value_stays_missing(self):
        self.assertListEqual(
            [lib.to_state_code(value, "US") for value in [None, ""]],
            [None, ""],
        )


if __name__ == "__main__":
    unittest.main()
