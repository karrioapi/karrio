import attr
from typing import List, Tuple
from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.core.units import Packages, Options
from purplship.core.models import (
    Message,
)
from purplship.core.models import ServiceLabel, ShipmentRequest
from purplship.universal.providers.shipping import (
    ShippingMixinSettings,
)
from purplship.core.utils.label import generate_label


@attr.s(auto_attribs=True)
class ShippingMixinProxy:
    settings: ShippingMixinSettings

    def create_shipment(
        self, request: Serializable[ShipmentRequest]
    ) -> Deserializable[Tuple[List[Tuple[str, ServiceLabel]], List[Message]]]:
        response = generate_service_label(request.serialize(), self.settings)

        return Deserializable(response)


def generate_service_label(
    request: ShipmentRequest, settings: ShippingMixinSettings
) -> Tuple[List[Tuple[str, ServiceLabel]], List[Message]]:
    messages: List[Message] = []
    service_labels: List[Tuple[str, ServiceLabel]] = []

    packages = Packages(request.parcels)
    options = Options(request.options)
    service = request.service
    service_name = next(
        (s.service_name for s in settings.services if s.service_code == service),
        service,
    )
    label_type = request.label_type or "PDF"

    for index, package in enumerate(packages, start=1):
        label = generate_label(request, package, settings.label_template)
        ref = f"{package.parcel.id or index}"
        service_label = ServiceLabel(
            label=label,
            label_type=label_type,
            service_code=service,
            service_name=service_name,
            tracking_number=options.generic_tracking_number_reference,
        )

        service_labels.append((ref, service_label))

    return service_labels, messages
