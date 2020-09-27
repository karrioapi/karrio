from typing import cast
from functools import partial
from pyfedex.pickup_service_v20 import PickupAvailabilityReply, CreatePickupReply, NotificationSeverityType
from purplship.core.utils import Job, Pipeline, to_xml, Serializable, build
from purplship.core.models import PickupRequest, PickupUpdateRequest, PickupCancellationRequest
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.pickup.request import pickup_request, parse_pickup_response
from purplship.providers.fedex.pickup.cancel import cancel_pickup_request, parse_cancel_pickup_reply
from purplship.providers.fedex.pickup.availability import pickup_availability_request


def create_pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - get availability
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        get_availability=lambda *_: _get_availability(payload=payload, settings=settings),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings)
    )
    return Serializable(request)


def update_pickup_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:
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
        get_availability=lambda *_: _get_availability(payload=cast(PickupRequest, payload), settings=settings),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
        cancel_pickup=partial(_cancel_pickup_request, payload=payload, settings=settings)
    )
    return Serializable(request)


def _get_availability(payload: PickupRequest, settings: Settings):
    data = pickup_availability_request(payload, settings)

    return Job(id="availability", data=data)


def _create_pickup(availability_response: str, payload: PickupRequest, settings: Settings):
    availability = build(PickupAvailabilityReply, to_xml(availability_response))
    data = pickup_request(payload, settings) if availability else None

    return Job(id="create_pickup", data=data, fallback="")


def _cancel_pickup_request(response: str, payload: PickupUpdateRequest, settings: Settings):
    reply = next(iter(to_xml(response).xpath(".//*[local-name() = $name]", name="CreatePickupReply")), None)
    new_pickup = build(CreatePickupReply, reply)
    data = (
        cancel_pickup_request(PickupCancellationRequest(confirmation_number=payload.confirmation_number), settings)
        if new_pickup is not None and new_pickup.HighestSeverity == NotificationSeverityType.SUCCESS.value
        else None
    )

    return Job(id="cancel_pickup", data=data, fallback="")
