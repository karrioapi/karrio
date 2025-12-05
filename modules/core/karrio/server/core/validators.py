import re
import phonenumbers
from datetime import datetime
from karrio.server.core.logging import logger

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.serializers as serializers

DIMENSIONS = ["width", "height", "length"]


def dimensions_required_together(value):
    any_dimension_specified = any(value.get(dim) is not None for dim in DIMENSIONS)
    has_any_dimension_undefined = any(value.get(dim) is None for dim in DIMENSIONS)
    dimension_unit_is_undefined = value.get("dimension_unit") is None

    if any_dimension_specified and has_any_dimension_undefined:
        raise serializers.ValidationError(
            {
                "dimensions": "When one dimension is specified, all must be specified with a dimension_unit"
            }
        )

    if (
        any_dimension_specified
        and not has_any_dimension_undefined
        and dimension_unit_is_undefined
    ):
        raise serializers.ValidationError(
            {
                "dimension_unit": "dimension_unit is required when dimensions are specified"
            }
        )


class TimeFormatValidator:
    """Validator for HH:MM time format that can be pickled."""

    def __init__(self, prop: str):
        self.prop = prop

    def __call__(self, value):
        try:
            datetime.strptime(value, "%H:%M")
        except Exception:
            raise serializers.ValidationError(
                "The time format must match HH:HM",
                code="invalid",
            )


class DateFormatValidator:
    """Validator for YYYY-MM-DD date format that can be pickled."""

    def __init__(self, prop: str):
        self.prop = prop

    def __call__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except Exception:
            raise serializers.ValidationError(
                "The date format must match YYYY-MM-DD",
                code="invalid",
            )


class DateTimeFormatValidator:
    """Validator for YYYY-MM-DD HH:MM datetime format that can be pickled."""

    def __init__(self, prop: str):
        self.prop = prop

    def __call__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
        except Exception:
            raise serializers.ValidationError(
                "The datetime format must match YYYY-MM-DD HH:HM",
                code="invalid",
            )


def valid_time_format(prop: str):
    """Factory function for time format validator."""
    return TimeFormatValidator(prop)


def valid_date_format(prop: str):
    """Factory function for date format validator."""
    return DateFormatValidator(prop)


def valid_datetime_format(prop: str):
    """Factory function for datetime format validator."""
    return DateTimeFormatValidator(prop)


class Base64Validator:
    """Validator for base64 encoded content that can be pickled."""

    def __init__(self, prop: str, max_size: int = 5242880):
        self.prop = prop
        self.max_size = max_size

    def __call__(self, value: str):
        error = None

        try:
            buffer = lib.to_buffer(value, validate=True)

            if buffer.getbuffer().nbytes > self.max_size:
                error = f"Error: file size exceeds {self.max_size} bytes."

        except Exception as e:
            logger.error("Invalid base64 file content", error=str(e))
            error = "Invalid base64 file content"
            raise serializers.ValidationError(
                error,
                code="invalid",
            )

        if error is not None:
            raise serializers.ValidationError(error, code="invalid")


def valid_base64(prop: str, max_size: int = 5242880):
    """Factory function for base64 validator."""
    return Base64Validator(prop, max_size)


class OptionDefaultSerializer(serializers.Serializer):
    def __init__(self, instance=None, **kwargs):
        data = kwargs.get("data", {})
        if data:
            # Get existing options from data and instance
            options = {
                **(
                    getattr(instance, "options", None) or {}
                ),  # Start with instance options
                **(data.get("options") or {}),  # Override with new options
            }

            # Get shipping_date from options or default to next business day
            shipping_date = options.get("shipping_date")
            shipment_date = options.get("shipment_date")

            if not shipping_date:
                shipping_date = lib.fdatetime(
                    lib.to_next_business_datetime(
                        lib.to_date(shipment_date) or datetime.now()
                    ),
                    output_format="%Y-%m-%dT%H:%M",
                )

            if not shipment_date:
                shipment_date = lib.fdate(
                    shipping_date, current_format="%Y-%m-%dT%H:%M"
                )

            # Update only the date fields in options
            options.update(
                {"shipping_date": shipping_date, "shipment_date": shipment_date}
            )

            # Update the data with merged options
            kwargs["data"]["options"] = options

        super().__init__(instance, **kwargs)


