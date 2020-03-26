"""PurplShip Settings base class definition"""

from abc import ABC
from dataclasses import dataclass


@dataclass
class Settings(ABC):
    """ 
    Unified API carrier Connection settings (Interface)
    """

    server_url: str
    carrier_name: str
