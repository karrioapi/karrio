import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestchronopostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), [TrackingRequest])

    def test_get_tracking(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking-cxf/TrackingServiceWS",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "delivered": True,
            "events": [
                {
                    "code": "DC",
                    "date": "2022-06-19",
                    "description": "Shipment in preparation to be shipped",
                    "location": "Web Services",
                    "time": "13:47 PM",
                },
                {
                    "code": "DB",
                    "date": "2022-06-20",
                    "description": "Shipment handed over by shipper",
                    "location": "AMBOISE",
                    "time": "16:54 PM",
                },
                {
                    "code": "DY",
                    "date": "2022-06-20",
                    "description": "Parcel Registered by the post office",
                    "location": "AMBOISE",
                    "time": "16:57 PM",
                },
                {
                    "code": "SC",
                    "date": "2022-06-21",
                    "description": "Sorted at departure location",
                    "location": "TOURS CHRONOPOST",
                    "time": "19:16 PM",
                },
                {
                    "code": "TS",
                    "date": "2022-06-21",
                    "description": "Shipment in transit",
                    "location": "HUB CHILLY MAZARIN CHRONOPOST",
                    "time": "23:36 PM",
                },
                {
                    "code": "TS",
                    "date": "2022-06-22",
                    "description": "Shipment in transit",
                    "location": "ARRAS CHRONOPOST",
                    "time": "02:43 AM",
                },
                {
                    "code": "SD",
                    "date": "2022-06-22",
                    "description": "Sorted at delivery location",
                    "location": "ARRAS CHRONOPOST",
                    "time": "02:44 AM",
                },
                {
                    "code": "TA",
                    "date": "2022-06-22",
                    "description": "Shipment in delivery to the consignee",
                    "location": "ARRAS CHRONOPOST",
                    "time": "07:12 AM",
                },
                {
                    "code": "D",
                    "date": "2022-06-22",
                    "description": "Delivered",
                    "location": "ARRAS CHRONOPOST",
                    "time": "08:30 AM",
                },
            ],
            "tracking_number": "89108749065090",
            "info": {
                "carrier_tracking_link": "https://www.chronopost.fr/tracking-no-cms/suivi-page?listeNumerosLT=89108749065090",
                "shipment_destination_postal_code": "62223",
            },
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "code": 1,
            "message": "System Error",
        }
    ],
]


TrackingRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/">
    <soapenv:Body>
        <soapenv:trackSkybillV2>
            <language>en_GB</language>
            <skybillNumber>89108749065090</skybillNumber>
        </soapenv:trackSkybillV2>
    </soapenv:Body>
</soapenv:Envelope>
"""

TrackingResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns2:trackSkybillV2Response xmlns:ns2="http://cxf.tracking.soap.chronopost.fr/">
            <return>
                <errorCode>0</errorCode>
                <listEventInfoComp>
                    <events>
                        <code>DC</code>
                        <eventDate>2022-06-19T13:47:53+02:00</eventDate>
                        <eventLabel>Shipment in preparation to be shipped</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC></NPC>
                        <officeLabel>Web Services</officeLabel>
                        <zipCode></zipCode>
                        <infoCompList>
                            <name>Partner number</name>
                            <value>GEO/XT8452370122486</value>
                        </infoCompList>
                    </events>
                    <events>
                        <code>DB</code>
                        <eventDate>2022-06-20T16:54:13+02:00</eventDate>
                        <eventLabel>Shipment handed over by shipper</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>37</NPC>
                        <officeLabel>AMBOISE</officeLabel>
                        <zipCode>37400</zipCode>
                        <infoCompList>
                            <name>Date of start delay</name>
                            <value>20220621-1000</value>
                        </infoCompList>
                    </events>
                    <events>
                        <code>DY</code>
                        <eventDate>2022-06-20T16:57:00+02:00</eventDate>
                        <eventLabel>Parcel Registered by the post office</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>37</NPC>
                        <officeLabel>AMBOISE</officeLabel>
                        <zipCode>37400</zipCode>
                    </events>
                    <events>
                        <code>SC</code>
                        <eventDate>2022-06-21T19:16:06+02:00</eventDate>
                        <eventLabel>Sorted at departure location</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>37</NPC>
                        <officeLabel>TOURS CHRONOPOST</officeLabel>
                        <zipCode>37000</zipCode>
                        <infoCompList>
                            <name>Comment</name>
                            <value>Sending supported by Chronopost, in transit</value>
                        </infoCompList>
                    </events>
                    <events>
                        <code>TS</code>
                        <eventDate>2022-06-21T23:36:06+02:00</eventDate>
                        <eventLabel>Shipment in transit</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>91</NPC>
                        <officeLabel>HUB CHILLY MAZARIN CHRONOPOST</officeLabel>
                        <zipCode>91090</zipCode>
                    </events>
                    <events>
                        <code>TS</code>
                        <eventDate>2022-06-22T02:43:25+02:00</eventDate>
                        <eventLabel>Shipment in transit</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>62</NPC>
                        <officeLabel>ARRAS CHRONOPOST</officeLabel>
                        <zipCode>62223</zipCode>
                    </events>
                    <events>
                        <code>SD</code>
                        <eventDate>2022-06-22T02:44:00+02:00</eventDate>
                        <eventLabel>Sorted at delivery location</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>62</NPC>
                        <officeLabel>ARRAS CHRONOPOST</officeLabel>
                        <zipCode>62223</zipCode>
                        <infoCompList>
                            <name>Comment</name>
                            <value>Ready for shipment delivery</value>
                        </infoCompList>
                    </events>
                    <events>
                        <code>TA</code>
                        <eventDate>2022-06-22T07:12:05+02:00</eventDate>
                        <eventLabel>Shipment in delivery to the consignee</eventLabel>
                        <highPriority>false</highPriority>
                        <NPC>62</NPC>
                        <officeLabel>ARRAS CHRONOPOST</officeLabel>
                        <zipCode>62223</zipCode>
                        <infoCompList>
                            <name>Delivery type</name>
                            <value>Standard Delivery</value>
                        </infoCompList>
                    </events>
                    <events>
                        <code>D</code>
                        <eventDate>2022-06-22T08:30:00+02:00</eventDate>
                        <eventLabel>Delivered</eventLabel>
                        <highPriority>true</highPriority>
                        <NPC>62</NPC>
                        <officeLabel>ARRAS CHRONOPOST</officeLabel>
                        <zipCode>62223</zipCode>
                        <infoCompList>
                            <name>Consignee's name</name>
                            <value>SOLVAREA</value>
                        </infoCompList>
                    </events>
                    <skybillNumber>89108749065090</skybillNumber>
                </listEventInfoComp>
            </return>
        </ns2:trackSkybillV2Response>
    </soap:Body>
</soap:Envelope>
"""

ErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns2:trackSkybillV2Response xmlns:ns2="http://cxf.tracking.soap.chronopost.fr/">
            <return>
                <errorCode>1</errorCode>
                <errorMessage>System Error</errorMessage>
            </return>
        </ns2:trackSkybillV2Response>
    </soap:Body>
</soap:Envelope>
"""
