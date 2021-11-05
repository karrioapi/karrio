from typing import Tuple, List, cast
from functools import partial
from purplship.core.utils import Serializable, Pipeline, Job
from purplship.core.models import (
    PickupCancelRequest,
    PickupUpdateRequest,
    PickupRequest,
    PickupDetails,
    Message
)

from purplship.providers.dicom.pickup.create import (
    _create_pickup as _create_pickup_job,
    parse_pickup_response,
    _retrieve_pickup
)
from purplship.providers.dicom.pickup.cancel import pickup_cancel_request
from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_pickup_update_response(response: dict, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    return parse_pickup_response(response, settings)


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Pipeline]:

    request: Pipeline = Pipeline(
        delete_pickup=lambda *_: _delete_pickup(payload, settings),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
        retrieve_pickup=partial(_retrieve_pickup, payload=payload, settings=settings)
    )

    return Serializable(request)


def _delete_pickup(payload: PickupUpdateRequest, settings: Settings) -> Job:
    data = pickup_cancel_request(
        settings=settings,
        payload=cast(PickupCancelRequest, payload)
    )

    return Job(id="delete_pickup", data=data)


def _create_pickup(deletion_response: str, payload: PickupUpdateRequest) -> Job:
    errors = parse_error_response(deletion_response)
    create_job: Job = (_create_pickup_job(cast(PickupRequest, payload)) if not any(errors) else None)
    data = (create_job.data if create_job is not None else None)

    return Job(id="create_pickup", data=data, fallback=("{}" if data is None else None))
