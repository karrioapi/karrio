"""Karrio MyDHL pickup API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.schemas.mydhl.pickup_create_response as pickup_res


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup response from MyDHL API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    pickup_response = lib.to_object(pickup_res.PickupCreateResponseType, response)
    pickup = _extract_details(pickup_response, settings)

    return pickup, messages


def _extract_details(
    pickup: pickup_res.PickupCreateResponseType,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from MyDHL pickup response

    pickup: The MyDHL PickupCreateResponseType object
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    # Extract first confirmation number using functional pattern
    confirmation_number = next(
        (num for num in (pickup.dispatchConfirmationNumbers or []) if num),
        ""
    )

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup.nextPickupDate) if pickup.nextPickupDate else None,
        ready_time=pickup.readyByTime if pickup.readyByTime else None,
        meta=dict(
            confirmation_numbers=pickup.dispatchConfirmationNumbers or [],
            warnings=pickup.warnings or [],
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a pickup request for the carrier API

    payload: The standardized PickupRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Extract pickup details
    address = lib.to_address(payload.address)
    pickup_date = payload.pickup_date or lib.today_str()
    ready_time = payload.ready_time or "09:00"
    closing_time = payload.closing_time or "17:00"

    
    # Example implementation for JSON request:
    request = {
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
    