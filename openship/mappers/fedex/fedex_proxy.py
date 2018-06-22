from gds_helpers import to_xml, export, request as http
from pyfedex import rate_v22 as Rate
from pysoap.envelope import Body, Envelope
from ...domain.proxy import Proxy
from .fedex_mapper import FedexMapper
from .fedex_client import FedexClient

class FedexProxy(Proxy):

    def __init__(self, client: FedexClient, mapper: FedexMapper = None):
        self.client = client
        self.mapper = FedexMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.RateRequest):
        body = Body()
        body.add_anytypeobjs_(RateRequest_)
        envelop = Envelope(Body=body) 

        xmlElt = export(envelop, name_="SOAP-ENV:Envelope", namespacedef_='xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v22"')
        xmlElt = xmlElt.replace('<tns:', '<'
        ).replace('</tns:', '</'
        ).replace('<ns:', '<'
        ).replace('</ns:', '</'
        ).replace('<Body', '<SOAP-ENV:Body'
        ).replace('</Body', '</SOAP-ENV:Body')

        result = http(
            url=self.client.server_url, 
            data=bytearray(xmlElt, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)