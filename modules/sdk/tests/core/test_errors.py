import unittest
from karrio.core.errors import (
    FieldError,
    FieldErrorCode,
    ShippingSDKError,
    ShippingSDKDetailedError,
    ParsedMessagesError,
    ValidationError,
    MethodNotSupportedError,
    OriginNotServicedError,
    DestinationNotServicedError,
    MultiParcelNotSupportedError,
    format_item_field,
)


class TestFieldErrorCode(unittest.TestCase):
    def test_required_error_code(self):
        self.assertDictEqual(
            FieldErrorCode.required.value,
            {"code": "required", "message": "This field is required"},
        )

    def test_invalid_error_code(self):
        self.assertDictEqual(
            FieldErrorCode.invalid.value,
            {"code": "invalid", "message": "This field is invalid"},
        )

    def test_exceeds_error_code(self):
        self.assertDictEqual(
            FieldErrorCode.exceeds.value,
            {"code": "exceeds", "message": "This field exceeds the max value"},
        )


class TestFormatItemField(unittest.TestCase):
    def test_format_item_field_default_list_name(self):
        self.assertEqual(format_item_field("weight", 0), "items[0].weight")
        self.assertEqual(format_item_field("description", 2), "items[2].description")

    def test_format_item_field_custom_list_name(self):
        self.assertEqual(
            format_item_field("weight", 0, "parcels"), "parcels[0].weight"
        )
        self.assertEqual(
            format_item_field("sku", 1, "commodities"), "commodities[1].sku"
        )


class TestFieldError(unittest.TestCase):
    def test_single_field_error(self):
        error = FieldError({"weight": FieldErrorCode.required})
        self.assertEqual(str(error), "Invalid request payload")
        self.assertEqual(error.code, "SHIPPING_SDK_FIELD_ERROR")
        self.assertDictEqual(
            error.details,
            {"weight": {"code": "required", "message": "This field is required"}},
        )

    def test_multiple_field_errors(self):
        error = FieldError({
            "weight": FieldErrorCode.required,
            "length": FieldErrorCode.exceeds,
        })
        self.assertDictEqual(
            error.details,
            {
                "weight": {"code": "required", "message": "This field is required"},
                "length": {"code": "exceeds", "message": "This field exceeds the max value"},
            },
        )

    def test_indexed_field_errors(self):
        """Test field errors with items[index].field format."""
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

    def test_parcel_indexed_field_errors(self):
        """Test field errors with parcels[index].field format (used in units.py)."""
        error = FieldError({
            "parcel[0].weight": FieldErrorCode.required,
            "parcel[1].weight": FieldErrorCode.exceeds,
        })
        self.assertDictEqual(
            error.details,
            {
                "parcel[0].weight": {"code": "required", "message": "This field is required"},
                "parcel[1].weight": {"code": "exceeds", "message": "This field exceeds the max value"},
            },
        )


class TestParsedMessagesError(unittest.TestCase):
    def test_empty_messages(self):
        error = ParsedMessagesError()
        self.assertEqual(str(error), "Invalid request payload")
        self.assertEqual(error.messages, [])

    def test_with_messages(self):
        messages = [
            {"code": "invalid_weight", "message": "Weight exceeds limit"},
            {"code": "invalid_address", "message": "Address not found"},
        ]
        error = ParsedMessagesError(messages=messages)
        self.assertEqual(error.messages, messages)


class TestShippingSDKErrors(unittest.TestCase):
    def test_base_error(self):
        error = ShippingSDKError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.code, "SHIPPING_SDK_INTERNAL_ERROR")

    def test_detailed_error_with_details(self):
        error = ShippingSDKDetailedError("Test error", details={"key": "value"})
        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.details, {"key": "value"})

    def test_validation_error(self):
        error = ValidationError("Invalid data")
        self.assertEqual(error.code, "SHIPPING_SDK_VALIDATING_ERROR")

    def test_method_not_supported_error(self):
        error = MethodNotSupportedError("get_rates", "TestCarrier")
        self.assertEqual(str(error), "get_rates not supported by TestCarrier")
        self.assertEqual(error.code, "SHIPPING_SDK_NON_SUPPORTED_ERROR")

    def test_origin_not_serviced_error(self):
        error = OriginNotServicedError("CA")
        self.assertEqual(str(error), "Origin address 'CA' is not serviced")
        self.assertEqual(error.code, "SHIPPING_SDK_ORIGIN_NOT_SERVICED_ERROR")

    def test_destination_not_serviced_error(self):
        error = DestinationNotServicedError("US")
        self.assertEqual(str(error), "Destination address 'US' is not serviced")
        self.assertEqual(error.code, "SHIPPING_SDK_DESTINATION_NOT_SERVICED_ERROR")

    def test_multi_parcel_not_supported_error(self):
        error = MultiParcelNotSupportedError()
        self.assertEqual(str(error), "Multi-parcel shipment not supported")
        self.assertEqual(error.code, "SHIPPING_SDK_MULTI_PARCEL_NOT_SUPPORTED_ERROR")


if __name__ == "__main__":
    unittest.main()
