import unittest
from unittest.mock import patch
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from gds_helpers import to_xml, export, to_dict
from purplship.domain.Types import PickupCancellationRequest, PickupRequest, PickupUpdateRequest
from tests.dhl.fixture import proxy
from tests.utils import strip
from purplship.mappers.dhl.dhl_proxy import _reformat_time


class TestDHLPickup(unittest.TestCase):
    def setUp(self):
        self.PURequest = BookPURequest()
        self.PURequest.build(to_xml(PickupRequestXML))

        self.ModifyPURequest = ModifyPURequest()
        self.ModifyPURequest.build(to_xml(ModifyPURequestXML))

        self.CancelPURequest = CancelPURequest()
        self.CancelPURequest.build(to_xml(CancelPURequestXML))

    def test_create_pickup_request(self):
        payload = PickupRequest(**request_data)
        PURequest_ = proxy.mapper.create_pickup_request(payload)
        # remove MessageTime for testing purpose
        PURequest_.Request.ServiceHeader.MessageTime = None
        PURequest_.Place.LocationType = None
        PURequest_.Place.Address1 = None
        PURequest_.Place.PackageLocation = None
        PURequest_.Place.StateCode = None
        self.assertEqual(
            export(PURequest_).replace("dhlPickup:", ""),
            export(self.PURequest).replace("dhlPickup:", ""),
        )

    def test_create_modify_pickup_request(self):
        payload = PickupUpdateRequest(**modification_data)
        ModifyPURequest_ = proxy.mapper.modify_pickup_request(payload)
        # remove MessageTime for testing purpose
        ModifyPURequest_.Request.ServiceHeader.MessageTime = None
        ModifyPURequest_.Place.LocationType = None
        ModifyPURequest_.Place.Address1 = None
        ModifyPURequest_.Place.PackageLocation = None
        ModifyPURequest_.Place.StateCode = None
        self.assertEqual(
            export(ModifyPURequest_).replace("dhlPickup:", ""),
            export(self.ModifyPURequest).replace("dhlPickup:", ""),
        )

    def test_create_pickup_cancellation_request(self):
        payload = PickupCancellationRequest(**cancellation_data)
        CancelPURequest_ = proxy.mapper.create_pickup_cancellation_request(payload)
        # remove MessageTime for testing purpose
        CancelPURequest_.Request.ServiceHeader.MessageTime = None
        CancelPURequest_.CancelTime = None
        self.assertEqual(
            export(CancelPURequest_).replace("dhlPickup:", ""),
            export(self.CancelPURequest).replace("dhlPickup:", ""),
        )

    @patch("purplship.carriers.dhl.dhl_proxy.http", return_value="<a></a>")
    def test_request_pickup(self, http_mock):
        proxy.request_pickup(self.PURequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(
            strip(xmlStr),
            _reformat_time(
                "CloseTime", _reformat_time("ReadyByTime", strip(PickupRequestXML))
            ),
        )

    @patch("purplship.carriers.dhl.dhl_proxy.http", return_value="<a></a>")
    def test_modify_pickup(self, http_mock):
        proxy.modify_pickup(self.ModifyPURequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(
            strip(xmlStr),
            _reformat_time(
                "CloseTime", _reformat_time("ReadyByTime", strip(ModifyPURequestXML))
            ),
        )

    @patch("purplship.carriers.dhl.dhl_proxy.http", return_value="<a></a>")
    def test_cancel_pickup(self, http_mock):
        proxy.cancel_pickup(self.CancelPURequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(CancelPURequestXML))

    def test_parse_request_pickup_response(self):
        parsed_response = proxy.mapper.parse_pickup_response(to_xml(PickupResponseXML))
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupResponse))

    def test_parse_modify_pickup_response(self):
        parsed_response = proxy.mapper.parse_pickup_response(to_xml(ModifyPURequestXML))
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedModifyPUResponse))

    def test_parse_cancellation_pickup_response(self):
        parsed_response = proxy.mapper.parse_pickup_cancellation_response(
            to_xml(CancelPUResponseXML)
        )
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedCancelPUResponse))

    def test_parse_request_pickup_error(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(PickupErrorResponseXML)
        )
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupErrorResponse))


if __name__ == "__main__":
    unittest.main()

request_data = {
    "date": "2013-10-19",
    "account_number": "123456789",
    "pieces": 2,
    "weight": 20,
    "weight_unit": "L",
    "ready_time": "10:20:00",
    "closing_time": "09:20:00",
    "city": "Montreal",
    "postal_code": "H8Z2Z3",
    "person_name": "Subhayu",
    "phone_number": "4801313131",
    "state_code": "QC",
    "country_code": "CA",
    "email_address": "test@mail.com",
    "instruction": "behind the front desk",
    "address_lines": ["234 rue Hubert"],
    "extra": {"RequestorContact": {"PersonName": "Rikhil", "Phone": "23162"}},
}

