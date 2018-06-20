import urllib.request
import ssl
from io import StringIO
from pydhl import DCT_Response_global as Response, DCT_req_global as Request
from .dhl_mapper import DHLMapper, DHLClient
from ...domain.proxy import Proxy

ctx = ssl._create_unverified_context()

class DHLProxy(Proxy):

    def __init__(self, client: DHLClient, mapper: DHLMapper, name : str = "DHL"):
        self.name = name
        self.client = client
        self.mapper = mapper

    def get_quotes(self, DCTRequest_: Request.DCTRequest) -> Response.DCTResponse:
        output = StringIO()
        output.write('<?xml version="1.0" encoding="utf-8"?>\n')
        DCTRequest_.export(output, 0, name_='p:DCTRequest')
        xmlElt = output.getvalue().replace('<p:DCTRequest schemaVersion="1.">',
                                            '<p:DCTRequest schemaVersion="1.0" xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd ">')
        output.close()
        
        req = urllib.request.Request(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        with urllib.request.urlopen(req, context=ctx) as f:
            return Response.parseString(f.read())


def initProxy(client: DHLClient) -> DHLProxy:
    mapper = DHLMapper(client)
    return DHLProxy(client, mapper)