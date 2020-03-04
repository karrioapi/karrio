"""PurplShip Sendle rate mapper module."""

from functools import reduce
from purplship.core.models import RateRequest
from pysendle.quotes import InternationalParcelQuote
from purplship.carriers.sendle.units import Plan


def international_quote_request(payload: RateRequest) -> InternationalParcelQuote:
    return InternationalParcelQuote(
        pickup_suburb=" ".join(payload.shipper.address_lines),
        pickup_postcode=payload.shipper.postal_code,
        delivery_country=payload.recipient.country_code,
        kilogram_weight=str(payload.shipment.total_weight or payload.shipment.items[0].weight),
        cubic_metre_volume=None,
        plan_name=reduce(
            lambda plan, s: Plan[s].value if s in Plan.__members__ else None,
            payload.shipment.services,
            None
        )
    )
