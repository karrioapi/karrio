import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestXML)

    def test_get_tracking(self):
        with patch("karrio.mappers.aramex.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ShippingAPI.V2/Tracking/Service_1_0.svc",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.aramex.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_non_existents_tracking_response(self):
        with patch("karrio.mappers.aramex.proxy.http") as mock:
            mock.return_value = TrackingNonExistentResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response),
                DP.to_dict(ParsedNonExistentTrackingResponse),
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.aramex.proxy.http") as mock:
            mock.return_value = ErrorResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedTrackingResponse = [
    [],
    [],
]

ParsedNonExistentTrackingResponse = [
    [],
    [
        {
            "carrier_id": "aramex",
            "carrier_name": "aramex",
            "message": 'Waybill "1Z12345E6205277936" Not Found',
        }
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "aramex",
            "carrier_name": "aramex",
            "code": "ERR01",
            "message": "ClientInfo - Invalid username or password",
        }
    ],
]


# Serialized request and responses

TrackingRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://ws.aramex.net/ShippingAPI/v1/" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays>
    <soap:Header/>
    <soap:Body>
        <v1:ShipmentTrackingRequest>
            <v1:ClientInfo>
                <v1:UserName>testingapi@aramex.com</v1:UserName>
                <v1:Password>R123456789$r</v1:Password>
                <v1:Version>1.0</v1:Version>
                <v1:AccountNumber>20016</v1:AccountNumber>
                <v1:AccountPin>331421</v1:AccountPin>
                <v1:AccountEntity>AMM</v1:AccountEntity>
                <v1:AccountCountryCode>JO</v1:AccountCountryCode>
            </v1:ClientInfo>
            <v1:Shipments>
                <arr:string>1Z12345E6205277936</arr:string>
            </v1:Shipments>
            <v1:GetLastTrackingUpdateOnly>false</v1:GetLastTrackingUpdateOnly>
        </v1:ShipmentTrackingRequest>
    </soap:Body>
</soap:Envelope>
"""

TrackingResponseXML = """<a></a>
"""

TrackingNonExistentResponseXML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <ShipmentTrackingResponse xmlns="http://ws.aramex.net/ShippingAPI/v1/">
         <Transaction i:nil="true" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <Notifications xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <HasErrors>false</HasErrors>
         <TrackingResults xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <NonExistingWaybills xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:string>1Z12345E6205277936</a:string>
         </NonExistingWaybills>
      </ShipmentTrackingResponse>
   </s:Body>
</s:Envelope>
"""

ErrorResponseXML = """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <ShipmentTrackingResponse xmlns="http://ws.aramex.net/ShippingAPI/v1/">
         <Transaction i:nil="true" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <Notifications xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <Notification>
               <Code>ERR01</Code>
               <Message>ClientInfo - Invalid username or password</Message>
            </Notification>
         </Notifications>
         <HasErrors>true</HasErrors>
         <TrackingResults xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <NonExistingWaybills xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
      </ShipmentTrackingResponse>
   </s:Body>
</s:Envelope>
"""
