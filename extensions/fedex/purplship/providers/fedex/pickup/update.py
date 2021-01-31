from typing import cast
from functools import partial
from fedex_lib.pickup_service_v20 import (
    CreatePickupReply,
    NotificationSeverityType,
)
from purplship.core.utils import Job, Pipeline, XP, Serializable
from purplship.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.pickup.create import (
    _get_availability,
    _create_pickup,
    parse_pickup_response,
)
from purplship.providers.fedex.pickup.cancel import pickup_cancel_request


parse_pickup_update_response = parse_pickup_response


def pickup_update_request(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - get availability
        2 - create pickup
        3 - cancel old pickup
    :param payload: PickupUpdateRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        get_availability=lambda *_: _get_availability(
            payload=cast(PickupRequest, payload), settings=settings
        ),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
        cancel_pickup=partial(
            _cancel_pickup_request, payload=payload, settings=settings
        ),
    )
    return Serializable(request)


def _cancel_pickup_request(
    response: str, payload: PickupUpdateRequest, settings: Settings
):
    reply = next(
        iter(
            XP.to_xml(response).xpath(
                ".//*[local-name() = $name]", name="CreatePickupReply"
            )
        ),
        None,
    )
    new_pickup = XP.build(CreatePickupReply, reply)
    data = (
        pickup_cancel_request(
            PickupCancelRequest(confirmation_number=payload.confirmation_number),
            settings,
        )
        if new_pickup is not None
        and new_pickup.HighestSeverity == NotificationSeverityType.SUCCESS.value
        else None
    )

    return Job(id="cancel_pickup", data=data, fallback="")
