from typing import Tuple, List, Union
from functools import partial
from karrio.schemas.purolator.pickup_service_1_2_1 import (
    SchedulePickUpResponse,
    SchedulePickUpRequest,
    RequestContext,
    Address,
    PhoneNumber,
    PickupInstruction,
    Weight,
    WeightUnit,
    NotificationEmails,
)
import karrio.lib as lib
from karrio.core.units import Phone, Packages
from karrio.core.models import (
    PickupUpdateRequest,
    PickupRequest,
    PickupDetails,
    Message,
)
from karrio.core.utils import (
    Serializable,
    create_envelope,
    Element,
    Pipeline,
    Job,
    XP,
)
from karrio.providers.purolator.pickup.validate import validate_pickup_request
from karrio.providers.purolator.error import parse_error_response
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.providers.purolator.units import PackagePresets
import karrio.lib as lib


def parse_pickup_response(
    _response: lib.Deserializable[Element],
    settings: Settings,
) -> Tuple[PickupDetails, List[Message]]:
    response = _response.deserialize()
    reply = XP.find(
        "SchedulePickUpResponse", response, SchedulePickUpResponse, first=True
    )
    pickup = (
        _extract_pickup_details(reply, settings)
        if reply is not None and reply.PickUpConfirmationNumber is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(
    reply: SchedulePickUpResponse, settings: Settings
) -> PickupDetails:
    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=reply.PickUpConfirmationNumber,
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    """
    Create a pickup request
    Steps
        1 - validate
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable
    """
    request: Pipeline = Pipeline(
        validate=lambda *_: _validate_pickup(payload=payload, settings=settings),
        schedule=partial(_schedule_pickup, payload=payload, settings=settings),
    )

    return Serializable(request)


def _schedule_pickup_request(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
) -> Serializable:
    """
    Create a serializable typed Envelope containing a SchedulePickUpRequest

    Options:
        - LoadingDockAvailable
        - TrailerAccessible

    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable
    """
    address = lib.to_address(payload.address)
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    phone = Phone(address.phone_number, address.country_code or "CA")
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=SchedulePickUpRequest(
            BillingAccountNumber=settings.account_number,
            PartnerID=None,
            PickupInstruction=PickupInstruction(
                Date=payload.pickup_date,
                AnyTimeAfter="".join(payload.ready_time.split(":")),
                UntilTime="".join(payload.closing_time.split(":")),
                TotalWeight=Weight(
                    Value=packages.weight.LB, WeightUnit=WeightUnit.LB.value
                ),
                TotalPieces=len(packages) or 1,
                BoxesIndicator=None,
                PickUpLocation=payload.package_location,
                AdditionalInstructions=payload.instruction,
                SupplyRequestCodes=None,
                TrailerAccessible=payload.options.get("TrailerAccessible"),
                LoadingDockAvailable=payload.options.get("LoadingDockAvailable"),
                ShipmentOnSkids=None,
                NumberOfSkids=None,
            ),
            Address=Address(
                Name=address.person_name or "",
                Company=address.company_name,
                Department=None,
                StreetNumber=address.street_number or "",
                StreetSuffix=None,
                StreetName=lib.text(address.address_line1),
                StreetType=None,
                StreetDirection=None,
                Suite=None,
                Floor=None,
                StreetAddress2=lib.text(address.address_line2),
                StreetAddress3=None,
                City=address.city,
                Province=address.state_code,
                Country=address.country_code,
                PostalCode=address.postal_code,
                PhoneNumber=PhoneNumber(
                    CountryCode=phone.country_code or "0",
                    AreaCode=phone.area_code or "0",
                    Phone=phone.phone or "0",
                    Extension=None,
                ),
                FaxNumber=None,
            ),
            ShipmentSummary=None,
            NotificationEmails=NotificationEmails(NotificationEmail=[address.email]),
        ),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))


def _validate_pickup(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
):
    data = validate_pickup_request(payload, settings)

    return Job(id="validate", data=data)


def _schedule_pickup(
    validation_response: str, payload: PickupRequest, settings: Settings
):
    errors = parse_error_response(XP.to_xml(validation_response), settings)
    data = _schedule_pickup_request(payload, settings) if len(errors) == 0 else None

    return Job(id="schedule", data=data, fallback="")
