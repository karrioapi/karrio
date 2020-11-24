from typing import cast, Tuple, List
from functools import partial
from purplship.core.utils import Job, Pipeline, Serializable, Element
from purplship.core.models import PickupRequest, PickupUpdateRequest, PickupDetails, Message

from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.pickup.create import (
    parse_pickup_response,

    _create_pickup_request,
    _get_pickup,
)


def parse_pickup_update_response(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    return parse_pickup_response(response, settings)


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:
    request: Pipeline = Pipeline(
        update_pickup=lambda *_: _update_pickup(payload, settings),
        get_pickup=partial(_get_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _update_pickup(payload: PickupUpdateRequest, settings: Settings) -> Job:
    data = Serializable(dict(
        confirmation_number=payload.confirmation_number,
        data=_create_pickup_request(cast(PickupRequest, payload), settings, update=True),
    ), _update_request_serializer)
    fallback = "" if data is None else ""

    return Job(id="update_pickup", data=data, fallback=fallback)


def _update_request_serializer(request: dict) -> dict:
    pickuprequest = request["confirmation_number"]
    data = request["data"].serialize()
    return dict(pickuprequest=pickuprequest, data=data)
