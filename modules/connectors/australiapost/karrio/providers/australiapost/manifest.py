import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.australiapost.error as error
import karrio.providers.australiapost.utils as provider_utils
import karrio.schemas.australiapost.manifest_request as australiapost


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ManifestDetails, list[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = (
        _extract_details(response, settings, ctx=_response.ctx)
        if response.get("order", {}).get("order_id") is not None
        else None
    )

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict | None = None,
) -> models.ManifestDetails:
    ctx = ctx or {}
    manifest_document = ctx.get("manifest")

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest_document),
        meta=dict(
            order_id=data["order"]["order_id"],
            order_reference=data["order"]["order_reference"],
            order_creation_date=data["order"]["order_creation_date"],
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)

    request = australiapost.ManifestRequestType(
        order_reference=lib.text(payload.reference),
        payment_method="CHARGE_TO_ACCOUNT",
        consignor=lib.text(address.company_name or address.contact, max=40),
        shipments=[australiapost.ShipmentType(shipment_id=id) for id in payload.shipment_identifiers],
    )

    return lib.Serializable(request, lib.to_dict)
