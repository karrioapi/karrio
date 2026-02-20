import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(
            **ReturnShipmentPayload
        )

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(
            self.ReturnShipmentRequest
        )
        serialized = request.serialize()

        # Verify the return label flag is set
        return_label = serialized[0].get("imageInfo", {}).get("returnLabel")
        print(return_label)
        self.assertTrue(return_label)

    def test_create_return_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentResponseJSON
            karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(
                url, f"{gateway.settings.server_url}/labels/v3/label"
            )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentResponseJSON
            parsed_response = (
                karrio.Shipment.create(self.ReturnShipmentRequest)
                .from_(gateway)
                .parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedReturnShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ReturnShipmentPayload = {
    "shipper": {
        "company_name": "Customer Inc",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "recipient": {
        "company_name": "Return Center",
        "address_line1": "1309 S Agnew Avenue",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "+1 123 456 7890",
        "state_code": "OK",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "usps_priority_mail",
    "is_return": True,
    "options": {
        "shipment_date": "2024-07-28",
    },
    "reference": "#Return 12345",
}

ParsedReturnShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "docs": {
            "invoice": ANY,
            "label": ANY,
            "extra_documents": [
                {
                    "category": "return_label",
                    "format": "PDF",
                    "base64": ANY,
                }
            ],
        },
        "label_type": "PDF",
        "meta": {
            "SKU": "DUXR0XXXXC06130",
            "postage": 18.76,
            "routingInformation": "42073108",
            "labelBrokerID": "LB00001",
        },
        "selected_rate": {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "service": "346",
            "total_charge": 18.76,
            "currency": "USD",
            "extra_charges": [
                {"amount": 18.76, "currency": "USD", "name": "Postage"},
            ],
            "meta": {
                "SKU": "DUXR0XXXXC06130",
                "zone": "06",
                "commitment": "3 Days",
            },
        },
        "return_shipment": {
            "tracking_number": "9234690361980900000999",
            "shipment_identifier": "9234690361980900000999",
            "tracking_url": "https://tools.usps.com/go/TrackConfirmAction?tLabels=9234690361980900000999",
            "meta": {"returnLabelBrokerID": "RLB00001"},
        },
        "shipment_identifier": "9234690361980900000142",
        "tracking_number": "9234690361980900000142",
    },
    [],
]

ReturnShipmentResponseJSON = """{
    "labelMetadata": {
        "labelAddress": {
            "streetAddress": "1309 S AGNEW AVE",
            "city": "OKLAHOMA CITY",
            "state": "OK",
            "ZIPCode": "73108"
        },
        "trackingNumber": "9234690361980900000142",
        "routingInformation": "42073108",
        "postage": 18.76,
        "extraServices": [],
        "fees": [],
        "zone": "06",
        "commitment": {
            "name": "3 Days",
            "scheduleDeliveryDate": "2024-07-31"
        },
        "weightUOM": "lb",
        "weight": 44.1,
        "dimensionalWeight": 0,
        "mailClass": "PRIORITY_MAIL",
        "processingCategory": "NON_MACHINABLE",
        "rateIndicator": "DR",
        "destinationEntryFacilityType": "NONE",
        "destinationEntryFacilityAddress": {},
        "SKU": "DUXR0XXXXC06130",
        "serviceTypeCode": "346",
        "labelBrokerID": "LB00001"
    },
    "labelImage": "JVBERi0xLjQKMSAwIG9iago8PC9UeXBlL0NhdGFsb2c+PgplbmRvYmoKJSVFT0YK",
    "receiptImage": "JVBERi0xLjQKMiAwIG9iago8PC9UeXBlL1JlY2VpcHQ+PgplbmRvYmoKJSVFT0YK",
    "returnLabelMetadata": {
        "trackingNumber": "9234690361980900000999",
        "labelBrokerID": "RLB00001"
    },
    "returnLabelImage": "JVBERi0xLjQKMyAwIG9iago8PC9UeXBlL1JldHVybj4+CmVuZG9iagoKJSVFT0YK"
}"""
