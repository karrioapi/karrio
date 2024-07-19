import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestNationexTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Shipments/103882774?tracking=true",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.nationex.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["103882774"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "nationex",
            "carrier_name": "nationex",
            "delivered": False,
            "events": [
                {
                    "code": "DataReceived",
                    "date": "2019-08-24",
                    "description": "Data received",
                    "location": "St-Hubert",
                    "time": "14:15 PM",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.nationex.com/en/search?id=103882774",
                "note": "If no answer leave under the stairs",
                "package_weight": 5.5,
                "shipment_destination_country": "CA",
                "shipment_destination_postal_code": "H2H2S2",
                "shipment_origin_country": "CA",
                "shipment_origin_postal_code": "H2H2S2",
                "shipment_package_count": 2,
                "shipment_service": "Delivery",
                "shipping_date": "2021-03-30",
            },
            "meta": {"accounty_number": "165556", "reference": "CX4335"},
            "status": "in_transit",
            "tracking_number": "103882774",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "nationex",
            "carrier_name": "nationex",
            "code": 404,
            "details": {"tracking_number": "103882774"},
            "message": "ShipmentId 501399432 does not exist",
        }
    ],
]


TrackingRequest = ["103882774"]

TrackingResponse = """{
  "CustomerId": 113300,
  "ShipmentId": 103882774,
  "ExpeditionDate": "2021-03-30",
  "TotalParcels": 2,
  "TotalWeight": 5.5,
  "ShipmentStatus": "Creation",
  "ShipmentStatusFr": "Données reçues",
  "ShipmentStatusEn": "Data received",
  "StatusHistories": [
    {
      "ShipmentStatus": "DataReceived",
      "ShipmentStatusFr": "Données reçues",
      "ShipmentStatusEn": "Data received",
      "StatusDate": "2019-08-24T14:15:22Z",
      "LastLocation": "St-Hubert"
    }
  ],
  "ShipmentType": "Delivery",
  "ReferenceNumber": "CX4335",
  "Note": "If no answer leave under the stairs",
  "BillingAccount": 165556,
  "Sender": {
    "Contact": "Sonia",
    "AccountNumber": "NC33233",
    "AccountName": "Coffee Shop",
    "Address1": "433 Apple street",
    "Address2": "3rd floor",
    "PostalCode": "H2H2S2",
    "City": "Montreal",
    "ProvinceState": "QC",
    "Phone": 555123456,
    "SmsNotification": true,
    "EmailNotification": true,
    "NoCivic": 880,
    "Suite": 400,
    "StreetName": "Rue Claudia",
    "Email": "example@gmail.com"
  },
  "Destination": {
    "Contact": "Sonia",
    "AccountNumber": "NC33233",
    "AccountName": "Coffee Shop",
    "Address1": "433 Apple street",
    "Address2": "3rd floor",
    "PostalCode": "H2H2S2",
    "City": "Montreal",
    "ProvinceState": "QC",
    "Phone": 4183776671,
    "SmsNotification": true,
    "EmailNotification": true,
    "NoCivic": 880,
    "Suite": 400,
    "StreetName": "Rue Claudia",
    "Email": "example@gmail.com"
  },
  "Accessory": {
    "InsuranceAmount": 0,
    "FrozenProtection": true,
    "DangerousGoods": true,
    "SNR": true
  },
  "Parcels": [
    {
      "ParcelId": 50133944801,
      "ParcelNumber": 0,
      "ReferenceNumber": "JDI394",
      "NCV": true,
      "Weight": 0,
      "Status": "Creation",
      "StatusDescriptionEn": "In transit",
      "StatusDescriptionFr": "En transit",
      "EstimatedDeliveryDate": "2021-04-16",
      "EstimatedDeliveryTime": "13:15",
      "EstimatedDeliveryTimeFr": "Entre 12:45 et 13:45",
      "EstimatedDeliveryTimeEn": "Between 12:45 and 13:45",
      "EstimatedPercentageBeforeDelivery": 88,
      "Dimensions": {
        "Height": 6.5,
        "Length": 12,
        "Width": 8,
        "Cubing": 2.6
      },
      "History": [
        {
          "ParcelHistoryId": 3049373748,
          "ProcessedDate": "2021-03-31 13:31:00",
          "ExceptionId": 5,
          "CityDepot": "Blainville",
          "DescriptionFr": "Destinataire indisponible - Tentative de livraison le jour ouvrable suivant",
          "DescriptionEn": "Unavailable consignee - Delivery attempt on next business day",
          "PhotoId": 18840452,
          "SignatureId": 0,
          "Geocoding": {
            "Longitude": -78.098725,
            "Latitude": 48.575377
          }
        }
      ]
    }
  ],
  "ConsolId": 103882771,
  "IsInvoiced": false,
  "IsScanned": false,
  "IsConsolidated": false,
  "Photos": [
    {
      "Id": 18840452,
      "Data": "iVBORw0KGgoAAAANSUhEUgAAAZsAAACBCAYAAAAWohexAAAEtUlEQVR4Xu3VwQkAMAwDsXj/pTPF /dQBGhCG23kECBAgQCAWWPy/7wkQIECAwImNERAgQIBALiA2ObEDBAgQICA2NkCAAAECuYDY5MQO ECBAgIDY2AABAgQI5AJikxM7QIAAAQJiYwMECBAgkAuITU7sAAECBAiIjQ0QIECAQC4gNjmxAwQI ECAgNjZAgAABArmA2OTEDhAgQICA2NgAAQIECOQCYpMTO0CAAAECYmMDBAgQIJALiE1O7AABAgQI iI0NECBAgEAuIDY5sQMECBAgIDY2QIAAAQK5gNjkxA4QIECAgNjYAAECBAjkAmKTEztAgAABAmJj AwQIECCQC4hNTuwAAQIECIiNDRAgQIBALiA2ObEDBAgQICA2NkCAAAECuYDY5MQOECBAgIDY2AAB AgQI5AJikxM7QIAAAQJiYwMECBAgkAuITU7sAAECBAiIjQ0QIECAQC4gNjmxAwQIECAgNjZAgAAB ArmA2OTEDhAgQICA2NgAAQIECOQCYpMTO0CAAAECYmMDBAgQIJALiE1O7AABAgQIiI0NECBAgEAu IDY5sQMECBAgIDY2QIAAAQK5gNjkxA4QIECAgNjYAAECBAjkAmKTEztAgAABAmJjAwQIECCQC4hN TuwAAQIECIiNDRAgQIBALiA2ObEDBAgQICA2NkCAAAECuYDY5MQOECBAgIDY2AABAgQI5AJikxM7 QIAAAQJiYwMECBAgkAuITU7sAAECBAiIjQ0QIECAQC4gNjmxAwQIECAgNjZAgAABArmA2OTEDhAg QICA2NgAAQIECOQCYpMTO0CAAAECYmMDBAgQIJALiE1O7AABAgQIiI0NECBAgEAuIDY5sQMECBAg IDY2QIAAAQK5gNjkxA4QIECAgNjYAAECBAjkAmKTEztAgAABAmJjAwQIECCQC4hNTuwAAQIECIiN DRAgQIBALiA2ObEDBAgQICA2NkCAAAECuYDY5MQOECBAgIDY2AABAgQI5AJikxM7QIAAAQJiYwME CBAgkAuITU7sAAECBAiIjQ0QIECAQC4gNjmxAwQIECAgNjZAgAABArmA2OTEDhAgQICA2NgAAQIE COQCYpMTO0CAAAECYmMDBAgQIJALiE1O7AABAgQIiI0NECBAgEAuIDY5sQMECBAgIDY2QIAAAQK5 gNjkxA4QIECAgNjYAAECBAjkAmKTEztAgAABAmJjAwQIECCQC4hNTuwAAQIECIiNDRAgQIBALiA2 ObEDBAgQICA2NkCAAAECuYDY5MQOECBAgIDY2AABAgQI5AJikxM7QIAAAQJiYwMECBAgkAuITU7s AAECBAiIjQ0QIECAQC4gNjmxAwQIECAgNjZAgAABArmA2OTEDhAgQICA2NgAAQIECOQCYpMTO0CA AAECYmMDBAgQIJALiE1O7AABAgQIiI0NECBAgEAuIDY5sQMECBAgIDY2QIAAAQK5gNjkxA4QIECA gNjYAAECBAjkAmKTEztAgAABAmJjAwQIECCQC4hNTuwAAQIECIiNDRAgQIBALiA2ObEDBAgQICA2 NkCAAAECuYDY5MQOECBAgIDY2AABAgQI5AJikxM7QIAAAQJiYwMECBAgkAs8wZUAgqa0VWgAAAAA SUVORK5CYII="
    }
  ]
}
"""

ErrorResponse = """{
  "code": 404,
  "message": "ShipmentId 501399432 does not exist"
}
"""
