"""PurplShip Client base class definition"""

import attr
from abc import ABC


@attr.s(auto_attribs=True)
class Settings(ABC):
    """ 
    Unified API carrier Connection settings (Interface)
    """

    server_url: str
    carrier_name: str
