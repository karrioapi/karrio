from .mapper import Mapper, Client

class Proxy:
    """ Unitied API carrier Proxy (Interface) """
    name: str
    client: Client
    mapper: Mapper