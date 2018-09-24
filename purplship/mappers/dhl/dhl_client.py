from purplship.domain.client import Client

class DHLClient(Client):

    def __init__(self, server_url: str, site_id: str, password: str, account_number: str, carrier_name: str = "DHL"):
        self.site_id = site_id
        self.password = password
        self.server_url = server_url
        self.account_number = account_number
        self.carrier_name = carrier_name