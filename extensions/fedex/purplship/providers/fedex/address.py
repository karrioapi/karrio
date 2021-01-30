from typing import Tuple, List
from fedex_lib.address_validation_service_v4 import (
    AddressValidationRequest as FedexAddressValidationRequest,
    AddressValidationReply,
    AddressToValidate,
    Address as FedexAddress,
    Contact,
    TransactionDetail,
    VersionId,
    NotificationSeverityType,
)
from purplship.core.utils import create_envelope, Serializable, Element, Envelope, SF, XP
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails, Address
from purplship.providers.fedex.utils import Settings, default_request_serializer
from purplship.providers.fedex.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    reply = XP.build(
        AddressValidationReply,
        next(iter(response.xpath(".//*[local-name() = $name]", name="AddressValidationReply")), None)
    )
    address: FedexAddress = next((result.EffectiveAddress for result in reply.AddressResults), None)
    success = reply.HighestSeverity == NotificationSeverityType.SUCCESS.value
    _, lines = (
        address.StreetLines if address is not None and len(address.StreetLines) > 1 else ["", ""]
    )
    validation_details = AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        complete_address=Address(
            city=address.City,
            state_code=address.StateOrProvinceCode,
            country_code=address.CountryCode,
            residential=address.Residential,
            address_line1=next(iter(address.StreetLines), None),
            address_line2=SF.concat_str(lines, join=True)
        ) if address is not None else None
    ) if success else None

    return validation_details, parse_error_response(response, settings)


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[Envelope]:
    contact = dict(
        PersonName=payload.address.person_name,
        CompanyName=payload.address.company_name,
        PhoneNumber=payload.address.phone_number,
        EMailAddress=payload.address.email
    )

    request = create_envelope(
        body_content=FedexAddressValidationRequest(
            WebAuthenticationDetail=settings.webAuthenticationDetail,
            ClientDetail=settings.clientDetail,
            TransactionDetail=TransactionDetail(CustomerTransactionId="AddressValidationRequest_v4"),
            Version=VersionId(ServiceId="aval", Major=4, Intermediate=0, Minor=0),
            InEffectAsOfTimestamp=None,
            AddressesToValidate=[
                AddressToValidate(
                    ClientReferenceId=None,
                    Contact=Contact(
                        ContactId=None,
                        PersonName=contact['person_name'],
                        Title=None,
                        CompanyName=contact['company_name'],
                        PhoneNumber=contact['phone_number'],
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=contact['email']
                    ) if any(contact.values()) else None,
                    Address=FedexAddress(
                        StreetLines=SF.concat_str(payload.address.address_line1, payload.address.address_line2),
                        City=payload.address.city,
                        StateOrProvinceCode=payload.address.city,
                        PostalCode=payload.address.postal_code,
                        UrbanizationCode=None,
                        CountryCode=payload.address.country_code,
                        CountryName=None,
                        Residential="" if payload.address.residential else None,
                    ),
                )
            ],
        )
    )

    return Serializable(
        request,
        default_request_serializer('v4', 'xmlns:v4="http://fedex.com/ws/addressvalidation/v4"')
    )

