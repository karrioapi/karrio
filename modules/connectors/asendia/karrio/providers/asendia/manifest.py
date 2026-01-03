"""Karrio Asendia manifest creation implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract manifest details from the response to populate ManifestDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ManifestRequestType),
# while XML schema types don't have this suffix (e.g., ManifestRequest).

import karrio.schemas.asendia.manifest_request as asendia_req
import karrio.schemas.asendia.manifest_response as asendia_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia.error as error
import karrio.providers.asendia.utils as provider_utils


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    """
    Parse manifest creation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ManifestDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract manifest details
    manifest = _extract_details(response, settings)

    return manifest, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    """
    Extract manifest details from carrier response data

    data: The carrier-specific manifest response data
    settings: The carrier connection settings

    Returns a ManifestDetails object with the manifest information
    """
    
    # For JSON APIs, convert dict to proper response object
    manifest = lib.to_object(asendia_res.ManifestResponseType, data)

    # Extract manifest details
    manifest_id = manifest.manifestId if hasattr(manifest, 'manifestId') else ""
    manifest_url = manifest.manifestUrl if hasattr(manifest, 'manifestUrl') else ""
    manifest_document = manifest.manifestData if hasattr(manifest, 'manifestData') else ""
    status = manifest.status if hasattr(manifest, 'status') else ""
    

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        manifest_id=manifest_id,
        doc=models.ManifestDocument(manifest=manifest_document) if manifest_document else None,
        meta=dict(
            status=status,
            manifest_url=manifest_url,
        ),
    ) if manifest_id else None


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a manifest request for the carrier API

    payload: The standardized ManifestRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    address = lib.to_address(payload.address) if payload.address else None

    
    # For JSON API request
    request = asendia_req.ManifestRequestType(
        accountNumber=settings.account_number,
        closeDate=payload.options.get("closeDate") if payload.options else None,
        shipments=[
            {"trackingNumber": identifier}
            for identifier in payload.shipment_identifiers
        ],
    )
    

    return lib.Serializable(request, lib.to_dict)