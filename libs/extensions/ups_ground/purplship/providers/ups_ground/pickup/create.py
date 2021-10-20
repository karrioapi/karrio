from typing import Tuple, List
from functools import partial
from ups_lib.freight_pickup_web_service_schema import (
    FreightPickupRequest,
    FreightPickupResponse,
)
from purplship.core.units import Packages
from purplship.core.utils import (
    Serializable,
    create_envelope,
    Envelope,
    Element,
    Job,
    Pipeline,
    NF,
    XP,
    DF,
    SF,
)
from purplship.core.models import (
    PickupRequest,
    PickupDetails,
    Message,
    ChargeDetails,
)
from purplship.providers.ups_ground.error import parse_error_response
from purplship.providers.ups_ground.units import PackagePresets
from purplship.providers.ups_ground.utils import (
    Settings,
    default_request_serializer,
)


def parse_pickup_response(
    response: Element, settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    reply = XP.find(
        "FreightPickupResponse", response, FreightPickupResponse, first=True
    )
    pickup = (
        _extract_pickup_details(response, settings)
        if reply is not None and reply.PRN is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(
    response: FreightPickupResponse, settings: Settings
) -> PickupDetails:
    pass

    # return PickupDetails(
    #     carrier_id=settings.carrier_id,
    #     carrier_name=settings.carrier_name,
    #     confirmation_number=pickup.PRN,
    #     pickup_charge=ChargeDetails(
    #         name=rate.RateType,
    #         currency=rate.CurrencyCode,
    #         amount=NF.decimal(rate.GrandTotalOfAllCharge),
    #     ),
    # )


def pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[Envelope]:
    packages = Packages(payload.parcels, PackagePresets)

    request = create_envelope(
        header_content=settings.Security, body_content=FreightPickupRequest()
    )

    return Serializable(
        request,
        default_request_serializer(
            "v11", 'xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1"'
        ),
    )