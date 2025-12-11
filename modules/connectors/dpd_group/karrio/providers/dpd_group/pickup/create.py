"""Karrio DPD Group pickup scheduling implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract pickup details from the response to populate PickupDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., PickupRequestType),
# while XML schema types don't have this suffix (e.g., PickupRequest).

import karrio.schemas.dpd_group.pickup_request as dpd_group_req
import karrio.schemas.dpd_group.pickup_response as dpd_group_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """
    Parse pickup scheduling response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (PickupDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract pickup details
    pickup = _extract_details(response, settings)

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """
    Extract pickup details from carrier response data

    data: The carrier-specific pickup response data
    settings: The carrier connection settings

    Returns a PickupDetails object with the pickup information
    """
    
    # For JSON APIs, convert dict to proper response object
    pickup = lib.to_object(dpd_group_res.PickupResponseType, data)

    # Extract pickup confirmation details
    confirmation_number = pickup.confirmationNumber if hasattr(pickup, 'confirmationNumber') else ""
    pickup_date = pickup.pickupDate if hasattr(pickup, 'pickupDate') else ""
    ready_time = pickup.readyTime if hasattr(pickup, 'readyTime') else ""
    closing_time = pickup.closingTime if hasattr(pickup, 'closingTime') else ""
    

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=lib.fdate(pickup_date),
        ready_time=ready_time,
        closing_time=closing_time,
    ) if confirmation_number else None


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
    # Convert karrio models to carrier-specific format
    address = lib.to_address(payload.address)

    
    # For JSON API request
    request = dpd_group_req.PickupRequestType(
        accountNumber=settings.account_number,
        pickupDate=payload.pickup_date,
        readyTime=payload.ready_time,
        closingTime=payload.closing_time,
        instruction=payload.instruction,
        address={
            "companyName": address.company_name,
            "personName": address.person_name,
            "street": address.address_line1,
            "city": address.city,
            "state": address.state_code,
            "postalCode": address.postal_code,
            "country": address.country_code,
            "phone": address.phone_number,
            "email": address.email,
        },
        parcelCount=len(payload.parcels) if payload.parcels else 1,
    )
    

    return lib.Serializable(request, lib.to_dict)