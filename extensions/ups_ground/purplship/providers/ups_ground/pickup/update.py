from functools import partial
from ups_lib.pickup_web_service_schema import PickupCreationResponse
from purplship.core.utils import Job, Pipeline, XP, Serializable
from purplship.core.models import (
    PickupUpdateRequest,
    PickupCancelRequest,
)
from purplship.providers.ups_ground.utils import Settings
from purplship.providers.ups_ground.pickup.create import (
    pickup_request,
    parse_pickup_response,
)
from purplship.providers.ups_ground.pickup.cancel import pickup_cancel_request

parse_pickup_update_response = parse_pickup_response


def pickup_update_request(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - create pickup
        2 - cancel old pickup
    :param payload: PickupUpdateRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        rate=lambda *_: pickup_request(payload=payload, settings=settings),
        cancel=partial(_cancel_pickup_request, payload=payload, settings=settings),
    )
    return Serializable(request)


def _cancel_pickup_request(
    response: str, payload: PickupUpdateRequest, settings: Settings
):
    new_pickup = XP.find(
        "PickupCreationResponse",
        XP.to_xml(response),
        PickupCreationResponse,
        first=True,
    )
    data = (
        pickup_cancel_request(
            PickupCancelRequest(confirmation_number=payload.confirmation_number),
            settings,
        )
        if new_pickup is not None and new_pickup.PRN is not None
        else None
    )

    return Job(id="cancel_pickup", data=data, fallback="")
