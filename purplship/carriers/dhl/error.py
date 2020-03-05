from typing import List, Callable
from functools import reduce
from purplship.core.utils.xml import Element
from purplship.core import Settings
from purplship.core.models import Error
from pydhl.dct_response_global_2_0 import ConditionType


def parse_error_response(response, settings: Settings) -> List[Error]:
    conditions = response.xpath(".//*[local-name() = $name]", name="Condition")
    return reduce(_extract_error(settings), conditions, [])


def _extract_error(settings: Settings) -> Callable[[List[Error], Element], List[Error]]:
    def extract(errors: List[Error], condition_node: Element) -> List[Error]:
        condition = ConditionType()
        condition.build(condition_node)
        return errors + [
            Error(
                code=condition.ConditionCode,
                message=condition.ConditionData,
                carrier=settings.carrier_name,
            )
        ]
    return extract
