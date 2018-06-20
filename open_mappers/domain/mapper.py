from .client import Client
from ...domain import entities as E 

class Mapper:
    """ Unitied API to carrier API Mapper (Interface) """
    client: Client

    def create_quote_request(self, payload: E.QuoteRequest):
        """ Create carrier specific quote request xml data from  """
        raise Exception("Not Supported")

    def create_quote_response(self, res) -> Tuple[List[E.Quote], List[E.Error]]):
        """ Create united API quote result list from carrier xml response  """
        raise Exception("Not Supported")
