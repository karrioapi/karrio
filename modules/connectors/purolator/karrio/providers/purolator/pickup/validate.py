from functools import partial
from typing import Union
from karrio.schemas.purolator.pickup_service_1_2_1 import (
    ValidatePickUpRequest,
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
from karrio.core.models import PickupUpdateRequest, PickupRequest
from karrio.core.utils import Serializable, create_envelope, Envelope, SF
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.providers.purolator.units import PackagePresets


def validate_pickup_request(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
) -> Serializable:
    """
    Create a serializable typed Envelope containing a ValidatePickUpRequest

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
        body_content=ValidatePickUpRequest(
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
