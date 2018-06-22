from io import StringIO
from gds_helpers import export, to_xml, request as http
from pydhl import DCT_Response_global as Response, DCT_req_global as Request
from .dhl_mapper import DHLMapper, DHLClient
from ...domain.proxy import Proxy

class DHLProxy(Proxy):

    def __init__(self, client: DHLClient, mapper: DHLMapper = None):
        self.client = client
        self.mapper = DHLMapper(client) if mapper is None else mapper

    def get_quotes(self, DCTRequest_: Request.DCTRequest):
        xmlElt = export(DCTRequest_, name_='p:DCTRequest', namespacedef_='schemaVersion="1.0" xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "')

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)