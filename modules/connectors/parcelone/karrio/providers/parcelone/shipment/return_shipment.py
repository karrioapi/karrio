"""ParcelOne return shipment wrapper.

Delegates to the standard shipment creation with the return option forced on.
ParcelOne has no dedicated return endpoint — returns go through POST /shipment
with ReturnShipmentIndicator set (handled in create.shipment_request via the
is_return option).
"""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.parcelone.shipment.create as create
import karrio.providers.parcelone.utils as provider_utils


def parse_return_shipment_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails, list[models.Message]]:
    return create.parse_shipment_response(_response, settings)


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = {**(payload.options or {}), "is_return": True}
    return create.shipment_request(
        models.ShipmentRequest(**{**lib.to_dict(payload), "options": options}),
        settings,
    )
