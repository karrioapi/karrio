"""Karrio USPS update pickup implementation."""

import karrio.schemas.usps.pickup_update_request as usps
import karrio.schemas.usps.pickup_update_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.usps.error as error
import karrio.providers.usps.utils as provider_utils
import karrio.providers.usps.units as provider_units


def parse_pickup_update_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = (
        _extract_details(response, settings)
        if "confirmationNumber" in response
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    details = lib.to_object(pickup.PickupUpdateResponseType, data)

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=details.confirmationNumber,
        pickup_date=lib.fdate(details.pickupDate),
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
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
                "usps_package_type": lib.OptionEnum("usps_package_type"),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to usps specific type
    request = usps.PickupUpdateRequestType(
        pickupDate=lib.fdate(payload.pickup_date),
        carrierPickupRequest=usps.CarrierPickupRequestType(
            pickupDate=lib.fdate(payload.pickup_date),
            pickupAddress=usps.PickupAddressType(
                firstName=address.person_name,
                lastName=None,
                firm=address.company_name,
                address=usps.AddressType(
                    streetAddress=address.address_line1,
                    secondaryAddress=address.address_line2,
                    city=address.city,
                    state=address.state,
                    ZIPCode=lib.to_zip5(address.postal_code),
                    ZIPPlus4=lib.to_zip4(address.postal_code) or "",
                    urbanization=None,
                ),
                contact=[
                    usps.ContactType(email=address.email)
                    for _ in [address.email]
                    if _ is not None
                ],
            ),
            packages=[
                usps.PackageType(
                    packageType=options.usps_package_type.state or "OTHER",
                    packageCount=len(packages),
                )
            ],
            estimatedWeight=packages.weight.LB,
            pickupLocation=lib.identity(
                usps.PickupLocationType(
                    packageLocation=payload.package_location,
                    specialInstructions=payload.instruction,
                )
                if any([payload.package_location, payload.instruction])
                else None
            ),
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(confirmationNumber=payload.confirmation_number),
    )
