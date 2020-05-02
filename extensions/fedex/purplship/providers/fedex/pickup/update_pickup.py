"""
1 - get availability
2 - cancel pickup
3 - create pickup
"""
from typing import cast
from functools import partial
from purplship.core.utils import Job, Pipeline, to_xml
from purplship.core.models import PickupRequest, PickupUpdateRequest, PickupCancellationRequest
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.package.pickup.request_pickup import _create_pickup, _get_pickup_availability
from purplship.providers.fedex.package.pickup.cancel_service import cancel_pickup_request


def update_pickup_request(payload: PickupUpdateRequest, settings: Settings):
    return Pipeline(
        get_availability=lambda *_: partial(_get_pickup_availability, payload=payload)(),
        create_pickup=partial(_create_pickup, payload=cast(PickupRequest, payload), settings=settings),
        cancel_pickup=partial(_cancel_pickup_request, settings=settings)
    )


def _cancel_pickup_request(create_response: str, settings: Settings):
    response_element = to_xml(create_response)
    cancel_request = None
    return Job(
        id="cancel_pickup",
        data=cancel_pickup_request(cancel_request, settings),
        fallback=""
    )
