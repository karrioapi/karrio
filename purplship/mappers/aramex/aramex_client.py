from purplship.domain.client import Client

class AramexClient(Client):

    def __init__(self, server_url: str, username: str, password: str, account_number: str, account_pin: str, carrier_name: str = "Aramex"):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.account_pin = account_pin
        self.carrier_name = carrier_name
        self.account_number = account_number