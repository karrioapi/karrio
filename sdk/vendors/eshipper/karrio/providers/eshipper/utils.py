import math
from typing import Optional
from karrio.core import Settings as BaseSettings
from karrio.core.utils import XP


class Settings(BaseSettings):
    """eshipper connection settings."""

    username: str
    password: str

    account_country_code: str = None

    @property
    def server_url(self):
        return (
            "http://test.eshipper.com/rpc2"
            if self.test
            else "http://web.eshipper.com/rpc2"
        )

    @property
    def carrier_name(self):
        return "eshipper"


def standard_request_serializer(request) -> str:
    return XP.export(request, namespacedef_='xmlns="http://www.eshipper.net/XMLSchema"')


def ceil(value: Optional[float]) -> Optional[int]:
    if value is None:
        return None
    return math.ceil(value)
