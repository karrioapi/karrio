from functools import partial
from pycanadapost.pickup import pickup_availability
from purplship.core.utils.pipeline import Job, Pipeline
from purplship.core.utils import to_xml
from purplship.core.models import PickupRequest
from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.pickup.request_pickup import pickup_request


def create_pickup_request(payload: PickupRequest, settings: Settings):
    return Pipeline(
        get_availability=lambda *_: partial(_get_pickup_availability, payload=payload)(),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings)
    )


def _create_pickup(availability_response: str, payload: PickupRequest, settings: Settings):
    availability = pickup_availability()
    node = next(
        iter(to_xml(availability_response).xpath(".//*[local-name() = $name]", name="pickup-availability")), None
    )
    if node is not None:
        availability.build(node)

    return Job(
        id="create_pickup",
        data=pickup_request(payload, settings) if availability.on_demand_tour else None,
        fallback=""
    )


def _get_pickup_availability(payload: PickupRequest):
    return Job(id="availability", data=payload.address.postal_code)
