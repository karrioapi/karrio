from functools import partial
from typing import Union

from purplship.core.utils import Serializable, Pipeline, Job, to_xml
from purplship.core.models import PickupRequest, PickupUpdateRequest

from purplship.providers.purolator.utils import Settings
from purplship.providers.purolator.error import parse_error_response
from purplship.providers.purolator.package.pickup_service.validate_pickup import (
    validate_pickup_request,
)
from purplship.providers.purolator.package.pickup_service.void_pickup import (
    void_pickup_request,
    parse_void_pickup_reply,
)
from purplship.providers.purolator.package.pickup_service.modify_pickup import (
    modify_pickup_request,
    parse_modify_pickup_reply,
)
from purplship.providers.purolator.package.pickup_service.schedule_pickup import (
    schedule_pickup_request,
    parse_schedule_pickup_reply,
)


def schedule_pickup_pipeline(
    payload: PickupRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - validate
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        validate=lambda *_: _validate_pickup(payload=payload, settings=settings),
        schedule=partial(_schedule_pickup, payload=payload, settings=settings),
    )

    return Serializable(request)


def modify_pickup_pipeline(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Modify a pickup request
    Steps
        1 - validate
        2 - modify pickup
    :param payload: PickupUpdateRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        validate=lambda *_: _validate_pickup(payload=payload, settings=settings),
        modify=partial(_modify_pickup, payload=payload, settings=settings),
    )

    return Serializable(request)


def _validate_pickup(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
):
    data = validate_pickup_request(payload, settings)

    return Job(id="validate", data=data)


def _schedule_pickup(
    validation_response: str, payload: PickupRequest, settings: Settings
):
    errors = parse_error_response(to_xml(validation_response), settings)
    data = schedule_pickup_request(payload, settings) if len(errors) == 0 else None

    return Job(id="schedule", data=data, fallback="")


def _modify_pickup(
    validation_response: str, payload: PickupUpdateRequest, settings: Settings
):
    errors = parse_error_response(to_xml(validation_response), settings)
    data = modify_pickup_request(payload, settings) if len(errors) == 0 else None

    return Job(id="modify", data=data, fallback="")
