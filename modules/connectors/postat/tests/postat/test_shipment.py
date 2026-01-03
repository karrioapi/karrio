"""PostAT carrier shipment tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestPostATShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = request.serialize()
        print(serialized)
        # Verify key elements in the XML request
        self.assertIn("ImportShipmentType", serialized)
        self.assertIn("Teststrasse", serialized)
        self.assertIn("Wien", serialized)

    def test_create_shipment(self):
        with patch("karrio.mappers.postat.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(mock.call_args)
            self.assertEqual(
                mock.call_args[1]["url"],
                gateway.settings.server_url
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.postat.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        serialized = request.serialize()
        print(serialized)
        # Verify key elements in the XML request
        self.assertIn("VoidShipmentType", serialized)
        self.assertIn("1000000500113230110301", serialized)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.postat.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            print(mock.call_args)
            self.assertEqual(
                mock.call_args[1]["url"],
                gateway.settings.server_url
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.postat.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "address_line1": "Musergasse 1",
        "city": "Wien",
        "postal_code": "1010",
        "country_code": "AT",
        "person_name": "Test Shipper",
        "company_name": "Test Company",
    },
    "recipient": {
        "address_line1": "Teststrasse 1",
        "city": "Wien",
        "postal_code": "1030",
        "country_code": "AT",
        "person_name": "Test Recipient",
        "email": "test@example.com",
    },
    "parcels": [{
        "weight": 17.0,
        "weight_unit": "KG",
    }],
    "service": "postat_standard_domestic",
}

ShipmentCancelPayload = {
    "shipment_identifier": "1000000500113230110301"
}

ShipmentResponse = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <ImportShipmentResponse xmlns="http://post.ondot.at">
         <ImportShipmentResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ColloRow>
               <ColloArticleList i:nil="true"/>
               <ColloCodeList>
                  <ColloCodeRow>
                     <Code>1000000500113230110301</Code>
                     <NumberTypeID>213</NumberTypeID>
                     <OUCarrierThirdPartyID>OEPAG-DEF</OUCarrierThirdPartyID>
                  </ColloCodeRow>
               </ColloCodeList>
               <Height i:nil="true"/>
               <Length i:nil="true"/>
               <Weight>17.0000</Weight>
               <Width i:nil="true"/>
            </ColloRow>
         </ImportShipmentResult>
         <zplLabelData i:nil="true" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"/>
         <pdfData>JVBERi0xLjQKJdP0zOEKMSAwIG9</pdfData>
      </ImportShipmentResponse>
   </s:Body>
</s:Envelope>"""

ShipmentCancelResponse = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <VoidShipmentResponse xmlns="http://post.ondot.at">
         <VoidShipmentResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <Success>true</Success>
            <ShipmentID/>
            <TrackingNumber>1000000500113230110301</TrackingNumber>
            <ErrorMessage i:nil="true"/>
            <ErrorCode i:nil="true"/>
         </VoidShipmentResult>
      </VoidShipmentResponse>
   </s:Body>
</s:Envelope>"""

ParsedShipmentResponse = [
    {
        "carrier_id": "postat",
        "carrier_name": "postat",
        "tracking_number": "1000000500113230110301",
        "shipment_identifier": "1000000500113230110301",
        "label_type": "PDF",
        "docs": {
            "label": "JVBERi0xLjQKJdP0zOEKMSAwIG9",
        },
        "meta": {
            "tracking_numbers": ["1000000500113230110301"],
        },
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "postat",
        "carrier_name": "postat",
        "success": True,
        "operation": "Cancel Shipment",
    },
    [],
]