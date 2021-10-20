from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import AddressValidationRequest, Message, AddressValidationDetails
from purplship.providers.carrier.utils import Settings
from purplship.providers.carrier.error import parse_error_response


def parse_address_validation_response(response, settings: Settings) -> Tuple[AddressValidationDetails, List[Message]]:
    successful = True  # retrieve success status from `response`
    validation_details = AddressValidationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=successful
    ) if successful else None

    return validation_details, parse_error_response(response, settings)


def address_validation_request(payload: AddressValidationRequest, settings: Settings) -> Serializable['CarrierAddressValidationRequest']:

    # request = CarrierAddressValidationRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierAddressValidationRequest') -> str:
    pass
