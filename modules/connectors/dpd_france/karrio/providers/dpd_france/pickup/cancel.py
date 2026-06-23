"""Karrio DPD France pickup cancel (TerminateCollectionRequestBc)."""

import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.error as error
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.eprintwebservice as dpd_france


def parse_pickup_cancel_response(
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
    request = dpd_france.TerminateCollectionRequestBc(
        request=dpd_france.TerminateCollectionRequestParcel(
            customer=dpd_france.Customer(
                countrycode=settings.customer_country_code,
                centernumber=settings.customer_center_number,
                number=settings.customer_number,
            ),
            parcel=dpd_france.ParcelBcIdRequest(
                Parcel=dpd_france.BcIdRequest(
                    Barcode=dpd_france.BarcodeData(
                        Identifier=dpd_france.BcIdentifier.BIC_3.value,
                        BarcodeValue=payload.confirmation_number,
                    ),
                ),
            ),
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

    return lib.Serializable(envelope, _serialize)


def _serialize(envelope: lib.Envelope) -> str:
    return lib.envelope_serializer(
        envelope,
        namespace=(
            'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software"'
        ),
        prefixes={
            "Envelope": "soapenv",
            "UserCredentials": "imt",
            "TerminateCollectionRequestBc": "imt",
        },
    )
