"""Karrio MyDHL address validation API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract address validation details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., AddressValidationRequestType),
# while XML schema types don't have this suffix (e.g., AddressValidationRequest).

import karrio.schemas.mydhl.address_validation_request as mydhl_req
import karrio.schemas.mydhl.address_validation_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_address_validation_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.AddressValidationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    validation_details = lib.identity(
        _extract_details(
            lib.to_object(mydhl_res.AddressValidationResponseType, response),
            settings,
        )
        if response.get("status") is None and response.get("address") is not None
        else None
    )

    return validation_details, messages


def _extract_details(
    validation: mydhl_res.AddressValidationResponseType,
    settings: provider_utils.Settings,
) -> models.AddressValidationDetails:
    """
    Extract address validation details from MyDHL response

    validation: The MyDHL AddressValidationResponseType object
    settings: The carrier connection settings

    Returns an AddressValidationDetails object
    """
    # Get first validated address using functional pattern
    validated_address = next(
        (addr for addr in (validation.address or []) if addr),
        None
    )

    # Determine success based on presence of validated address
    success = validated_address is not None

    return models.AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        complete_address=lib.identity(
            models.Address(
                postal_code=lib.text(str(validated_address.postalCode)),
                city=validated_address.cityName,
                country_code=validated_address.countryCode,
                state_code=validated_address.countyName,
            )
            if validated_address
            else None
        ),
    )


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create an address validation request for the carrier API.

    The DHL address-validate endpoint uses GET with query parameters:
    - type: 'delivery' or 'pickup'
    - countryCode: ISO 2-letter country code
    - postalCode: postal/zip code
    - cityName: city name

    payload: The standardized AddressValidationRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object with query parameters for the GET request
    """
    address = lib.to_address(payload.address)

    # Build query parameters for GET request (not POST body)
    request = mydhl_req.AddressValidationRequestType(
        type="delivery",
        countryCode=address.country_code,
        postalCode=address.postal_code,
        cityName=address.city,
        countyName=address.suburb,
        strictValidation=True,
    )

    return lib.Serializable(request, lib.to_dict)