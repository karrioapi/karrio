from .mapper import Mapper, Client

class Proxy:
    """ Unitied API carrier Proxy (Interface) """
    client: Client
    mapper: Mapper

    def get_quotes(self, xmlObj):
        """ export xmlObj as xml string and request quote from carrier  """
        raise Exception("Not Supported")

    def get_trackings(self, xmlObj):
        """ export xmlObj as xml string and request tracking from carrier  """
        raise Exception("Not Supported")

    def create_shipment(self, xmlObj):
        """ export xmlObj as xml string and request shipment creation from carrier  """
        raise Exception("Not Supported")

    def request_pickup(self, xmlObj):
        """ export xmlObj as xml string and request pickup from carrier  """
        raise Exception("Not Supported")

    def modify_pickup(self, xmlObj):
        """ export xmlObj as xml string and request pickup modification from carrier  """
        raise Exception("Not Supported")

    def cancel_pickup(self, xmlObj):
        """ export xmlObj as xml string and request pickup cancellation from carrier  """
        raise Exception("Not Supported")