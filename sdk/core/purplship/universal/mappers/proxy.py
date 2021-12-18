import attr
from typing import List, Tuple
from purplship.core.utils import (
    Serializable,
    Deserializable,
)
from purplship.core.models import (
    Message,
    RateRequest,
    ServiceLevel,
)
from sdk.core.purplship.core.models import ServiceLabel, ShipmentRequest
from sdk.core.purplship.universal.providers.utils import (
    RatingMixinSettings,
    ShippingMixinSettings,
    filter_service_level,
    generate_service_label,
)


@attr.s(auto_attribs=True)
class RatingMixinProxy:
    settings: RatingMixinSettings

    def get_rates(
        self, request: Serializable[RateRequest]
    ) -> Deserializable[Tuple[List[ServiceLevel], List[Message]]]:
        response = filter_service_level(request.serialize(), self.settings)

        return Deserializable(response)


@attr.s(auto_attribs=True)
class ShippingMixinProxy:
    settings: ShippingMixinSettings

    def create_shipment(
        self, request: Serializable[ShipmentRequest]
    ) -> Deserializable[Tuple[ServiceLabel, List[Message]]]:
        response = generate_service_label(request.serialize(), self.settings)

        return Deserializable(response)
