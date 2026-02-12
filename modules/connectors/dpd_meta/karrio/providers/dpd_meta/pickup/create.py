"""Karrio DPD Group pickup scheduling implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpd_meta.error as error
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.pickup_create_request as dpd_req
import karrio.schemas.dpd_meta.pickup_create_response as dpd_res


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """Parse DPD META-API pickup scheduling response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    pickup_data = response[0] if isinstance(response, list) else response
    scheduled = (
        (pickup_data or {}).get("scheduledPickupResponse")
        if isinstance(pickup_data, dict)
        else None
    )
    pickup_item = next(
        (p for p in (scheduled or []) if p.get("pickupreference")), None
    )

    # Parse inline errors from items without pickupreference
    messages += [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=item.get("statusCode") or "PICKUP_ERROR",
            message=lib.text(item.get("statusDescription"), max=200),
        )
        for item in (scheduled or [])
        if not item.get("pickupreference") and item.get("statusDescription")
    ]

    pickup = lib.identity(
        _extract_details(pickup_item, settings)
        if pickup_item and not any(messages)
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from DPD META-API response."""
    pickup = lib.to_object(dpd_res.ScheduledPickupResponseType, data)

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=pickup.pickupreference,
        meta=dict(
            status_code=pickup.statusCode,
            status_description=pickup.statusDescription,
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a DPD META-API pickup scheduling request."""
    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)

    request = dpd_req.PickupCreateRequestType(
        customerInfos=dpd_req.CustomerInfosType(
            customerAccountNumber=(
                settings.customer_account_number or settings.customer_id
            ),
            customerID=settings.customer_id,
        ),
        shipmentNumbers=payload.shipment_identifiers or None,
        parcelNumbers=(
            [payload.package_location] if payload.package_location else None
        ),
        pickup=dpd_req.PickupType(
            date=lib.fdate(payload.pickup_date, "%Y-%m-%d"),
            fromTime=lib.ftime(payload.ready_time, current_format="%H:%M", output_format="%H%M") or "0900",
            toTime=lib.ftime(payload.closing_time, current_format="%H:%M", output_format="%H%M") or "1700",
        ),
        numberOfParcels=len(packages) if any(packages) else 1,
        pickupAddress=dpd_req.PickupAddressType(
            companyName=address.company_name or "",
            name1=address.person_name or "",
            street=address.street_name or address.address_line1 or "",
            houseNumber=address.street_number or "",
            city=address.city,
            state=lib.text(address.state_code, max=2),
            zipCode=address.postal_code,
            country=address.country_code,
        ),
        pickupContact=dpd_req.PickupContactType(
            contactPerson=address.person_name or "",
            phone1=address.phone_number or "",
            email=address.email or "",
        ),
        pickupWeight=str(max(int(packages.weight.G or 0), 1000)),
        comment=payload.instruction,
    )

    return lib.Serializable(request, lib.to_dict)
