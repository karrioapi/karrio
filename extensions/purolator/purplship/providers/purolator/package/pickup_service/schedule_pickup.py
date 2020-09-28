from typing import Tuple, List
from functools import partial
from pypurolator.pickup_service_1_2_1 import (
    SchedulePickUpResponse,
    SchedulePickUpRequest,
    RequestContext,
    Address,
    PhoneNumber,
    PickupInstruction,
    Weight,
    WeightUnit,
    NotificationEmails
)
from purplship.core.units import Phone, Packages
from purplship.core.models import PickupUpdateRequest, PickupDetails, Message
from purplship.core.utils import (
    Serializable, create_envelope, Envelope, Element, concat_str, build
)
from purplship.providers.purolator.error import parse_error_response
from purplship.providers.purolator.utils import Settings, standard_request_serializer
from purplship.providers.purolator.units import PackagePresets


def parse_schedule_pickup_reply(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    reply = build(
        SchedulePickUpResponse,
        next(iter(response.xpath(".//*[local-name() = $name]", name="SchedulePickUpResponse")), None)
    )
    pickup = (
        _extract_pickup_details(reply, settings)
        if reply is not None and reply.PickUpConfirmationNumber is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(reply: SchedulePickUpResponse, settings: Settings) -> PickupDetails:

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=reply.PickUpConfirmationNumber,
    )


def schedule_pickup_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable[Envelope]:
    """
    schedule_pickup_request create a serializable typed Envelope containing a SchedulePickUpRequest

    Options:
        - LoadingDockAvailable
        - TrailerAccessible

    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[PickupRequest]
    """
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    phone = Phone(payload.address.phone_number)
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
                Date=payload.date,
                AnyTimeAfter="".join(payload.ready_time.split(':')),
                UntilTime="".join(payload.closing_time.split(':')),
                TotalWeight=Weight(
                    Value=packages.weight.LB,
                    WeightUnit=WeightUnit.LB.value
                ),
                TotalPieces=len(packages) or 1,
                BoxesIndicator=None,
                PickUpLocation=payload.package_location,
                AdditionalInstructions=payload.instruction,
                SupplyRequestCodes=None,
                TrailerAccessible=payload.options.get('TrailerAccessible'),
                LoadingDockAvailable=payload.options.get('LoadingDockAvailable'),
                ShipmentOnSkids=None,
                NumberOfSkids=None
            ),
            Address=Address(
                Name=payload.address.person_name or "",
                Company=payload.address.company_name,
                Department=None,
                StreetNumber="",
                StreetSuffix=None,
                StreetName=concat_str(payload.address.address_line1, join=True),
                StreetType=None,
                StreetDirection=None,
                Suite=None,
                Floor=None,
                StreetAddress2=concat_str(payload.address.address_line2, join=True),
                StreetAddress3=None,
                City=payload.address.city,
                Province=payload.address.state_code,
                Country=payload.address.country_code,
                PostalCode=payload.address.postal_code,
                PhoneNumber=PhoneNumber(
                    CountryCode=phone.country_code or "0",
                    AreaCode=phone.area_code or "0",
                    Phone=phone.phone or "0",
                    Extension=None
                ),
                FaxNumber=None,
            ),
            ShipmentSummary=None,
            NotificationEmails=NotificationEmails(
                NotificationEmail=[payload.address.email]
            )
        )
    )

    return Serializable(request, partial(standard_request_serializer, version='v1'))
