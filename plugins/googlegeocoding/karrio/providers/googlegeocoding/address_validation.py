"""Karrio Google Geocoding address validation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.googlegeocoding.utils as provider_utils


def parse_address_validation_response(
    response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.AddressValidationDetails, typing.List[models.Message]]:
    """Parse address validation response from Google Geocoding API."""
    result = response.deserialize()
    messages: typing.List[models.Message] = []

    status = result.get("status", "")

    # Check for errors
    if status not in ("OK", "ZERO_RESULTS"):
        messages.append(
            models.Message(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                message=result.get("error_message", f"Geocoding failed with status: {status}"),
                code=status,
            )
        )
        return None, messages

    results = result.get("results") or []

    # Find a ROOFTOP location (most accurate)
    rooftop_match = next(
        (
            r for r in results
            if r.get("geometry", {}).get("location_type") == "ROOFTOP"
        ),
        None,
    )

    success = status == "OK" and rooftop_match is not None

    # Try to extract normalized address from the result
    complete_address = None
    if rooftop_match:
        components = rooftop_match.get("address_components", [])
        complete_address = _parse_address_components(components)

    details = models.AddressValidationDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        success=success,
        complete_address=complete_address,
    )

    return details, messages


def _parse_address_components(components: list) -> models.Address:
    """Parse Google address components into a unified Address model."""
    def get_component(types: list) -> str:
        for comp in components:
            if any(t in comp.get("types", []) for t in types):
                return comp.get("long_name", "")
        return None

    street_number = get_component(["street_number"]) or ""
    route = get_component(["route"]) or ""
    address_line1 = f"{street_number} {route}".strip() if street_number or route else None

    return models.Address(
        address_line1=address_line1,
        city=get_component(["locality", "administrative_area_level_3"]),
        state_code=get_component(["administrative_area_level_1"]),
        postal_code=get_component(["postal_code"]),
        country_code=get_component(["country"]),
    )


def address_validation_request(
    payload: models.AddressValidationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create address validation request for Google Geocoding API."""
    address = payload.address
    options = payload.options or {}

    # Format address for search
    address_parts = [
        address.address_line1 or "",
        address.address_line2 or "",
        address.postal_code or "",
        address.city or "",
    ]
    address_string = " ".join(part for part in address_parts if part)

    if not address_string:
        raise Exception(
            "At least one address info must be provided (address_line1, city and/or postal_code)"
        )

    # Add state and country for better accuracy
    if address.state_code:
        address_string = f"{address_string} {address.state_code}"
    if address.country_code:
        address_string = f"{address_string} {address.country_code}"

    # Replace spaces with + for URL encoding
    formatted_address = address_string.replace(" ", "+")

    request = dict(
        address=formatted_address,
        key=settings.api_key,
        location_type=options.get("location_type", "ROOFTOP"),
    )

    return lib.Serializable(request, lib.to_dict)
