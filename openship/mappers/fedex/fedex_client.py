from ...domain.client import Client

class FedexClient(Client):

    def __init__(self, server_url, user_key, password, account_number, meter_number):
        self.server_url = server_url
        self.user_key = user_key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number