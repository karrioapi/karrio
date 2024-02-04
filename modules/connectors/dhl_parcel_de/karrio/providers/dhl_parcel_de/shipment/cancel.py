import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.utils as provider_utils
import karrio.providers.dhl_parcel_de.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = (response.get("status") or {}).get("title", "").lower() == "ok"

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
    request = dict(
        shipment=",".join(
            list(
                set(
                    [
                        payload.shipment_identifier,
                        *((payload.options or {}).get("shipment_identifiers") or []),
                    ]
                )
            )
        ),
        profile=settings.profile,
    )

    return lib.Serializable(request)
