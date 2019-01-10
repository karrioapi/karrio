from .datatypes import *
from .factories import *

class Quote:
    """ manage quotes operations """

    @staticmethod
    def create(shipper: dict, recipient: dict, shipment: dict) -> shipment_request:
        """ Create a quote request payload """
        return shipment_request(
            shipper=party(**shipper),
            recipient=party(**recipient), 
            shipment=create_shipment_options_type(**shipment)
        )

class Tracking:
    """ manage tracking operations """

    @staticmethod
    def create(**args) -> tracking_request:
        """ Create a tracking request payload """
        return tracking_request(**args)

class Shipment:
    """ manage shipment operations """

    @staticmethod
    def create(shipper: Dict, recipient: Dict, shipment: Dict) -> shipment_request:
        """ Create a shipment details request payload """
        return shipment_request(
            shipper=party(**shipper),
            recipient=party(**recipient), 
            shipment=create_shipment_options_type(**shipment)
        )

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

