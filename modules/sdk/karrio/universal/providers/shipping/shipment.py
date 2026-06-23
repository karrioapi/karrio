import karrio.lib as lib
from karrio.core.models import (
    Documents,
    Message,
    ServiceLabel,
    ShipmentDetails,
    ShipmentRequest,
)
from karrio.core.utils import Serializable
from karrio.core.utils.transformer import to_multi_piece_shipment
from karrio.universal.providers.shipping.utils import ShippingMixinSettings


def parse_shipment_response(
    _response: lib.Deserializable[tuple[list[tuple[str, ServiceLabel]], list[Message]]],
    settings: ShippingMixinSettings,
) -> tuple[ShipmentDetails, list[Message]]:
    service_labels, errors = _response.deserialize()
    shipment = to_multi_piece_shipment(
        [(package_ref, _extract_details(service_label, settings)) for package_ref, service_label in service_labels]
    )

    return shipment, errors


def _extract_details(service_label: ServiceLabel, settings: ShippingMixinSettings) -> ShipmentDetails:
    return ShipmentDetails(
        carrier_name=getattr(settings, "custom_carrier_name", settings.carrier_name),
        carrier_id=settings.carrier_id,
        label_type=service_label.label_type,
        tracking_number=service_label.tracking_number,
        shipment_identifier=service_label.tracking_number,
        meta=dict(service_name=service_label.service_name),
        docs=Documents(label=service_label.label),
    )


def shipment_request(payload: ShipmentRequest, _) -> Serializable:
    return Serializable(payload)
