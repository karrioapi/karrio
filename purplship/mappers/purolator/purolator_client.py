from purplship.domain.client import Client

class PurolatorClient(Client):

    def __init__(self, server_url: str, username: str, password: str, carrier_name: str = "Purolator"):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.carrier_name = carrier_name