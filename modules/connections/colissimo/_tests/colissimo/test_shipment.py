
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestColissimoShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.colissimo.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.colissimo.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "chronopost_13",
    "shipper": {
        "company_name": "Chef Royale",
        "person_name": "Jean Dupont",
        "address_line1": "28 rue du Clair Bocage",
        "city": "La Seyne-sur-mer",
        "postal_code": "83500",
        "country_code": "FR",
        "phone_number": "+330447110494",
    },
    "recipient": {
        "company_name": "HautSide",
        "person_name": "Lucas Dupont",
        "address_line1": "72 rue Reine Elisabeth",
        "city": "Menton",
        "postal_code": "06500",
        "country_code": "FR",
    },
    "parcels": [
        {
            "height": 15,
            "length": 60.0,
            "width": 30,
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "label_type": "PDF",
    "reference": "Ref. 123456",
    "options": {"shipment_date": "2022-08-16"},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "colissimo",
        "carrier_name": "colissimo",
        "docs": {
            "label": ANY
        },
        "shipment_identifier": "EW112720413FR",
        "tracking_number": "EW112720413FR",
        "meta": {
            "carrier_tracking_link": "https://www.laposte.fr/outils/suivre-vos-envois?code=EW112720413FR"
        },
    },
    [],
]


ShipmentRequest = {
  "contractNumber": "string",
  "password": "string",
  "outputFormat": {
    "x": 0,
    "y": 0,
    "outputPrintingType": "string",
    "dematerialized": True,
    "returnType": "string",
    "printCODDocument": True
  },
  "letter": {
    "service": {
      "productCode": "string",
      "depositDate": "2019-08-24T14:15:22Z",
      "mailBoxPicking": True,
      "mailBoxPickingDate": "2019-08-24T14:15:22Z",
      "vatCode": 0,
      "vatPercentage": 0,
      "vatAmount": 0,
      "transportationAmount": 0,
      "totalAmount": 0,
      "orderNumber": "string",
      "commercialName": "string",
      "returnTypeChoice": 0,
      "reseauPostal": "string"
    },
    "parcel": {
      "parcelNumber": "string",
      "insuranceAmount": 0,
      "insuranceValue": 0,
      "recommendationLevel": "string",
      "weight": 0,
      "nonMachinable": True,
      "returnReceipt": True,
      "instructions": "string",
      "pickupLocationId": "string",
      "ftd": True,
      "ddp": True,
      "codamount": 0,
      "codcurrency": "string",
      "cod": True
    },
    "sender": {
      "senderParcelRef": "string",
      "address": {
        "companyName": "string",
        "lastName": "string",
        "firstName": "string",
        "line0": "string",
        "line1": "string",
        "line2": "string",
        "line3": "string",
        "countryCode": "string",
        "countryLabel": "string",
        "city": "string",
        "zipCode": "string",
        "phoneNumber": "string",
        "mobileNumber": "string",
        "doorCode1": "string",
        "doorCode2": "string",
        "intercom": "string",
        "email": "string",
        "language": "string",
        "stateOrProvinceCode": "string"
      }
    },
    "addressee": {
      "addresseeParcelRef": "string",
      "codeBarForReference": True,
      "serviceInfo": "string",
      "promotionCode": "string",
      "address": {
        "companyName": "string",
        "lastName": "string",
        "firstName": "string",
        "line0": "string",
        "line1": "string",
        "line2": "string",
        "line3": "string",
        "countryCode": "string",
        "countryLabel": "string",
        "city": "string",
        "zipCode": "string",
        "phoneNumber": "string",
        "mobileNumber": "string",
        "doorCode1": "string",
        "doorCode2": "string",
        "intercom": "string",
        "email": "string",
        "language": "string",
        "stateOrProvinceCode": "string"
      }
    },
    "features": {
      "printTrackingBarcode": True
    }
  },
  "fields": {
    "field": [
      {
        "key": "string",
        "value": "string"
      }
    ],
    "customField": [
      {
        "key": "string",
        "value": "string"
      }
    ]
  }
}

ShipmentResponse = """{
  "label": "string"
}
"""
