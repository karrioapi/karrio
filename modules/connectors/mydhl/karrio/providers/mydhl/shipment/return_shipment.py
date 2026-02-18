"""Mydhl return shipment wrapper.

Delegates to the standard shipment creation with the return option forced on.
"""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.shipment.create as create
import karrio.providers.mydhl.utils as provider_utils


def parse_return_shipment_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    return create.parse_shipment_response(_response, settings)


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = {
        **(payload.options or {}),
        "mydhl_return_to_seller": True,
    }

    return create.shipment_request(
        models.ShipmentRequest(**{**lib.to_dict(payload), "options": options}),
        settings,
    )
