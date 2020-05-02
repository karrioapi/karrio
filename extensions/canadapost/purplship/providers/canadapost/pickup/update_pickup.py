from typing import cast
from purplship.core.models import PickupUpdateRequest, PickupRequest
from purplship.core.utils import Serializable
from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.pickup.request_pickup import pickup_request


def update_pickup_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[dict]:
    request = dict(
        confirmation_number=payload.confirmation_number,
        data=pickup_request(cast(PickupRequest, payload), settings)
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: dict) -> dict:
    pickuprequest = request['confirmation_number']
    data = request['data'].serialize()
    return dict(pickuprequest=pickuprequest, data=data)
