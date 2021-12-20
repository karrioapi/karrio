import attr
from typing import List, Tuple
from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.core.models import (
    Message,
)
from purplship.core.models import ServiceLabel, ShipmentRequest
from purplship.universal.providers.shipping import (
    ShippingMixinSettings,
)


@attr.s(auto_attribs=True)
class ShippingMixinProxy:
    settings: ShippingMixinSettings

    def create_shipment(
        self, request: Serializable[ShipmentRequest]
    ) -> Deserializable[Tuple[ServiceLabel, List[Message]]]:
        response = generate_service_label(request.serialize(), self.settings)

        return Deserializable(response)


def generate_service_label(
    request: ShipmentRequest, settings: ShippingMixinSettings
) -> Tuple[ServiceLabel, List[Message]]:

    messages: List[Message] = []
    service_label = ServiceLabel(
        label="",
        label_type="",
        tracking_number="",
    )

    return service_label, messages
