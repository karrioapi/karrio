from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    Documents,
    ShipmentRequest,
    ShipmentDetails,
    Message,
)
from purplship.universal.providers.shipping.utils import ShippingMixinSettings
from purplship.core.models import ServiceLabel
from purplship.core.utils.transformer import to_multi_piece_shipment


def parse_shipment_response(
    response: Tuple[List[Tuple[str, ServiceLabel]], List[Message]],
    settings: ShippingMixinSettings,
) -> Tuple[ShipmentDetails, List[Message]]:
    service_labels, errors = response
    shipments = to_multi_piece_shipment(
        [
            (package_ref, _extract_details(service_label, settings))
            for package_ref, service_label in service_labels
        ]
    )

    return shipments, errors


def _extract_details(
    service_label: ServiceLabel, settings: ShippingMixinSettings
) -> ShipmentDetails:
    return ShipmentDetails(
        carrier_name=settings.custom_carrier_name,
        carrier_id=settings.carrier_id,
        label_type=service_label.label_type,
        tracking_number=service_label.tracking_number,
        shipment_identifier=service_label.tracking_number,
        meta=dict(service_name=service_label.service_name),
        docs=Documents(label=service_label.label),
    )


def shipment_request(payload: ShipmentRequest, _) -> Serializable[ShipmentRequest]:
    return Serializable(payload)
