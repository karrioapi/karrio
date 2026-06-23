"""Karrio DPD France pickup create (CreateCollectionRequestBc)."""

import typing

import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.error as error
import karrio.providers.dpd_france.utils as provider_utils
import karrio.schemas.dpd_france.eprintwebservice as dpd_france


def parse_pickup_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    result = lib.find_element("CreateCollectionRequestBcResult", response, first=True)
    confirmation = (result.text or "").strip() if result is not None else None

    pickup = (
        models.PickupDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            confirmation_number=confirmation,
        )
        if confirmation
        else None
    )

    return pickup, messages


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)
    parcel_count = payload.parcels_count or len(payload.parcels or []) or 1

    request = dpd_france.CreateCollectionRequestBc(
        request=dpd_france.CollectionRequestRequest(
            customer_countrycode=settings.customer_country_code,
            customer_centernumber=settings.customer_center_number,
            customer_number=settings.customer_number,
            shipperaddress=dpd_france.Address(
                countryPrefix=address.country_code,
                zipCode=address.postal_code,
                city=address.city,
                street=(address.street or "")[:35],
                name=(address.company_name or address.person_name),
                phoneNumber=address.phone_number,
            ),
            parcel_count=parcel_count,
            referencenumber=getattr(payload, "reference", None),
            pick_date=lib.fdate(payload.pickup_date),
            time_from=payload.ready_time,
            time_to=payload.closing_time,
            pick_remark=payload.instruction,
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
            "CreateCollectionRequestBc": "imt",
        },
    )
