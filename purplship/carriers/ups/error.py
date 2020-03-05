from typing import List, Callable
from functools import reduce
from pyups.error_1_1 import CodeType
from purplship.core.models import Error
from purplship.core.utils.xml import Element
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    notifications = response.xpath(".//*[local-name() = $name]", name="PrimaryErrorCode")
    return reduce(_extract_error(settings), notifications, [])


def _extract_error(settings: Settings) -> Callable[[List[Error], Element], Element]:
    def extract(errors: List[Error], error_ode: Element) -> List[Error]:
        error = CodeType()
        error.build(error_ode)
        return errors + [
            Error(
                code=error.Code,
                message=error.Description,
                carrier=settings.carrier_name,
            )
        ]

    return extract
