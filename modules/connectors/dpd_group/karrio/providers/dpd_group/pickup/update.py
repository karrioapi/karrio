"""Karrio DPD Group pickup update API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils


def parse_pickup_update_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup update response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract updated pickup details
    pickup = _extract_details(response, settings)

    return pickup, messages


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from carrier response data

    data: The carrier-specific pickup response data
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    
    # Example implementation for JSON response:
    # Extract pickup details from the JSON response
    # confirmation_number = response.get("confirmationNumber")
    # pickup_date = response.get("pickupDate")
    # ready_time = response.get("readyTime")
    # closing_time = response.get("closingTime")

    # For development, return sample data
    confirmation_number = "PICKUP123"
    pickup_date = lib.today_str()
    ready_time = "10:00"
    closing_time = "18:00"
    

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup_date),
        ready_time=ready_time,
        closing_time=closing_time,
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a pickup update request for the carrier API

    payload: The standardized PickupUpdateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract pickup update details
    confirmation_number = payload.confirmation_number
    address = lib.to_address(payload.address)
    pickup_date = payload.pickup_date or lib.today_str()
    ready_time = payload.ready_time or "10:00"
    closing_time = payload.closing_time or "18:00"

    
    # Example implementation for JSON request:
    request = {
        "confirmationNumber": confirmation_number,
        "pickupDate": pickup_date,
        "readyTime": ready_time,
        "closingTime": closing_time,
        "address": {
            "addressLine1": address.address_line1,
            "city": address.city,
            "postalCode": address.postal_code,
            "countryCode": address.country_code,
            "stateCode": address.state_code,
            "personName": address.person_name,
            "companyName": address.company_name,
            "phoneNumber": address.phone_number,
            "email": address.email,
        }
    }

    return lib.Serializable(request, lib.to_dict)
    