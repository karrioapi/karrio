from io import StringIO
from lxml import etree
from gds_helpers import export, to_xml, request as http
from purplship.mappers.dhl.dhl_mapper import DHLMapper
from purplship.mappers.dhl.dhl_client import DHLClient
from purplship.domain.proxy import Proxy
from pydhl.DCT_req_global import DCTRequest
from pydhl.tracking_request_known import KnownTrackingRequest
from pydhl.ship_val_global_req_61 import ShipmentRequest
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest

class DHLProxy(Proxy):

    def __init__(self, client: DHLClient, mapper: DHLMapper = None):
        self.client = client
        self.mapper = DHLMapper(client) if mapper is None else mapper

    def get_quotes(self, DCTRequest_: DCTRequest) -> etree.ElementBase:
        xmlElt = export(
            DCTRequest_, 
            name_='p:DCTRequest', 
            namespacedef_='xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "'
        ).replace('schemaVersion="1."', 'schemaVersion="1.0"')

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)

    def get_trackings(self, KnownTrackingRequest_: KnownTrackingRequest) -> etree.ElementBase:
        xmlElt = export(
            KnownTrackingRequest_, 
            name_='req:KnownTrackingRequest',
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com TrackingRequestKnown.xsd"'
        )

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)

    def create_shipment(self, ShipmentRequest_: ShipmentRequest) -> etree.ElementBase:
        xmlElt = export(
            ShipmentRequest_, 
            name_='req:ShipmentRequest',
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" schemaVersion="6.1"'
        ).replace("<Image>b'", "<Image>").replace("'</Image>", "</Image>")

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)

    def request_pickup(self, PickupRequest_: BookPURequest) -> etree.ElementBase:
        xmlElt = export(
            PickupRequest_, 
            name_='req:BookPURequest',
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req.xsd"'
        ).replace("dhlPickup:", ""
        ).replace('schemaVersion="1."', 'schemaVersion="1.0"')
        
        xmlElt = _reformat_time('CloseTime', _reformat_time('ReadyByTime', xmlElt))

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)

    def modify_pickup(self, ModifyPURequest_: ModifyPURequest) -> etree.ElementBase:
        xmlElt = export(
            ModifyPURequest_, 
            name_='req:ModifyPURequest',
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com modify-pickup-Global-req.xsd"'
        ).replace("dhlPickup:", ""
        ).replace('schemaVersion="1."', 'schemaVersion="1.0"')
        
        xmlElt = _reformat_time('CloseTime', _reformat_time('ReadyByTime', xmlElt))

        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)

    def cancel_pickup(self, CancelPURequest_: CancelPURequest) -> etree.ElementBase:
        xmlElt = export(
            CancelPURequest_, 
            name_='req:CancelPURequest',
            namespacedef_='xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd" schemaVersion="2.0"'
        )
        
        result = http(url=self.client.server_url, data=bytearray(xmlElt, "utf-8"), headers={'Content-Type': 'application/xml'}, method="POST")
        return to_xml(result)
        

def _reformat_time(tag: str, xmlStr: str) -> str:
    """
    Change time format from 00:00:00 to 00:00
    """
    parts = xmlStr.split(tag)
    subs = parts[1].split(':')
    return f"{parts[0]}{tag}{subs[0]}:{subs[1]}</{tag}{parts[2]}"

