"""
Canada Post AddressComplete Validator Plugin.

This module provides address validation using the Canada Post AddressComplete API.
"""


import requests
import logging
import karrio.lib as lib
import karrio.core.validators as abstract


logger = logging.getLogger(__name__)


class Validator(abstract.AddressValidatorAbstract):
    config: dict = {}
    """
    Google Geocode address validator implementation.

    This class provides methods to validate addresses using the Google Geocode API.
    """

    @staticmethod
    def get_url() -> str:
        """
        Get the Google Geocode API URL.

        Returns:
            URL string for the Google Geocode API
        """
        return "https://maps.googleapis.com/maps/api/geocode/json"

    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        """
        Get information about the Google Geocode validator.

        Args:
            is_authenticated: Whether to include the API key in the result

        Returns:
            Dictionary with information about the validator
        """
        return dict(
            provider="google",
            key=(Validator.get_api_key() if is_authenticated else None),
        )

    @staticmethod
    def get_api_key() -> str:
        """
        Get the Google Geocode API key from configuration.

        Returns:
            API key string

        Raises:
            Exception: If no API key is configured
        """
        key = Validator.config.get("GOOGLE_CLOUD_API_KEY")

        if key is None or len(key) == 0:
            raise Exception("No GOOGLE_CLOUD_API_KEY provided for address validation")

        return key

    @staticmethod
    def format_address(address) -> str:
        """
        Format an address object for the Google Geocode API.

        Args:
            address: Address object to format

        Returns:
            Formatted address string

        Raises:
            Exception: If required address fields are missing
        """
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
    def validate(address) -> dict:
        """
        Validate an address using the Google Geocode API.

        Args:
            address: Address object to validate

        Returns:
            Address validation result with success flag and metadata
        """
        formatted_address = Validator.format_address(address)

        logger.debug(
            f"sending address validation request to Google Geocode API: {formatted_address}"
        )
        response = requests.request(
            "GET",
            Validator.get_url(),
            params=dict(
                address=formatted_address,
                key=Validator.get_api_key(),
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

        return dict(
            success=success, meta=(meta or dict(validation_results=results))
        )
