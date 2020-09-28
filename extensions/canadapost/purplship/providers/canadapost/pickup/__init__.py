from functools import partial
from typing import cast
from pycanadapost.pickup import pickup_availability
from purplship.core.utils import Job, Pipeline, to_xml, Serializable
from purplship.core.utils.soap import build
from purplship.core.models import PickupRequest, PickupUpdateRequest

from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.pickup.pickup_request import (
    parse_pickup_response,
    pickup_request,
)
from purplship.providers.canadapost.pickup.cancel_pickup import (
    cancel_pickup_request,
    parse_cancel_pickup_response,
)


def create_pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[Pipeline]:
    request: Pipeline = Pipeline(
        get_availability=lambda *_: partial(
            _get_pickup_availability, payload=payload
        )(),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def update_pickup_request(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[dict]:
    request = dict(
        confirmation_number=payload.confirmation_number,
        data=pickup_request(cast(PickupRequest, payload), settings, update=True),
    )
    return Serializable(request, _update_request_serializer)


def _get_pickup_availability(payload: PickupRequest):
    return Job(id="availability", data=payload.address.postal_code)


def _create_pickup(
    availability_response: str, payload: PickupRequest, settings: Settings
):
    availability = build(pickup_availability, to_xml(availability_response))

    return Job(
        id="create_pickup",
        data=pickup_request(payload, settings) if availability.on_demand_tour else None,
        fallback="",
    )


def _update_request_serializer(request: dict) -> dict:
    pickuprequest = request["confirmation_number"]
    data = request["data"].serialize()
    return dict(pickuprequest=pickuprequest, data=data)
