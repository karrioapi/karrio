from pyfedex.rate_v22 import WebAuthenticationCredential, WebAuthenticationDetail, ClientDetail
from ...domain.client import Client

class FedexClient(Client):

    def __init__(self, server_url, user_key, password, account_number, meter_number):
        self.server_url = server_url
        self.account_number = account_number
        self.meter_number = meter_number

        userCredential = WebAuthenticationCredential(Key=user_key, Password=password)
        self.webAuthenticationDetail = WebAuthenticationDetail(UserCredential=userCredential)
        self.clientDetail = ClientDetail(AccountNumber=self.account_number, MeterNumber=self.meter_number)