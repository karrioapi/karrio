from io import StringIO
from typing import List, Union
from gds_helpers import export, to_xml, request as http, exec_parrallel, bundle_xml
from purplship.mappers.caps.caps_mapper import CanadaPostMapper, CanadaPostClient
from pycaps import rating as Rate, pickuprequest as Pick
from purplship.domain.proxy import Proxy
from base64 import b64encode
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType

from functools import reduce

class CanadaPostProxy(Proxy):

    def __init__(self, client: CanadaPostClient, mapper: CanadaPostMapper = None):
        self.client = client
        self.mapper = CanadaPostMapper(client) if mapper is None else mapper

        pair = "%s:%s" % (self.client.username, self.client.password)
        self.authorization = b64encode(pair.encode("utf-8")).decode('ascii')

    """ Proxy interface methods """

    def get_quotes(self, mailing_scenario: Rate.mailing_scenario) -> "XMLElement":
        xmlStr = export(
            mailing_scenario, 
            namespacedef_='xmlns="http://www.canadapost.ca/ws/ship/rate-v3"'
        )

        result = http(
            url="%s/rs/ship/price" % self.client.server_url, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={
                'Content-Type': 'application/vnd.cpc.ship.rate-v3+xml',
                'Accept': 'application/vnd.cpc.ship.rate-v3+xml',
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="POST"
        )
        return to_xml(result)

    def get_trackings(self, tracking_pins: List[str]) -> "XMLElement":
        """
        get_trackings make parrallel request for each pin
        """
        results = exec_parrallel(self._get_tracking, tracking_pins)

        return to_xml(bundle_xml(xml_strings=results))

    def create_shipment(self, shipment: Union[NonContractShipmentType, ShipmentType]) -> "XMLElement":
        is_non_contract = isinstance(shipment, NonContractShipmentType) 

        if is_non_contract:
            req_type = 'application/vnd.cpc.ncshipment-v4+xml'
            namespace = 'xmlns="http://www.canadapost.ca/ws/ncshipment-v4"'
            name = 'non-contract-shipment'
            url_ = f"{self.client.server_url}/rs/{self.client.customer_number}/ncshipment"
        else:
            req_type = 'application/vnd.cpc.shipment-v8+xml'
            namespace = 'xmlns="http://www.canadapost.ca/ws/shipment-v8"'
            name = 'shipment'
            url_ = f"{self.client.server_url}/rs/{self.client.customer_number}/{shipment.customer_request_id}/shipment"

        xmlStr = export(shipment, name_=name, namespacedef_=namespace)

        result = http(
            url=url_, 
            data=bytearray(xmlStr, "utf-8"), 
            headers={
                'Content-Type': req_type,
                'Accept': req_type,
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="POST"
        )

        response = to_xml(result)

        if any([s.text == 'create' for s in response.xpath('.//*[local-name() = $name]', name="shipment-status")]):
            results = exec_parrallel(self._get_info, [
                link for link in response.xpath('.//*[local-name() = $name]', name="link") if link.get('rel') in [
                    'price', 'receipt'
                ]
            ])
            return to_xml(bundle_xml(xml_strings=[result] + results))
        
        return response

    def request_pickup(self, pickup_request_details: Pick.PickupRequestDetailsType, method: str = "POST") -> "XMLElement":
        xmlStr = export(
            pickup_request_details, 
            name_='pickup-request-details',
            namespacedef_='xmlns="http://www.canadapost.ca/ws/pickuprequest"'
        )
        result = http(
            url="%s/enab/%s/pickuprequest" % (self.client.server_url, self.client.customer_number), 
            data=bytearray(xmlStr, "utf-8"), 
            headers={
                'Content-Type': 'application/vnd.cpc.pickuprequest+xml',
                'Accept': 'application/vnd.cpc.pickuprequest+xml',
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="POST"
        )
        return to_xml(result)

    def modify_pickup(self, pickup_request_details: Pick.PickupRequestDetailsType) -> "XMLElement":
        """
        pickup update is similar to pickup request except that it is a PUT
        """
        return self.request_pickup(pickup_request_details, "PUT")

    def cancel_pickup(self, rel: str) -> "XMLElement":
        """
        Invoke the link returned from a prior call to Get Pickup Requests where rel= “self”
        <link rel="self" .../>
        """
        result = http(
            url=rel, 
            headers={
                'Accept': 'application/vnd.cpc.pickuprequest+xml',
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="DELETE"
        )
        return to_xml(result)

    """ Canada Post Proxy interface methods """

    def _get_tracking(self, tracking_pin: str) -> "XMLElement":
        result = http(
            url="%s/vis/track/pin/%s/summary" % (self.client.server_url, tracking_pin), 
            headers={
                'Accept': 'application/vnd.cpc.track+xml',
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="GET"
        )
        return result

    def _get_info(self, link: 'XMLElement') -> str:
        href = link.get('href')
        is_ncdetails = all([(key in href) for key in ['details', 'ncshipment']])
        args = dict([
            ("url", href),
            ("headers", dict([
                    ('Accept', link.get('media-type')),
                    ('Authorization', "Basic %s" % self.authorization),
                    ('Accept-language', 'en-CA')
                ] + [('Content-Type', link.get('media-type'))] if is_ncdetails else []
            )), 
            ("method", "POST" if is_ncdetails else "GET")
        ])
        return http(**args)

