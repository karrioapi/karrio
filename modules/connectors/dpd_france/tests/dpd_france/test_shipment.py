"""DPD France shipment tests (create + cancel)."""

import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

from .fixture import gateway


class TestDPDFranceShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.MultiPieceShipmentRequest = models.ShipmentRequest(**MultiPieceShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), [ShipmentRequestXML])

    def test_create_shipment(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.server_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/CreateShipmentWithLabelsBc",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXML
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedShipmentResponse)

    def test_parse_shipment_error_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseXML
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedShipmentErrorResponse)

    def test_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        self.assertEqual(request.serialize(), ShipmentCancelRequestXML)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.server_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/TerminateShipment",
            )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseXML
            parsed = karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedShipmentCancelResponse)

    def test_create_multi_piece_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)
        self.assertEqual(request.serialize(), MultiPieceShipmentRequestXML)

    def test_create_multi_piece_shipment(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Shipment.create(self.MultiPieceShipmentRequest).from_(gateway)

            self.assertEqual(mock.call_count, 2)
            for call in mock.call_args_list:
                self.assertEqual(call[1]["url"], gateway.settings.server_url)
                self.assertEqual(
                    call[1]["headers"]["SOAPAction"],
                    "http://www.cargonet.software/CreateShipmentWithLabelsBc",
                )

    def test_parse_multi_piece_shipment_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.side_effect = [MultiPieceShipmentResponseXML1, MultiPieceShipmentResponseXML2]
            parsed = karrio.Shipment.create(self.MultiPieceShipmentRequest).from_(gateway).parse()
            shipment, messages = parsed

            self.assertEqual(messages, [])
            self.assertIsNotNone(shipment)
            self.assertEqual(shipment.tracking_number, "%010BARCODE001")
            self.assertEqual(shipment.shipment_identifier, "250000000000000000A1")
            self.assertEqual(shipment.label_type, "PDF")
            self.assertEqual(
                sorted(shipment.meta["tracking_numbers"]),
                ["%010BARCODE001", "%010BARCODE002"],
            )
            self.assertEqual(
                sorted(shipment.meta["shipment_identifiers"]),
                ["250000000000000000A1", "250000000000000000A2"],
            )
            # Bundled label is a real PDF; just confirm it's longer than either input
            self.assertGreater(len(shipment.docs.label), len(_PDF_BASE64))


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "dpd_france_classic",
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
}

ShipmentCancelPayload = {"shipment_identifier": "250123456789012345"}

ParsedShipmentResponse = [
    {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "docs": {"label": "JVBERi0xLjQKJeLjz9MK"},
        "label_type": "PDF",
        "meta": {},
        "shipment_identifier": "250123456789012345",
        "tracking_number": "%010250123456789012345001",
    },
    [],
]

ParsedShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_france",
            "carrier_name": "dpd_france",
            "code": "IpPermissionDenied",
            "details": {},
            "message": "Caller IP not whitelisted",
        }
    ],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:CreateShipmentWithLabelsBc>
            <imt:request>
                <imt:receiveraddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>06500</imt:zipCode>
                    <imt:city>Menton</imt:city>
                    <imt:street>72 rue Reine Elisabeth</imt:street>
                    <imt:name>HautSide</imt:name>
                </imt:receiveraddress>
                <imt:shipperaddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>83500</imt:zipCode>
                    <imt:city>La Seyne-sur-mer</imt:city>
                    <imt:street>28 rue du Clair Bocage</imt:street>
                    <imt:name>Chef Royale</imt:name>
                    <imt:phoneNumber>+330447110494</imt:phoneNumber>
                </imt:shipperaddress>
                <imt:customer_countrycode>250</imt:customer_countrycode>
                <imt:customer_centernumber>123</imt:customer_centernumber>
                <imt:customer_number>456789</imt:customer_number>
                <imt:weight>5.0</imt:weight>
                <imt:referencenumber>Ref. 123456</imt:referencenumber>
                <imt:labelType>
                    <tns:type>PDF</tns:type>
                </imt:labelType>
            </imt:request>
        </imt:CreateShipmentWithLabelsBc>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentCancelRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:TerminateShipment>
            <imt:request>
                <imt:customer>
                    <imt:centernumber>123</imt:centernumber>
                    <imt:number>456789</imt:number>
                    <imt:countrycode>250</imt:countrycode>
                </imt:customer>
                <BarcodeSource xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
                <imt:BarcodeId>250123456789012345</imt:BarcodeId>
            </imt:request>
        </imt:TerminateShipment>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateShipmentWithLabelsBcResponse xmlns="http://www.cargonet.software">
      <CreateShipmentWithLabelsBcResult>
        <shipments>
          <ShipmentBc>
            <Shipment>
              <BarcodeId>250123456789012345</BarcodeId>
              <BarcodeSource>1</BarcodeSource>
              <BarCode>%010250123456789012345001</BarCode>
            </Shipment>
            <Type>Standard</Type>
          </ShipmentBc>
        </shipments>
        <labels>
          <Label>
            <type>PDF</type>
            <label>JVBERi0xLjQKJeLjz9MK</label>
          </Label>
        </labels>
      </CreateShipmentWithLabelsBcResult>
    </CreateShipmentWithLabelsBcResponse>
  </soap:Body>
