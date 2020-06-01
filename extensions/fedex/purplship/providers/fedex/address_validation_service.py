from typing import Tuple, List
from pyfedex.address_validation_service_v4 import (
    AddressValidationRequest as FedexAddressValidationRequest,
    AddressToValidate,
    Address,
    Contact,
    TransactionDetail,
    VersionId,
)
from purplship.core.utils import Serializable, export, Element, concat_str
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.core.utils.soap import create_envelope
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    validation_details = _extract_address_validation(response, settings)
    return validation_details, parse_error_response(response, settings)


def _extract_address_validation(node: Element, settings: Settings) -> AddressValidationDetails:

    return AddressValidationDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        address=None
    )


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[FedexAddressValidationRequest]:

    request = FedexAddressValidationRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="crs", Major=26, Intermediate=0, Minor=0),
        InEffectAsOfTimestamp=None,
        AddressesToValidate=[
            AddressToValidate(
                ClientReferenceId=None,
                Contact=Contact(
                    ContactId=None,
                    PersonName=payload.address.person_name,
                    Title=None,
                    CompanyName=payload.address.company_name,
                    PhoneNumber=payload.address.phone_number,
                    PhoneExtension=None,
                    TollFreePhoneNumber=None,
                    PagerNumber=None,
                    FaxNumber=None,
                    EMailAddress=payload.address.email
                ),
                Address=Address(
                    StreetLines=concat_str(payload.address.address_line1, payload.address.address_line2),
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
    return Serializable(request, _request_serializer)


def _request_serializer(request: FedexAddressValidationRequest) -> str:
    namespacedef_ = ''

    return export(
        create_envelope(body_content=request),
        namespacedef_=namespacedef_
    )
