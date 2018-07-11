import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Tracking
from tests.dhl.fixture import proxy, strip


class TestDHLTracking(unittest.TestCase):

    @patch("openship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_create_tracking_request(self, http_mock):
        payload = Tracking.create(tracking_numbers=["8346088391"])
        tracking_req_xml_obj = proxy.mapper.create_tracking_request(payload)
        # remove MessageTime for testing purpose
        tracking_req_xml_obj.Request.ServiceHeader.MessageTime = None

        proxy.get_trackings(tracking_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(TrackingRequestXml))

    def test_tracking_auth_error_parsing(self):
        parsed_response = proxy.mapper.parse_error_response(to_xml(AuthError))
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedAuthError))

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedTrackingResponse))


if __name__ == '__main__':
    unittest.main()


ParsedAuthError = [
    {
        "carrier": "carrier_name",
        "code": "111",
        "message": " Error Parsing incoming request XML\n                    Error: Datatype error: In element\n                    'Password' : Value 'testPwd'\n                    with length '7' is less than minimum\n                    length facet of '8'.. at line 11, column 33"
    }
]

ParsedTrackingResponse = [
    [
        {
            "carrier": "carrier_name",
            "events": [
                {
                    "code": "PU",
                    "date": "2009-08-28",
                    "description": "Shipment picked up",
                    "location": "Barcelona - Spain ",
                    "signatory": "960528602",
                    "time": "13:26:00"
                },
                {
                    "code": "PO",
                    "date": "2009-08-28",
                    "description": "Departing origin",
                    "location": "Barcelona - Spain ",
                    "signatory": " 00:00:00",
                    "time": "19:27:00"
                },
                {
                    "code": "RW",
                    "date": "2009-08-28",
                    "description": "",
                    "location": "Barcelona - Spain ",
                    "signatory": "",
                    "time": "19:27:00"
                },
                {
                    "code": "PL",
                    "date": "2009-08-28",
                    "description": "Processed at Location Barcelona - Spain ",
                    "location": "Barcelona - Spain ",
                    "signatory": "",
                    "time": "20:39:01"
                },
                {
                    "code": "AF",
                    "date": "2009-08-28",
                    "description": "Arrived at DHL facility in Barcelona -\n                        Spain ",
                    "location": "Barcelona - Spain ",
                    "signatory": "",
                    "time": "21:17:57"
                },
                {
                    "code": "DF",
                    "date": "2009-08-28",
                    "description": "Departed from DHL facility in Barcelona\n                        - Spain ",
                    "location": "Barcelona - Spain ",
                    "signatory": "",
                    "time": "22:01:00"
                },
                {
                    "code": "AF",
                    "date": "2009-08-29",
                    "description": "Arrived at DHL facility in Leipzig -\n                        Germany ",
                    "location": "Leipzig - Germany ",
                    "signatory": "",
                    "time": "00:32:16"
                },
                {
                    "code": "PL",
                    "date": "2009-08-29",
                    "description": "Processed at Location Leipzig - Germany ",
                    "location": "Leipzig - Germany ",
                    "signatory": "",
                    "time": "01:05:03"
                },
                {
                    "code": "DF",
                    "date": "2009-08-29",
                    "description": "Departed from DHL facility in Leipzig -\n                        Germany ",
                    "location": "Leipzig - Germany ",
                    "signatory": "",
                    "time": "05:52:19"
                },
                {
                    "code": "AF",
                    "date": "2009-08-30",
                    "description": "Arrived at DHL facility in Bergamo -\n                        Italy ",
                    "location": "Bergamo - Italy ",
                    "signatory": "",
                    "time": "19:43:22"
                },
                {
                    "code": "PL",
                    "date": "2009-08-30",
                    "description": "Processed at Location Bergamo - Italy ",
                    "location": "Bergamo - Italy ",
                    "signatory": "",
                    "time": "23:30:00"
                },
                {
                    "code": "DF",
                    "date": "2009-08-31",
                    "description": "Departed from DHL facility in Bergamo -\n                        Italy ",
                    "location": "Bergamo - Italy ",
                    "signatory": "",
                    "time": "02:06:00"
                },
                {
                    "code": "DF",
                    "date": "2009-08-31",
                    "description": "Departed from DHL facility in Milan -\n                        Italy ",
                    "location": "Milan - Italy ",
                    "signatory": "",
                    "time": "06:23:00"
                },
                {
                    "code": "AR",
                    "date": "2009-08-31",
                    "description": "Arrived at DHL facility in Milan -\n                        Italy ",
                    "location": "Milan - Italy ",
                    "signatory": "",
                    "time": "08:59:00"
                },
                {
                    "code": "WC",
                    "date": "2009-08-31",
                    "description": "With delivery courier",
                    "location": "Milan - Italy ",
                    "signatory": "",
                    "time": "09:19:00"
                },
                {
                    "code": "OK",
                    "date": "2009-08-31",
                    "description": "Shipment delivered",
                    "location": "Milan - Italy ",
                    "signatory": "CAMPAGNA",
                    "time": "10:09:00"
                }
            ],
            "shipment_date": "2009-08-28 13:26:00",
            "tracking_number": "3180831640"
        },
        {
            "carrier": "carrier_name",
            "events": [
                {
                    "code": "PU",
                    "date": "2009-08-26",
                    "description": "Shipment picked up",
                    "location": "Singapore - Singapore ",
                    "signatory": "",
                    "time": "10:00:00"
                }
            ],
            "shipment_date": "2009-08-26 10:00:00",
            "tracking_number": "7740842550"
        },
        {
            "carrier": "carrier_name",
            "events": [
                {
                    "code": "PU",
                    "date": "2009-08-13",
                    "description": "Shipment picked up",
                    "location": "Hong Kong - Hong Kong ",
                    "signatory": "",
                    "time": "23:58:00"
                },
                {
                    "code": "RW",
                    "date": "2009-08-14",
                    "description": "",
                    "location": "Hong Kong - Hong Kong ",
                    "signatory": "21.20",
                    "time": "02:19:50"
                }
            ],
            "shipment_date": "2009-08-13 23:58:00",
            "tracking_number": "1815115363"
        }
    ],
    []
]


