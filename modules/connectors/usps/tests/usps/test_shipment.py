import unittest
import urllib.parse
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway


class TestUSPSShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**shipment_cancel_data)

    def test_create_shipment_request(self):
        requests = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(requests.serialize(), ShipmentRequestXML)

    def test_create_cancel_shipment_request(self):
        requests = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(requests.serialize(), ShipmentCancelRequestXML)

    @patch("karrio.mappers.usps.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentRequestQuery)}",
        )

    @patch("karrio.mappers.usps.proxy.http", return_value="<a></a>")
    def test_cancel_shipment(self, http_mock):
        karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentCancelRequestQuery)}",
        )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.http") as mocks:
            mocks.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps.proxy.http") as mocks:
            mocks.return_value = ShipmentCancelResponseXML
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentCancelResponse)
            )


if __name__ == "__main__":
    unittest.main()


shipment_cancel_data = {
    "shipment_identifier": "123456789012",
}

shipment_data = {
    "shipper": {
        "company_name": "Horizon",
        "address_line1": "1309 S Agnew Avenue",
        "address_line2": "Apt 303",
        "city": "Oklahoma City",
        "postal_code": "73108",
        "country_code": "US",
        "person_name": "Lina Smith",
        "phone_number": "1234567890",
        "state_code": "OK",
    },
    "recipient": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [
        {
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 20.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {
                "insurance": 75.0,
            },
        }
    ],
    "service": "usps_priority_mail_express_flat_rate_boxes",
}


ParsedShipmentResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "shipment_identifier": "420063719270110101010XXXXXXXXX",
        "tracking_number": "420063719270110101010XXXXXXXXX",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=420063719270110101010XXXXXXXXX"
        },
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "operation": "Shipment Cancel",
        "success": True,
    },
    [],
]

ShipmentRequestXML = """<eVSRequest USERID="username">
    <Revision>1</Revision>
    <ImageParameters>
        <ImageParameter>6X4LABEL</ImageParameter>
        <LabelSequence>
            <PackageNumber>1</PackageNumber>
            <TotalPackages>1</TotalPackages>
        </LabelSequence>
    </ImageParameters>
    <FromName>Lina Smith</FromName>
    <FromFirm>Horizon</FromFirm>
    <FromAddress1>Apt 303</FromAddress1>
    <FromAddress2>1309 S Agnew Avenue</FromAddress2>
    <FromCity>Oklahoma City</FromCity>
    <FromState>OK</FromState>
    <FromZip5>73108</FromZip5>
    <FromZip4></FromZip4>
    <FromPhone>1234567890</FromPhone>
    <AllowNonCleansedOriginAddr></AllowNonCleansedOriginAddr>
    <ToName>Tall Tom</ToName>
    <ToFirm>ABC Corp.</ToFirm>
    <ToAddress1></ToAddress1>
    <ToAddress2>1098 N Fraser Street</ToAddress2>
    <ToCity>Georgetown</ToCity>
    <ToState>SC</ToState>
    <ToZip5>29440</ToZip5>
    <ToZip4></ToZip4>
    <ToPhone>8005554526</ToPhone>
    <AllowNonCleansedDestAddr>false</AllowNonCleansedDestAddr>
    <WeightInOunces>705.48</WeightInOunces>
    <ServiceType>PRIORITY EXPRESS</ServiceType>
    <Container>VARIABLE</Container>
    <Width>4.72</Width>
    <Length>2.36</Length>
    <Height>3.54</Height>
    <InsuredAmount>75</InsuredAmount>
    <ExtraServices>
        <ExtraService>100</ExtraService>
    </ExtraServices>
    <MID>847654321</MID>
    <SenderName>Lina Smith</SenderName>
    <RecipientName>Tall Tom</RecipientName>
    <ReceiptOption>SEPARATE PAGE</ReceiptOption>
    <ImageType>PDF</ImageType>
    <NonDeliveryOption>RETURN</NonDeliveryOption>
    <AltReturnAddress1></AltReturnAddress1>
</eVSRequest>
"""

ShipmentRequestQuery = {"API": "eVS", "XML": ShipmentRequestXML}

ShipmentCancelRequestXML = """<eVSCancelRequest USERID="username">
    <BarcodeNumber>123456789012</BarcodeNumber>
</eVSCancelRequest>
"""

ShipmentCancelRequestQuery = {"API": "eVSCancel", "XML": ShipmentCancelRequestXML}

ShipmentResponseXML = """<eVSResponse>
    <BarcodeNumber>420063719270110101010XXXXXXXXX</BarcodeNumber>
    <LabelImage>SUkqAAgAAAASAP4ABAAB</LabelImage>
    <ToName>TALL TOM</ToName>
    <ToFirm>ABC CORP.</ToFirm>
    <ToAddress1/>
    <ToAddress2>1098 N FRASER ST</ToAddress2>
    <ToCity>GEORGETOWN</ToCity>
    <ToState>SC</ToState>
    <ToZip5>29440</ToZip5>
    <ToZip4>2849</ToZip4>
    <Postnet>294402849981</Postnet>
    <RDC>0006</RDC>
    <Postage>8.76</Postage>
    <ExtraServices>
        <ExtraService>
            <ServiceID>120</ServiceID>
            <ServiceName>Adult Signature Restricted Delivery</ServiceName>
            <Price>6.90</Price>
        </ExtraService>
    </ExtraServices>
    <Zone>05</Zone>
    <CarrierRoute>C002</CarrierRoute>
    <PermitHolderName>Not Valid Test Label</PermitHolderName>
    <InductionType>ePostage</InductionType>
    <LogMessage/>
    <Commitment>
        <CommitmentName>3-Day</CommitmentName>
        <ScheduledDeliveryDate>2020-10-05</ScheduledDeliveryDate>
    </Commitment>
</eVSResponse>
"""

ShipmentCancelResponseXML = """<eVSCancelResponse>
    <BarcodeNumber>420902109411202901089817001111</BarcodeNumber>
    <Status>Cancelled</Status>
    <Reason>Order Cancelled Successfully</Reason>
</eVSCancelResponse>
"""
