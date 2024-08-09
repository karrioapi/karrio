import unittest
import urllib.parse
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from ..fixture import gateway


class TestUSPSPriorityMailShipment(unittest.TestCase):
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

    @patch("karrio.mappers.usps_wt_international.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        expected_url = f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentRequestQuery)}"
        self.assertEqual(
            urllib.parse.unquote(url),
            urllib.parse.unquote(expected_url),
        )

    @patch("karrio.mappers.usps_wt_international.proxy.http", return_value="<a></a>")
    def test_cancel_shipment(self, http_mock):
        karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}?{urllib.parse.urlencode(ShipmentCancelRequestQuery)}",
        )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.usps_wt_international.proxy.http") as mocks:
            mocks.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.usps_wt_international.proxy.http") as mocks:
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
            "options": {"insurance": 90.0},
        }
    ],
    "service": "usps_priority_mail_international_large_flat_rate_box",
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
        "shipment_identifier": "HE200448219US",
        "tracking_number": "HE200448219US",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=HE200448219US"
        },
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "usps_international",
        "carrier_name": "usps_international",
        "operation": "Shipment Cancel",
        "success": True,
    },
    [],
]

ShipmentRequestXML = """<eVSPriorityMailIntlRequest USERID="username" PASSWORD="password">
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
    <FromState>Oklahoma</FromState>
    <FromZip5>73108</FromZip5>
    <FromZip4></FromZip4>
    <FromPhone>1234567890</FromPhone>
    <ToFirstName>John</ToFirstName>
    <ToFirm>Coffee Five</ToFirm>
    <ToAddress1></ToAddress1>
    <ToAddress2>01 R. da Quitanda, 86 - quiosque</ToAddress2>
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
    <Insured>y</Insured>
    <InsuredAmount>90.0</InsuredAmount>
    <GrossPounds>4</GrossPounds>
    <GrossOunces>70</GrossOunces>
    <ContentType>MERCHANDISE</ContentType>
    <ContentTypeOther>N/A</ContentTypeOther>
    <Agreement>N</Agreement>
    <LicenseNumber>LIC-24356879</LicenseNumber>
    <CertificateNumber>CERT-97865342</CertificateNumber>
    <InvoiceNumber>INV-040903</InvoiceNumber>
    <ImageType>PDF</ImageType>
    <ImageLayout>ALLINONEFILE</ImageLayout>
    <LabelDate>05/15/2021</LabelDate>
    <Width>4.72</Width>
    <Length>2.36</Length>
    <Height>3.54</Height>
    <Machinable>false</Machinable>
    <DestinationRateIndicator>I</DestinationRateIndicator>
    <MID>847654321</MID>
</eVSPriorityMailIntlRequest>
"""

ShipmentRequestQuery = {"API": "eVSPriorityMailIntl", "XML": ShipmentRequestXML}

ShipmentCancelRequestXML = """<eVSICancelRequest USERID="username" PASSWORD="password">
    <BarcodeNumber>123456789012</BarcodeNumber>
</eVSICancelRequest>
"""

ShipmentCancelRequestQuery = {"API": "eVSICancel", "XML": ShipmentCancelRequestXML}

