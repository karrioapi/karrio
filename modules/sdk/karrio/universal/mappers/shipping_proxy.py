import uuid

import attr

import karrio.lib as lib
from karrio.addons.label import generate_label
from karrio.core.models import Message, ServiceLabel, ShipmentRequest
from karrio.universal.providers.shipping import (
    ShippingMixinSettings,
)


@attr.s(auto_attribs=True)
class ShippingMixinProxy:
    settings: ShippingMixinSettings

    def create_shipment(
        self, request: lib.Serializable
    ) -> lib.Deserializable[tuple[list[tuple[str, ServiceLabel]], list[Message]]]:
        response = generate_service_label(request.serialize(), self.settings)

        return lib.Deserializable(response)


def generate_service_label(
    shipment: ShipmentRequest, settings: ShippingMixinSettings
) -> tuple[list[tuple[str, ServiceLabel]], list[Message]]:
    messages: list[Message] = []
    service_labels: list[tuple[str, ServiceLabel]] = []

    packages = lib.to_packages(shipment.parcels)
    service = shipment.service
    # Multiple ServiceLevels can share a `service_code` (e.g. UPS Standard /
    # Saturday / Return all carry `ups_standard` because UPS defines one
    # carrier code 11). When the caller has already picked a variant — its
    # `service_name` was merged onto `options` by the gateway at booking time
    # via `selected_rate.meta` — honor that variant. Without this, the label
    # prints whichever variant the rate-sheet iterator hit first.
    options = shipment.options or {}
    requested_service_name = options.get("service_name") if isinstance(options, dict) else None
    matching = [s for s in settings.services if s.service_code == service]
    service_name = (
        next(
            (
                s.service_name
                for s in matching
                if (s.service_name or "").strip().lower() == str(requested_service_name).strip().lower()
            ),
            None,
        )
        if requested_service_name
        else None
    )
    if service_name is None:
        service_name = next((s.service_name for s in matching), service)

    for index, package in enumerate(packages, start=1):
        tracking_number = package.parcel.reference_number or str(int(uuid.uuid4().hex[:10], base=16))
        label_type = shipment.label_type or "PDF"
        label = generate_label(shipment, package, service_name, tracking_number, settings, index)
        ref = f"{package.parcel.id or index}"

        service_label = ServiceLabel(
            label=label,
            label_type=label_type,
            service_code=service,
            service_name=service_name,
            tracking_number=tracking_number,
        )

        service_labels.append((ref, service_label))

    return service_labels, messages
