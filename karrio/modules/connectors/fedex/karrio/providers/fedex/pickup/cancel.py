import karrio.schemas.fedex.cancel_pickup_request as fedex
import karrio.schemas.fedex.cancel_pickup_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.fedex.error as error
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.units as provider_units


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = any(lib.failsafe(lambda: response["output"]["pickupConfirmationCode"]))

    confirmation = lib.identity(
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Pickup",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            # fmt: off
            {
                "fedex_carrier_code": lib.OptionEnum("carrierCode"),
                "fedex_pickup_location": lib.OptionEnum("location"),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to fedex specific type
    request = fedex.CancelPickupRequestType(
        associatedAccountNumber=fedex.AssociatedAccountNumberType(
            value=settings.account_number,
        ),
        pickupConfirmationCode=payload.confirmation_number,
        remarks=payload.reason,
        carrierCode=options.fedex_carrier_code.state,
        accountAddressOfRecord=lib.identity(
            fedex.AccountAddressOfRecordType(
                streetLines=address.address_lines,
                urbanizationCode=None,
                city=address.city,
                stateOrProvinceCode=provider_utils.state_code(address),
                postalCode=address.postal_code,
                countryCode=address.country_code,
                residential=address.residential,
                addressClassification=None,
            )
            if payload.address
            else None
        ),
        scheduledDate=lib.fdate(payload.pickup_date, "%Y-%m-%d"),
        location=options.fedex_pickup_location.state,
    )

    return lib.Serializable(request, lib.to_dict)