ShipmentResponseXML = """<eVSPriorityMailIntlResponse>
    <Postage>38.52</Postage>
    <TotalValue>15.00</TotalValue>
    <SDRValue>10.83</SDRValue>
    <BarcodeNumber>HE200448219US</BarcodeNumber>
    <LabelImage>SUkqAAgAAAASAP4ABAAB...</LabelImage>
    <Page2Image></Page2Image>
    <Page3Image></Page3Image>
    <Page4Image></Page4Image>
    <Page5Image></Page5Image>
    <Page6Image></Page6Image>
    <Prohibitions> An issue of a publication in which more than 5 percent of its total advertising space is primarily directed to a Canadian market and which indicates: (a) Specifically where goods or services may be obtained in Canada, or (b) Specific items or conditions relating to the sale or provision of goods or services in Canada. All alcoholic beverages including wines, etc. An issue of a publication that contains an advertisement primarily directed to a Canadian market is a prohibited import if that advertisement does not appear in identical form in all editions of the issue distributed in the country of origin. Articles so marked as to create the false impression that they were made in Canada, Great Britain or any other British country. Commercial tags of metal. Firearms, except as follows: Firearms may be mailed to Canada if the importer has the required documentation and if the firearms meet the requirements in Publication 52, subchapter 43 and part 632. Before mailing, customers must visit cbsa-asfc.gc.ca/import/iefw-iefa-eng.html to review Canadian import requirements. Gold bullion, gold dust, and nonmanufactured precious metals. Non-refillable lighters or any other lighter that contains fuel. New lighters with no fuel may be sent. Oleomargarine and other butter substitutes, including altered or renovated butter. Perishable infectious biological substances. Perishable noninfectious biological substances. Plumage and skins of wild birds. Prison-made goods being sold or intended for sale by a person or firm. Radioactive materials. Replica or inert munitions, as well as other devices that simulate explosive devices or munitions, including replica or inert grenades or other simulated military munitions, whether or not such items are for display purposes. Reprints of Canadian or British works copyrighted in Canada. Reproductions of Canadian postage stamps unless printed in publications in black and white only and with a defacing line drawn across each reproduction. Shipments bearing caution labels indicating the contents are flammable. Smoke-making devices for motor vehicles and boats. Used or secondhand hives or bee supplies. Vaping liquids containing 66 mg/g or more nicotine by weight. Note: The U.S. Postal Service measures the concentration of nicotine solutions by volume rather than by weight, so it is possible that a product that does not exceed Canada's weight restriction would exceed the Postal Service's volume restriction. Nicotine solutions with a concentration of 16.67 percent (166 mg/ml) or more, when nicotine is the only toxic material in the liquid, are classified as "dangerous goods" (see 136.1) and as such are prohibited in international mail. (See also Observation 1</Prohibitions>
    <Restrictions>Coins; banknotes; currency notes; securities payable to bearer; traveler's checks; gold, silver, platinum, manufactured or not; jewelry; and other valuable articles may be sent only in registered items First-Class Package International Service with Registered Mail service. Exceptions: Coins sent to or from collectors or dealers may be mailed in ordinary (uninsured) parcels. Drugs and medicines must comply with Canadian law. Eggs for hatching must be packed in new, clean containers and accompanied by a certificate issued by a veterinarian of the U.S. Department of Agriculture, or one issued by a State veterinarian and endorsed by a veterinarian of that Bureau, stating that to the best of his or her knowledge the eggs come from a flock that is free from Newcastle disease, fowl pest, or fowl typhoid. See 135.3 for method of packing. Meat and meat food products must be accompanied by an export certificate issued by the U.S. Department of Agriculture and labeled in accordance with Canadian regulations. Exception to these requirements are: 1. bona fide sample shipments weighing less than 10 kg; 2. meat products addressed to a government department or agency; 3. meat products intended for personal consumption when they enter Canada in the possession of the importer. Pet food that contains biologically appropriate raw food or bones and raw food - such as heat-processed, shelf-stable pet foods, treats, and compound chews - must be accompanied by an import permit from the Canadian Food Inspection Agency and a zoo sanitary certificate from the United States Department of Agriculture (USDA) Animal and Plant Health Inspection Service (APHIS) Veterinarian Services. Attach a copy of both documents to the outside of the mailpiece for review by the Canada Border Service Agency. Precious stones, set or not set; all items used as dress ornaments and coming under the term "jewelry" including articles of gold or other precious metal for personal use such as cigarette holders, cases, powder cases, card cases, opera glasses, fountain pens, watches, etc., are permitted in insured parcels provided the articles have value not over $5 U.S. A parcel containing a number of such articles valued at $5 or less may be insured for the total value of the contents up to a maximum of $200. Veterinary biological products including serums and vaccines must be accompanied by a permit issued by the Veterinary Director General, Ministry of Agriculture of Canada.</Restrictions>
    <Observations>1. As noted in the Prohibitions section, Canada prohibits certain vaping products. However, vaping products, otherwise known as electronic smoking products (i.e., electronic products for the vaporization and administration of inhaled doses of nicotine including electronic cigarettes, cigars, cigarillos, and pipes, as well as cartridges of nicotine solutions and related products), that make health claims are subject to the Canadian Food and Drugs Act (FDA). "Health claims" refers to any statement that represents the product as a drug or device under section 2 of the FDA - for example, a statement that the product will help someone quit smoking. Vaping products that make health claims require authorization under the FDA before being commercially imported, advertised, or sold in Canada. A vaping product that makes health claims is considered a prescription drug, and before importation to Canada, it requires a Drug Establishment License and an assigned corresponding Drug Identification Number (DIN). For more information, visit canada.ca/en/health-canada/topics/licensing-authorizing-manufacturing-drug-health-products.html. Vaping products with no health claims and no drugs other than nicotine are not subject to the FDA. 2. Banknotes valued at $100 or more must be put up in a compact package and securely tied with strong twine before wrapping. The wrapper must be linen or other strong, woven material, linen lined paper, or two thicknesses of strong kraft paper. After wrapping, the package must be again securely tied or stitched and sealed at the points of closing. 3. The name of the Canadian province in which the office of destination is located must appear as part of the address. 4. The following must not be accepted for insurance: Bees, postage stamps (canceled and uncanceled) and albums in which they are mounted, and parcels addressed to CFPOs. 5. Canadian Forces Mail (CFPO) is processed through Canadian military post offices and must be addressed in the following manner: (a) NUMBER, RANK, NAME UNIT (b) CFPO (NUMBER) (c) BELLEVILLE ON K0K 3R0 (d) CANADA Maximum weight limits for mail addressed to members of the Canadian Forces based outside of Canada (CFPO) is 22 pounds. Parcels for CFPO addresses may not be insured. Direct sacks of printed matter (M-bags) are not permitted for CFPO addresses. 6. A letter fully prepaid and bearing the same address as that of a parcel may be tied or otherwise securely attached to the outside of the parcel. Stamps to cover postage on the parcel must be affixed to the wrapper of the parcel. Stamps to pay postage on the letter must be affixed to the envelope thereof. 7. Certain types of merchandise must be marked to show country of origin in the manner prescribed by the Canadian customs regulations. 8. Goods valued under 20 Canadian dollars are duty and excise tax exempt. Goods over 20 Canadian dollars will be subject to the applicable duties and excise taxes. Gift shipments received by mail that are valued under 60 Canadian dollars are duty and excise tax exempt. 9. For all casual and commercial goods valued at or under 1,600 Canadian dollars, Canada Post will collect assessed duties, excise taxes, and a handling fee from the addressee. This handling fee is set by Canada Post (see http://www.canadapost.ca/tools/pg/manual/PGcustoms-e.asp). All commercial mail items over 1,600 Canadian dollars will be held by Canada Customs and Excise until proper invoice and accounting documentation is provided by the addressee. 10. The Canada Customs Invoice can be obtained from stationery, office supply, or printing companies. If mailers are unable to obtain the Canada Customs Invoice locally, they should visit the following Web site: www.canadapost.ca. In addition, commercial invoices are acceptable provided that each invoice has the required information for customs purposes. 11. Information on Canadian customs regulations may be obtained from the Office of International Marketing/223, Bureau of International Commerce, Department of Commerce, Washington, DC 20230, or any field office of that Department. Obtaining post code information: 12. Information on Canadian post code directories can be obtained from: (a) NATIONAL PHILATELIC CENTER CANADA POST CORPORATION STATION 1 ANTIGONISH NS B2G 2R8 Telephone: 1-800-565-4362 Fax: 1-902-863-6796 (b) To obtain Canadian post codes for specific addresses, call the General Information line at 1-416-979-8822 or access the Canada Post Corporation web site on the Internet at http://www.canadapost.ca. 13. Pursuant to the Canada Customs Act and a need to heighten border security, Canada will deny entry of all postal items (except postcards) that do not bear complete sender and addressee information in roman letters and arabic numerals.</Observations>
    <Regulations>Country Code: CA Reciprocal Service Name: There is no reciprocal service. Required Customs Form/Endorsement 1. Business papers and commercial documents. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). 2. Merchandise samples and gift shipments (non-commercial parcels). PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). 3. Merchandise (commercial shipments) and all articles subject to customs duty. PS Form 2976-B placed inside PS Form 2976-E (plastic envelope). Notes: 1. Gift shipments (non-commercial parcels) require a sales receipt, invoice or other documentation to support the declared value. 2. Coins; banknotes; currency notes, including paper money; securities of any kind payable to bearer; traveler's checks; platinum, gold, and silver; precious stones; jewelry; watches; and other valuable articles are prohibited in Priority Mail Express International shipments to Canada. 3. Priority Mail Express International shipments may have a street address or a post office box address. A local telephone number for the addressee MUST be provided for shipments addressed to a post office box address. A local telephone number for the addressee should be provided if possible for shipments to a street address. Areas Served: All</Regulations>
    <AdditionalRestrictions>No Additional Restrictions Data found.</AdditionalRestrictions>
    <ParcelIndemnityCoverage/>
    <InsuranceFee>0.00</InsuranceFee>
    <RemainingBarcodes>9954</RemainingBarcodes>
</eVSPriorityMailIntlResponse>
"""

ShipmentCancelResponseXML = """<eVSICancelResponse>
    <BarcodeNumber>EC502016316US</BarcodeNumber>
    <Status>Cancelled</Status>
    <Reason>Order Cancelled Successfully</Reason>
</eVSICancelResponse>
"""
