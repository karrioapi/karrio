from purplship.core.models import RateRequest
from purplship.core.units import Dimension, WeightUnit, DimensionUnit, Weight
from pyaustraliapost.domestic_parcel_postage import ServiceRequest


def calculate_domestic_parcel_request(payload: RateRequest) -> ServiceRequest:
    weight_unit: WeightUnit = WeightUnit[payload.parcel.weight_unit or "KG"]
    dimension_unit: DimensionUnit = DimensionUnit[payload.parcel.dimension_unit or "CM"]
    request = ServiceRequest(
        from_postcode=payload.shipper.postal_code,
        to_postcode=payload.recipient.postal_code,
        length=Dimension(payload.parcel.length, dimension_unit).CM,
        width=Dimension(payload.parcel.width, dimension_unit).CM,
        height=Dimension(payload.parcel.height, dimension_unit).CM,
        weight=Weight(payload.parcel.weight, weight_unit).KG,
    )
    return request
