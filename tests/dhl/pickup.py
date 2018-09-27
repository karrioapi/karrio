import unittest
from unittest.mock import patch
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from gds_helpers import to_xml
from tests.dhl.fixture import proxy
from tests.utils import strip
import time


class TestDHLPickup(unittest.TestCase):
    def setUp(self):
        self.PURequest = BookPURequest()
        self.PURequest.build(to_xml(PickupRequestXML))

        self.ModifyPURequest = ModifyPURequest()
        self.ModifyPURequest.build(to_xml(ModifyPURequestXML))

        self.CancelPURequest = CancelPURequest()
        self.CancelPURequest.build(to_xml(CancelPURequestXML))

    @patch("purplship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_create_pickup_request(self, http_mock):
        proxy.request_pickup(self.PURequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(PickupRequestXML))

    @patch("purplship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_modify_pickup_request(self, http_mock):
        proxy.modify_pickup(self.ModifyPURequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ModifyPURequestXML))

    @patch("purplship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_cancel_pickup_request(self, http_mock):
        proxy.cancel_pickup(self.CancelPURequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(CancelPURequestXML))

if __name__ == '__main__':
    unittest.main()

CancelPURequestXML = """<req:CancelPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd" schemaVersion="1.">
	<Request>
        <ServiceHeader>
			<MessageTime>2001-12-19T09:30:47-05:00</MessageTime>
			<MessageReference>1234567890123456789012345678901</MessageReference>
			<SiteID>CustomerSiteID</SiteID>
            <Password>customerPassword</Password>
		</ServiceHeader>
    </Request>
	<RegionCode>AM</RegionCode>
	<ConfirmationNumber>743511</ConfirmationNumber>
	<RequestorName>Rikhil</RequestorName>
    <CountryCode>BR</CountryCode>
	<Reason>001</Reason>
	<PickupDate>2013-10-10</PickupDate>
	<CancelTime>10:20</CancelTime>
</req:CancelPURequest>
"""

ModifyPURequestXML = """<req:ModifyPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com modify-pickup-Global-req.xsd" schemaVersion="1.">
    <Request>
        <ServiceHeader>
		<MessageTime>2013-08-03T09:30:47-05:00</MessageTime>
		<MessageReference>1234567890123456789012345678901</MessageReference>
		<SiteID>CustomerSiteID</SiteID>
        <Password>customerPassword</Password>
	</ServiceHeader>
    </Request>
    <RegionCode>AP</RegionCode>
    <ConfirmationNumber>100094</ConfirmationNumber>
    <Requestor>
		<AccountType>D</AccountType>
		<AccountNumber>123456789</AccountNumber>
		<RequestorContact>
			<PersonName>Rikhil Jain</PersonName>
			<Phone>2342345322</Phone>
		</RequestorContact>
    </Requestor>
	<Place>
        <CompanyName>String</CompanyName>
        <City>Kuala Lumpur</City>
        <CountryCode>MY</CountryCode>
	    <PostalCode>2516251</PostalCode>
	</Place>
	<Pickup>
		<PickupDate>2013-08-05</PickupDate>
		<ReadyByTime>08:20</ReadyByTime>
		<CloseTime>10:20</CloseTime>
	</Pickup>
	<PickupContact>
		<PersonName>Rikhil</PersonName>
		<Phone>4801313131</Phone>
	</PickupContact>
	<OriginSvcArea>KUL</OriginSvcArea>
</req:ModifyPURequest>
"""

PickupRequestXML = """<req:BookPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req.xsd" schemaVersion="1.">
    <Request>
        <ServiceHeader>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
    </Request>
    <RegionCode>AM</RegionCode>
    <Requestor>
        <AccountType>D</AccountType>
        <AccountNumber>123456789</AccountNumber>
        <RequestorContact>
            <PersonName>Rikhil</PersonName>
            <Phone>23162</Phone>
        </RequestorContact>
    </Requestor>
    <Place>
        <City>Montreal</City>
        <CountryCode>CA</CountryCode>
        <PostalCode>H8Z2Z3</PostalCode>
    </Place>
    <Pickup>
        <PickupDate>2013-10-19</PickupDate>
        <ReadyByTime>10:20:00</ReadyByTime>
        <CloseTime>09:20:00</CloseTime>
        <Pieces>2</Pieces>
        <weight>
            <Weight>20.</Weight>
            <WeightUnit>L</WeightUnit>
        </weight>
        <SpecialInstructions>behind the front desk</SpecialInstructions>
    </Pickup>
    <PickupContact>
        <PersonName>Subhayu</PersonName>
        <Phone>4801313131</Phone>
    </PickupContact>
</req:BookPURequest>
"""
