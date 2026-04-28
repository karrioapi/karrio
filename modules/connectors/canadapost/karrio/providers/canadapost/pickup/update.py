from functools import partial
from typing import cast

import karrio.lib as lib
from karrio.core.models import (
    Message,
    PickupDetails,
    PickupRequest,
    PickupUpdateRequest,
)
from karrio.core.utils import Element, Job, Pipeline, Serializable
from karrio.providers.canadapost.pickup.create import (
    _create_pickup_request,
    _get_pickup,
    parse_pickup_response,
)
from karrio.providers.canadapost.utils import Settings


def parse_pickup_update_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> tuple[PickupDetails, list[Message]]:
    response = _response.deserialize()
    return parse_pickup_response(response, settings)


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable:
    request: Pipeline = Pipeline(
        update_pickup=lambda *_: _update_pickup(payload, settings),
        get_pickup=partial(_get_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _update_pickup(payload: PickupUpdateRequest, settings: Settings) -> Job:
    data = Serializable(
        dict(
            confirmation_number=payload.confirmation_number,
            data=_create_pickup_request(cast(PickupRequest, payload), settings, update=True),
        ),
        _update_request_serializer,
    )
    fallback = "" if data is None else ""

    return Job(id="update_pickup", data=data, fallback=fallback)


def _update_request_serializer(request: dict) -> dict:
    pickuprequest = request["confirmation_number"]
    data = request["data"].serialize()
    return dict(pickuprequest=pickuprequest, data=data)
