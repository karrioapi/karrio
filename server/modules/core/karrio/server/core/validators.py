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

        except Exception:
            raise serializers.ValidationError(
                "Invalid base64 file content",
                code="invalid",
            )

        if any(error or ""):
            raise serializers.ValidationError(error, code="invalid")

    return validate


class OptionDefaultSerializer(serializers.Serializer):
    def validate(self, data):
        options = {
            **getattr(self.instance, "options", {}),
            **(data.get("options") or {}),
        }
        data.update(
            dict(
                options={
                    "shipment_date": datetime.now().strftime("%Y-%m-%d"),
                    **options,
                }
            )
        )

        return data


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
    @staticmethod
    def get_info(is_authenticated: bool = None) -> dict:
        raise Exception("get_info method is not implemented")

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        raise Exception("validate method is not implemented")


class GoogleGeocode(AddressValidatorAbstract):
    @staticmethod
    def get_url() -> str:
        return "https://maps.googleapis.com/maps/api/geocode/json"

    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        return dict(
            provider="google",
            key=(GoogleGeocode.get_api_key() if is_authenticated else None),
        )

    @staticmethod
    def get_api_key() -> str:
        key = config.GOOGLE_CLOUD_API_KEY

        if key is None or len(key) == 0:
            raise Exception("No GOOGLE_CLOUD_API_KEY provided for address validation")

        return key

    @staticmethod
    def format_address(address: datatypes.Address) -> str:
        address_string = lib.join(
            address.address_line1 or "",
            address.address_line2 or "",
            address.postal_code or "",
            address.city or "",
            join=True,
        )

        if address_string is None:
            raise Exception(
                "At least one address info must be provided (address_line1, city and/or postal_code)"
            )

        enriched_address = lib.join(
            address_string,
            address.state_code or "",
            address.country_code or "",
            join=True,
        )

        return enriched_address.replace(" ", "+")

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        formatted_address = GoogleGeocode.format_address(address)

        logger.debug(
            f"sending address validation request to Google Geocode API: {formatted_address}"
        )
        response = requests.request(
            "GET",
            GoogleGeocode.get_url(),
            params=dict(
                address=formatted_address,
                key=GoogleGeocode.get_api_key(),
                location_type="ROOFTOP",
            ),
        )
        response_data = response.json()

        is_ok = response_data.get("status") == "OK"
        results = response_data.get("results") or []
        meta = next(
            (
                r
                for r in results
                if r.get("geometry", {}).get("location_type") == "ROOFTOP"
            ),
            None,
        )
        success = is_ok and (meta is not None)

        return datatypes.AddressValidation(
            success=success, meta=(meta or dict(validation_results=results))
        )


class CanadaPostAddressComplete(AddressValidatorAbstract):
    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        return dict(
            provider="canadapost",
            key=(CanadaPostAddressComplete.get_api_key() if is_authenticated else None),
        )

    @staticmethod
    def get_url() -> str:
        return "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/2.1/json.ws"

    @staticmethod
    def get_api_key() -> str:
        key = config.CANADAPOST_ADDRESS_COMPLETE_API_KEY

        if key is None or len(key) == 0:
            raise Exception(
                "No CANADAPOST_ADDRESS_COMPLETE_API_KEY provided for address validation"
            )

        return key

    @staticmethod
    def format_address(address: datatypes.Address) -> str:
        address_string = lib.join(
            address.address_line1 or "",
            address.address_line2 or "",
            address.city or "",
            address.postal_code or "",
            join=True,
            separator=", ",
        )

        if address_string is None:
            raise Exception(
                "At least one address info must be provided (address_line1, city and/or postal_code)"
            )

        return address_string

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        formatted_address = CanadaPostAddressComplete.format_address(address)

        logger.debug(
            f"sending address validation request to Canada Post Address Complete API: {formatted_address}"
        )
        response = requests.request(
            "GET",
            CanadaPostAddressComplete.get_url(),
            params=dict(
                key=CanadaPostAddressComplete.get_api_key(),
                SearchTerm=formatted_address,
                Country=address.country_code,
                MaxResults=5,
                MaxSuggestions=5,
                SearchFor="Places",
                LanguagePreference="EN",
            ),
        )
        results = response.json()
        is_ok = response.status_code == 200
        meta = next(
            (
                r
                for r in results
                if (
                    r.get("Text").replace(",", "").lower()
                    == address.address_line1.replace(",", "").lower()
                    and r.get("Next") == "Retrieve"  # means it is a permanent address
                )
            ),
            None,
        )
        success = is_ok and (meta is not None)

        return datatypes.AddressValidation(
            success=success, meta=(meta or dict(validation_results=results))
        )


class Address:
    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        is_enabled = any(
            [config.GOOGLE_CLOUD_API_KEY, config.CANADAPOST_ADDRESS_COMPLETE_API_KEY]
        )

        if is_enabled:
            return {
                "is_enabled": is_enabled,
                **Address.get_validator().get_info(is_authenticated),
            }

        return dict(is_enabled=is_enabled)

    @staticmethod
    def get_validator() -> typing.Type[AddressValidatorAbstract]:
        if any(config.GOOGLE_CLOUD_API_KEY or ""):
            return GoogleGeocode
        elif any(config.CANADAPOST_ADDRESS_COMPLETE_API_KEY or ""):
            return CanadaPostAddressComplete

        raise Exception("No address validation service provider configured")

    @staticmethod
    def validate(address: datatypes.Address) -> datatypes.AddressValidation:
        return Address.get_validator().validate(address)
