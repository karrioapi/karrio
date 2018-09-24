from purplship.domain.client import Client

class UPSClient(Client):

    def __init__(self, server_url: str, username: str, password: str, account_number: str, access_license_number: str, carrier_name: str = "UPS"):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.account_number = account_number
        self.access_license_number = access_license_number
        self.carrier_name = carrier_name