</soap:Envelope>"""

ShipmentCancelResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TerminateShipmentResponse xmlns="http://www.cargonet.software"/>
  </soap:Body>
</soap:Envelope>"""

ErrorResponseXML = """<?xml version="1.0"?>
<Error><ErrorId>IpPermissionDenied</ErrorId><ErrorMessage>Caller IP not whitelisted</ErrorMessage></Error>"""


# Minimal valid PDF (single blank page) base64 — used to verify bundle_base64
# can merge real PDFs in multi-piece tests.
_PDF_BASE64 = (
    "JVBERi0xLjMKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0"
    "IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoK"
    "MyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoK"
    "PDwKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PAo+PgovTWVkaWFCb3ggWyAwIDAgNzIgNzIgXQov"
    "UGFyZW50IDEgMCBSCj4+CmVuZG9iagp4cmVmCjAgNQowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAw"
    "MDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA3NCAwMDAwMCBuIAowMDAwMDAwMTE0IDAwMDAwIG4gCjAw"
    "MDAwMDAxNjMgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA1Ci9Sb290IDMgMCBSCi9JbmZvIDIg"
    "MCBSCj4+CnN0YXJ0eHJlZgoyNTEKJSVFT0YK"
)

MultiPieceShipmentPayload = {
    "service": "dpd_france_classic",
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
        {"weight": 5.0, "weight_unit": "KG"},
        {"weight": 3.5, "weight_unit": "KG"},
    ],
    "label_type": "PDF",
    "reference": "Ref. MULTI",
}


def _multi_envelope(weight: str) -> str:
    return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:CreateShipmentWithLabelsBc>
            <imt:request>
                <imt:receiveraddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>06500</imt:zipCode>
                    <imt:city>Menton</imt:city>
                    <imt:street>72 rue Reine Elisabeth</imt:street>
                    <imt:name>HautSide</imt:name>
                </imt:receiveraddress>
                <imt:shipperaddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>83500</imt:zipCode>
                    <imt:city>La Seyne-sur-mer</imt:city>
                    <imt:street>28 rue du Clair Bocage</imt:street>
                    <imt:name>Chef Royale</imt:name>
                    <imt:phoneNumber>+330447110494</imt:phoneNumber>
                </imt:shipperaddress>
                <imt:customer_countrycode>250</imt:customer_countrycode>
                <imt:customer_centernumber>123</imt:customer_centernumber>
                <imt:customer_number>456789</imt:customer_number>
                <imt:weight>{weight}</imt:weight>
                <imt:referencenumber>Ref. MULTI</imt:referencenumber>
                <imt:labelType>
                    <tns:type>PDF</tns:type>
                </imt:labelType>
            </imt:request>
        </imt:CreateShipmentWithLabelsBc>
    </soapenv:Body>
</soapenv:Envelope>
"""


MultiPieceShipmentRequestXML = [_multi_envelope("5.0"), _multi_envelope("3.5")]


def _multi_response(barcode_id: str, barcode: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateShipmentWithLabelsBcResponse xmlns="http://www.cargonet.software">
      <CreateShipmentWithLabelsBcResult>
        <shipments>
          <ShipmentBc>
            <Shipment>
              <BarcodeId>{barcode_id}</BarcodeId>
              <BarcodeSource>1</BarcodeSource>
              <BarCode>{barcode}</BarCode>
            </Shipment>
            <Type>Standard</Type>
          </ShipmentBc>
        </shipments>
        <labels>
          <Label>
            <type>PDF</type>
            <label>{_PDF_BASE64}</label>
          </Label>
        </labels>
      </CreateShipmentWithLabelsBcResult>
    </CreateShipmentWithLabelsBcResponse>
  </soap:Body>
</soap:Envelope>"""


MultiPieceShipmentResponseXML1 = _multi_response("250000000000000000A1", "%010BARCODE001")
MultiPieceShipmentResponseXML2 = _multi_response("250000000000000000A2", "%010BARCODE002")
