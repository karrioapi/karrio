"""UPS return shipment wrapper.

Delegates to the standard shipment creation API with the UPS return service
option forced on. UPS returns use the same /api/shipments/v2409/ship endpoint
with a ReturnService code in the request body.

Documentation: vendors/Shipping.yaml (ReturnService element)
"""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.shipment.create as create
import karrio.providers.ups.utils as provider_utils


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
        "ups_return_service": (
            (payload.options or {}).get("ups_return_service")
            or "ups_return_3_attempt"
        ),
    }

    return create.shipment_request(
        models.ShipmentRequest(**{**lib.to_dict(payload), "options": options}),
        settings,
    )
