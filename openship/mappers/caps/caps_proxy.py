from io import StringIO
from gds_helpers import export, to_xml, request as http
from .caps_mapper import CanadaPostMapper, CanadaPostClient
from pycaps import rating as Rate, track as Track
from ...domain.proxy import Proxy
from base64 import b64encode

class CanadaPostProxy(Proxy):

    def __init__(self, client: CanadaPostClient, mapper: CanadaPostMapper = None):
        self.client = client
        self.mapper = CanadaPostMapper(client) if mapper is None else mapper

        pair = "%s:%s" % (self.client.username, self.client.password)
        self.authorization = b64encode(pair.encode("utf-8")) 

    def get_quotes(self, mailing_scenario: Rate.mailing_scenario):
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

    def get_trackings(self, tracking_pin: str):
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