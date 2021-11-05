from typing import List, Callable
from functools import reduce
from purplship.core.utils.xml import Element
from purplship.providers.dhl_express import Settings
from purplship.core.models import Message
from dhl_express_lib.dct_response_global_2_0 import ConditionType


def parse_error_response(response, settings: Settings) -> List[Message]:
    conditions = response.xpath(".//*[local-name() = $name]", name="Condition")
    return reduce(_extract_error(settings), conditions, [])


def _extract_error(
    settings: Settings,
) -> Callable[[List[Message], Element], List[Message]]:
    def extract(errors: List[Message], condition_node: Element) -> List[Message]:
        condition = ConditionType()
        condition.build(condition_node)
        return errors + [
            Message(
                code=condition.ConditionCode,
                message=condition.ConditionData,
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
            )
        ]

    return extract
