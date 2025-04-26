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
    Canada Post AddressComplete validator implementation.

    This class provides methods to validate addresses using the Canada Post AddressComplete API.
    """

    @staticmethod
    def get_info(is_authenticated: bool = True) -> dict:
        """
        Get information about the Canada Post AddressComplete validator.

        Args:
            is_authenticated: Whether to include the API key in the result

        Returns:
            Dictionary with information about the validator
        """
        return dict(
            provider="canadapost",
            key=(Validator.get_api_key() if is_authenticated else None),
        )

    @staticmethod
    def get_url() -> str:
        """
        Get the Canada Post AddressComplete API URL.

        Returns:
            URL string for the Canada Post AddressComplete API
        """
        return "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/2.1/json.ws"

    @staticmethod
    def get_api_key() -> str:
        """
        Get the Canada Post AddressComplete API key from configuration.

        Returns:
            API key string

        Raises:
            Exception: If no API key is configured
        """
        key = Validator.config.get("CANADAPOST_ADDRESS_COMPLETE_API_KEY")

        if key is None or len(key) == 0:
            raise Exception(
                "No CANADAPOST_ADDRESS_COMPLETE_API_KEY provided for address validation"
            )

        return key

    @staticmethod
    def format_address(address) -> str:
        """
        Format an address object for the Canada Post AddressComplete API.

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
    def validate(address) -> dict:
        """
        Validate an address using the Canada Post AddressComplete API.

        Args:
            address: Address object to validate

        Returns:
            Address validation result with success flag and metadata
        """
        formatted_address = Validator.format_address(address)

        logger.debug(
            f"sending address validation request to Canada Post Address Complete API: {formatted_address}"
        )
        response = requests.request(
            "GET",
            Validator.get_url(),
            params=dict(
                key=Validator.get_api_key(),
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

        return dict(
            success=success, meta=(meta or dict(validation_results=results))
        )

