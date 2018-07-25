from ...domain.client import Client

class CanadaPostClient(Client):

    def __init__(self, server_url: str, username: str, password: str, customer_number: str, carrier_name: str = "CanadaPost"):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.customer_number = customer_number
        self.carrier_name = carrier_name