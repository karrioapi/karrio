"""PurplShip Sendle rate mapper module."""

from functools import reduce
from purplship.core.models import RateRequest
from pysendle.quotes import DomesticParcelQuote
from purplship.carriers.sendle.units import Plan


def domestic_quote_request(payload: RateRequest) -> DomesticParcelQuote:
    return DomesticParcelQuote(
        pickup_suburb=" ".join(payload.shipper.address_lines),
        pickup_postcode=payload.shipper.postal_code,
        delivery_suburb=" ".join(payload.recipient.address_lines),
        delivery_postcode=payload.recipient.postal_code,
        kilogram_weight=str(payload.shipment.total_weight or payload.shipment.items[0].weight),
        cubic_metre_volume=(
            payload.shipment.extra.get('cubic_metre_volume') or
            payload.shipment.items[0].extra.get('cubic_metre_volume')
        ),
        plan_name=reduce(
            lambda plan, s: Plan[s].value if s in Plan.__members__ else None,
            payload.shipment.services,
            None
        )
    )
