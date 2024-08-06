import unittest
import urllib.parse
from unittest.mock import patch, ANY
import karrio
import karrio.lib as lib
import karrio.core.models as models
from ..fixture import gateway


class TestUSPSPriorityExpressShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        requests = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(requests.serialize(), ShipmentRequestXML)

    @patch("karrio.mappers.usps_wt_international.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        expected_url = f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentRequestQuery)}"
        self.assertEqual(
            urllib.parse.unquote(url),
            urllib.parse.unquote(expected_url),
        )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps_wt_international.proxy.http") as mocks:
            mocks.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


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
            "options": {"usps_insurance_express_mail_international": 50.0},
        }
    ],
    "service": "usps_priority_mail_express_international_legal_flat_rate_envelope",
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
    "options": {"shipment_date": "2021-05-15"},
}


ParsedShipmentResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "shipment_identifier": "EB321424860US",
        "tracking_number": "EB321424860US",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=EB321424860US"
        },
    },
    [],
]


ShipmentRequestXML = """<eVSExpressMailIntlRequest USERID="username" PASSWORD="password">
    <Revision>2</Revision>
    <ImageParameters>
        <ImageParameter>6X4LABEL</ImageParameter>
    </ImageParameters>
    <FromFirstName>Admin</FromFirstName>
    <FromLastName>Lina Smith</FromLastName>
    <FromFirm>Horizon</FromFirm>
    <FromAddress1>Apt 303</FromAddress1>
    <FromAddress2>1309 S Agnew Avenue</FromAddress2>
    <FromCity>Oklahoma City</FromCity>
    <FromZip5>73108</FromZip5>
    <FromZip4></FromZip4>
    <FromPhone>1234567890</FromPhone>
    <ToFirstName>John</ToFirstName>
    <ToLastName>John</ToLastName>
    <ToFirm>Coffee Five</ToFirm>
    <ToAddress1></ToAddress1>
    <ToAddress2>R. da Quitanda, 86 - quiosque 01</ToAddress2>
    <ToCity>Centro</ToCity>
    <ToProvince>Rio de Janeiro</ToProvince>
    <ToCountry>Brazil</ToCountry>
    <ToPostalCode>29440</ToPostalCode>
    <ToPhone>8005554526</ToPhone>
    <NonDeliveryOption>RETURN</NonDeliveryOption>
    <RedirectZip4></RedirectZip4>
    <ShippingContents>
        <ItemDetail>
            <Description>N/A</Description>
            <Quantity>1</Quantity>
            <Value>30.0</Value>
            <NetPounds>4.41</NetPounds>
            <NetOunces>70.549999999999997</NetOunces>
            <HSTariffNumber>XXXXX0000123</HSTariffNumber>
            <CountryOfOrigin>United States</CountryOfOrigin>
        </ItemDetail>
    </ShippingContents>
    <InsuredAmount>50</InsuredAmount>
    <GrossPounds>4.41</GrossPounds>
    <GrossOunces>70.549999999999997</GrossOunces>
    <ContentType>MERCHANDISE</ContentType>
    <ContentTypeOther>N/A</ContentTypeOther>
    <Agreement>Y</Agreement>
    <LicenseNumber>LIC-24356879</LicenseNumber>
    <CertificateNumber>CERT-97865342</CertificateNumber>
    <InvoiceNumber>INV-040903</InvoiceNumber>
    <ImageType>PDF</ImageType>
    <ImageLayout>ALLINONEFILE</ImageLayout>
    <LabelDate>05/15/2021</LabelDate>
    <Length>2.36</Length>
    <Width>4.72</Width>
    <Height>3.54</Height>
    <Machinable>false</Machinable>
    <DestinationRateIndicator>I</DestinationRateIndicator>
    <MID>847654321</MID>
</eVSExpressMailIntlRequest>
"""

ShipmentRequestQuery = {"API": "eVSExpressMailIntl", "XML": ShipmentRequestXML}

