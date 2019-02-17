from purplship.domain.client import Client


class FedexClient(Client):
    def __init__(
        self,
        server_url: str,
        user_key: str,
        password: str,
        account_number: str,
        meter_number: str,
        carrier_name: str = "Fedex",
    ):
        self.server_url = server_url
        self.user_key = user_key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number
        self.carrier_name = carrier_name
