"""Karrio AddressComplete address validation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.addresscomplete.utils as provider_utils


def parse_address_validation_response(
    response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.AddressValidationDetails, typing.List[models.Message]]:
    """Parse address validation response from Canada Post AddressComplete API."""
    result = response.deserialize()
    messages: typing.List[models.Message] = []

    # Check for errors in the response
    if isinstance(result, dict) and result.get("Error"):
        messages.append(
            models.Message(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                message=result.get("Description", "Unknown error"),
                code=result.get("Error"),
            )
        )
        return None, messages

    # Process results
    results = result if isinstance(result, list) else []

    # Find a matching permanent address (Next == "Retrieve" means it's a permanent address)
    address_match = next(
        (r for r in results if r.get("Next") == "Retrieve"),
        None,
    )

    success = address_match is not None

    details = models.AddressValidationDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        success=success,
        complete_address=None,  # AddressComplete doesn't return a normalized address in Find
    )

    return details, messages


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create address validation request for Canada Post AddressComplete API."""
    address = payload.address
    options = payload.options or {}

    # Format address for search
    address_parts = [
        address.address_line1 or "",
        address.address_line2 or "",
        address.city or "",
        address.postal_code or "",
    ]
    search_term = ", ".join(part for part in address_parts if part)

    if not search_term:
        raise Exception(
            "At least one address info must be provided (address_line1, city and/or postal_code)"
        )

    request = dict(
        Key=settings.api_key,
        SearchTerm=search_term,
        Country=address.country_code,
        MaxResults=options.get("max_results", 5),
        MaxSuggestions=options.get("max_suggestions", 5),
        SearchFor="Places",
        LanguagePreference=options.get("language", "EN"),
    )

    return lib.Serializable(request, lib.to_dict)
