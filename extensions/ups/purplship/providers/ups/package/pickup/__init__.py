from typing import cast
from functools import partial
from pyups.pickup_web_service_schema import PickupCreationResponse, RateResultType
from purplship.core.utils import Job, Pipeline, to_xml, Serializable, build
from purplship.core.models import PickupRequest, PickupUpdateRequest, PickupCancellationRequest
from purplship.providers.ups.utils import Settings
from purplship.providers.ups.package.pickup.create import create_pickup_request, parse_pickup_response
from purplship.providers.ups.package.pickup.cancel import cancel_pickup_request, parse_cancel_pickup_response
from purplship.providers.ups.package.pickup.rate import pickup_rate_request


def create_pickup_pipeline(payload: PickupRequest, settings: Settings) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - rate pickup
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        rate=lambda *_: _rate_pickup(payload=payload, settings=settings),
        create=partial(_create_pickup, payload=payload, settings=settings)
    )
    return Serializable(request)


def update_pickup_pipeline(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - rate pickup
        2 - create pickup
        3 - cancel old pickup
    :param payload: PickupUpdateRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        rate=lambda *_: _rate_pickup(payload=cast(PickupRequest, payload), settings=settings),
        create=partial(_create_pickup, payload=payload, settings=settings),
        cancel=partial(_cancel_pickup_request, payload=payload, settings=settings)
    )
    return Serializable(request)


def _rate_pickup(payload: PickupRequest, settings: Settings):
    data = pickup_rate_request(payload, settings)

    return Job(id="availability", data=data)


def _create_pickup(rate_response: str, payload: PickupRequest, settings: Settings):
    rate_result = build(RateResultType, to_xml(rate_response))
    data = create_pickup_request(payload, settings) if rate_result else None

    return Job(id="create_pickup", data=data, fallback="")


def _cancel_pickup_request(response: str, payload: PickupUpdateRequest, settings: Settings):
    reply = next(iter(to_xml(response).xpath(".//*[local-name() = $name]", name="PickupCreationResponse")), None)
    new_pickup = build(PickupCreationResponse, reply)
    data = (
        cancel_pickup_request(PickupCancellationRequest(confirmation_number=payload.confirmation_number), settings)
        if new_pickup is not None and new_pickup.PRN is not None
        else None
    )

    return Job(id="cancel_pickup", data=data, fallback="")
