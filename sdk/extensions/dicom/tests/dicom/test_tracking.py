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

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.dicom.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/tracking/1Z12345E6205277936",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dicom.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dicom.proxy.http") as mock:
            mock.return_value = ErrorResponseJSON
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
    [
        {
            "carrier_id": "dicom",
            "carrier_name": "dicom",
            "events": [
                {
                    "code": "Delivered",
                    "date": "2021-02-10",
                    "description": "Shipper Release NSR",
                    "location": "MTL",
                    "time": "04:27",
                }
            ],
            "tracking_number": "W1234567",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dicom",
            "carrier_name": "dicom",
            "message": "Authorization has been denied for this request.",
        }
    ],
]

TrackingRequestJSON = ["1Z12345E6205277936"]

TrackingResponseJSON = """{
  "custRefNum": "string",
  "activities": [
    {
      "activityDate": "2021-02-10T04:27:31Z",
      "createDate": "2021-02-10T04:27:31Z",
      "status": "Delivered",
      "statusDetail": "Shipper Release NSR",
      "code": "DL",
      "codeDetail": "NI",
      "group": "DL",
      "additionalInformation": "Package did not need a signature.",
      "terminal": "MTL",
      "latitude": "45.46770054493765",
      "longitude": "-73.71983885765076",
      "height": "10.5",
      "weight": "5.0",
      "width": "5.0",
      "length": "5.5",
      "parcelId": "2"
    }
  ],
  "activityImages": [
    {
      "imageDate": "2021-02-10T04:27:31Z",
      "url": "https://www.dicom.com/",
      "clientName": "Georges",
      "imageType": "POD"
    }
  ],
  "isAuthorized": true,
  "id": "78852145",
  "trackingNumber": "W1234567",
  "category": "Parcel",
  "paymentType": "Prepaid",
  "billingAccount": "400040",
  "note": "This is a note for the driver",
  "status": "0",
  "direction": "CA",
  "sender": {
    "id": "4658",
    "addressLine1": "10500 mystreet",
    "addressLine2": "Suite 10",
    "streetNumber": "10500",
    "streetType": "AVE",
    "streetName": "mystreet",
    "streetDirection": "N",
    "suite": "10",
    "city": "Montreal",
    "provinceCode": "QC",
    "postalCode": "H9P2T7",
    "countryCode": "CA",
    "customerName": "Test Company",
    "customerNickName": "string",
    "contact": {
      "language": "en",
      "email": "example@dicom.com",
      "department": "IT",
      "telephone": "4501234567",
      "extension": "320",
      "fullName": "FullName Contact"
    }
  },
  "consignee": {
    "id": "4658",
    "addressLine1": "10500 mystreet",
    "addressLine2": "Suite 10",
    "streetNumber": "10500",
    "streetType": "AVE",
    "streetName": "mystreet",
    "streetDirection": "N",
    "suite": "10",
    "city": "Montreal",
    "provinceCode": "QC",
    "postalCode": "H9P2T7",
    "countryCode": "CA",
    "customerName": "Test Company",
    "customerNickName": "string",
    "contact": {
      "language": "en",
      "email": "example@dicom.com",
      "department": "IT",
      "telephone": "4501234567",
      "extension": "320",
      "fullName": "FullName Contact"
    }
  },
  "unitOfMeasurement": "K",
  "parcels": [
    {
      "id": "1",
      "parcelType": "Box",
      "quantity": "3",
      "weight": "5",
      "length": "5",
      "depth": "5",
      "width": "5",
      "note": "Special instruction...",
      "status": 0,
      "FCA_Class": "100.00",
      "hazmat": {
        "number": "100",
        "phone": "4510214786"
      },
      "requestReturnLabel": true,
      "returnWaybill": "Q1234568"
    }
  ],
  "surcharges": [
    {
      "id": "4658723",
      "value": "Heating",
      "type": "HEAT",
      "name": "Heating",
      "amount": 0
    }
  ],
  "createDate": "2021-02-10T04:27:31Z",
  "updateDate": "2021-02-10T04:27:31Z",
  "deliveryType": "GRD",
  "references": [
    {
      "type": "INV",
      "code": "123"
    }
  ],
  "returnAddress": {
    "id": "4658",
    "addressLine1": "10500 mystreet",
    "addressLine2": "Suite 10",
    "streetNumber": "10500",
    "streetType": "AVE",
    "streetName": "mystreet",
    "streetDirection": "N",
    "suite": "10",
    "city": "Montreal",
    "provinceCode": "QC",
    "postalCode": "H9P2T7",
    "countryCode": "CA",
    "customerName": "Test Company",
    "customerNickName": "string",
    "contact": {
      "language": "en",
      "email": "example@dicom.com",
      "department": "IT",
      "telephone": "4501234567",
      "extension": "320",
      "fullName": "FullName Contact"
    }
  },
  "appointment": {
    "ID": "string",
    "type": "Scheduled",
    "date": "2021-02-10T04:27:31Z",
    "time": "15:00",
    "phone": "5142648798"
  },
  "promoCodes": [
    {
      "code": "PROMO-465871"
    }
  ],
  "internationalDetails": {
    "currency": "USD",
    "exchangeRate": 0,
    "totalRetailValue": "500",
    "dutyBilling": "N",
    "descriptionOfGoods": "Floor Cleaner",
    "importerOfRecord": {
      "id": "4658",
      "addressLine1": "10500 mystreet",
      "addressLine2": "Suite 10",
      "streetNumber": "10500",
      "streetType": "AVE",
      "streetName": "mystreet",
      "streetDirection": "N",
      "suite": "10",
      "city": "Montreal",
      "provinceCode": "QC",
      "postalCode": "H9P2T7",
      "countryCode": "CA",
      "customerName": "Test Company",
      "customerNickName": "string",
      "contact": {
        "language": "en",
        "email": "example@dicom.com",
        "department": "IT",
        "telephone": "4501234567",
        "extension": "320",
        "fullName": "FullName Contact"
      }
    },
    "broker": {
      "id": "45612456",
      "href": "",
      "otherBroker": "Levingstone",
      "CSA_BusinessNumber": "789"
    },
    "purpose": "COM",
    "products": [
      {
        "id": "123",
        "Quantity": 1
      }
    ],
    "borderStatus": "LVS",
    "isDicomBroker": true
  },
  "pickupDate": "2021-02-10T04:27:31Z"
}
"""

ErrorResponseJSON = """{
  "Message": "Authorization has been denied for this request."
}
"""
