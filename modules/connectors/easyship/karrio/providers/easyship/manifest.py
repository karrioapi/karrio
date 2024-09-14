"""Karrio Easyship manifest API implementation."""

import karrio.schemas.easyship.manifest_request as easyship
import karrio.schemas.easyship.manifest_response as manifest

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    details = None  # manifest details parsing
    manifest = None  # extract carrier manifest file

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest),
        meta=dict(),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to easyship specific type
    request = easyship.ManifestRequestType(
        courieraccountid=None,
        shipmentids=[],
    )

    return lib.Serializable(request, lib.to_dict)
