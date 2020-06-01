from typing import Tuple, List
from pydhl.routing_global_req_2_0 import (
    RouteRequest,
    RequestTypeType,
    MetaData,
)
from purplship.core.utils import Serializable, export, Element, concat_str
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.providers.dhl.units import CountryRegion
from purplship.providers.dhl.utils import Settings
from purplship.providers.dhl.error import parse_error_response


def parse_route_response(response: Element, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    validation_details = _extract_address_validation(response, settings)
    return validation_details, parse_error_response(response, settings)


def _extract_address_validation(node: Element, settings: Settings) -> AddressValidationDetails:

    return AddressValidationDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
    )


def route_request(payload: AddressValidationRequest, settings: Settings) -> Serializable[RouteRequest]:

    request = RouteRequest(
        schemaVersion=2.0,
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
        ),
        RegionCode=CountryRegion[payload.address.country_code].value,
        RequestType=RequestTypeType.D.value,
        Address1=concat_str(payload.address.address_line1),
        Address2=concat_str(payload.address.address_line2),
        Address3=None,
        PostalCode=payload.address.postal_code,
        City=payload.address.city,
        Division=None,
        CountryCode=payload.address.country_code,
        CountryName=None,
        OriginCountryCode=payload.address.country_code,
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RouteRequest) -> str:
    namespacedef_ = 'xmlns:ns1="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com routing-global-req.xsd"'

    return export(request, namespacedef_=namespacedef_)
