import unittest
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest
from ..fixture import gateway


class TestUSPSFirstClassShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        requests = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(requests.serialize(), ShipmentRequestXML)

    # @patch("karrio.mappers.usps_wt_international.proxy.http", return_value="<a></a>")
    # def test_create_shipment(self, http_mock):
    #     karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
    #
    #     url = http_mock.call_args[1]["url"]
    #     self.assertEqual(
    #         url,
    #         f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentRequestQuery)}",
    #     )

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
    "service": "usps_first_class_package_international_service",
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
        "shipment_identifier": "LZ333007778US",
        "tracking_number": "LZ333007778US",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=LZ333007778US"
        },
    },
    [],
]


ShipmentRequestXML = """<eVSFirstClassMailIntlRequest USERID="username" PASSWORD="password">
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
    <ToAddress2>01 R. da Quitanda, 86 - quiosque</ToAddress2>
    <ToCity>Centro</ToCity>
    <ToProvince>Rio de Janeiro</ToProvince>
    <ToCountry>Brazil</ToCountry>
    <ToPostalCode>29440</ToPostalCode>
    <ToPhone>8005554526</ToPhone>
    <ShippingContents>
        <ItemDetail>
            <Description>N/A</Description>
            <Quantity>1</Quantity>
            <Value>30</Value>
            <NetPounds>4.41</NetPounds>
            <NetOunces>70.55</NetOunces>
            <HSTariffNumber>XXXXX0000123</HSTariffNumber>
            <CountryOfOrigin>United States</CountryOfOrigin>
        </ItemDetail>
    </ShippingContents>
    <GrossPounds>4.41</GrossPounds>
    <GrossOunces>70.55</GrossOunces>
    <ContentType>MERCHANDISE</ContentType>
    <ContentTypeOther>N/A</ContentTypeOther>
    <Agreement>N</Agreement>
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
</eVSFirstClassMailIntlRequest>
"""

ShipmentRequestQuery = {"API": "eVSFirstClassMailIntl", "XML": ShipmentRequestXML}

ShipmentResponseXML = """<eVSFirstClassMailIntlResponse>
    <Postage>30.42</Postage>
    <TotalValue>1.11</TotalValue>
    <BarcodeNumber>LZ333007778US</BarcodeNumber>
    <LabelImage>SUkqAAgAAAASAP4ABAAB...</LabelImage>
    <Page2Image></Page2Image>
    <Page3Image></Page3Image>
    <Prohibitions>Antiquities, art fossils, historical documents, numismatic material, specimens of flora and fauna, and similar cultural heritage objects that are significant to a nation's identity. Coins; bank notes; currency notes (paper money); securities of any kind payable to bearer; traveler's checks; platinum, gold, and silver (except for jewelry items meeting the requirement in "Restrictions" below); precious stones (except when contained in jewelry items meeting the requirement in "Restrictions" below); and other valuable articles are prohibited. Dog collars with protrusions designed to puncture or bruise an animal's skin. Fruit cartons (used or new). Fur, including raw, tanned, or processed furs or pelts, and goods that may contain such fur that are derived from domesticated cat and dog breeds. Goods bearing the name "Anzac." Goods produced wholly or partly in prisons or by convict labor. Laser pointers and similar handheld devices designed or adapted to emit a laser beam with an accessible emission level greater than 1 megawatt (MW). Most food, plant, and animal products, including the use of products such as straw and other plant material as packing materials. Perishable infectious biological substances. Radioactive materials. Registered philatelic articles with fictitious addresses. Replica firearms, including any article that has the appearance of a firearm that could reasonably be mistaken as a firearm. Seditious literature. Signal jammers capable of preventing or disrupting mobile telephone and satellite navigation services. Silencers for firearms. Tobacco products, including cigarettes and loose-leaf tobacco. Exception: Cigars. Note: Although Australia also permits chewing tobacco and oral snuff in amounts up to 3.3 pounds (1.5 kg), the U.S. Postal Service does not permit these types of smokeless tobacco in international mail - see 136.4. Used bedding.</Prohibitions>
    <Restrictions>Airsoft (BB) guns that do not have the appearance of fully automatic firearms require prior approval granted by relevant police representatives. The addressee must submit an application to import the item via the police certification test. Drugs, medicines, and therapeutic substances such as antibiotics, growth hormones, kava, psychoactive substances, and steroids require an import permit from the Australian Department of Health, Office of Drug Control. Fish or parts of fish, including all species of bony fish, sharks, rays, crustaceans, mollusks, and other marine organisms (but not including marine mammals, marine reptiles, or toothfish), whether fresh, frozen, smoked, or preserved in airtight containers, require an import permit from the Australian Fisheries Management Authority (AFMA). Jewelry is permitted only when sent as an insured parcel using Priority Mail International service. In addition, Australian Customs regulations prohibit importation of jewelry that is made with ivory or from endangered species, such as snake, elephant, or crocodile, that does not have an accompanying Import/Export Permit in relation to the Convention on International Trade in Endangered Species of Wild Fauna and Flora (CITES). Knives (such as daggers and throwing knives), throwing blades, or throwing axes require written Police Certification (B709B form or B709X form) from the Australian Police Firearms Registry. Meat and other animal products; powdered or concentrated milk; and other dairy products requires permission to import from the Australian quarantine authorities. Permission of the Australian Director-General of Health is required to import medicines.</Restrictions>
    <Observations>Duty may be levied on catalogs, price lists, circulars, and all advertising introduced into Australia through the mail, regardless of the class of mail used.</Observations>
    <Regulations>Country Code: AU Reciprocal Service Name: Express Post Required Customs Form/Endorsement 1. Business and commercial papers. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). Endorse item clearly next to mailing label as BUSINESS PAPERS. 2. Merchandise samples without commercial value microfilm, microfiche, and computer data. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). 3. Merchandise and all articles subject to customs duty. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). Note: 1. Coins; banknotes; currency notes, including paper money; securities of any kind payable to bearer; traveler's checks; platinum, gold, and silver; precious stones; jewelry; watches; and other valuable articles are prohibited in Priority Mail Express International shipments to Australia. 2. Priority Mail Express International With Guarantee service - which offers a date-certain, postage-refund guarantee - is available to Australia. Areas Served: All except Lord Howe Island and the Australian Antarctic territories.</Regulations>
    <AdditionalRestrictions>No Additional Restrictions Data found.</AdditionalRestrictions>
    <ExtraServices>
        <ExtraService>
            <ServiceID>109</ServiceID>
            <ServiceName>Electronic USPS Delivery Confirmation International (E-USPS DELCON INTL)</ServiceName>
            <Price>0.00</Price>
        </ExtraService>
    </ExtraServices>
    <RemainingBarcodes>9810</RemainingBarcodes>
</eVSFirstClassMailIntlResponse>
"""
