from typing import Optional
from functools import partial
from karrio.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest
)
from karrio.core.utils import (
    Pipeline,
    Job,
    Serializable,
    XP
)
from karrio.providers.canpar.utils import Settings
from karrio.providers.canpar.error import parse_error_response
from karrio.providers.canpar.pickup.cancel import pickup_cancel_request
from karrio.providers.canpar.pickup.create import pickup_request, parse_pickup_response

parse_pickup_update_response = parse_pickup_response


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:
    """
    Modify a pickup request
    Steps
        1 - cancel former pickup
        2 - create a new one
    :param payload: PickupUpdateRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        cancel=lambda *_: _cancel_pickup(payload, settings),
        schedule=partial(_create_pickup, payload=payload, settings=settings)
    )

    return Serializable(request)


def _cancel_pickup(payload: PickupUpdateRequest, settings: Settings) -> Job:
    data = PickupCancelRequest(
        confirmation_number=payload.confirmation_number,
        address=payload.address,
        pickup_date=payload.pickup_date,
        reason='change pickup',
    )

    return Job(id='cancel', data=pickup_cancel_request(data, settings))


def _create_pickup(cancel_response: str, payload: PickupUpdateRequest, settings: Settings) -> Job:
    errors = parse_error_response(XP.to_xml(cancel_response), settings)
    canceled = len(errors) == 0
    data: Optional[PickupRequest] = (
        pickup_request(payload, settings) if canceled else None
    )
    fallback: Optional[str] = None if canceled else ''

    return Job(id='schedule', data=data, fallback=fallback)