modification_data = {
    "date": "2013-10-19",
    "account_number": "123456789",
    "confirmation_number": "100094",
    "ready_time": "10:20:00",
    "closing_time": "09:20:00",
    "city": "Montreal",
    "postal_code": "H8Z2Z3",
    "person_name": "Rikhil",
    "phone_number": "4801313131",
    "country_code": "CA",
    "email_address": "test@mail.com",
    "extra": {
        "RequestorContact": {"PersonName": "Rikhil", "Phone": "23162"},
        "OriginSvcArea": "KUL",
    },
}

cancellation_data = {
    "confirmation_number": "743511",
    "person_name": "Rikhil",
    "pickup_date": "2013-10-10",
    "country_code": "BR",
    "extra": {"Reason": "001"},
}

ParsedPickupResponse = [
    {
        "carrier": "carrier_name",
        "confirmation_number": "3674",
        "pickup_charge": None,
        "pickup_date": "2013-10-09",
        "ref_times": [
            {"name": "ReadyByTime", "value": "10:30"},
            {"name": "CallInTime", "value": "08:30"},
        ],
    },
    [],
]

ParsedModifyPUResponse = [
    {
        "carrier": "carrier_name",
        "confirmation_number": 100094,
        "pickup_charge": None,
        "pickup_date": None,
        "ref_times": [],
    },
    [],
]

ParsedCancelPUResponse = [{"confirmation_number": "100129"}, []]

ParsedPickupErrorResponse = [
    None,
    [
        {
            "carrier": "carrier_name",
            "code": "PU012",
            "message": " Pickup NOT scheduled.  Ready by time is passed the station cutoff time. For pickup assistance call customer service representative.",
        }
    ],
]

PickupErrorResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<res:PickupErrorResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com pickup-err-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2013-10-10T04:19:50+01:00</MessageTime>
            <MessageReference>Esteemed Courier Service of DHL</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    <Status>
        <ActionStatus>Error</ActionStatus>
        <Condition>
            <ConditionCode>PU012</ConditionCode>
            <ConditionData> Pickup NOT scheduled.  Ready by time is passed the station cutoff time. For pickup assistance call customer service representative.</ConditionData>
        </Condition>
    </Status>    
    </Response>
</res:PickupErrorResponse>
"""

CancelPURequestXML = """<req:CancelPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd" schemaVersion="2.0">
	<Request>
        <ServiceHeader>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
	    </ServiceHeader>
    </Request>
	<RegionCode>AM</RegionCode>
	<ConfirmationNumber>743511</ConfirmationNumber>
	<RequestorName>Rikhil</RequestorName>
    <CountryCode>BR</CountryCode>
	<Reason>001</Reason>
	<PickupDate>2013-10-10</PickupDate>
</req:CancelPURequest>
"""

CancelPUResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<res:CancelPUResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com pickup-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2013-08-05T18:24:33+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
	<RegionCode>EU</RegionCode>
    <Note>
        <ActionNote>Success</ActionNote>
    </Note>
    <ConfirmationNumber>100129</ConfirmationNumber>
    <OriginSvcArea>GB</OriginSvcArea>
</res:CancelPUResponse>
"""

ModifyPURequestXML = """<req:ModifyPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com modify-pickup-Global-req.xsd" schemaVersion="1.0">
    <Request>
        <ServiceHeader>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
	    </ServiceHeader>
    </Request>
    <RegionCode>AM</RegionCode>
    <ConfirmationNumber>100094</ConfirmationNumber>
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
	</Pickup>
	<PickupContact>
		<PersonName>Rikhil</PersonName>
		<Phone>4801313131</Phone>
	</PickupContact>
	<OriginSvcArea>KUL</OriginSvcArea>
</req:ModifyPURequest>
"""

ModifyPUResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<res:ModifyPUResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com pickup-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2013-07-22T15:00:41+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
	<RegionCode>AM</RegionCode>
    <Note>
        <ActionNote>Success</ActionNote>
    </Note>
    <ConfirmationNumber>100629</ConfirmationNumber>
    <NextPickupDate>2013-07-22</NextPickupDate>
    <CurrencyCode>USD</CurrencyCode>
    <OriginSvcArea>JCC</OriginSvcArea>
</res:ModifyPUResponse>
"""

PickupResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<res:BookPUResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com pickup-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2013-10-10T03:47:23+01:00</MessageTime>
            <MessageReference>Esteemed Courier Service of DHL</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
    <RegionCode>AM</RegionCode>
    <Note>
        <ActionNote>Success</ActionNote>
        <Condition>
            <ConditionCode>PU021</ConditionCode>
            <ConditionData> NOTICE!  Packages picked up after hours may
                be inspected by a DHL Courier for FAA security purposes.</ConditionData>
        </Condition>
    </Note>
    <ConfirmationNumber>3674</ConfirmationNumber>
    <ReadyByTime>10:30</ReadyByTime>
    <NextPickupDate>2013-10-09</NextPickupDate>
    <CallInTime>08:30</CallInTime>
    <OriginSvcArea>BEL</OriginSvcArea>
</res:BookPUResponse>
"""

PickupRequestXML = """<req:BookPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req.xsd" schemaVersion="1.0">
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
