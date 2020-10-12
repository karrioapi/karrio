from typing import Tuple, List
from pycanpar.CanparAddonsService import (
    schedulePickupV2,
    SchedulePickupV2Rq,
    PickupV2,
    Address
)
from purplship.core.models import (
    PickupRequest,
    PickupDetails,
    Message
)
from purplship.core.utils import (
    Envelope,
    Element,
    create_envelope,
    Serializable,
    format_datetime,
    build
)
from purplship.core.units import Packages
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings, default_request_serializer
from purplship.providers.canpar.units import WeightUnit


def parse_schedule_pickup_response(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    pickup_node = next(iter(response.xpath(".//*[local-name() = $name]", name="pickup")), None)
    pickup = build(PickupV2, pickup_node)
    details: PickupDetails = PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=str(pickup.id),
        pickup_date=format_datetime(pickup.pickup_date, '%Y-%m-%dT%H:%M:%S')
    )

    return details, parse_error_response(response, settings)


def schedule_pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels)

    request = create_envelope(
        body_content=schedulePickupV2(
            request=SchedulePickupV2Rq(
                password=settings.password,
                pickup=PickupV2(
                    collect=None,
                    comments=payload.instruction,
                    created_by=payload.address.person_name,
                    pickup_address=Address(
                        address_line_1=payload.address.address_line1,
                        address_line_2=payload.address.address_line2,
                        address_line_3=None,
                        attention=payload.address.person_name,
                        city=payload.address.city,
                        country=payload.address.country_code,
                        email=payload.address.email,
                        extension=None,
                        name=payload.address.company_name,
                        phone=payload.address.phone_number,
                        postal_code=payload.address.postal_code,
                        province=payload.address.state_code,
                        residential=payload.address.residential,
                    ),
                    pickup_date=format_datetime(
                        f"{payload.date} {payload.ready_time}", '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S'
                    ),
                    pickup_location=payload.package_location,
                    pickup_phone=payload.address.phone_number,
                    shipper_num=None,
                    unit_of_measure=WeightUnit.LB.value,
                    weight=packages.weight.LB
                ),
                user_id=settings.user_id
            )
        )
    )

    return Serializable(request, default_request_serializer)
