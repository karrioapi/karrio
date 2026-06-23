"""DPD France return shipment tests (CreateReverseInverseShipmentWithLabelsBc)."""

import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

from .fixture import gateway


class TestDPDFranceReturnShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ReturnShipmentRequest = models.ShipmentRequest(**ReturnShipmentPayload)

    def test_create_return_shipment_request(self):
        request = gateway.mapper.create_return_shipment_request(self.ReturnShipmentRequest)
        self.assertEqual(request.serialize(), [ReturnShipmentRequestXML])

    def test_create_return_shipment(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.server_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/CreateReverseInverseShipmentWithLabelsBc",
            )

    def test_parse_return_shipment_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ReturnShipmentResponseXML
            parsed = karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedReturnShipmentResponse)

    def test_parse_return_shipment_error_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseXML
            parsed = karrio.Shipment.create(self.ReturnShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedReturnShipmentErrorResponse)


if __name__ == "__main__":
    unittest.main()


# is_return=True triggers Shipment.create to swap shipper/recipient and route
# to create_return_shipment. We define payload in the OUTBOUND orientation
# (shipper=original sender, recipient=customer); the swap inverts these so
# the SOAP envelope's <shipperaddress> is the customer and <receiveraddress>
# is the original sender — matching cargoNET's reverse-inverse semantics.
ReturnShipmentPayload = {
    "service": "dpd_france_classic",
    "is_return": True,
    "shipper": {
        "company_name": "Original Sender",
        "address_line1": "99 rue Origin",
        "city": "Lyon",
        "postal_code": "69001",
        "country_code": "FR",
    },
    "recipient": {
        "company_name": "Customer",
        "address_line1": "1 rue Retour",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
    },
    "parcels": [{"weight": 2.0, "weight_unit": "KG"}],
    "label_type": "PDF",
    "reference": "RET-001",
}


# Minimal valid PDF (single blank page) base64 — needed by lib.bundle_base64
# which validates EOF marker via PyPDF2.
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

ParsedReturnShipmentResponse = [
    {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "docs": {"label": _PDF_BASE64},
        "label_type": "PDF",
        "meta": {},
        "shipment_identifier": "250RETURN0001",
        "tracking_number": "%010RETBC001",
    },
    [],
]

ParsedReturnShipmentErrorResponse = [
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


# test_create_return_shipment_request invokes the mapper DIRECTLY, bypassing
# the address swap in Shipment.create. So the mapper sees the payload as-is
# (shipper=Original Sender, recipient=Customer) and emits matching addresses.
# When invoked via Shipment.create with is_return=True, the SDK swaps first.
ReturnShipmentRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:CreateReverseInverseShipmentWithLabelsBc>
            <imt:request>
                <imt:receiveraddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>75001</imt:zipCode>
                    <imt:city>Paris</imt:city>
                    <imt:street>1 rue Retour</imt:street>
                    <imt:name>Customer</imt:name>
                </imt:receiveraddress>
                <imt:shipperaddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>69001</imt:zipCode>
                    <imt:city>Lyon</imt:city>
                    <imt:street>99 rue Origin</imt:street>
                    <imt:name>Original Sender</imt:name>
                </imt:shipperaddress>
                <imt:customer_countrycode>250</imt:customer_countrycode>
                <imt:customer_centernumber>123</imt:customer_centernumber>
                <imt:customer_number>456789</imt:customer_number>
                <imt:weight>2.0</imt:weight>
                <imt:referencenumber>RET-001</imt:referencenumber>
                <imt:labelType>
                    <tns:type>PDF</tns:type>
                </imt:labelType>
            </imt:request>
        </imt:CreateReverseInverseShipmentWithLabelsBc>
    </soapenv:Body>
</soapenv:Envelope>
"""

ReturnShipmentResponseXML = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateReverseInverseShipmentWithLabelsBcResponse xmlns="http://www.cargonet.software">
      <CreateReverseInverseShipmentWithLabelsBcResult>
        <shipments>
          <ShipmentBc>
            <Shipment>
              <BarcodeId>250RETURN0001</BarcodeId>
              <BarcodeSource>1</BarcodeSource>
              <BarCode>%010RETBC001</BarCode>
            </Shipment>
            <Type>Reverse</Type>
          </ShipmentBc>
        </shipments>
        <labels>
          <Label>
            <type>PDF</type>
            <label>{_PDF_BASE64}</label>
          </Label>
        </labels>
      </CreateReverseInverseShipmentWithLabelsBcResult>
    </CreateReverseInverseShipmentWithLabelsBcResponse>
  </soap:Body>
</soap:Envelope>"""

ErrorResponseXML = """<?xml version="1.0"?>
<Error><ErrorId>IpPermissionDenied</ErrorId><ErrorMessage>Caller IP not whitelisted</ErrorMessage></Error>"""