AuthError = '''<?xml version="1.0" encoding="UTF-8"?>
<req:ShipmentTrackingErrorResponse xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com track-err-res.xsd">
    <Response>
        <ServiceHeader>
            <MessageTime>2018-06-28T01:12:53+01:00</MessageTime>
        </ServiceHeader>
        <Status>
            <ActionStatus>Failure</ActionStatus>
            <Condition>
                <ConditionCode>111</ConditionCode>
                <ConditionData> Error Parsing incoming request XML
                    Error: Datatype error: In element
                    &apos;Password&apos; : Value &apos;testPwd&apos;
                    with length &apos;7&apos; is less than minimum
                    length facet of &apos;8&apos;.. at line 11, column 33</ConditionData>
            </Condition>
        </Status>
    </Response>
</req:ShipmentTrackingErrorResponse>
<!-- ServiceInvocationId:20180628011253_42d7_3a8bef3e-ebbd-4e1a-b248-d01e51b1c77f -->
'''

TrackingRequestXml = '''<req:KnownTrackingRequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com TrackingRequestKnown.xsd">
	<Request>
		<ServiceHeader>
			<MessageReference>1234567890123456789012345678901</MessageReference>
			<SiteID>site_id</SiteID>
			<Password>password</Password>
		</ServiceHeader>
	</Request>
	<LanguageCode>en</LanguageCode>
	<AWBNumber>8346088391</AWBNumber>
	<LevelOfDetails>ALL_CHECK_POINTS</LevelOfDetails>
        
</req:KnownTrackingRequest>
'''

