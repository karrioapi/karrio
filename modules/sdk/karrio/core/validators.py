"""
Abstract base class for address validators.

This module defines the interface that all address validators must implement.
"""

import typing

class AddressValidatorAbstract:
    """
    Abstract base class for address validators.

    All address validators must implement this interface.
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
    def get_url() -> str:
        """
        Get the URL for the validation API.

        Returns:
            URL string for the validation API

        Raises:
            Exception: If the method is not implemented
        """
        raise Exception("get_url method is not implemented")

    @staticmethod
    def get_api_key() -> str:
        """
        Get the API key for the validation service.

        Returns:
            API key string

        Raises:
            Exception: If the method is not implemented or no API key is configured
        """
        raise Exception("get_api_key method is not implemented")

    @staticmethod
    def format_address(address) -> str:
        """
        Format an address object for the validation API.

        Args:
            address: Address object to format

        Returns:
            Formatted address string

        Raises:
            Exception: If the method is not implemented
        """
        raise Exception("format_address method is not implemented")

    @staticmethod
    def validate(address) -> typing.Any:
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
