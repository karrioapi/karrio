"""Karrio Hermes pickup scheduling implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hermes.error as error
import karrio.providers.hermes.utils as provider_utils
import karrio.schemas.hermes.pickup_create_request as hermes_req
import karrio.schemas.hermes.pickup_create_response as hermes_res


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.PickupDetails], typing.List[models.Message]]:
    """Parse Hermes pickup response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have a valid pickup order ID
    pickup = None
    if response.get("pickupOrderID"):
        pickup = _extract_details(response, settings)

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from Hermes response."""
    response = lib.to_object(hermes_res.PickupCreateResponseType, data)

    # Hermes returns pickupOrderID as the confirmation number
    confirmation_number = response.pickupOrderID or ""

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation_number,
        pickup_date=None,  # Not returned in response
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a Hermes pickup request."""
    # Hermes only supports one-time pickups via API
    pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    if pickup_type not in ("one_time", None):
        raise lib.exceptions.FieldError({
            "pickup_type": f"Hermes only supports 'one_time' pickups via API. Received: '{pickup_type}'. "
            "For daily/recurring pickups, please contact Hermes to set up a regular pickup schedule."
        })

    address = lib.to_address(payload.address)

    # Parse parcel counts by size (XS, S, M, L, XL)
    # Default to counting all parcels as M (medium) if not specified
    parcel_count = hermes_req.ParcelCountType(
        pickupParcelCountXS=0,
        pickupParcelCountS=0,
        pickupParcelCountM=len(payload.parcels) if payload.parcels else 1,
        pickupParcelCountL=0,
        pickupParcelCountXL=0,
    )

    # Map time slot from ready_time/closing_time
    # Valid values per OpenAPI: BETWEEN_10_AND_13, BETWEEN_12_AND_15, BETWEEN_14_AND_17
    time_slot = None
    if payload.ready_time:
        hour = int(payload.ready_time.split(":")[0]) if ":" in payload.ready_time else 12
        if hour < 12:
            time_slot = "BETWEEN_10_AND_13"
        elif hour < 14:
            time_slot = "BETWEEN_12_AND_15"
        else:
            time_slot = "BETWEEN_14_AND_17"

    # Create the request using generated schema types
    request = hermes_req.PickupCreateRequestType(
        pickupAddress=hermes_req.PickupAddressType(
            street=address.street_name,
            houseNumber=address.street_number or "",
            zipCode=address.postal_code,
            town=address.city,
            countryCode=address.country_code,
            addressAddition=address.address_line2 or address.company_name or None,
        ),
        pickupName=hermes_req.PickupNameType(
            title=None,
            gender=None,
            firstname=address.person_name.split()[0] if address.person_name else None,
            middlename=None,
            lastname=" ".join(address.person_name.split()[1:]) if address.person_name and len(address.person_name.split()) > 1 else address.person_name,
        ),
        phone=address.phone_number or None,
        pickupDate=payload.pickup_date,
        pickupTimeSlot=time_slot,
        parcelCount=parcel_count,
    )

    return lib.Serializable(request, lib.to_dict)