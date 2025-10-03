import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDTDCTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [TrackingResponse]
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.tracking_server_url}/dtdc-api/rest/JSONCnTrk/getTrackDetails",
            )

    def test_tracking_response_parsing(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [TrackingResponse]
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_tracking_error_response_parsing(self):
        with patch("karrio.mappers.dtdc.proxy.lib.request") as mock:
            mock.side_effect = [ErrorTrackingResponse]
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()

TrackingPayload = {"tracking_numbers": ["7X9150223"]}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dtdc",
            "carrier_name": "dtdc",
            "delivered": True,
            "events": [
                {
                    "code": "DLV",
                    "date": "2017-06-21",
                    "description": "Delivered",
                    "location": "MUMBAI APEX",
                    "time": "16:14",
                },
                {
                    "code": "OUTDLV",
                    "date": "2017-06-21",
                    "description": "Out For Delivery",
                    "location": "MUMBAI APEX",
                    "time": "16:11",
                },
                {
                    "code": "OBMD",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "16:03",
                },
                {
                    "code": "IBMD",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "16:03",
                },
                {
                    "code": "IPMF",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "16:03",
                },
                {
                    "code": "CDIN",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:55",
                },
                {
                    "code": "CDOUT",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:46",
                },
                {
                    "code": "IBMD",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:33",
                },
                {
                    "code": "OPMF",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:33",
                },
                {
                    "code": "OBMD",
                    "date": "2017-06-21",
                    "description": "In Transit",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:33",
                },
                {
                    "code": "BKD",
                    "date": "2017-06-21",
                    "description": "Booked",
                    "location": "BANGALORE SURFACE APEX",
                    "time": "15:30",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.dtdc.com/tracking?trackid=B32242001",
                "shipment_service": "AVENUE ROAD",
                "customer_name": "AVENUE ROAD",
                "shipment_package_count": 1,
                "package_weight": 0.1,
            },
            "status": "delivered",
            "tracking_number": "B32242001",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dtdc",
            "carrier_name": "dtdc",
            "code": 401,
            "details": {},
            "message": "Unauthorized: Authentication token was either missing or "
            "invalid.",
        }
    ],
]

TrackingRequest = [{"strcnno": "7X9150223"}]

TrackingResponse = """{
  "statusCode": 200,
  "statusFlag": true,
  "status": "SUCCESS",
  "errorDetails": null,
  "trackHeader": {
    "strShipmentNo": "B32242001",
    "strRefNo": "",
    "strCNType": "CP",
    "strCNTypeCode": "BF014",
    "strCNTypeName": "AVENUE ROAD",
    "strCNProduct": "LITE",
    "strModeCode": "",
    "strMode": "",
    "strCNProdCODFOD": "",
    "strOrigin": "BANGALORE",
    "strOriginRemarks": "Booked By",
    "strBookedDate": "21062017",
    "strBookedTime": "15:30:25",
    "strPieces": "1",
    "strWeightUnit": "KG",
    "strWeight": "0.1000",
    "strDestination": "MUMBAI",
    "strStatus": "Delivered",
    "strStatusTransOn": "21062017",
    "strStatusTransTime": "1614",
    "strStatusRelCode": "",
    "strStatusRelName": "",
    "strRemarks": "SIGN",
    "strNoOfAttempts": "1",
    "strRtoNumber": ""
  },
  "trackDetails": [
    {
      "strCode": "BKD",
      "strAction": "Booked",
      "strManifestNo": "",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "",
      "strActionDate": "21062017",
      "strActionTime": "1530",
      "sTrRemarks": ""
    },
    {
      "strCode": "OBMD",
      "strAction": "In Transit",
      "strManifestNo": "B7701202",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1533",
      "sTrRemarks": ""
    },
    {
      "strCode": "OPMF",
      "strAction": "In Transit",
      "strManifestNo": "B7701203",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1533",
      "sTrRemarks": ""
    },
    {
      "strCode": "IBMD",
      "strAction": "In Transit",
      "strManifestNo": "B7701202",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1533",
      "sTrRemarks": ""
    },
    {
      "strCode": "CDOUT",
      "strAction": "In Transit",
      "strManifestNo": "",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1546",
      "sTrRemarks": ""
    },
    {
      "strCode": "CDIN",
      "strAction": "In Transit",
      "strManifestNo": "",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1555",
      "sTrRemarks": ""
    },
    {
      "strCode": "IPMF",
      "strAction": "In Transit",
      "strManifestNo": "B7701203",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1603",
      "sTrRemarks": "0.00"
    },
    {
      "strCode": "IBMD",
      "strAction": "In Transit",
      "strManifestNo": "B7701202",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1603",
      "sTrRemarks": ""
    },
    {
      "strCode": "OBMD",
      "strAction": "In Transit",
      "strManifestNo": "B7701202",
      "strOrigin": "BANGALORE SURFACE APEX",
      "strDestination": "MUMBAI APEX",
      "strActionDate": "21062017",
      "strActionTime": "1603",
      "sTrRemarks": ""
    },
    {
      "strCode": "OUTDLV",
      "strAction": "Out For Delivery",
      "strManifestNo": "",
      "strOrigin": "MUMBAI APEX",
      "strDestination": "",
      "strActionDate": "21062017",
      "strActionTime": "1611",
      "sTrRemarks": ""
    },
    {
      "strCode": "DLV",
      "strAction": "Delivered",
      "strManifestNo": "",
      "strOrigin": "MUMBAI APEX",
      "strDestination": "",
      "strActionDate": "21062017",
      "strActionTime": "1614",
      "sTrRemarks": "SIGN"
    }
  ]
}
"""

ErrorTrackingResponse = """{
	"timestamp": "2025-08-10T02:38:24.802+00:00",
	"status": 401,
	"error": "Unauthorized",
	"message": "Unauthorized: Authentication token was either missing or invalid.",
	"path": "/dtdc-tracking-api/dtdc-api/rest/JSONCnTrk/getTrackDetails"
}
"""