TrackingResponseXml = '''<?xml version="1.0" encoding="UTF-8"?>
<req:TrackingResponse xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com TrackingResponse.xsd">
    <Response>
        <ServiceHeader>
            <MessageTime>2002-06-25T11:28:56-08:00</MessageTime>
            <MessageReference>1234567890123456789012345678</MessageReference>
            <SiteID>TestSiteID</SiteID>
        </ServiceHeader>
    </Response>
    <AWBInfo>
        <AWBNumber>3180831640</AWBNumber>
        <Status>
            <ActionStatus>success</ActionStatus>
        </Status>
        <ShipmentInfo>
            <OriginServiceArea>
                <ServiceAreaCode>BCN</ServiceAreaCode>
                <Description>Barcelona - Spain </Description>
            </OriginServiceArea>
            <DestinationServiceArea>
                <ServiceAreaCode>MIL</ServiceAreaCode>
                <Description>Milan - Italy </Description>
            </DestinationServiceArea>
            <ShipperName>HOTEL VINCI MARITIMO</ShipperName>
            <ShipperAccountNumber>960528602</ShipperAccountNumber>
            <ConsigneeName>PHARMA WORKS</ConsigneeName>
            <ShipmentDate>2009-08-28T13:26:00</ShipmentDate>
            <Pieces>1</Pieces>
            <Weight>0.74</Weight>
            <WeightUnit>K</WeightUnit>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>13:26:00</Time>
                <ServiceEvent>
                    <EventCode>PU</EventCode>
                    <Description>Shipment picked up</Description>
                </ServiceEvent>
                <Signatory>960528602</Signatory>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>19:27:00</Time>
                <ServiceEvent>
                    <EventCode>PO</EventCode>
                    <Description>Departing origin</Description>
                </ServiceEvent>
                <Signatory> 00:00:00</Signatory>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>19:27:00</Time>
                <ServiceEvent>
                    <EventCode>RW</EventCode>
                    <Description/>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>20:39:01</Time>
                <ServiceEvent>
                    <EventCode>PL</EventCode>
                    <Description>Processed at Location Barcelona - Spain </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>21:17:57</Time>
                <ServiceEvent>
                    <EventCode>AF</EventCode>
                    <Description>Arrived at DHL facility in Barcelona -
                        Spain </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-28</Date>
                <Time>22:01:00</Time>
                <ServiceEvent>
                    <EventCode>DF</EventCode>
                    <Description>Departed from DHL facility in Barcelona
                        - Spain </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BCN</ServiceAreaCode>
                    <Description>Barcelona - Spain </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-29</Date>
                <Time>00:32:16</Time>
                <ServiceEvent>
                    <EventCode>AF</EventCode>
                    <Description>Arrived at DHL facility in Leipzig -
                        Germany </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>LEJ</ServiceAreaCode>
                    <Description>Leipzig - Germany </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-29</Date>
                <Time>01:05:03</Time>
                <ServiceEvent>
                    <EventCode>PL</EventCode>
                    <Description>Processed at Location Leipzig - Germany </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>LEJ</ServiceAreaCode>
                    <Description>Leipzig - Germany </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-29</Date>
                <Time>05:52:19</Time>
                <ServiceEvent>
                    <EventCode>DF</EventCode>
                    <Description>Departed from DHL facility in Leipzig -
                        Germany </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>LEJ</ServiceAreaCode>
                    <Description>Leipzig - Germany </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-30</Date>
                <Time>19:43:22</Time>
                <ServiceEvent>
                    <EventCode>AF</EventCode>
                    <Description>Arrived at DHL facility in Bergamo -
                        Italy </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BGY</ServiceAreaCode>
                    <Description>Bergamo - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-30</Date>
                <Time>23:30:00</Time>
                <ServiceEvent>
                    <EventCode>PL</EventCode>
                    <Description>Processed at Location Bergamo - Italy </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BGY</ServiceAreaCode>
                    <Description>Bergamo - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-31</Date>
                <Time>02:06:00</Time>
                <ServiceEvent>
                    <EventCode>DF</EventCode>
                    <Description>Departed from DHL facility in Bergamo -
                        Italy </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>BGY</ServiceAreaCode>
                    <Description>Bergamo - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-31</Date>
                <Time>06:23:00</Time>
                <ServiceEvent>
                    <EventCode>DF</EventCode>
                    <Description>Departed from DHL facility in Milan -
                        Italy </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>MIL</ServiceAreaCode>
                    <Description>Milan - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-31</Date>
                <Time>08:59:00</Time>
                <ServiceEvent>
                    <EventCode>AR</EventCode>
                    <Description>Arrived at DHL facility in Milan -
                        Italy </Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>MIL</ServiceAreaCode>
                    <Description>Milan - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-31</Date>
                <Time>09:19:00</Time>
                <ServiceEvent>
                    <EventCode>WC</EventCode>
                    <Description>With delivery courier</Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>MIL</ServiceAreaCode>
                    <Description>Milan - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-31</Date>
                <Time>10:09:00</Time>
                <ServiceEvent>
                    <EventCode>OK</EventCode>
                    <Description>Shipment delivered</Description>
                </ServiceEvent>
                <Signatory>CAMPAGNA</Signatory>
                <ServiceArea>
                    <ServiceAreaCode>MIL</ServiceAreaCode>
                    <Description>Milan - Italy </Description>
                </ServiceArea>
            </ShipmentEvent>
        </ShipmentInfo>
    </AWBInfo>
    <AWBInfo>
        <AWBNumber>7740842550</AWBNumber>
        <Status>
            <ActionStatus>success</ActionStatus>
        </Status>
        <ShipmentInfo>
            <OriginServiceArea>
                <ServiceAreaCode>SIN</ServiceAreaCode>
                <Description>Singapore - Singapore </Description>
            </OriginServiceArea>
            <DestinationServiceArea>
                <ServiceAreaCode>HKG</ServiceAreaCode>
                <Description>Hong Kong - Hong Kong </Description>
            </DestinationServiceArea>
            <ShipperName>QUINTILES LAB. EAST ASIA C/O DESC</ShipperName>
            <ShipperAccountNumber>610318744</ShipperAccountNumber>
            <ConsigneeName>QUEEN ELIZABETH HOSP.</ConsigneeName>
            <ShipmentDate>2009-08-26T10:00:00</ShipmentDate>
            <Pieces>3</Pieces>
            <WeightUnit>K</WeightUnit>
            <ShipmentEvent>
                <Date>2009-08-26</Date>
                <Time>10:00:00</Time>
                <ServiceEvent>
                    <EventCode>PU</EventCode>
                    <Description>Shipment picked up</Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>SIN</ServiceAreaCode>
                    <Description>Singapore - Singapore </Description>
                </ServiceArea>
            </ShipmentEvent>
        </ShipmentInfo>
    </AWBInfo>
    <AWBInfo>
        <AWBNumber>1815115363</AWBNumber>
        <Status>
            <ActionStatus>success</ActionStatus>
        </Status>
        <ShipmentInfo>
            <OriginServiceArea>
                <ServiceAreaCode>HKG</ServiceAreaCode>
                <Description>Hong Kong - Hong Kong </Description>
            </OriginServiceArea>
            <DestinationServiceArea>
                <ServiceAreaCode>SIN</ServiceAreaCode>
                <Description>Singapore - Singapore </Description>
            </DestinationServiceArea>
            <ShipperName>GENDA INTL LTD</ShipperName>
            <ShipperAccountNumber>631016670</ShipperAccountNumber>
            <ConsigneeName>IWATANI CORPORATION SG PTE</ConsigneeName>
            <ShipmentDate>2009-08-13T23:58:00</ShipmentDate>
            <Pieces>1</Pieces>
            <Weight>24.5</Weight>
            <WeightUnit>K</WeightUnit>
            <ShipmentEvent>
                <Date>2009-08-13</Date>
                <Time>23:58:00</Time>
                <ServiceEvent>
                    <EventCode>PU</EventCode>
                    <Description>Shipment picked up</Description>
                </ServiceEvent>
                <Signatory/>
                <ServiceArea>
                    <ServiceAreaCode>HKG</ServiceAreaCode>
                    <Description>Hong Kong - Hong Kong </Description>
                </ServiceArea>
            </ShipmentEvent>
            <ShipmentEvent>
                <Date>2009-08-14</Date>
                <Time>02:19:50</Time>
                <ServiceEvent>
                    <EventCode>RW</EventCode>
                    <Description/>
                </ServiceEvent>
                <Signatory>21.20</Signatory>
                <ServiceArea>
                    <ServiceAreaCode>HKG</ServiceAreaCode>
                    <Description>Hong Kong - Hong Kong </Description>
                </ServiceArea>
            </ShipmentEvent>
        </ShipmentInfo>
    </AWBInfo>
</req:TrackingResponse>
'''
