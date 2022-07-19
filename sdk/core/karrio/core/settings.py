"""Karrio Settings abstract class definition"""

import attr
from typing import Optional
from abc import ABC


@attr.s(auto_attribs=True)
class Settings(ABC):
    """
    Unified API carrier Connection settings (Interface)
    """

    carrier_id: str
    id: str = None
    test_mode: bool = False
    account_country_code: str = None
    metadata: dict = {}

    @property
    def server_url(self) -> Optional[str]:
        return None

    @property
    def carrier_name(self) -> Optional[str]:
        return None
