from gds_helpers import to_xml, export, request as http
from pyfedex import rate_v22 as Rate, track_service_v14 as Track
from pysoap.envelope import Body, Envelope
from ...domain.proxy import Proxy
from .fedex_mapper import FedexMapper
from .fedex_client import FedexClient

class FedexProxy(Proxy):

    def __init__(self, client: FedexClient, mapper: FedexMapper = None):
        self.client = client
        self.mapper = FedexMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.RateRequest):
        envelope_ = _create_envelope(body_content=RateRequest_)
        xmlStr = _export_envolope(
            envelope_, 
            envelope_prefix='SOAP-ENV:', 
            child_name='RateRequest',
            namespacedef_='xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v22"'
        )
        result = http(
            url=self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def get_trackings(self, TrackRequest_: Track.TrackRequest):
        envelope_ = _create_envelope(body_content=TrackRequest_)
        xmlStr = _export_envolope(
            envelope_, 
            envelope_prefix='soapenv:', 
            child_name='TrackRequest', 
            child_prefix='v14:',
            namespacedef_='xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14"'
        )
        result = http(
            url=self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)






def _create_envelope(body_content):
    body = Body()
    body.add_anytypeobjs_(body_content)
    return Envelope(Body=body) 

def _export_envolope(envelope, envelope_prefix, child_name, child_prefix = '', **args):
    return export(
        envelope, 
        **args
    ).replace('<tns:', '<%s' % envelope_prefix
    ).replace('</tns:', '</%s' % envelope_prefix
    ).replace('<ns:', '<%s' % child_prefix
    ).replace('</ns:', '</%s' % child_prefix
    ).replace('<%s%s' % (envelope_prefix, child_name), '<%s%s' % (child_prefix, child_name)
    ).replace('</%s%s' % (envelope_prefix, child_name), '</%s%s' % (child_prefix, child_name))