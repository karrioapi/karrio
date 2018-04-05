from .client import Client
from .mapper import Mapper

class Provider:
    name: str
    client: Client
    mapper: Mapper