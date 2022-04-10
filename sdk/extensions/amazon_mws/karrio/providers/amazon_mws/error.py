from typing import List
from karrio.core.models import Message
from karrio.core.utils import DP
from karrio.providers.amazon_mws.utils import Settings


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    pass


def _extract_error(error: dict, settings: Settings) -> Message:
    pass
