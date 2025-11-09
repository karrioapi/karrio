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

    validation_response = lib.to_object(mydhl_res.AddressValidationResponseType, response)
    validation_details = _extract_details(validation_response, settings)

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
        complete_address=lib.to_address(
            postal_code=str(validated_address.postalCode) if validated_address and validated_address.postalCode else None,
            city=validated_address.cityName if validated_address else None,
            country_code=validated_address.countryCode if validated_address else None,
            state_code=validated_address.countyName if validated_address else None,
        ) if validated_address else None,
        meta=dict(
            warnings=validation.warnings or [],
            service_area=lib.to_dict(validated_address.serviceArea) if validated_address and validated_address.serviceArea else None,
        ),
    )


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create an address validation request for the carrier API

    payload: The standardized AddressValidationRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract the address from payload
    address = lib.to_address(payload.address)

    
    # For JSON API request - Using camelCase attribute names to match schema definition
    request = mydhl_req.AddressValidationRequestType(
        streetAddress=address.address_line1,
        cityLocality=address.city,
        postalCode=address.postal_code,
        countryCode=address.country_code,
        stateProvince=address.state_code,
    )
    

    return lib.Serializable(request, lib.to_dict)