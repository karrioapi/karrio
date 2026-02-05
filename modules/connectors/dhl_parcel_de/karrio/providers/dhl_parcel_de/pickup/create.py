"""Karrio DHL Germany pickup create implementation."""

import karrio.schemas.dhl_parcel_de.pickup_request as dhl
import karrio.schemas.dhl_parcel_de.pickup_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup_details = lib.identity(
        _extract_details(response, settings, _response.ctx)
        if isinstance(response, dict) and response.get("confirmation") is not None
        else None
    )

    return pickup_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.PickupDetails:
    details = lib.to_object(pickup.PickupResponseType, data)
    confirmation = details.confirmation.value

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=confirmation.orderID,
        pickup_date=lib.fdate(confirmation.pickupDate),
        meta=dict(
            pickup_type=confirmation.pickupType,
            free_of_charge=confirmation.freeOfCharge,
            confirmed_shipments=[
                dict(
                    transportation_type=s.transportationType,
                    shipment_no=s.shipmentNo,
                    order_date=s.orderDate,
                )
                for s in (confirmation.confirmedShipments or [])
            ],
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # DHL Parcel DE only supports one-time pickups via API
    pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    if pickup_type not in ("one_time", None):
        raise lib.exceptions.FieldError(
            {
                "pickup_type": f"DHL Parcel DE only supports 'one_time' pickups via API. Received: '{pickup_type}'. "
                "For daily/recurring pickups, please contact DHL to set up a regular pickup schedule."
            }
        )

    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            {
                "billing_number": lib.OptionEnum("billing_number"),
                "dhl_parcel_de_pickup_location_type": lib.OptionEnum(
                    "pickupLocationType"
                ),
                "dhl_parcel_de_as_id": lib.OptionEnum("asId"),
                "dhl_parcel_de_transportation_type": lib.OptionEnum(
                    "transportationType"
                ),
                "dhl_parcel_de_shipment_size": lib.OptionEnum("shipmentSize"),
                "dhl_parcel_de_send_confirmation_email": lib.OptionEnum(
                    "sendConfirmationEmail", bool
                ),
                "dhl_parcel_de_send_time_window_email": lib.OptionEnum(
                    "sendTimeWindowEmail", bool
                ),
                "dhl_parcel_de_pickup_date_type": lib.OptionEnum("pickupDateType"),
            },
        ),
    )

    billing_number = (
        settings.connection_config.pickup_billing_number.state
        or options.billing_number.state
    )
    pickup_date_type = options.dhl_parcel_de_pickup_date_type.state or (
        "ASAP" if not payload.pickup_date else "Date"
    )
    location_type = options.dhl_parcel_de_pickup_location_type.state or "Address"
    transportation_type = options.dhl_parcel_de_transportation_type.state or "PAKET"
    send_confirmation = options.dhl_parcel_de_send_confirmation_email.state
    send_time_window = options.dhl_parcel_de_send_time_window_email.state

    # Build the request
    request = dhl.PickupRequestType(
        customerDetails=dhl.CustomerDetailsType(
            accountNumber=None,
            billingNumber=billing_number,
        ),
        pickupLocation=dhl.PickupLocationType(
            type=location_type,
            pickupAddress=lib.identity(
                dhl.PickupAddressType(
                    name1=address.company_name or address.person_name,
                    name2=lib.identity(
                        address.person_name if address.company_name else None
                    ),
                    addressStreet=lib.identity(
                        address.street_name
                        if address.street_number
                        else address.address_line1
                    ),
                    addressHouse=lib.text(
                        (
                            address.street_number
                            if address.street_number
                            else address.address_line2
                        ),
                        max=10,
                    ),
                    postalCode=address.postal_code,
                    city=address.city,
                    country=address.country_code,
                    state=address.state_code,
                )
                if location_type == "Address"
                else None
            ),
            asId=options.dhl_parcel_de_as_id.state if location_type == "Id" else None,
        ),
        businessHours=lib.identity(
            [
                dhl.BusinessHourType(
                    timeFrom=payload.ready_time,
                    timeUntil=payload.closing_time,
                )
            ]
            if payload.ready_time and payload.closing_time
            else None
        ),
        contactPerson=[
            dhl.ContactPersonType(
                name=address.person_name or address.company_name,
                phone=address.phone_number,
                email=address.email,
                emailNotification=lib.identity(
                    dhl.EmailNotificationType(
                        sendPickupConfirmationEmail=send_confirmation,
                        sendPickupTimeWindowEmail=send_time_window,
                    )
                    if address.email
                    and (send_confirmation is not None or send_time_window is not None)
                    else None
                ),
            )
        ],
        pickupDetails=dhl.PickupDetailsType(
            pickupDate=dhl.PickupDateType(
                type=pickup_date_type,
                value=payload.pickup_date if pickup_date_type == "Date" else None,
            ),
            totalWeight=lib.identity(
                dhl.TotalWeightType(
                    uom="g",
                    value=lib.to_int(packages.weight.G),
                )
                if packages.weight.G
                else None
            ),
            comment=payload.instruction,
        ),
        shipmentDetails=dhl.ShipmentDetailsType(
            shipments=[
                dhl.ShipmentType(
                    transportationType=transportation_type,
                    size=options.dhl_parcel_de_shipment_size.state,
                )
                for _ in range(
                    len(packages)
                    if (payload.options or {}).get("shipment_identifiers")
                    else 1
                )
            ]
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            pickup_date=payload.pickup_date,
            address=payload.address,
        ),
    )
