import urllib.parse
from typing import Tuple, List
from functools import partial
from dicom_lib.pickups import (
    PickupRequest as DicomPickupRequest,
    Sender,
    Contact,
    Pickup,
)
from purplship.core.utils import Serializable, Pipeline, Job, DP, SF
from purplship.core.models import (
    PickupRequest,
    PickupDetails,
    Message
)

from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_pickup_response(response: dict, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    pickup = next(
        (Pickup(**pickup) for pickup in response.get('pickups', [])),
        None
    )
    details = (_extract_details(pickup, settings) if pickup is not None else None)

    return details, errors


def _extract_details(pickup: Pickup, settings: Settings) -> PickupDetails:

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=str(pickup.id),
        closing_time=pickup.officeClose,
        pickup_date=pickup.date,
        ready_time=pickup.ready
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:

    request: Pipeline = Pipeline(
        create_pickup=lambda *_: _create_pickup(payload),
        retrieve_pickup=partial(_retrieve_pickup, payload=payload, settings=settings)
    )

    return Serializable(request)


def _create_pickup(payload: PickupRequest) -> Job:

    request = DicomPickupRequest(
        date=payload.pickup_date,
        ready=payload.ready_time,
        category=payload.options.get("category", "Parcel"),
        officeClose=payload.closing_time,
        sender=Sender(
            city=payload.address.city,
            provinceCode=payload.address.state_code,
            postalCode=payload.address.postal_code,
            countryCode=payload.address.country_code,
            customerName=payload.address.company_name,
            streetNumber=SF.concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
            contact=Contact(
                fullName=payload.address.person_name,
                email=payload.address.email,
                telephone=payload.address.phone_number,
            )
        ),
        location=payload.options.get("dicom_location", "OT"),
        otherLocation=payload.package_location
    )

    return Job(id="create_pickup", data=Serializable(request, DP.to_dict))


def _retrieve_pickup(creation_response: str, payload: PickupRequest, settings: Settings) -> Job:
    errors = parse_error_response(DP.to_dict(creation_response), settings)
    data = (
        Serializable(
            dict(
                category=payload.options.get("category", "Parcel"),
                pickupDate=payload.pickup_date,
                streetNumber=SF.concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
                postalCode=payload.address.postal_code,
                offset=10,
            ),
            urllib.parse.urlencode
        )
        if not any(errors) else None
    )

    return Job(id="retrieve_pickup", data=data, fallback=('{}' if data is None else None))
