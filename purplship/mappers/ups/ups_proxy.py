from typing import Union
from lxml import etree
from gds_helpers import to_xml, export, request as http, bundle_xml, exec_parrallel
from pysoap.envelope import Body, Envelope, Header
from pysoap import create_envelope, clean_namespaces
from purplship.domain.proxy import Proxy
from purplship.mappers.ups.ups_mapper import UPSMapper
from purplship.mappers.ups.ups_client import UPSClient
from pyups.freight_rate import FreightRateRequest
from pyups.package_rate import RateRequest
from pyups.package_track import TrackRequest
from pyups.freight_ship import FreightShipRequest
from pyups.package_ship import ShipmentRequest
from pyups.freight_pickup import FreightPickupRequest, FreightCancelPickupRequest

class UPSProxy(Proxy):

    def __init__(self, client: UPSClient, mapper: UPSMapper = None):
        self.client : UPSClient = client
        self.mapper : UPSMapper = UPSMapper(client) if mapper is None else mapper

    def get_quotes(self, RateRequest_: Union[RateRequest, FreightRateRequest]) -> etree.ElementBase:
        is_freight = isinstance(RateRequest_, FreightRateRequest)

        if is_freight:
            url_ = '%s/FreightRate' % self.client.server_url
            body_child_name_ = "FreightRateRequest"
            body_child_prefix_ = 'frt:'
            namespace_ = '''
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:wsf="http://www.ups.com/schema/wsf" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
        else:
            url_ = '%s/Rate' % self.client.server_url
            body_child_name_ = "RateRequest"
            body_child_prefix_ = 'rate:'
            namespace_ = '''
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"
            '''.replace(' ', '').replace('\n', ' ')

        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=RateRequest_),
            namespacedef_=namespace_
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            header_child_name='UPSSecurity',
            body_child_name=body_child_name_,
            body_child_prefix=body_child_prefix_
        ).replace('common:Code', 'rate:Code')
        result = http(
            url=url_, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def get_trackings(self, TrackRequests_: TrackRequest) -> etree.ElementBase:
        """
        get_trackings make parrallel request for each TrackRequest
        """
        results = exec_parrallel(self._get_tracking, TrackRequests_)

        return to_xml(bundle_xml(xml_strings=results))

    def create_shipment(self, ShipRequest_: Union[FreightShipRequest, ShipmentRequest]) -> etree.ElementBase:
        is_freight = isinstance(ShipRequest_, FreightShipRequest)

        if is_freight:
            url_ = f"{self.client.server_url}/FreightShip"
            body_child_name_ = "FreightShipRequest"
            body_child_prefix_ = 'fsp:'
            namespace_ = '''
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:wsf="http://www.ups.com/schema/wsf" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" 
                xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
        else:
            url_ = f"{self.client.server_url}/Ship"
            body_child_name_ = "Shipment"
            body_child_prefix_ = 'ship:'
            namespace_ = '''
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" 
                xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" 
                xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
            
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=ShipRequest_),
            namespacedef_=namespace_
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            body_child_prefix=body_child_prefix_,
            header_child_name='UPSSecurity',
            body_child_name=body_child_name_
        )
        result = http(
            url=url_, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def request_pickup(self, FreightPickupRequest_: FreightPickupRequest) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=FreightPickupRequest_),
            namespacedef_='''
                xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:upsa="http://www.ups.com/XMLSchema/XOLTWS/upssa/v1.0" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:wsf="http://www.ups.com/schema/wsf"
                xmlns="http://www.ups.com/XMLSchema/XOLTWS/FreightPickup/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            header_child_name='UPSSecurity',
            body_child_name='FreightPickupRequest'
        ).replace('fpu:', '')
        result = http(
            url='%s/FreightPickup' % self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)

    def cancel_pickup(self, FreightCancelPickupRequest_: FreightCancelPickupRequest) -> etree.ElementBase:
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=FreightCancelPickupRequest_),
            namespacedef_='''
                xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:upsa="http://www.ups.com/XMLSchema/XOLTWS/upssa/v1.0" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                xmlns:wsf="http://www.ups.com/schema/wsf"
                xmlns="http://www.ups.com/XMLSchema/XOLTWS/FreightPickup/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
        )
        xmlStr = clean_namespaces(
            envelopeStr, 
            envelope_prefix='tns:', 
            header_child_prefix='upss:',
            body_child_prefix='fpu:',
            header_child_name='UPSSecurity',
            body_child_name='FreightCancelPickupRequest'
        ).replace('fpu:', '')
        result = http(
            url='%s/FreightRate' % self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={'Content-Type': 'application/xml'}, 
            method="POST"
        )
        return to_xml(result)


    """ Private functions """

    def _get_tracking(self, TrackRequest_: TrackRequest):
        envelopeStr = export(
            create_envelope(header_content=self.mapper.Security, body_content=TrackRequest_), 
            namespacedef_='''
                xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                xmlns:trk="http://www.ups.com/XMLSchema/XOLTWS/Track/v2.0" 
                xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
            '''.replace(' ', '').replace('\n', ' ')
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
        return result