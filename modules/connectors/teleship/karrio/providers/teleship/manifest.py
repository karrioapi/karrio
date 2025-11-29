"""Karrio Teleship manifest creation implementation."""

import typing
import karrio.schemas.teleship.manifest_request as teleship
import karrio.schemas.teleship.manifest_response as manifest
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_manifest_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object(manifest.ManifestResponseType, response)

    manifest_details = lib.identity(
        models.ManifestDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            id=details.id,
            doc=None,
            meta=dict(
                status=details.status,
                reference=details.reference,
                createdAt=details.createdAt,
            ),
        )
        if details and details.id
        else None
    )

    return manifest_details, messages


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)

    request = teleship.ManifestRequestType(
        shipmentIds=payload.shipment_identifiers,
        reference=payload.reference,
        address=lib.identity(
            teleship.ManifestRequestAddressType(
                name=address.person_name,
                email=address.email,
                phone=address.phone_number,
                company=address.company_name,
                address=teleship.AddressAddressType(
                    line1=address.address_line1,
                    line2=address.address_line2,
                    city=address.city,
                    state=address.state_code,
                    postcode=address.postal_code,
                    country=address.country_code,
                ),
            )
            if address
            else None
        ),
    )

    return lib.Serializable(request, lib.to_dict)
