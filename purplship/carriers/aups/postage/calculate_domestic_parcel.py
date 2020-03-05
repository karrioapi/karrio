from purplship.core.models import RateRequest, Item
from purplship.core.units import Dimension, WeightUnit, DimensionUnit, Weight
from pyaups.domestic_parcel_postage import ServiceRequest


def calculate_domestic_parcel_request(payload: RateRequest) -> ServiceRequest:
    weight_unit: WeightUnit = WeightUnit[payload.shipment.weight_unit or "KG"]
    dimension_unit: DimensionUnit = DimensionUnit[payload.shipment.dimension_unit or "CM"]
    item: Item = payload.shipment.items[0]
    request = ServiceRequest(
        from_postcode=payload.shipper.postal_code,
        to_postcode=payload.recipient.postal_code,
        length=Dimension(item.length, dimension_unit).CM,
        width=Dimension(item.width, dimension_unit).CM,
        height=Dimension(item.height, dimension_unit).CM,
        weight=Weight(item.weight or payload.shipment.total_weight, weight_unit).KG,
    )
    return request
