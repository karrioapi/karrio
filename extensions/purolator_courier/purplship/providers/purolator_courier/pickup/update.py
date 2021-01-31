from typing import Tuple, List
from functools import partial
from purolator_lib.pickup_service_1_2_1 import (
    ModifyPickupInstruction,
    ModifyPickUpRequest,
    ModifyPickUpResponse,
    RequestContext,
)
from purplship.core.models import PickupUpdateRequest, PickupDetails, Message
from purplship.core.utils import (
    Serializable, create_envelope, Envelope, Element, XP, Pipeline, Job
)
from purplship.providers.purolator_courier.pickup.create import _validate_pickup
from purplship.providers.purolator_courier.error import parse_error_response
from purplship.providers.purolator_courier.utils import Settings, standard_request_serializer


def parse_pickup_update_response(
    response: Element, settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    reply = XP.build(
        ModifyPickUpResponse,
        next(
            iter(
                response.xpath(
                    ".//*[local-name() = $name]", name="ModifyPickUpResponse"
                )
            ),
            None,
        ),
    )
    pickup = (
        _extract_pickup_details(reply, settings)
        if reply is not None and reply.PickUpConfirmationNumber is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(
    reply: ModifyPickUpResponse, settings: Settings
) -> PickupDetails:

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=reply.PickUpConfirmationNumber,
    )


def pickup_update_request(
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


def _modify_pickup_request(
    payload: PickupUpdateRequest, settings: Settings
) -> Serializable[Envelope]:
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=ModifyPickUpRequest(
            BillingAccountNumber=settings.account_number,
            ConfirmationNumber=payload.confirmation_number,
            ModifyPickupInstruction=ModifyPickupInstruction(
                UntilTime="".join(payload.closing_time.split(":")),
                PickUpLocation=payload.package_location,
                SupplyRequestCodes=None,
                TrailerAccessible=payload.options.get("TrailerAccessible"),
                LoadingDockAvailable=payload.options.get("LoadingDockAvailable"),
                ShipmentOnSkids=None,
                NumberOfSkids=None,
            ),
            ShipmentSummary=None,
        ),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))


def _modify_pickup(
    validation_response: str, payload: PickupUpdateRequest, settings: Settings
):
    errors = parse_error_response(XP.to_xml(validation_response), settings)
    data = _modify_pickup_request(payload, settings) if len(errors) == 0 else None

    return Job(id="modify", data=data, fallback="")