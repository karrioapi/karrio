from purplship.core.models import RateRequest, Item
from purplship.core.units import WeightUnit, Weight
from pyaups.international_parcel_postage import ServiceRequest


def calculate_international_parcel_request(payload: RateRequest) -> ServiceRequest:
    weight_unit: WeightUnit = WeightUnit[payload.shipment.weight_unit or "KG"]
    item: Item = payload.shipment.items[0]
    weight: float = item.weight or payload.shipment.total_weight
    request = ServiceRequest(
        country_code=payload.recipient.country_code,
        weight=Weight(weight, weight_unit).KG
    )
    return request
