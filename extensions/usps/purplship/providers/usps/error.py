from typing import List
from usps_lib.error import Error
from purplship.core.utils import Element, XP
from purplship.core.models import Message
from purplship.providers.usps.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    error_nodes = (
        [response] if response.tag == 'Error' else
        response.xpath(".//*[local-name() = $name]", name="Error")
    )
    errors = [XP.build(Error, node) for node in error_nodes]

    return [
        Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=str(error.Number),
            message=error.Description,
        )
        for error in errors
    ]
