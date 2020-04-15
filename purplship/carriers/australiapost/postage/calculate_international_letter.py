from purplship.core.models import RateRequest
from purplship.core.units import WeightUnit, Weight
from pyaustraliapost.international_letter_postage import ServiceRequest


def calculate_international_letter_request(payload: RateRequest) -> ServiceRequest:
    weight_unit: WeightUnit = WeightUnit[payload.parcel.weight_unit or "KG"]
    request = ServiceRequest(
        country_code=payload.recipient.country_code,
        weight=Weight(payload.parcel.weight, weight_unit).KG,
    )
    return request
