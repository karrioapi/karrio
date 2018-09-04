from .datatypes import *
from .definitions import *

class Quote():
    """ manage quotes operations """

    @staticmethod
    def create(**args) -> quote_request:
        """ Create a quote request payload """
        return quote_request(**quote_request_type(**args)._asdict())

    @staticmethod
    def parse(**args) -> quote_details:
        """ create a quote details data """
        return quote_details(**args)

class Tracking():
    """ manage tracking operations """

    @staticmethod
    def create(**args) -> quote_request:
        """ Create a tracking request payload """
        return tracking_request(**args)

    @staticmethod
    def parse(**args) -> tracking_details:
        """ create a tracking details data """
        return tracking_details(**args)

class Shipment():
    """ manage shipment operations """

    @staticmethod
    def create(**args) -> shipment_request:
        """ Create a shipment details request payload """
        return shipment_request(**shipment_request_type(**args)._asdict())

    @staticmethod
    def parse(**args) -> shipment_details:
        """ create a shipment details data """
        return shipment_details(**args)






class Error():
    def __init__(self, message: str = None, code: str = None, carrier: str = None):
        self.message = message
        self.code = code
        self.carrier = carrier
