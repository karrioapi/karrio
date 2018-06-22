from xml.dom.minidom import parseString
from io import StringIO
import urllib.request
import ssl
from pyfedex import rate_v22 as Rate
from pysoap import envelope as soap
from ...domain.proxy import Proxy
from .fedex_mapper import FedexMapper
from .fedex_client import FedexClient

ctx = ssl._create_unverified_context()

class FedexProxy(Proxy):

    def __init__(self, client: FedexClient, mapper: FedexMapper = None):
        self.client = client
        self.mapper = FedexMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.RateRequest) -> Rate.RateReply:
        body = soap.Body()
        body.add_anytypeobjs_(RateRequest_)
        envelop = soap.Envelope(Body=body) 

        output = StringIO()
        envelop.export(output, 0, namespace_="SOAP-ENV:")
        xmlElt = output.getvalue(
        ).replace('tns:', ''
        ).replace('ns:', ''
        ).replace('<Body', '<SOAP-ENV:Body'
        ).replace('</Body', '</SOAP-ENV:Body'
        ).replace('<SOAP-ENV:Envelope>', '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v22">')
        output.close()
        req = urllib.request.Request(
            url=self.client.server_url, 
            data=bytearray(xmlElt, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)