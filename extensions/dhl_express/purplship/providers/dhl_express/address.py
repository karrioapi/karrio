from typing import Tuple, List
from dhl_express_lib.routing_global_req_2_0 import (
    RouteRequest,
    RequestTypeType as RequestType,
    MetaData,
    Note
)
from purplship.core.units import CountryState, Country
from purplship.core.utils import Serializable, Element, SF, XP
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.providers.dhl_express.units import CountryRegion
from purplship.providers.dhl_express.utils import Settings
from purplship.providers.dhl_express.error import parse_error_response


def parse_address_validation_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    notes = response.xpath(".//*[local-name() = $name]", name="Note")
    success = next((True for note in notes if XP.build(Note, note).ActionNote == "Success"), False)
    validation_details = AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success
    )

    return validation_details, parse_error_response(response, settings)


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[RouteRequest]:
    country = (
        Country[payload.address.country_code] if payload.address.country_code is not None else None
    )
    division = (
        CountryState[country.name].value[payload.address.state_code].value if (
            country.name in CountryState.__members__ and
            payload.address.state_code in CountryState[country.name].value.__members__
        ) else None
    )

    request = RouteRequest(
        schemaVersion="2.0",
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
        ),
        RegionCode=CountryRegion[payload.address.country_code].value,
        RequestType=RequestType.D.value,
        Address1=SF.concat_str(payload.address.address_line1, join=True),
        Address2=SF.concat_str(payload.address.address_line2, join=True),
        Address3=None,
        PostalCode=payload.address.postal_code,
        City=payload.address.city,
        Division=division,
        CountryCode=country.name,
        CountryName=country.value,
        OriginCountryCode=payload.address.country_code,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RouteRequest) -> str:
    namespacedef_ = (
        'xmlns:ns1="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xsi:schemaLocation="http://www.dhl.com routing-global-req.xsd"'
    )

    return XP.export(request, namespacedef_=namespacedef_).replace('schemaVersion="2."', 'schemaVersion="2.0"')
