import re
import typing
import logging
import requests  # type: ignore
import phonenumbers
from constance import config
from datetime import datetime

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.serializers as serializers
import karrio.server.core.datatypes as datatypes

# Try to import the references module, which may not be available in all environments
try:
    import karrio.references as references
except ImportError:
    references = None

logger = logging.getLogger(__name__)
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


def valid_time_format(prop: str):
    def validate(value):

        try:
            datetime.strptime(value, "%H:%M")
        except Exception:
            raise serializers.ValidationError(
                "The time format must match HH:HM",
                code="invalid",
            )

    return validate


def valid_date_format(prop: str):
    def validate(value):

        try:
            datetime.strptime(value, "%Y-%m-%d")
        except Exception:
            raise serializers.ValidationError(
                "The date format must match YYYY-MM-DD",
                code="invalid",
            )

    return validate


def valid_datetime_format(prop: str):
    def validate(value):

        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
        except Exception:
            raise serializers.ValidationError(
                "The datetime format must match YYYY-MM-DD HH:HM",
                code="invalid",
            )

    return validate


def valid_base64(prop: str, max_size: int = 5242880):
    def validate(value: str):
        error = None

        try:
            buffer = lib.to_buffer(value, validate=True)

            if buffer.getbuffer().nbytes > max_size:
                error = f"Error: file size exceeds {max_size} bytes."

        except Exception as e:
            logger.exception(e)
            error = "Invalid base64 file content"
            raise serializers.ValidationError(
                error,
                code="invalid",
            )

        if error is not None:
            raise serializers.ValidationError(error, code="invalid")

    return validate


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
            preset = next(
                (
                    presets[data["package_preset"]]
                    for _, presets in dataunits.REFERENCE_MODELS[
                        "package_presets"
                    ].items()
                    if data["package_preset"] in presets
                ),
                {},
            )

            data.update(
                {
                    **data,
                    "width": data.get("width", preset.get("width")),
                    "length": data.get("length", preset.get("length")),
                    "height": data.get("height", preset.get("height")),
                    "dimension_unit": data.get(
                        "dimension_unit", preset.get("dimension_unit")
                    ),
                }
            )

        return data


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
                logger.warning(e)
                raise serializers.ValidationError(
                    {"phone_number": "Invalid phone number format"}
                )

        return data


class AddressValidatorAbstract:
    """
    Abstract base class for address validators.

    This class defines the interface that all address validators must implement.
    Note: This class is kept here for backwards compatibility.
    New validators should use the karrio.validators.abstract.AddressValidatorAbstract class.
    """

    @staticmethod
    def get_info(is_authenticated: bool = None) -> dict:
        """
        Get information about the validator.

        Args:
            is_authenticated: Whether authenticated information should be returned

        Returns:
            Dictionary with information about the validator

        Raises:
            Exception: If the method is not implemented
        """
        raise Exception("get_info method is not implemented")

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        """
        Validate an address using the service.

        Args:
            address: Address object to validate

        Returns:
            Address validation result

        Raises:
            Exception: If the method is not implemented
        """
        raise Exception("validate method is not implemented")


class Address:
    """
    Address validation service provider.

    This class provides methods to validate addresses using various service providers
    which are loaded as plugins.
    """

    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        """
        Get information about the available address validation services.

        Args:
            is_authenticated: Whether to include sensitive information like API keys

        Returns:
            Dictionary with information about the available validators
        """
        # If references module is available, get validator plugins info
        refs = references.REFERENCES
        if len(refs.get("address_validators", {})) > 0:
            # Return information about the first available validator
            validator_name = next(iter(refs["address_validators"].keys()))
            validator_class = None

            # Try to get the validator class from the references
            try:
                # Import the validator module dynamically
                import importlib
                module = importlib.import_module(f"karrio.validators.{validator_name}")
                if hasattr(module, "METADATA"):
                    validator_class = module.METADATA.Validator
            except (ImportError, AttributeError) as e:
                logger.warning(f"Could not import validator {validator_name}: {e}")

            if validator_class is not None:
                # Return validator info with is_enabled=True
                validator_info = validator_class.get_info(is_authenticated)
                return {"is_enabled": True, **validator_info}

        # Check for legacy config-based validation
        is_enabled = any(
            [config.GOOGLE_CLOUD_API_KEY, config.CANADAPOST_ADDRESS_COMPLETE_API_KEY]
        )

        if is_enabled:
            # Legacy validation is enabled, use the legacy validator
            return {
                "is_enabled": is_enabled,
                **Address._get_legacy_validator().get_info(is_authenticated),
            }

        # No validation is available
        return dict(is_enabled=False)

    @staticmethod
    def _get_legacy_validator() -> typing.Type[AddressValidatorAbstract]:
        """
        Get a legacy validator instance based on configuration.

        This method is used for backwards compatibility with the old validation system.

        Returns:
            An instance of a validator class

        Raises:
            Exception: If no validator is configured
        """
        # For backwards compatibility, check if Google or Canada Post is configured
        if any(config.GOOGLE_CLOUD_API_KEY or ""):
            from karrio.validators.googlegeocoding import Validator as GoogleGeocode
            return GoogleGeocode
        elif any(config.CANADAPOST_ADDRESS_COMPLETE_API_KEY or ""):
            from karrio.validators.addresscomplete import Validator as AddressComplete
            return AddressComplete

        raise Exception("No address validation service provider configured")

    @staticmethod
    def get_validator() -> typing.Type:
        """
        Get a validator instance based on configuration or plugins.

        This method first checks for validator plugins, then falls back to
        legacy validators if no plugins are available.

        Returns:
            An instance of a validator class

        Raises:
            Exception: If no validator is configured
        """
        # If references module is available, check for validator plugins
        refs = references.REFERENCES
        if len(refs.get("address_validators", {})) > 0:
            # Get the first available validator
                validator_name = next(iter(refs["address_validators"].keys()))

                # Try to get the validator class from the references
                try:
                    # Import the validator module dynamically
                    import importlib
                    module = importlib.import_module(f"karrio.validators.{validator_name}")
                    if hasattr(module, "METADATA"):
                        return module.METADATA.Validator
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Could not import validator {validator_name}: {e}")

        # Fall back to legacy validator
        return Address._get_legacy_validator()

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        """
        Validate an address using the configured validator.

        Args:
            address: The address to validate

        Returns:
            AddressValidation object with validation results
        """
        validator = Address.get_validator()
        result = validator.validate(address)

        # Handle the case where the validator returns a dict instead of AddressValidation
        if isinstance(result, dict):
            return datatypes.AddressValidation(**result)

        return result
