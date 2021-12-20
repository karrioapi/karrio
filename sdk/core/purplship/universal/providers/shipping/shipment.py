from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    Message,
)
from purplship.universal.providers.shipping.utils import ShippingMixinSettings
from sdk.core.purplship.core.models import ServiceLabel


def parse_shipment_response(
    response: Tuple[ServiceLabel, List[Message]], settings: ShippingMixinSettings
) -> Tuple[List[ShipmentDetails], List[Message]]:
    service_label, errors = response
    shipments = _extract_details(service_label, settings)

    return shipments, errors


def _extract_details(
    service_label: ServiceLabel, settings: ShippingMixinSettings
) -> ShipmentDetails:
    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        label=service_label.label,
        tracking_number=service_label.tracking_number,
        shipment_identifier=service_label.tracking_number,
        meta=dict(service_name=service_label.service_name),
    )


def shipment_request(payload: ShipmentRequest, _) -> Serializable[ShipmentRequest]:
    return Serializable(payload)
