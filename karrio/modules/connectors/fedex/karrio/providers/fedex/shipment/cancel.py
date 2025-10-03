import karrio.schemas.fedex.cancel_request as fedex
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex.error as error
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = lib.failsafe(lambda: response["output"]["cancelledShipment"])

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success is True
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = fedex.CancelRequestType(
        accountNumber=fedex.AccountNumberType(
            value=settings.account_number,
        ),
        emailShipment=None,
        senderCountryCode=None,
        deletionControl="DELETE_ALL_PACKAGES",
        trackingNumber=payload.shipment_identifier,
    )

    return lib.Serializable(request, lib.to_dict)
