"""USPS return shipment wrapper.

Delegates to the standard shipment creation API with the USPS return receipt
option forced on. USPS returns use the same /labels/v3/label endpoint
with returnLabel=true in the request body.

Documentation: schemas/label_request.json (returnLabel field)
"""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.usps.shipment.create as create
import karrio.providers.usps.utils as provider_utils


def parse_return_shipment_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    return create.parse_shipment_response(_response, settings)


def return_shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = {
        **(payload.options or {}),
        "usps_return_receipt": True,
    }

    return create.shipment_request(
        models.ShipmentRequest(**{**lib.to_dict(payload), "options": options}),
        settings,
    )
