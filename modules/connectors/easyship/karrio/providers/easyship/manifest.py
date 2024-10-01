"""Karrio Easyship manifest API implementation."""

import karrio.schemas.easyship.manifest_request as easyship
import karrio.schemas.easyship.manifest_response as manifests

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
    details = lib.identity(
        _extract_details(response, settings)
        if response.get("manifest") is not None
        else None
    )

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    details = lib.to_object(manifests.ManifestType, data["manifest"])

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=data["manifest_file"]),
        meta=dict(
            courier_umbrella_name=details.courier_umbrella_name,
            courier_account_id=details.courier_account_id,
            manifest_url=details.document.url,
            reference=details.ref_number,
            manifest_id=details.id,
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "ManifestOptions",
            {
                "easyship_courier_account_id": lib.OptionEnum(
                    "easyship_courier_account_id"
                ),
            },
        ),
    )

    # map data to convert karrio model to easyship specific type
    request = easyship.ManifestRequestType(
        courier_account_id=options.easyship_courier_account_id.state,
        shipment_ids=payload.shipment_identifiers,
    )

    return lib.Serializable(request, lib.to_dict)
