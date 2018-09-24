from gds_helpers import to_xml, export, request as http
from pyfedex import rate_v22 as Rate, track_service_v14 as Track
from pysoap.envelope import Body, Envelope
from pysoap import create_envelope, clean_namespaces
from purplship.domain.proxy import Proxy
from purplship.mappers.fedex.fedex_mapper import FedexMapper
from purplship.mappers.fedex.fedex_client import FedexClient

class FedexProxy(Proxy):

    def __init__(self, client: FedexClient, mapper: FedexMapper = None):
        self.client = client
        self.mapper = FedexMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.RateRequest):
        envelopeStr = export( 
            create_envelope(body_content=RateRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://fedex.com/ws/rate/v22"'
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:',
            body_child_prefix='ns:',
            body_child_name='RateRequest'
        )

        result = http(
            url=self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def get_trackings(self, TrackRequest_: Track.TrackRequest):
        envelopeStr = export( 
            create_envelope(body_content=TrackRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/track/v14"'
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            body_child_prefix='ns:',
            body_child_name='TrackRequest'
        )
        result = http(
            url=self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)
