import karrio.schemas.asendia_us.cancel_request as asendia
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia_us.error as error
import karrio.providers.asendia_us.utils as provider_utils
import karrio.providers.asendia_us.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = response.get("responseStatusCode") == 200

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = asendia.CancelRequestType(
        accountNumber=settings.account_number,
        subAccountNumber=settings.connection_config.sub_account_number.state,
        packageID=payload.shipment_identifier,
    )

    return lib.Serializable(request, lib.to_dict)
