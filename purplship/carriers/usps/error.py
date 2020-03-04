from typing import List
from pyusps.error import Error as USPSError
from purplship.core.utils.xml import Element
from purplship.core.models import Error
from purplship.carriers.usps.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    error_nodes: List[USPSError] = [
        (lambda error: (error, error.build(node)))(USPSError())[0] for node in
        ([response] if response.tag == "Error" else response.xpath(".//*[local-name() = $name]", name="Error"))
    ]
    return [
        Error(
            carrier=settings.carrier_name,
            code=str(error.Number),
            message=error.Description
        )
        for error in error_nodes
    ]
