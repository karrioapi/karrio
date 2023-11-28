import math
from typing import Optional
from karrio.core import Settings as BaseSettings
from karrio.core.utils import XP


class Settings(BaseSettings):
    """Freightcom connection settings."""

    username: str
    password: str

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def server_url(self):
        return (
            "https://test.freightcom.com/rpc2"
            if self.test_mode
            else "https://app.freightcom.com/rpc2"
        )

    @property
    def carrier_name(self):
        return "freightcom"


def standard_request_serializer(element) -> str:
    return XP.export(
        element, namespacedef_='xmlns="http://www.freightcom.net/XMLSchema"'
    )


def ceil(value: Optional[float]) -> Optional[int]:
    if value is None:
        return None
    return math.ceil(value)
