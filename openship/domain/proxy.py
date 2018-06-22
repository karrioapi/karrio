from .mapper import Mapper, Client

class Proxy:
    """ Unitied API carrier Proxy (Interface) """
    name: str
    client: Client
    mapper: Mapper

    def get_quotes(self, xmlObj):
        """ export xmlObj as xml string and request quote from carrier  """
        raise Exception("Not Supported")