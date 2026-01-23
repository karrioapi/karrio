"""Karrio DHL Germany pickup create implementation."""

import karrio.schemas.dhl_parcel_de.pickup_request as dhl
import karrio.schemas.dhl_parcel_de.pickup_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
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
        if response.get("confirmation") is not None
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
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
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
            },
        ),
    )

    # Resolve billing number from options (passed from shipment.meta) or fallback to default
    billing_number = options.billing_number.state or settings.get_billing_number()

    # Parse ready and closing times
    ready_time = payload.ready_time or "09:00"
    closing_time = payload.closing_time or "17:00"

    # Compute total weight in grams
    total_weight_kg = packages.weight.value if packages.weight else 0
    total_weight_grams = int(total_weight_kg * 1000)

    # Build the request
    request = dhl.PickupRequestType(
        customerDetails=dhl.CustomerDetailsType(
            accountNumber=billing_number,
            billingNumber=billing_number,
        ),
        pickupLocation=dhl.PickupLocationType(
            type=options.dhl_parcel_de_pickup_location_type.state or "Address",
            pickupAddress=dhl.PickupAddressType(
                name1=address.company_name or address.person_name,
                name2=lib.identity(
                    address.person_name if address.company_name else None
                ),
                addressStreet=address.street,
                addressHouse=(
                    lib.text(address.street_number) if address.street_number else None
                ),
                postalCode=address.postal_code,
                city=address.city,
                country=address.country_code,
                state=address.state_code,
            ),
            asId=options.dhl_parcel_de_as_id.state,
        ),
        businessHours=[
            dhl.BusinessHourType(
                timeFrom=ready_time,
                timeUntil=closing_time,
            )
        ],
        contactPerson=[
            dhl.ContactPersonType(
                name=address.person_name or address.company_name,
                phone=address.phone_number,
                email=address.email,
                emailNotification=lib.identity(
                    dhl.EmailNotificationType(
                        sendPickupConfirmationEmail=options.dhl_parcel_de_send_confirmation_email.state,
                        sendPickupTimeWindowEmail=options.dhl_parcel_de_send_time_window_email.state,
                    )
                    if address.email
                    else None
                ),
            )
        ],
        pickupDetails=dhl.PickupDetailsType(
            pickupDate=dhl.PickupDateType(
                type="Date",
                value=payload.pickup_date,
            ),
            totalWeight=dhl.TotalWeightType(
                uom="g",
                value=total_weight_grams,
            ),
            comment=payload.instruction,
        ),
        shipmentDetails=lib.identity(
            dhl.ShipmentDetailsType(
                shipments=[
                    dhl.ShipmentType(
                        transportationType=options.dhl_parcel_de_transportation_type.state
                        or "PAKET",
                        replacement=False,
                        shipmentNo=None,
                        size=options.dhl_parcel_de_shipment_size.state,
                        pickupServices=None,
                        customerReference=None,
                    )
                    for _ in range(len(packages) or 1)
                ]
            )
            if len(packages) > 0
            else None
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
