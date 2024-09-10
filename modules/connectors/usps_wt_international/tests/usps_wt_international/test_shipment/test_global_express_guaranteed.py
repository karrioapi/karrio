import unittest
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest
from ..fixture import gateway


class TestUSPSGXGShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        requests = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(requests.serialize(), ShipmentRequestXML)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps_wt_international.proxy.http") as mocks:
            mocks.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


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
        "company_name": "Coffee Five",
        "address_line1": "R. da Quitanda, 86 - quiosque 01",
        "city": "Centro",
        "postal_code": "29440",
        "country_code": "BR",
        "person_name": "John",
        "phone_number": "8005554526",
        "state_code": "Rio de Janeiro",
    },
    "parcels": [
        {
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 2.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "usps_global_express_guaranteed_non_document_non_rectangular",
    "customs": {
        "content_type": "merchandise",
        "incoterm": "DDU",
        "invoice": "INV-040903",
        "commodities": [
            {
                "weight": 2,
                "weight_unit": "KG",
                "quantity": 1,
                "sku": "XXXXX0000123",
                "value_amount": 30,
                "value_currency": "USD",
                "origin_country": "US",
            }
        ],
        "duty": {
            "paid_by": "recipient",
            "currency": "USD",
            "declared_value": 60,
        },
        "certify": True,
        "signer": "Admin",
        "options": {
            "license_number": "LIC-24356879",
            "certificate_number": "CERT-97865342",
        },
    },
    "options": {"shipment_date": "2021-05-15", "insurance": 75.0},
}


ParsedShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "shipment_identifier": "8300100690",
        "tracking_number": "8300100690",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=8300100690"
        },
    },
    [],
]


ShipmentRequestXML = """<eVSGXGGetLabelRequest USERID="username" PASSWORD="password">
    <Revision>2</Revision>
    <FromFirstName>Admin</FromFirstName>
    <FromLastName>Lina Smith</FromLastName>
    <FromFirm>Horizon</FromFirm>
    <FromAddress1>1309 S Agnew Avenue</FromAddress1>
    <FromAddress2>Apt 303</FromAddress2>
    <FromCity>Oklahoma City</FromCity>
    <FromState>Oklahoma</FromState>
    <FromZIP5>73108</FromZIP5>
    <FromPhone>1234567890</FromPhone>
    <ToLastName>John</ToLastName>
    <ToFirm>Coffee Five</ToFirm>
    <ToAddress1>01 R. da Quitanda, 86 - quiosque</ToAddress1>
    <ToAddress2></ToAddress2>
    <ToPostalCode>29440</ToPostalCode>
    <ToPhone>8005554526</ToPhone>
    <ToDPID>000</ToDPID>
    <ToProvince>Rio de Janeiro</ToProvince>
    <Container>PACKAGE</Container>
    <ContentType>NON-DOC</ContentType>
    <ShippingContents>
        <ItemDetail>
            <Description>N/A</Description>
            <Commodity>N/A</Commodity>
            <Quantity>1</Quantity>
            <UnitValue>30</UnitValue>
            <NetPounds>4.41</NetPounds>
            <NetOunces>70.55</NetOunces>
            <HSTariffNumber>XXXXX0000123</HSTariffNumber>
            <CountryofManufacture>United States</CountryofManufacture>
        </ItemDetail>
    </ShippingContents>
    <PurposeOfShipment>MERCHANDISE</PurposeOfShipment>
    <Agreement>N</Agreement>
    <InsuredValue>75.0</InsuredValue>
    <GrossPounds>4.41</GrossPounds>
    <GrossOunces>70.55</GrossOunces>
    <Length>2.36</Length>
    <Width>4.72</Width>
    <Height>3.54</Height>
    <InvoiceNumber>INV-040903</InvoiceNumber>
    <TermsDelivery>DDU</TermsDelivery>
    <CountryUltDest>Brazil</CountryUltDest>
    <ImageType>PDF</ImageType>
    <ShipDate>05/15/2021</ShipDate>
    <Machinable>false</Machinable>
    <DestinationRateIndicator>I</DestinationRateIndicator>
    <MID>847654321</MID>
</eVSGXGGetLabelRequest>
"""

ShipmentRequestQuery = {"API": "eVSGXGGetLabel", "XML": ShipmentRequestXML}

ShipmentResponseXML = """<eVSGXGGetLabelResponse>
    <Postage>5.00</Postage>
    <CommodityGuarantee>
        <CommodityType>W</CommodityType>
        <GuaranteeDate>10/22/2020</GuaranteeDate>
    </CommodityGuarantee>
    <Insurance/>
    <USPSBarcodeNumber>8300100690</USPSBarcodeNumber>
    <FedExBarcodeNumber>898300100697</FedExBarcodeNumber>
    <LabelImage>SUkqAAgAAAASAP4ABAAB...</LabelImage>
    <LabelImagePage2></LabelImagePage2>
    <LabelImagePage3></LabelImagePage3>
    <LabelImagePage4></LabelImagePage4>
    <CIImage></CIImage>
    <CIImagePage2></CIImagePage2>
    <CIImagePage3></CIImagePage3>
    <CIImagePage4></CIImagePage4>
    <InsuranceFee>0.00</InsuranceFee>
    <DimensionalWeight>4</DimensionalWeight>
    <LogMessage/>
    <RemainingBarcodes>989</RemainingBarcodes>
</eVSGXGGetLabelResponse>
"""
