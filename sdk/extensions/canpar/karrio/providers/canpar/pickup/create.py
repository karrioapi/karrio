from functools import partial
from typing import Tuple, List
from karrio.schemas.canpar.CanparAddonsService import (
    schedulePickupV2,
    SchedulePickupV2Rq,
    PickupV2,
    Address,
)
import karrio.lib as lib
from karrio.core.models import PickupRequest, PickupDetails, Message
from karrio.core.utils import Element, create_envelope, Serializable, DF, XP
from karrio.core.units import Packages
from karrio.providers.canpar.error import parse_error_response
from karrio.providers.canpar.utils import Settings
from karrio.providers.canpar.units import WeightUnit


def parse_pickup_response(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> Tuple[PickupDetails, List[Message]]:
    response = _response.deserialize()
    pickup_node = lib.find_element("pickup", response, first=True)
    pickup = XP.to_object(PickupV2, pickup_node)
    details: PickupDetails = PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=str(pickup.id),
        pickup_date=DF.fdatetime(pickup.pickup_date, "%Y-%m-%dT%H:%M:%S"),
    )

    return details, parse_error_response(response, settings)


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    packages = Packages(payload.parcels)
    weight = packages.weight.value
    weight_unit = WeightUnit[packages.weight.unit].value if weight is not None else None
    address = lib.to_address(payload.address)

    request = create_envelope(
        body_content=schedulePickupV2(
            request=SchedulePickupV2Rq(
                password=settings.password,
                pickup=PickupV2(
                    collect=None,
                    comments=payload.instruction,
                    created_by=address.person_name,
                    pickup_address=Address(
                        address_line_1=address.street,
                        address_line_2=address.address_line2,
                        address_line_3=None,
                        attention=address.person_name,
                        city=address.city,
                        country=address.country_code,
                        email=address.email,
                        extension=None,
                        name=address.company_name,
                        phone=address.phone_number,
                        postal_code=address.postal_code,
                        province=address.state_code,
                        residential=address.residential,
                    ),
                    pickup_date=DF.fdatetime(
                        f"{payload.pickup_date} {payload.ready_time}",
                        "%Y-%m-%d %H:%M",
                        "%Y-%m-%dT%H:%M:%S",
                    ),
                    pickup_location=payload.package_location,
                    pickup_phone=address.phone_number,
                    shipper_num=None,
                    unit_of_measure=weight_unit,
                    weight=weight,
                ),
                user_id=settings.username,
            )
        )
    )

    return Serializable(
        request,
        partial(
            settings.serialize,
            extra_namespace='xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"',
            special_prefixes=dict(pickup_children="xsd1"),
        ),
    )
