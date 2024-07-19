import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCanadaPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TRACKING_PAYLOAD)

    @patch("karrio.mappers.canadapost.proxy.lib.request", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackingRequest).from_(gateway)

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(reqUrl, TrackingRequestURL)

    def test_tracking_auth_error_parsing(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = AuthError
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedAuthError,
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXml
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedTrackingResponse,
            )

    def test_tracking_unknown_response_parsing(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = UnknownTrackingNumberResponse
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedUnknownTrackingNumberResponse,
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["7023210039414604"]

ParsedAuthError = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "E002",
            "message": "AAA Authentication Failure",
            "details": {},
        }
    ],
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "delivered": False,
            "estimated_delivery": "2011-04-05",
            "events": [
                {
                    "code": "20",
                    "date": "2011-02-03",
                    "description": "Signature image recorded for Online viewing",
                    "location": "SAINTE-FOY, QC",
                    "time": "11:59 AM",
                },
                {
                    "code": "0174",
                    "date": "2011-02-03",
                    "description": "Item out for delivery",
                    "location": "SAINTE-FOY, QC",
                    "time": "08:27 AM",
                },
                {
                    "code": "0100",
                    "date": "2011-02-02",
                    "description": "Item processed at postal facility",
                    "location": "QUEBEC, QC",
                    "time": "14:45 PM",
                },
                {
                    "code": "0173",
                    "date": "2011-02-02",
                    "description": "Customer addressing error found; attempting to correct. Possible delay",
                    "location": "QUEBEC, QC",
                    "time": "06:19 AM",
                },
                {
                    "code": "1496",
                    "date": "2011-02-01",
                    "description": "Item successfully delivered",
                    "location": "QUEBEC, QC",
                    "time": "07:59 AM",
                },
                {
                    "code": "20",
                    "date": "2011-02-01",
                    "description": "Signature image recorded for Online viewing",
                    "location": "QUEBEC, QC",
                    "time": "07:59 AM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.canadapost-postescanada.ca/track-reperage/en#/resultList?searchFor=7023210039414604",
                "shipment_delivery_date": "2011-04-05",
                "shipment_destination_postal_code": "K0J1T0",
                "shipment_service": "Expedited Parcels",
                "signed_by": "HETU",
            },
            "status": "in_transit",
            "tracking_number": "7023210039414604",
        }
    ],
    [],
]

ParsedUnknownTrackingNumberResponse = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "004",
            "message": "No Pin History",
            "details": {},
        }
    ],
]


AuthError = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/messages">
        <message>
            <code>E002</code>
            <description>AAA Authentication Failure</description>
        </message>
    </messages>
</wrapper>
"""

TrackingRequestURL = (
    f"""{gateway.settings.server_url}/vis/track/pin/7023210039414604/detail"""
)

TrackingResponseXml = """<wrapper>
    <tracking-detail>
        <pin>7023210039414604</pin>
        <active-exists>1</active-exists>
        <archive-exists/>
        <changed-expected-date/>
        <destination-postal-id>K0J1T0</destination-postal-id>
        <duplicate-flag-ind/>
        <expected-delivery-date>2011-04-05</expected-delivery-date>
        <changed-expected-delivery-reason/>
        <mailed-by-customer-number>0007023210</mailed-by-customer-number>
        <mailed-on-behalf-of-customer-number>0007023210</mailed-on-behalf-of-customer-number>
        <original-pin/>
        <service-name>Expedited Parcels</service-name>
        <service-name-2>Colis acc&#233;l&#233;r&#233;s</service-name-2>
        <customer-ref-1>APRIL1REF1A</customer-ref-1>
        <customer-ref-2>APRIL1REF1C</customer-ref-2>
        <return-pin/>
        <signature-image-exists>false</signature-image-exists>
        <suppress-signature>false</suppress-signature>
        <delivery-options>
            <item>
                <delivery-option>CH_HLD_PCK_UP</delivery-option>
                <delivery-option-description>Card for Pickup</delivery-option-description>
            </item>
            <item>
                <delivery-option>CH_SGN_OPTION</delivery-option>
                <delivery-option-description>Signature Required</delivery-option-description>
            </item>
            <item>
                <delivery-option>CH_SGN_OPTION</delivery-option>
                <delivery-option-description>Proof of Age Required</delivery-option-description>
            </item>
            <item>
                <delivery-option>CH_COD_VALUE</delivery-option>
                <delivery-option-description>COD Amount</delivery-option-description>
            </item>
        </delivery-options>
        <significant-events>
            <occurrence>
                <event-identifier>20</event-identifier>
                <event-date>2011-02-03</event-date>
                <event-time>11:59:59</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Signature image recorded for Online viewing</event-description>
                <signatory-name>HETU</signatory-name>
                <event-site>SAINTE-FOY</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
            <occurrence>
                <event-identifier>0174</event-identifier>
                <event-date>2011-02-03</event-date>
                <event-time>08:27:43</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Item out for delivery</event-description>
                <signatory-name></signatory-name>
                <event-site>SAINTE-FOY</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
            <occurrence>
                <event-identifier>0100</event-identifier>
                <event-date>2011-02-02</event-date>
                <event-time>14:45:48</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Item processed at postal facility</event-description>
                <signatory-name></signatory-name>
                <event-site>QUEBEC</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
            <occurrence>
                <event-identifier>0173</event-identifier>
                <event-date>2011-02-02</event-date>
                <event-time>06:19:57</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Customer addressing error found; attempting to correct. Possible delay</event-description>
                <signatory-name></signatory-name>
                <event-site>QUEBEC</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
            <occurrence>
                <event-identifier>1496</event-identifier>
                <event-date>2011-02-01</event-date>
                <event-time>07:59:52</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Item successfully delivered</event-description>
                <signatory-name></signatory-name>
                <event-site>QUEBEC</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
            <occurrence>
                <event-identifier>20</event-identifier>
                <event-date>2011-02-01</event-date>
                <event-time>07:59:52</event-time>
                <event-time-zone>EST</event-time-zone>
                <event-description>Signature image recorded for Online viewing</event-description>
                <signatory-name>R GREGOIRE</signatory-name>
                <event-site>QUEBEC</event-site>
                <event-province>QC</event-province>
                <event-retail-location-id></event-retail-location-id>
                <event-retail-name></event-retail-name>
            </occurrence>
        </significant-events>
    </tracking-detail>
</wrapper>
"""

UnknownTrackingNumberResponse = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/track">
        <message>
            <code>004</code>
            <description>No Pin History</description>
        </message>
    </messages>
</wrapper>
"""
