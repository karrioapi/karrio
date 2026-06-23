"""Karrio DPD France shipment cancel (TerminateShipment)."""

import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.error as error
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.eprintwebservice as dpd_france


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = len(messages) == 0

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
    request = dpd_france.TerminateShipment(
        request=dpd_france.TerminateShipmentRequest(
            customer=dpd_france.Customer(
                countrycode=settings.customer_country_code,
                centernumber=settings.customer_center_number,
                number=settings.customer_number,
            ),
            BarcodeId=payload.shipment_identifier,
        )
    )

    envelope = lib.Envelope(
        Header=lib.Header(
            dpd_france.UserCredentials(
                userid=settings.userid,
                password=settings.password,
            )
        ),
        Body=lib.Body(request),
    )

    return lib.Serializable(
        envelope,
        lambda env: lib.envelope_serializer(
            env,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software"'
            ),
            prefixes={
                "Envelope": "soapenv",
                "UserCredentials": "imt",
                "TerminateShipment": "imt",
            },
        ),
    )
