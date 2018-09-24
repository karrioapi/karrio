from gds_helpers import to_xml, export, request as http
from pyups import freight_rate as Rate, package_track as Track
from pysoap.envelope import Body, Envelope, Header
from pysoap import create_envelope, clean_namespaces
from purplship.domain.proxy import Proxy
from purplship.mappers.ups.ups_mapper import UPSMapper
from purplship.mappers.ups.ups_client import UPSClient

class UPSProxy(Proxy):

    def __init__(self, client: UPSClient, mapper: UPSMapper = None):
        self.client = client
        self.mapper = UPSMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Rate.FreightRateRequest):
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=RateRequest_),
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"'
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            body_child_prefix='frt:',
            header_child_name='UPSSecurity',
            body_child_name='FreightRateRequest'
        )
        result = http(
            url='%s/FreightRate' % self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def get_trackings(self, TrackRequest_: Track.TrackRequest):
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=TrackRequest_), 
            namespacedef_='xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:trk="http://www.ups.com/XMLSchema/XOLTWS/Track/v2.0" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            body_child_prefix='trk:',
            header_child_name='UPSSecurity',
            body_child_name='TrackRequest'
        )
        result = http(
            url='%s/Track' % self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)