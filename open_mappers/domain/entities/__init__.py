from .datatypes import *
from .definitions import *

class Quotes():
    """ manage quotes operations """

    def create(**args) -> quote_request:
        """ Create a quote request payload """
        return quote_request(**quote_request_type(**args)._asdict())

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










class charge():
    def __init__(self, name: str = None, value: str = None):
        self.name = name
        self.value = value

class Error():
    def __init__(self, message: str = None, severity: str = None):
        self.message = message
        self.severity = value


class Quote():
    def __init__(self, provider: str, service_name: str, service_type: str, base_charge: float, duties_and_taxes: float, total_charge: float, discount: float = None, extra_charges: List[charge] = []):
        self.provider = provider
        self.service_name = service_name
        self.service_type = service_type
        self.base_charge = base_charge
        self.duties_and_taxes = duties_and_taxes
        self.total_charge = total_charge
        self.discount = discount
        self.extra_charges = extra_charges

    # delivery_time: str = None
    # pickup_time: str = None
    # delivery_date: str = None
    # pickup_date: str = None
    # code: str = None