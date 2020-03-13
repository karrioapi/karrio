"""PurplShip Sendle rate mapper module."""

from functools import reduce
from purplship.core.models import RateRequest
from purplship.core.units import WeightUnit, Weight
from purplship.core.utils.helpers import concat_str
from pysendle.quotes import DomesticParcelQuote
from purplship.carriers.sendle.units import Plan


def domestic_quote_request(payload: RateRequest) -> DomesticParcelQuote:
    weight_unit = WeightUnit[payload.parcel.weight_unit or "KG"]
    return DomesticParcelQuote(
        pickup_suburb=concat_str(
            payload.shipper.address_line_1, payload.shipper.address_line_2,
            join=True
        ),
        pickup_postcode=payload.shipper.postal_code,
        delivery_suburb=concat_str(
            payload.recipient.address_line_1, payload.recipient.address_line_2,
            join=True
        ),
        delivery_postcode=payload.recipient.postal_code,
        kilogram_weight=str(Weight(payload.parcel.weight, weight_unit).KG),
        cubic_metre_volume=None,
        plan_name=reduce(
            lambda plan, s: Plan[s].value if s in Plan.__members__ else None,
            payload.parcel.services,
            None
        )
    )
