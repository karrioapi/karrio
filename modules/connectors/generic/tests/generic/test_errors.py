import unittest
from karrio.core.units import Packages, Weight
from karrio.core.models import Parcel, RateRequest, ShipmentRequest
from karrio.core.errors import FieldError, FieldErrorCode, format_item_field
from karrio.core.utils import DP


class TestFieldErrorFormat(unittest.TestCase):
    """Test that field errors are formatted with items[index].field pattern."""

    maxDiff = None

    def test_single_parcel_missing_weight(self):
        """Test error format when single parcel is missing required weight."""
        parcels = [Parcel(weight=None, weight_unit="LB")]

        with self.assertRaises(FieldError) as ctx:
            Packages(parcels, required=["weight"])

        self.assertDictEqual(
            ctx.exception.details,
            {
                "parcel[0].weight": {
                    "code": "required",
                    "message": "This field is required",
                }
            },
        )

    def test_multiple_parcels_missing_weight(self):
        """Test error format when multiple parcels are missing required fields."""
        parcels = [
            Parcel(weight=None, weight_unit="LB"),
            Parcel(weight=5.0, weight_unit="LB"),
            Parcel(weight=None, weight_unit="LB"),
        ]

        with self.assertRaises(FieldError) as ctx:
            Packages(parcels, required=["weight"])

        self.assertDictEqual(
            ctx.exception.details,
            {
                "parcel[0].weight": {
                    "code": "required",
                    "message": "This field is required",
                },
                "parcel[2].weight": {
                    "code": "required",
                    "message": "This field is required",
                },
            },
        )

    def test_parcel_weight_exceeds_max(self):
        """Test error format when parcel weight exceeds maximum."""
        parcels = [
            Parcel(weight=5.0, weight_unit="LB"),
            Parcel(weight=15.0, weight_unit="LB"),
        ]

        with self.assertRaises(FieldError) as ctx:
            Packages(parcels, max_weight=Weight(10.0, "LB"))

        self.assertDictEqual(
            ctx.exception.details,
            {
                "parcel[1].weight": {
                    "code": "exceeds",
                    "message": "This field exceeds the max value",
                }
            },
        )

    def test_mixed_validation_errors(self):
        """Test error format with both required and exceeds errors."""
        parcels = [
            Parcel(weight=None, weight_unit="LB"),
            Parcel(weight=15.0, weight_unit="LB"),
            Parcel(weight=None, weight_unit="LB"),
        ]

        with self.assertRaises(FieldError) as ctx:
            Packages(parcels, required=["weight"], max_weight=Weight(10.0, "LB"))

        self.assertDictEqual(
            ctx.exception.details,
            {
                "parcel[0].weight": {
                    "code": "required",
                    "message": "This field is required",
                },
                "parcel[1].weight": {
                    "code": "exceeds",
                    "message": "This field exceeds the max value",
                },
                "parcel[2].weight": {
                    "code": "required",
                    "message": "This field is required",
                },
            },
        )

    def test_valid_parcels_no_error(self):
        """Test that valid parcels don't raise errors."""
        parcels = [
            Parcel(weight=5.0, weight_unit="LB"),
            Parcel(weight=8.0, weight_unit="LB"),
        ]

        packages = Packages(parcels, required=["weight"], max_weight=Weight(10.0, "LB"))
        self.assertEqual(len(packages), 2)


class TestFieldErrorCodeValues(unittest.TestCase):
    """Test FieldErrorCode enum values."""

    def test_required_code(self):
        self.assertDictEqual(
            FieldErrorCode.required.value,
            {"code": "required", "message": "This field is required"},
        )

    def test_invalid_code(self):
        self.assertDictEqual(
            FieldErrorCode.invalid.value,
            {"code": "invalid", "message": "This field is invalid"},
        )

    def test_exceeds_code(self):
        self.assertDictEqual(
            FieldErrorCode.exceeds.value,
            {"code": "exceeds", "message": "This field exceeds the max value"},
        )


class TestFormatItemFieldHelper(unittest.TestCase):
    """Test the format_item_field helper function."""

    def test_default_list_name(self):
        self.assertEqual(format_item_field("weight", 0), "items[0].weight")
        self.assertEqual(format_item_field("description", 2), "items[2].description")

    def test_custom_list_name(self):
        self.assertEqual(format_item_field("weight", 0, "parcels"), "parcels[0].weight")
        self.assertEqual(format_item_field("sku", 1, "commodities"), "commodities[1].sku")


class TestFieldErrorProperties(unittest.TestCase):
    """Test FieldError exception properties."""

    def test_error_code(self):
        error = FieldError({"field": FieldErrorCode.required})
        self.assertEqual(error.code, "SHIPPING_SDK_FIELD_ERROR")

    def test_error_message(self):
        error = FieldError({"field": FieldErrorCode.required})
        self.assertEqual(str(error), "Invalid request payload")

    def test_indexed_field_in_details(self):
        error = FieldError({
            "items[0].weight": FieldErrorCode.required,
            "items[1].description": FieldErrorCode.invalid,
        })
        self.assertDictEqual(
            error.details,
            {
                "items[0].weight": {"code": "required", "message": "This field is required"},
                "items[1].description": {"code": "invalid", "message": "This field is invalid"},
            },
        )


if __name__ == "__main__":
    unittest.main()
