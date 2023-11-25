import re
import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import (
    PickupCancelRequest,
    PickupRequest,
    PickupUpdateRequest,
)
from karrio import Pickup
from .fixture import gateway


class TestDHLPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.BookPURequest = PickupRequest(**book_pickup_payload)
        self.ModifyPURequest = PickupUpdateRequest(**modification_data)
        self.CancelPURequest = PickupCancelRequest(**cancellation_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.BookPURequest)
        # remove MessageTime for testing purpose
        serialized_request = re.sub(
            "            <MessageTime>[^>]+</MessageTime>", "", request.serialize()
        )

        self.assertEqual(serialized_request, PickupRequestXML)

    def test_create_modify_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.ModifyPURequest)
        # remove MessageTime for testing purpose
        serialized_request = re.sub(
            "            <MessageTime>[^>]+</MessageTime>", "", request.serialize()
        )

        self.assertEqual(serialized_request, ModifyPURequestXML)

    def test_create_pickup_cancellation_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.CancelPURequest)
        # remove MessageTime for testing purpose
        serialized_request = re.sub(
            "            <MessageTime>[^>]+</MessageTime>",
            "",
            re.sub("    <CancelTime>[^>]+</CancelTime>", "", request.serialize()),
        )

        self.assertEqual(serialized_request, CancelPURequestXML)

    def test_parse_request_pickup_response(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = PickupResponseXML
            parsed_response = Pickup.schedule(self.BookPURequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupResponse)
            )

    def test_parse_modify_pickup_response(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = ModifyPURequestXML
            parsed_response = Pickup.update(self.ModifyPURequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedModifyPUResponse)
            )

    def test_parse_cancellation_pickup_response(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = CancelPUResponseXML
            parsed_response = Pickup.cancel(self.CancelPURequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedCancelPUResponse)
            )

    def test_parse_request_pickup_error(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = PickupErrorResponseXML
            parsed_response = Pickup.schedule(self.BookPURequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

book_pickup_payload = {
    "pickup_date": "2013-10-19",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "instruction": "behind the front desk",
    "address": {
        "city": "Montreal",
        "postal_code": "H8Z2Z3",
        "person_name": "Subhayu",
        "phone_number": "4801313131",
        "state_code": "QC",
        "country_code": "CA",
        "email": "test@mail.com",
        "address_line1": "234 rue Hubert",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
}

modification_data = {
    "pickup_date": "2013-10-19",
    "confirmation_number": "100094",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "address": {
        "city": "Montreal",
        "postal_code": "H8Z2Z3",
        "person_name": "Rikhil",
        "phone_number": "4801313131",
        "country_code": "CA",
        "email": "test@mail.com",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
}

cancellation_data = {
    "confirmation_number": "743511",
    "pickup_date": "2013-10-10",
    "address": {
        "person_name": "Rikhil",
        "country_code": "BR",
    },
}

ParsedPickupResponse = [
    {
        "carrier_name": "dhl_express",
        "carrier_id": "carrier_id",
        "confirmation_number": "3674",
        "pickup_date": "2013-10-09",
        "closing_time": "08:30",
        "ready_time": "10:30",
    },
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "PU021",
            "message": " NOTICE!  Packages picked up after hours may\n                be inspected by a DHL Courier for FAA security purposes.",
        }
    ],
]


ParsedModifyPUResponse = [
    {
        "carrier_name": "dhl_express",
        "carrier_id": "carrier_id",
        "confirmation_number": "100094",
        "pickup_charge": None,
        "pickup_date": None,
        "ref_times": [],
    },
    [],
]

ParsedCancelPUResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "dhl_express",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]

ParsedPickupErrorResponse = [
    None,
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
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

CancelPURequestXML = """<req:CancelPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com cancel-pickup-global-req.xsd" schemaVersion="3.0">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>XMLPI</SoftwareName>
            <SoftwareVersion>1.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <ConfirmationNumber>743511</ConfirmationNumber>
    <RequestorName>Rikhil</RequestorName>
    <CountryCode>BR</CountryCode>
    <Reason>006</Reason>
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

ModifyPURequestXML = """<req:ModifyPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com modify-pickup-Global-req.xsd" schemaVersion="3.0">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>XMLPI</SoftwareName>
            <SoftwareVersion>1.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <ConfirmationNumber>100094</ConfirmationNumber>
    <Requestor>
        <AccountType>D</AccountType>
        <AccountNumber>123456789</AccountNumber>
        <RequestorContact>
            <PersonName>Rikhil</PersonName>
            <Phone>4801313131</Phone>
        </RequestorContact>
    </Requestor>
    <Place>
        <LocationType>B</LocationType>
        <Address1></Address1>
        <City>Montreal</City>
        <CountryCode>CA</CountryCode>
        <PostalCode>H8Z2Z3</PostalCode>
    </Place>
    <Pickup>
        <PickupDate>2013-10-19</PickupDate>
        <ReadyByTime>10:20</ReadyByTime>
        <CloseTime>09:20</CloseTime>
        <Pieces>1</Pieces>
        <RemotePickupFlag>Y</RemotePickupFlag>
        <weight>
            <Weight>20</Weight>
            <WeightUnit>L</WeightUnit>
        </weight>
        <SpecialInstructions></SpecialInstructions>
    </Pickup>
    <PickupContact>
        <PersonName>Rikhil</PersonName>
        <Phone>4801313131</Phone>
    </PickupContact>
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
    <ReadyByTime>10:30:00</ReadyByTime>
    <NextPickupDate>2013-10-09</NextPickupDate>
    <CallInTime>08:30:00</CallInTime>
    <OriginSvcArea>BEL</OriginSvcArea>
</res:BookPUResponse>
"""

PickupRequestXML = """<req:BookPURequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com book-pickup-global-req_EA.xsd" schemaVersion="3.0">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>XMLPI</SoftwareName>
            <SoftwareVersion>3.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <Requestor>
        <AccountType>D</AccountType>
        <AccountNumber>123456789</AccountNumber>
        <RequestorContact>
            <PersonName>Subhayu</PersonName>
            <Phone>4801313131</Phone>
        </RequestorContact>
    </Requestor>
    <Place>
        <LocationType>B</LocationType>
        <Address1>234 rue Hubert</Address1>
        <City>Montreal</City>
        <StateCode>QC</StateCode>
        <CountryCode>CA</CountryCode>
        <PostalCode>H8Z2Z3</PostalCode>
    </Place>
    <Pickup>
        <PickupDate>2013-10-19</PickupDate>
        <ReadyByTime>10:20</ReadyByTime>
        <CloseTime>09:20</CloseTime>
        <Pieces>1</Pieces>
        <RemotePickupFlag>Y</RemotePickupFlag>
        <weight>
            <Weight>20</Weight>
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
