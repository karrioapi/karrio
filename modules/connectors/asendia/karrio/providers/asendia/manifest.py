"""Karrio Asendia manifest creation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia.error as error
import karrio.providers.asendia.utils as provider_utils
import karrio.schemas.asendia.manifest_request as asendia_req
import karrio.schemas.asendia.manifest_response as asendia_res


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ManifestDetails], typing.List[models.Message]]:
    """Parse manifest creation response from Asendia API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Parse response to typed object
    manifest = lib.to_object(asendia_res.ManifestResponseType, response)

    # Check for errors in response
    if manifest.errorMessage:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="MANIFEST_ERROR",
                message=manifest.errorMessage,
            )
        )

    # Add messages for failed parcels
    if manifest.errorParcelIds:
        for parcel_id in manifest.errorParcelIds:
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="PARCEL_ERROR",
                    message=f"Failed to include parcel: {parcel_id}",
                )
            )

    # Extract manifest details if successful
    has_manifest = manifest.id is not None and manifest.errorMessage is None

    details = _extract_details(manifest, settings) if has_manifest else None

    return details, messages


def _extract_details(
    manifest: asendia_res.ManifestResponseType,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    """Extract manifest details from Asendia response."""
    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        id=manifest.id,
        meta=dict(
            status=manifest.status,
            created_at=manifest.createdAt,
            manifest_document_location=manifest.manifestDocumentLocation,
            parcels_location=manifest.parcelsLocation,
            manifest_location=manifest.manifestLocation,
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a manifest request for Asendia API.

    Asendia uses POST /api/manifests with parcel IDs.
    The shipment_identifiers should be the parcel IDs returned from create shipment.
    """
    request = asendia_req.ManifestRequestType(
        parcelIds=payload.shipment_identifiers,
    )

    return lib.Serializable(request, lib.to_dict)