ShipmentResponseXML = """<eVSExpressMailIntlResponse>
    <Postage>67.84</Postage>
    <TotalValue>15.00</TotalValue>
    <SDRValue>10.83</SDRValue>
    <BarcodeNumber>EB321424860US</BarcodeNumber>
    <LabelImage>SUkqAAgAAAASAP4ABAAB...</LabelImage>
    <Page2Image>.....removed.....</Page2Image>
    <Page3Image>.....removed.....</Page3Image>
    <Page4Image>.....removed.....</Page4Image>
    <Page5Image>.....removed.....</Page5Image>
    <Page6Image></Page6Image>
    <Prohibitions>Banknotes; currency notes; paper money; securities payable to bearer; and traveler's checks. Coins; manufactured and unmanufactured platinum, gold, and silver; precious stones; jewels; expensive jewelry; and other valuable articles. Commercial samples that promote tobacco products or smoking-related merchandise. Commercial shipments that contain cigarettes, cigarillos, cigars, loose and packaged tobacco, pipes, and other smoking devices. Items that are fragile, either by nature or due to inadequate packing, that could cause harm to individuals or equipment. Medicines whose formulas are not listed in the official pharmacopeias or not licensed by the Brazilian Department of Public Health. Perishable infectious biological substances. Perishable noninfectious biological substances. Playing cards. Poniards, stilettos, poniard blades; canes, umbrellas, or any other articles containing swords, daggers, or guns; handcuffs, and blackjacks. Primary educational books not written in Portuguese. Radioactive materials. Regulation arms and munitions of Brazil and parts. Air guns. Reducing tubes and silencers for firearms. Salted or smoked meat, and other foodstuffs of animal origin. Seeds and seedlings of coffee, shrubs. Used consumer goods (See Observation #5 for exception).</Prohibitions>
    <Restrictions>Medicines must be accompanied by a prescription from the attendant Brazilian doctor. This prescription should be on a chemist's form, bearing the name, private address or office of the doctor, his registration number with the Brazil National Medical Council and a Portuguese translation of the instructions, as necessary. Postal packages containing medicaments and not satisfying the above-mentioned conditions will be returned to the senders or, if abandoned, treated as undeliverable items. Postage stamps are admitted only in registered First-Class Package International Service with Registered Mail service shipments. Saccharine and other artificial sweeteners for artificial beverages require permission from the Brazilian Department of Public Health for importation.</Restrictions>
    <Observations>1. Empresa Brasileira de Correios e Telégrafos (ECT) is introducing a "Fee for Postal Dispatch" with a current value of 15 Brazilian reals (BRL) for items presented to customs. If the addressee has not properly paid this fee, ECT will return the item to the sender. 2. Import licenses are required for many kinds of goods. ECT recommends that the sender ascertain from the addressee before mailing that the addressee holds the necessary documents. A shipment that does not have a required import permit is subject to confiscation as contraband. 3. The mailer must affix all necessary or relevant documents including invoices, export/import licenses, certificates of origin, health certificates, etc., to the outside of the item. 4. Imports are allowed by mail, including mail order catalog shipments, up to a value of U.S. $500 (U.S. $1,000 for computer software) without the requirement of an import license provided the item is not for resale. Shipments valued at no more than U.S. $50 are duty-free and are delivered to the addressee; shipments above U.S. $50 can be picked up at the post office upon payment of import duties. Imports that are prohibited or subject to special regulations must comply with applicable Brazilian government provisions. Identical shipments from the same source to the same person or address in Brazil within a 90-day period are considered part of the same shipment and may be subject to confiscation. Other merchandise that usually enters duty-free include items such as newspapers, maps, books, and magazines. 5. The mailer must fully and accurately complete the customs declarations, including the landline or mobile telephone number of the addressee, if available, and detailed information concerning the contents and value of the item, such as branded product description, model, serial number, and value of each individual article within the item. ECT immediately returns to the sender an item that does not have a properly completed customs declaration. 6. The importer tax identification (ID) number is required for all items containing goods. In Brazil, the importer tax ID number is known as "CPF" (format: 000.000.000-00) for natural persons and as "CNPJ" (format: 00.000.000/0000-00) for legal persons. This information must be provided either by the mailer in the importer reference field of the customs declaration form or on the commercial invoice, or by the importer through the Correios website at www2.correios.com.br/sistemas/rastreamento. 7. Shipments that do not indicate the applicable postage and fees on PS Form 2976-A will hinder the customs clearance process, causing delays to clear the items. 8. Used consumer goods may only be sent to charitable organizations that are recognized by the Brazilian government as being entities which serve the public interest.</Observations>
    <Regulations>Country Code: BR Reciprocal Service Name; Serca Required Customs Form/Endorsement 1. Correspondence and business papers. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). Endorse item clearly next to mailing label as BUSINESS PAPERS. 2. Merchandise, merchandise samples without commercial value, documents, computer data, and all articles subject to customs duty. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). Include an invoice with all commercial shipments. Note: Coins; banknotes; currency notes, including paper money; securities of any kind payable to bearer; traveler's checks; platinum, gold, and silver; precious stones; jewelry; watches; and other valuable articles are prohibited in Priority Mail Express International shipments to Brazil. Areas Served: All</Regulations>
    <AdditionalRestrictions>No Additional Restrictions Data found.</AdditionalRestrictions>
    <InsuranceFee>0</InsuranceFee>
    <GuaranteeAvailability>3-5 business days to many major markets</GuaranteeAvailability>
    <RemainingBarcodes>9773</RemainingBarcodes>
</eVSExpressMailIntlResponse>
"""
