from functools import partial
from typing import cast
from pycanadapost.pickup import pickup_availability
from purplship.core.utils import Job, Pipeline, to_xml, Serializable, bundle_xml
from purplship.core.utils.soap import build
from purplship.core.models import PickupRequest, PickupUpdateRequest

from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.error import parse_error_response
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
        get_availability=lambda *_: _get_pickup_availability(payload),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def update_pickup_request(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[Pipeline]:
    request: Pipeline = Pipeline(
        update_pickup=lambda *_: _update_pickup(payload, settings),
        get_pickup=partial(_get_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _get_pickup_availability(payload: PickupRequest):
    return Job(id="availability", data=payload.address.postal_code)


def _create_pickup(
    availability_response: str, payload: PickupRequest, settings: Settings
):
    availability = build(pickup_availability, to_xml(availability_response))
    data = pickup_request(payload, settings) if availability.on_demand_tour else None

    return Job(id="create_pickup", data=data, fallback="" if data is None else "")


def _update_pickup(payload: PickupUpdateRequest, settings: Settings) -> Job:
    data = Serializable(dict(
        confirmation_number=payload.confirmation_number,
        data=pickup_request(cast(PickupRequest, payload), settings, update=True),
    ), _update_request_serializer)

    return Job(id="update_pickup", data=data, fallback="" if data is None else "")


def _get_pickup(update_response: str, payload: PickupUpdateRequest, settings: Settings) -> Job:
    errors = parse_error_response(to_xml(bundle_xml([update_response])), settings)
    data = None if any(errors) else f"/enab/{settings.customer_number}/pickuprequest/{payload.confirmation_number}/details"

    return Job(id="get_pickup", data=Serializable(data), fallback="" if data is None else "")


def _update_request_serializer(request: dict) -> dict:
    pickuprequest = request["confirmation_number"]
    data = request["data"].serialize()
    return dict(pickuprequest=pickuprequest, data=data)
