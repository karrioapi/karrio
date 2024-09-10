"""Karrio SEKO Logistics manifest API implementation."""

import karrio.schemas.seko.manifest_response as manifest

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = lib.identity(
        _extract_details(response, settings)
        if any(response.get("OutboundManifest") or [])
        else None
    )

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    details = lib.to_object(manifest.ManifestResponseType, data)
    manifest_numbers = [_.ManifestNumber for _ in details.OutboundManifest]
    manifest_connotes: list = sum(
        [_.ManifestedConnotes for _ in details.OutboundManifest], []
    )
    manifest_doc = lib.bundle_base64(
        [_.ManifestContent for _ in details.OutboundManifest], "PDF"
    )

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest_doc),
        meta=dict(
            ManifestNumber=manifest_numbers[0],
            ManifestNumbers=manifest_numbers,
            ManifestConnotes=manifest_connotes,
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to seko specific type
    request = payload.shipment_identifiers

    return lib.Serializable(request, lib.to_dict)
