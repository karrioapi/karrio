"""FedEx return shipment wrapper.

Delegates to the standard shipment creation API with the FedEx return shipment
option forced on. FedEx returns use the same /ship/v1/shipments endpoint
with returnShipmentDetail in the request body.

Documentation: schemas/shipping_request.json (ReturnShipmentDetailType)
"""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.fedex.shipment.create as create
import karrio.providers.fedex.utils as provider_utils


def parse_return_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    return create.parse_shipment_response(_response, settings)


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = {
        **(payload.options or {}),
        "fedex_return_shipment": True,
    }

    return create.shipment_request(
        models.ShipmentRequest(**{**lib.to_dict(payload), "options": options}),
        settings,
    )
