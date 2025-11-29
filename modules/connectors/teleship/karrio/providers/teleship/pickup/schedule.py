"""Karrio Teleship pickup scheduling implementation."""

import typing
import karrio.schemas.teleship.pickup_request as teleship
import karrio.schemas.teleship.pickup_response as pickup
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object(pickup.PickupResponseType, response)

    pickup_details = lib.identity(
        models.PickupDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            confirmation_number=details.pickup.id,
            pickup_date=lib.fdatetime(
                details.pickup.startAt,
                current_format="%Y-%m-%dT%H:%M:%S.%fZ",
                output_format="%Y-%m-%d",
            ),
            meta=lib.to_dict(details.pickup),
        )
        if details and details.pickup and details.pickup.id
        else None
    )

    return pickup_details, messages


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)

    request = teleship.PickupRequestType(
        startAt=payload.pickup_date,
        endAt=payload.closing_time or payload.pickup_date,
        shipmentIds=payload.shipment_identifiers,
        address=teleship.PickupRequestAddressType(
            name=address.person_name,
            email=address.email,
            phone=address.phone_number,
            company=address.company_name,
            address=teleship.AddressAddressType(
                line1=address.address_line1,
                line2=address.address_line2,
                city=address.city,
                state=address.state_code,
                postcode=address.postal_code,
                country=address.country_code,
            ),
        ),
        reference=payload.instruction,
    )

    return lib.Serializable(request, lib.to_dict)
