import karrio.schemas.fedex.pickup_request as fedex
import karrio.schemas.fedex.pickup_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.fedex.error as error
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.units as provider_units


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = lib.identity(
        _extract_details(response, settings, _response.ctx)
        if (response.get("output") or {}).get("pickupConfirmationCode")
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.PickupDetails:
    details = lib.to_object(pickup.PickupResponseType, data)

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=details.output.pickupConfirmationCode,
        pickup_date=lib.fdate(ctx["pickup_date"]),
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
            # fmt: off
            {
                "fedex_carrier_code": lib.OptionEnum("carrierCode"),
                "fedex_pickup_location": lib.OptionEnum("location"),
                "fedex_user_message": lib.OptionEnum("userMessage"),
                "fedex_early_pickup": lib.OptionEnum("earlyPickup"),
                "fedex_building_part": lib.OptionEnum("buildingPart"),
                "fedex_pickup_date_type": lib.OptionEnum("pickupDateType"),
                "fedex_supplies_requested": lib.OptionEnum("suppliesRequested"),
                "fedex_pickup_address_type": lib.OptionEnum("pickupAddressType"),
                "fedex_building_part_description": lib.OptionEnum("buildingPartDescription"),
                "fedex_associated_account_number_type": lib.OptionEnum("associatedAccountNumberType"),
            },
            # fmt: on
        ),
    )

    # Map unified pickup_type to FedEx pickup type
    # one_time -> ON_CALL, daily/recurring -> REGULAR_STOP
    unified_pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    fedex_pickup_type = (
        "REGULAR_STOP"
        if unified_pickup_type in ("daily", "recurring")
        else "ON_CALL"
    )

    # Normalize times to HH:MM format to handle both HH:MM and HH:MM:SS inputs
    ready_time = lib.ftime(payload.ready_time, try_formats=["%H:%M:%S", "%H:%M"]) or payload.ready_time
    closing_time = lib.ftime(payload.closing_time, try_formats=["%H:%M:%S", "%H:%M"]) or payload.closing_time

    # map data to convert karrio model to fedex specific type
    request = fedex.PickupRequestType(
        associatedAccountNumber=fedex.AccountNumberType(
            value=settings.account_number,
        ),
        originDetail=fedex.OriginDetailType(
            pickupAddressType=options.fedex_pickup_address_type.state,
            pickupLocation=fedex.PickupLocationType(
                contact=fedex.ContactType(
                    companyName=address.company_name,
                    personName=address.person_name,
                    phoneNumber=address.phone_number,
                    phoneExtension=None,
                ),
                address=fedex.AccountAddressOfRecordType(
                    streetLines=address.address_lines,
                    city=address.city,
                    stateOrProvinceCode=address.state_code,
                    postalCode=address.postal_code,
                    countryCode=address.country_code,
                    residential=address.residential,
                    addressClassification=None,
                    urbanizationCode=None,
                ),
                accountNumber=fedex.AccountNumberType(
                    value=settings.account_number,
                ),
                deliveryInstructions=options.instructions.state,
            ),
            readyDateTimestamp=f"{payload.pickup_date}T{ready_time}:00Z",
            customerCloseTime=f"{closing_time}:00",
            pickupDateType=options.fedex_pickup_date_type.state,
            packageLocation=payload.package_location,
            buildingPart=options.fedex_building_part.state,
            buildingPartDescription=options.fedex_building_part_description.state,
            earlyPickup=options.fedex_early_pickup.state,
            suppliesRequested=options.fedex_supplies_requested.state,
            geographicalPostalCode=options.geographical_postal_code.state,
        ),
        associatedAccountNumberType=options.fedex_associated_account_number_type.state,
        totalWeight=fedex.TotalWeightType(
            units=packages.weight_unit,
            value=packages.weight.value,
        ),
        packageCount=len(packages),
        carrierCode=options.fedex_carrier_code.state or "FDXE",
        accountAddressOfRecord=None,
        remarks=None,
        countryRelationships=None,
        pickupType=fedex_pickup_type,
        trackingNumber=None,
        commodityDescription=lib.text(packages.description, max=100),
        expressFreightDetail=None,
        oversizePackageCount=None,
        pickupNotificationDetail=lib.identity(
            fedex.PickupNotificationDetailType(
                emailDetails=[
                    fedex.EmailDetailType(
                        address=address.email,
                        locale="en_US",
                    )
                ],
                format="TEXT",
                userMessage=options.fedex_user_message.state,
            )
            if address.email
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
