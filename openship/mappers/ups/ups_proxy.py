from gds_helpers import to_xml, export, request as http
from pyups import freight_rate as Rate, package_track as Track
from pysoap.envelope import Body, Envelope, Header
from pysoap import create_envelope, clean_namespaces
from ...domain.proxy import Proxy
from .ups_mapper import UPSMapper
from .ups_client import UPSClient

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






def _create_envelope(body_content, header_content = None) -> Envelope:
    body = Body()
    header = None
    if header_content is not None: 
        header = Header()
        header.add_anytypeobjs_(header_content)
    body.add_anytypeobjs_(body_content)

    return Envelope(
        Header=header,
        Body=body
    ) 

def _export_envolope(envelope, envelope_prefix, body_child_name, header_child_name = '', header_child_prefix = '', body_child_prefix = '', **args):
    return export(
        envelope, 
        **args
    ).replace('<%s%s' % (envelope_prefix, header_child_name), '<%s%s' % (header_child_prefix, header_child_name)
    ).replace('</%s%s' % (envelope_prefix, header_child_name), '</%s%s' % (header_child_prefix, header_child_name)
    ).replace('<%s%s' % (envelope_prefix, body_child_name), '<%s%s' % (body_child_prefix, body_child_name)
    ).replace('</%s%s' % (envelope_prefix, body_child_name), '</%s%s' % (body_child_prefix, body_child_name))