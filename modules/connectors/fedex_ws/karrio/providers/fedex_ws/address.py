from typing import Tuple, List
from karrio.schemas.fedex_ws.address_validation_service_v4 import (
    AddressValidationRequest as FedexAddressValidationRequest,
    AddressValidationReply,
    AddressToValidate,
    Address as FedexAddress,
    Contact,
    TransactionDetail,
    VersionId,
    NotificationSeverityType,
)
import karrio.lib as lib
from karrio.core.utils import create_envelope, Serializable, Element, SF, XP
from karrio.core.models import (
    AddressValidationRequest,
    Message,
    AddressValidationDetails,
    Address,
)
from karrio.providers.fedex_ws.utils import Settings, default_request_serializer
from karrio.providers.fedex_ws.error import parse_error_response
import karrio.lib as lib


def parse_address_validation_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> Tuple[AddressValidationDetails, List[Message]]:
    response = _response.deserialize()
    reply = XP.to_object(
        AddressValidationReply,
        lib.find_element("AddressValidationReply", response, first=True),
    )
    address: FedexAddress = next(
        (result.EffectiveAddress for result in reply.AddressResults), None
    )
    success = reply.HighestSeverity == NotificationSeverityType.SUCCESS.value
    _, lines = (
        address.StreetLines
        if address is not None and len(address.StreetLines) > 1
        else ["", ""]
    )
    validation_details = (
        AddressValidationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            complete_address=(
                Address(
                    city=address.City,
                    state_code=address.StateOrProvinceCode,
                    country_code=address.CountryCode,
                    residential=address.Residential,
                    address_line1=next(iter(address.StreetLines), None),
                    address_line2=SF.concat_str(lines, join=True),
                )
                if address is not None
                else None
            ),
        )
        if success
        else None
    )

    return validation_details, parse_error_response(response, settings)


def address_validation_request(
    payload: AddressValidationRequest, settings: Settings
) -> Serializable:
    address = lib.to_address(payload.address)

    request = create_envelope(
        body_content=FedexAddressValidationRequest(
            WebAuthenticationDetail=settings.webAuthenticationDetail,
            ClientDetail=settings.clientDetail,
            TransactionDetail=TransactionDetail(
                CustomerTransactionId="AddressValidationRequest_v4"
            ),
            Version=VersionId(ServiceId="aval", Major=4, Intermediate=0, Minor=0),
            InEffectAsOfTimestamp=None,
            AddressesToValidate=[
                AddressToValidate(
                    ClientReferenceId=None,
                    Contact=(
                        Contact(
                            ContactId=None,
                            PersonName=address.person_name,
                            Title=None,
                            CompanyName=address.company_name,
                            PhoneNumber=address.phone_number,
                            PhoneExtension=None,
                            TollFreePhoneNumber=None,
                            PagerNumber=None,
                            FaxNumber=None,
                            EMailAddress=address.email,
                        )
                        if any(
                            [
                                address.person_name,
                                address.company_name,
                                address.phone_number,
                                address.email,
                            ]
                        )
                        else None
                    ),
                    Address=FedexAddress(
                        StreetLines=lib.join(
                            address.street,
                            address.address_line2,
                        ),
                        City=address.city,
                        StateOrProvinceCode=address.city,
                        PostalCode=address.postal_code,
                        UrbanizationCode=None,
                        CountryCode=address.country_code,
                        CountryName=None,
                        Residential="" if address.residential else None,
                    ),
                )
            ],
        )
    )

    return Serializable(
        request,
        default_request_serializer(
            "v4", 'xmlns:v4="http://fedex.com/ws/addressvalidation/v4"'
        ),
    )
