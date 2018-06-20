from ...domain.client import Client

class DHLClient(Client):

    def __init__(self, server_url: str, site_id: str, password: str, account_number: str):
        self.site_id = site_id
        self.password = password
        self.server_url = server_url
        self.account_number = account_number