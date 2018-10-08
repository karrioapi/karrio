from .datatypes import *
from .definitions import *

class Quote:
    """ manage quotes operations """

    @staticmethod
    def create(**args) -> quote_request:
        """ Create a quote request payload """
        return quote_request(**quote_request_type(**args)._asdict())

class Tracking:
    """ manage tracking operations """

    @staticmethod
    def create(**args) -> tracking_request:
        """ Create a tracking request payload """
        return tracking_request(**args)

class Shipment:
    """ manage shipment operations """

    @staticmethod
    def create(**args) -> shipment_request:
        """ Create a shipment details request payload """
        return shipment_request(**shipment_request_type(**args)._asdict())

class Pickup:
    """ manage pickup operations """

    @staticmethod
    def request(**args) -> pickup_request:
        """ Create a pickup request payload """
        return pickup_request(**args)

    @staticmethod
    def cancellation(**args) -> pickup_cancellation_request:
        """ Create a pickup cancel request payload """
        return pickup_cancellation_request(**args)

