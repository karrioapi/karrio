import time
from ...domain.client import Client
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request

class DHLClient(Client):

    def __init__(self, server_url: str, site_id: str, password: str, account_number: str):
        self.site_id = site_id
        self.password = password
        self.server_url = server_url
        self.account_number = account_number

    def initRequest(self) -> Request:
        ServiceHeader_ = ServiceHeader(
            MessageReference="1234567890123456789012345678901",
            MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
            SiteID=self.site_id, 
            Password=self.password
        )
        MetaData_ = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")
        return Request(ServiceHeader=ServiceHeader_, MetaData=MetaData_)