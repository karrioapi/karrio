from .datatypes import *
from .definitions import *

class Quote():
    """ manage quotes operations """

    def create(**args) -> quote_request:
        """ Create a quote request payload """
        return quote_request(**quote_request_type(**args)._asdict())

    def parse(**args) -> quote_details:
        """ create a quote details data """
        return quote_details(**args)

class Party():
    """ manage party operations """

    def create(**args) -> party:
        """ create a party request payload """
        return party(**party_type(**args)._asdict())

class ShipmentDetails():
    """ manage shipment details operations """

    def create(**args) -> shipment_details:
        """ Create a shipment details request payload """
        return shipment_details(**shipment_details_type(**args)._asdict())






class Error():
    def __init__(self, message: str = None, code: str = None):
        self.message = message
        self.code = code
