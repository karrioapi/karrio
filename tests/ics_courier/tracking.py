import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.ics_courier.fixture import gateway


class TestICSCourierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TrackingRequestXML)

    def test_get_tracking(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                gateway.settings.server_url,
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"],
                "http://www.icscourier.ca/TracePackge",
            )

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = [
    "ND6CN800064800L1C4C2",
    "ND6CN800064816N5P1V2",
    "ND6CN800064805N2L0E9",
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "ics_courier",
            "carrier_name": "ics_courier",
            "delivered": True,
            "events": [
                {
                    "date": "2021-08-17",
                    "description": "Delivered at: TRESA BANMAN 92 REDAN ST   ST. THOMAS, ON, N5P 1V2",
                    "time": "09:03",
                },
                {
                    "date": "2021-08-17",
                    "description": "Out for Delivery",
                    "time": "07:15",
                },
                {
                    "date": "2021-08-17",
                    "description": "In Sort Process",
                    "time": "04:43",
                },
                {
                    "date": "2021-08-17",
                    "description": "At ICS Branch LONDON, ON for processing",
                    "time": "04:43",
                },
                {
                    "date": "2021-08-16",
                    "description": "At ICS Branch ETOBICOKE, ON for processing",
                    "time": "18:36",
                },
                {"date": "2021-08-16", "description": "In Transit", "time": "18:36"},
            ],
            "tracking_number": "ND6CN800064816N5P1V2",
        },
        {
            "carrier_id": "ics_courier",
            "carrier_name": "ics_courier",
            "delivered": True,
            "events": [
                {
                    "date": "2021-08-17",
                    "description": "Delivered at: RAKIKA RAFI 318 SPRUCE ST BUZZER CODE 189, BUILDING  WATERLOO, ON, N2L 0E9",
                    "time": "12:10",
                },
                {
                    "date": "2021-08-17",
                    "description": "Out for Delivery",
                    "time": "07:13",
                },
                {
                    "date": "2021-08-17",
                    "description": "In Sort Process",
                    "time": "03:10",
                },
                {
                    "date": "2021-08-17",
                    "description": "At ICS Branch CAMBRIDGE, ON for processing",
                    "time": "03:10",
                },
                {
                    "date": "2021-08-16",
                    "description": "At ICS Branch ETOBICOKE, ON for processing",
                    "time": "18:36",
                },
                {"date": "2021-08-16", "description": "In Transit", "time": "18:36"},
            ],
            "tracking_number": "ND6CN800064805N2L0E9",
        },
        {
            "carrier_id": "ics_courier",
            "carrier_name": "ics_courier",
            "delivered": True,
            "events": [
                {
                    "date": "2021-08-17",
                    "description": "Delivered at: ROBERTA TILLEY 64 PENFOUND DR   BOWMANVILLE, ON, L1C 4C2",
                    "time": "09:04",
                },
                {
                    "date": "2021-08-17",
                    "description": "Out for Delivery",
                    "time": "06:59",
                },
                {
                    "date": "2021-08-17",
                    "description": "In Sort Process",
                    "time": "02:20",
                },
                {
                    "date": "2021-08-17",
                    "description": "At ICS Branch SCARBOROUGH, ON for processing",
                    "time": "02:20",
                },
                {"date": "2021-08-16", "description": "In Transit", "time": "20:03"},
                {
                    "date": "2021-08-16",
                    "description": "At ICS Branch ETOBICOKE, ON for processing",
                    "time": "19:58",
                },
            ],
            "tracking_number": "ND6CN800064800L1C4C2",
        },
    ],
    [],
]

TrackingRequestXML = """<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns: xsd="http://www.w3.org/2001/XMLSchema" xmlns: soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Header/>
    <soap12:Body>
        <soap12:TracePackge>
            <TrackNums>
                <string>ND6CN800064800L1C4C2</string>
                <string>ND6CN800064816N5P1V2</string>
                <string>ND6CN800064805N2L0E9</string>
            </TrackNums>
            <DetailInfo>true</DetailInfo>
        </soap12:TracePackge>
    </soap12:Body>
</soap12:Envelope>
"""

TrackingResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <TracePackgeResponse xmlns="http://www.icscourier.ca/">
            <TracePackgeResult>
                <TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-17T09:03:47</StatusDate>
                        <Status>Delivered at: TRESA BANMAN 92 REDAN ST   ST. THOMAS, ON, N5P 1V2</Status>
                        <Signby>NSR</Signby>
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-17T07:15:44</StatusDate>
                        <Status>Out for Delivery</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-17T04:43:13</StatusDate>
                        <Status>In Sort Process</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-17T04:43:11</StatusDate>
                        <Status>At ICS Branch LONDON, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-16T18:36:17</StatusDate>
                        <Status>In Transit</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064816N5P1V2</TrackingNum>
                        <StatusDate>2021-08-16T18:36:17</StatusDate>
                        <Status>At ICS Branch ETOBICOKE, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-16T18:36:17</StatusDate>
                        <Status>In Transit</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-16T18:36:17</StatusDate>
                        <Status>At ICS Branch ETOBICOKE, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-17T03:10:19</StatusDate>
                        <Status>In Sort Process</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-17T03:10:17</StatusDate>
                        <Status>At ICS Branch CAMBRIDGE, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-17T12:10:06</StatusDate>
                        <Status>Delivered at: RAKIKA RAFI 318 SPRUCE ST BUZZER CODE 189, BUILDING  WATERLOO, ON, N2L 0E9</Status>
                        <Signby>NSR</Signby>
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064805N2L0E9</TrackingNum>
                        <StatusDate>2021-08-17T07:13:27</StatusDate>
                        <Status>Out for Delivery</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-17T06:59:18</StatusDate>
                        <Status>Out for Delivery</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-17T09:04:49</StatusDate>
                        <Status>Delivered at: ROBERTA TILLEY 64 PENFOUND DR   BOWMANVILLE, ON, L1C 4C2</Status>
                        <Signby>NSR</Signby>
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-17T02:20:27</StatusDate>
                        <Status>At ICS Branch SCARBOROUGH, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-17T02:20:29</StatusDate>
                        <Status>In Sort Process</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-16T19:58:00</StatusDate>
                        <Status>At ICS Branch ETOBICOKE, ON for processing</Status>
                        <Signby />
                    </TrackingInfo>
                    <TrackingInfo>
                        <TrackingNum>ND6CN800064800L1C4C2</TrackingNum>
                        <StatusDate>2021-08-16T20:03:00</StatusDate>
                        <Status>In Transit</Status>
                        <Signby />
                    </TrackingInfo>
                </TrackingInfo>
            </TracePackgeResult>
        </TracePackgeResponse>
    </soap:Body>
</soap:Envelope>
"""

TrackingNotFoundResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TracePackgeResponse xmlns="http://www.icscourier.ca/">
      <TracePackgeResult>
        <Err>
          <_ErrCode>string</_ErrCode>
          <_ErrDescription>string</_ErrDescription>
        </Err>
        <TrackingInfo>
          <TrackingInfo>
            <TrackingNum>string</TrackingNum>
            <StatusDate>dateTime</StatusDate>
            <Status>string</Status>
            <Signby>string</Signby>
          </TrackingInfo>
          <TrackingInfo>
            <TrackingNum>string</TrackingNum>
            <StatusDate>dateTime</StatusDate>
            <Status>string</Status>
            <Signby>string</Signby>
          </TrackingInfo>
        </TrackingInfo>
      </TracePackgeResult>
    </TracePackgeResponse>
  </soap12:Body>
</soap12:Envelope>
"""
