import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize()["05308801410058"], TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/soap/services/ParcelLifeCycleService/V2_0",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["05308801410058"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "delivered": False,
            "events": [
                {
                    "code": "ReturningFromDelivery",
                    "date": "2021-08-19",
                    "description": "After an unsuccessful delivery attempt the parcel is back at the recipient depot.",
                    "location": "Mechelen (BE)",
                    "time": "05:11 AM",
                },
                {
                    "code": "PickedUp",
                    "date": "2021-08-19",
                    "description": "DPD has received your parcel.",
                    "location": "Mechelen (BE)",
                    "time": "03:57 AM",
                },
                {
                    "code": "Courier",
                    "date": "2021-08-19",
                    "description": "The parcel has left the parcel delivery centre and is on its way to the consignee.",
                    "location": "Mechelen (BE)",
                    "time": "11:32 AM",
                },
                {
                    "code": "Courier",
                    "date": "2021-08-19",
                    "description": "The parcel has left the parcel delivery centre and is on its way to the consignee.",
                    "location": "Mechelen (BE)",
                    "time": "10:30 AM",
                },
                {
                    "code": "ParcelShop",
                    "date": "2021-08-18",
                    "description": "Delivered by driver to Pickup parcelshop",
                    "location": "Mechelen (BE)",
                    "time": "04:41 AM",
                },
                {
                    "code": "ParcelShop",
                    "date": "2021-08-18",
                    "description": "Delivered by driver to Pickup parcelshop",
                    "location": "Mechelen (BE)",
                    "time": "04:16 AM",
                },
                {
                    "code": "ParcelShop",
                    "date": "2021-08-18",
                    "description": "Delivered by driver to Pickup parcelshop",
                    "location": "Mechelen (BE)",
                    "time": "04:15 AM",
                },
                {
                    "code": "ParcelShop",
                    "date": "2021-08-18",
                    "description": "Delivered by driver to Pickup parcelshop",
                    "location": "Mechelen (BE)",
                    "time": "04:09 AM",
                },
                {
                    "code": "DeliveryFailure",
                    "date": "2021-08-18",
                    "description": "Unfortunately we have not been able to deliver your parcel.",
                    "location": "Aschaffenburg (DE)",
                    "time": "02:43 AM",
                },
                {
                    "code": "DeliveryFailure",
                    "date": "2021-08-18",
                    "description": "Unfortunately we have not been able to deliver your parcel.",
                    "location": "Mechelen (BE)",
                    "time": "02:43 AM",
                },
                {
                    "code": "Courier",
                    "date": "2021-08-18",
                    "description": "The parcel has left the parcel delivery centre and is on its way to the consignee.",
                    "location": "Aschaffenburg (DE)",
                    "time": "10:14 AM",
                },
                {
                    "code": "Courier",
                    "date": "2021-08-18",
                    "description": "The parcel has left the parcel delivery centre and is on its way to the consignee.",
                    "location": "Mechelen (BE)",
                    "time": "07:34 AM",
                },
                {
                    "code": "Depot",
                    "date": "2021-08-18",
                    "description": "At parcel delivery centre.",
                    "location": "Mechelen (BE)",
                    "time": "04:09 AM",
                },
                {
                    "code": "BetweenDepots",
                    "date": "2021-08-17",
                    "description": "The parcel is at the parcel dispatch centre.",
                    "location": "Puurs (BE)",
                    "time": "07:48 AM",
                },
                {
                    "code": "BetweenDepots",
                    "date": "2021-08-17",
                    "description": "The parcel is at the parcel dispatch centre.",
                    "location": "Puurs (BE)",
                    "time": "07:11 AM",
                },
            ],
            "status": "out_for_delivery",
            "tracking_number": "05308801410058",
            "info": {
                "carrier_tracking_link": "https://www.dpdgroup.com/be/mydpd/my-parcels/track?lang=en&parcelNumber=05308801410058"
            },
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dpd",
            "carrier_name": "dpd",
            "code": "DELICOM_ERR_AUTHENTICATION",
            "details": {"tracking_number": "05308801410058"},
            "message": "Authentication failure, check delisId and password.",
        }
    ],
]


TrackingRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" xmlns:ns1="http://dpd.com/common/service/types/ParcelLifeCycleService/2.0">
    <soapenv:Header>
        <ns:authentication>
            <delisId>KD*****</delisId>
            <authToken>****</authToken>
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
                     <content>DPD PARCELSHOP DELIVERY</content>
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
                  <content>8/17/2021 7:11:26 PM</content>
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
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Puurs (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/17/2021 7:48:00 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>Depot</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>At parcel delivery centre.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 4:09:55 AM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>Courier</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel has left the parcel delivery centre and is on its way to the consignee.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 7:34:34 AM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>Courier</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel has left the parcel delivery centre and is on its way to the consignee.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Aschaffenburg (DE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 10:14:00 AM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>DeliveryFailure</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Unfortunately we have not been able to deliver your parcel.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 2:43:31 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>DeliveryFailure</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Unfortunately we have not been able to deliver your parcel.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Aschaffenburg (DE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 2:43:31 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>ParcelShop</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Delivered by driver to Pickup parcelshop</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 4:09:35 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>ParcelShop</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Delivered by driver to Pickup parcelshop</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 4:15:56 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>ParcelShop</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Delivered by driver to Pickup parcelshop</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 4:16:57 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>ParcelShop</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>Delivered by driver to Pickup parcelshop</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/18/2021 4:41:00 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>Courier</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel has left the parcel delivery centre and is on its way to the consignee.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 10:30:00 AM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>Courier</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>The parcel has left the parcel delivery centre and is on its way to the consignee.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 11:32:51 AM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>PickedUp</status>
               <label>
                  <content>Parcel handed to DPD</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>DPD has received your parcel.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>false</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 3:57:33 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
            <statusInfo>
               <status>ReturningFromDelivery</status>
               <label>
                  <content>Parcel out for delivery</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </label>
               <description>
                  <content>
                     <content>After an unsuccessful delivery attempt the parcel is back at the recipient depot.</content>
                     <bold>false</bold>
                     <paragraph>false</paragraph>
                  </content>
               </description>
               <statusHasBeenReached>true</statusHasBeenReached>
               <isCurrentStatus>true</isCurrentStatus>
               <showContactInfo>true</showContactInfo>
               <location>
                  <content>Mechelen (BE)</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </location>
               <date>
                  <content>8/19/2021 5:11:26 PM</content>
                  <bold>true</bold>
                  <paragraph>false</paragraph>
               </date>
            </statusInfo>
         </trackingresult>
      </getTrackingDataResponse>
   </soap:Body>
</soap:Envelope>
"""

ErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soap:Body>
      <soap:Fault>
         <faultcode>soap:Server</faultcode>
         <faultstring>Fault occured</faultstring>
         <detail>
            <ns:authenticationFault xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0">
               <errorCode>DELICOM_ERR_AUTHENTICATION</errorCode>
               <errorMessage>Authentication failure, check delisId and password.</errorMessage>
            </ns:authenticationFault>
         </detail>
      </soap:Fault>
   </soap:Body>
</soap:Envelope>
"""
