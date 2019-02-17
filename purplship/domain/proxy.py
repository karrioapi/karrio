from abc import ABC
from purplship.domain.client import Client
from purplship.domain.mapper import Mapper


class Proxy(ABC):
    """ 
    Unitied API carrier Proxy (Interface) 
    ...

    Attributes
    ----------
    client : Client
        a carrier client (holding connection settings)
    mapper : Mapper
        a carrier mapper for specific carrier data type mapping 
    """

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