class PresetSerializer(serializers.Serializer):
    def validate(self, data):
        import karrio.server.core.dataunits as dataunits

        dimensions_required_together(data)

        if data is not None and "package_preset" in data:
            package_presets = dataunits.REFERENCE_MODELS.get("package_presets", {})
            preset_name = data["package_preset"]

            # Find the preset across all carriers
            preset = lib.identity(
                next(
                    (
                        presets[preset_name]
                        for carrier_id, presets in package_presets.items()
                        if preset_name in presets
                    ),
                    None,
                )
                or {}
            )

            data.update(
                {
                    **data,
                    "width": data.get("width") or preset.get("width"),
                    "length": data.get("length") or preset.get("length"),
                    "height": data.get("height") or preset.get("height"),
                    "dimension_unit": data.get("dimension_unit")
                    or preset.get("dimension_unit"),
                }
            )

        return data


def shipment_documents_accessor(cls=None, *, include_base64: bool = False):
    """
    Class decorator that computes shipping_documents for Shipment serializers.

    When applied to a serializer class, this decorator overrides to_representation()
    to dynamically build the shipping_documents list based on the shipment's
    label and invoice fields.

    Args:
        include_base64: If True, includes base64 content in shipping_documents.
                       If False (default), only includes URLs.

    Usage:
        @shipment_documents_accessor
        class Shipment(Serializer):
            ...  # shipping_documents will have URLs only

        @shipment_documents_accessor(include_base64=True)
        class PurchasedShipment(Shipment):
            ...  # shipping_documents will include base64 content
    """

    def decorator(klass):
        # Store the flag on the class for reference
        klass._include_base64_documents = include_base64

        # Store original to_representation
        original_to_representation = klass.to_representation

        def to_representation(self, instance):
            # Get the original serialized data
            data = original_to_representation(self, instance)

            # Build shipping_documents dynamically
            documents = []

            # Add label document if exists
            label = getattr(instance, "label", None)
            if label:
                label_format = getattr(instance, "label_type", None) or "PDF"
                documents.append(
                    {
                        "category": "label",
                        "format": label_format,
                        "url": getattr(instance, "label_url", None),
                        "base64": label if include_base64 else None,
                    }
                )

            # Add invoice document if exists
            invoice = getattr(instance, "invoice", None)
            if invoice:
                documents.append(
                    {
                        "category": "invoice",
                        "format": "PDF",
                        "url": getattr(instance, "invoice_url", None),
                        "base64": invoice if include_base64 else None,
                    }
                )

            # Update the data with computed shipping_documents
            data["shipping_documents"] = documents

            return data

        klass.to_representation = to_representation
        return klass

    # Handle both @shipment_documents_accessor and @shipment_documents_accessor(...)
    if cls is not None:
        # Called as @shipment_documents_accessor without parentheses
        return decorator(cls)
    else:
        # Called as @shipment_documents_accessor(...) with arguments
        return decorator


class AugmentedAddressSerializer(serializers.Serializer):
    def validate(self, data):
        # Format and validate Postal Code
        if all(data.get(key) is not None for key in ["country_code", "postal_code"]):
            postal_code = data["postal_code"]
            country_code = data["country_code"]

            if country_code == units.Country.CA.name:
                formatted = "".join(
                    [c for c in postal_code.split() if c not in ["-", "_"]]
                ).upper()
                if not re.match(r"^([A-Za-z]\d[A-Za-z][-]?\d[A-Za-z]\d)", formatted):
                    raise serializers.ValidationError(
                        {"postal_code": "The Canadian postal code must match Z9Z9Z9"}
                    )

            elif country_code == units.Country.US.name:
                formatted = "".join(postal_code.split())
                if not re.match(r"^\d{5}(-\d{4})?$", formatted):
                    raise serializers.ValidationError(
                        {
                            "postal_code": "The American postal code must match 12345 or 12345-6789"
                        }
                    )

            else:
                formatted = postal_code

            data.update({**data, "postal_code": formatted})

        # Format and validate Phone Number
        if all(
            data.get(key) is not None and data.get(key) != ""
            for key in ["country_code", "phone_number"]
        ):
            phone_number = data["phone_number"]
            country_code = data["country_code"]

            try:
                formatted = phonenumbers.parse(phone_number, country_code)
                data.update(
                    {
                        **data,
                        "phone_number": phonenumbers.format_number(
                            formatted, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                        ),
                    }
                )
            except Exception as e:
                logger.warning("Invalid phone number format", error=str(e))
                raise serializers.ValidationError(
                    {"phone_number": "Invalid phone number format"}
                )

        return data
