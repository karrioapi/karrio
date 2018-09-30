from io import StringIO
from gds_helpers import export, to_xml, request as http
from purplship.mappers.caps.caps_mapper import CanadaPostMapper, CanadaPostClient
from pycaps import rating as Rate, shipment as Ship, pickuprequest as Pick
from purplship.domain.proxy import Proxy
from base64 import b64encode

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

    def get_trackings(self, tracking_pin: str) -> "XMLElement":
        """
        get_trackings currently only get one tracking_pin
        """
        return self._get_tracking(tracking_pin)

    def create_shipment(self, shipment: Ship.ShipmentType) -> "XMLElement":
        xmlStr = export(
            shipment, 
            name_='shipment',
            namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"'
        )
        mail_on_behalf = self.client.customer_number

        result = http(
            url="%s/rs/%s/%s/shipment" % (self.client.server_url, self.client.customer_number, mail_on_behalf), 
            data=bytearray(xmlStr, "utf-8"), 
            headers={
                'Content-Type': 'application/vnd.cpc.shipment-v8+xml',
                'Accept': 'application/vnd.cpc.shipment-v8+xml',
                'Authorization': "Basic %s" % self.authorization,
                'Accept-language': 'en-CA'
            }, 
            method="POST"
        )
        return to_xml(result)

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
        return to_xml(result)