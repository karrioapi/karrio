"""Karrio DPD Group pickup scheduling implementation."""

import typing
import karrio.lib as lib
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

    # Check if we have valid pickup data
    has_pickup = "scheduledPickupResponse" in response if isinstance(response, dict) else False

    pickup = _extract_details(response, settings) if has_pickup and not any(messages) else None

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from DPD META-API response."""
    response = lib.to_object(dpd_res.PickupCreateResponseType, data)

    # Get first scheduled pickup response
    if response.scheduledPickupResponse and len(response.scheduledPickupResponse) > 0:
        pickup = response.scheduledPickupResponse[0]

        return models.PickupDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            confirmation_number=pickup.pickupreference,
            meta=dict(
                status_code=pickup.statusCode,
                status_description=pickup.statusDescription,
            ),
        )

    return None


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a DPD META-API pickup scheduling request."""
    # DPD only supports one-time pickups via API
    pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    if pickup_type not in ("one_time", None):
        raise lib.exceptions.FieldError({
            "pickup_type": f"DPD only supports 'one_time' pickups via API. Received: '{pickup_type}'. "
            "For daily/recurring pickups, please contact DPD to set up a regular pickup schedule."
        })

    # Convert karrio models to carrier-specific format
    address = lib.to_address(payload.address)

    # Build pickup request
    options = lib.units.ShippingOptions(payload.options or {})

    request = dpd_req.PickupCreateRequestType(
        customerInfos=dpd_req.CustomerInfosType(
            customerAccountNumber=settings.customer_account_number or settings.customer_id or "",
            customerSubAccountNumber=None,
            customerID=settings.customer_id or "",
        ),
        shipmentNumbers=options.get("shipment_numbers", []) if options else [],
        parcelNumbers=payload.package_location if payload.package_location else [],
        pickup=dpd_req.PickupType(
            date=lib.fdate(payload.pickup_date, "%Y-%m-%d"),
            fromTime=payload.ready_time or "09:00",
            toTime=payload.closing_time or "17:00",
        ),
        numberOfParcels=len(payload.parcels) if payload.parcels else 1,
        pickupAddress=dpd_req.PickupAddressType(
            companyName=address.company_name or "",
            name1=address.person_name or "",
            street=address.street_name or address.address_line1 or "",
            houseNumber=address.street_number or "",
            city=address.city,
            zipCode=address.postal_code,
            country=address.country_code,
        ),
        pickupContact=dpd_req.PickupContactType(
            contactPerson=address.person_name or "",
            phone1=address.phone_number or "",
            email=address.email or "",
        ),
        comment=payload.instruction or "",
    )

    return lib.Serializable(request, lib.to_dict)
