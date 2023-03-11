
import unittest
from unittest.mock import patch, ANY
from tests.dpd.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["05308801410058"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = """<soapenv:Header>
      <ns:authentication>
         <delisId>KD*****</delisId>
         <authToken>*****</authToken>
         <messageLanguage>en_EN</messageLanguage>
      </ns:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <ns1:getTrackingData>
         <parcelLabelNumber>05308801410058</parcelLabelNumber>
      </ns1:getTrackingData>
   </soapenv:Body>
</soapenv:Envelope>
"""

TrackingResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soap:Body>
      <getTrackingDataResponse xmlns="http://dpd.com/common/service/types/ParcelLifeCycleService/2.0">
         <trackingresult>
            <shipmentInfo>
               <serviceDescription>
                  <label>
                     <content>Your DPD service:</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </label>
                  <content>
                     <content>DPD HOME</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </serviceDescription>
               <status>SHIPMENT</status>
               <statusHasBeenReached>false</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>false</showContactInfo>
            </shipmentInfo>
            <statusInfo>
               <status>BetweenDepots</status>
               <label>
                  <content>In transit</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel is at the parcel dispatch centre.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Puurs (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 10:41:25 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>BetweenDepots</status>
               <label>
                  <content>In transit</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel is at the parcel dispatch centre.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>true</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Puurs (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 11:32:00 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
         </trackingresult>
      </getTrackingDataResponse>
   </soap:Body>
</soap:Envelope>
"""

ErrorResponse = """<a></a>
"""


LoginRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/LoginService/2.0">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:getAuth>
         <delisId>KD*****</delisId>
         <password>*******</password>
         <messageLanguage>en_EN</messageLanguage>
      </ns:getAuth>
   </soapenv:Body>
</soapenv:Envelope>
"""

LoginResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soap:Body>
      <getAuthResponse xmlns="http://dpd.com/common/service/types/LoginService/2.1">
         <return>
            <delisId>SWSTEST</delisId>
            <customerUid>SWSTEST</customerUid>
            <authToken>GFadfGob14GWWgQcIldI6zYtuR7cyEHe2z6eWzb7BpFmcFvrzclRljlcV1OF</authToken>
            <depot>0530</depot>
            <authTokenExpires>2020-05-08T13:02:56.06</authTokenExpires>
         </return>
      </getAuthResponse>
   </soap:Body>
</soap:Envelope>
"""
