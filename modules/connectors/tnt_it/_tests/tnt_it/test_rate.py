import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTNTConnectItalyRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
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
    "options": {},
    "reference": "REF-001",
}

ParsedRateResponse = []


RateRequest = """<Document>
	<Application>MYSHP</Application>
	<Version>3.0</Version>
	<Login>
		<Customer>xxxxxx</Customer>
		<User>xxxxxx</User>
		<Password>xxxxxx</Password>
		<LangID>IT</LangID>
	</Login>
	<ApplicationFunction>priceCheck</ApplicationFunction>
	<Details>
		<AccountNo>99999999</AccountNo>
		<Package>
			<Items>
				<ItemSeqNo>0</ItemSeqNo>
				<Type>0</Type>
				<INumber>1</INumber>
				<IWeight>10</IWeight>
				<IDescription/>
				<Length>30</Length>
				<Height>30</Height>
				<Width>40</Width>
			</Items>
		</Package>
		<Common>
			<ContactName>TEST -</ContactName>
			<Service/>
			<Insurance/>
			<InsuranceCurrency>EUR</InsuranceCurrency>
			<SenderReference/>
			<Payment>0</Payment>
			<Instructions/>
			<SpecialGoods>N</SpecialGoods>
		</Common>
		<Domestic>
			<COD>
				<Amount/>
				<Currency>EUR</Currency>
				<SenderComm/>
				<SenderRefund>N</SenderRefund>
			</COD>
			<OperationalOptions>
				<Option>0</Option>
			</OperationalOptions>
			<EOM>
				<Division/>
				<Enclosure/>
				<Unification/>
				<OfferNo/>
			</EOM>
		</Domestic>
		<CheckPriceEnabled>Y</CheckPriceEnabled>
	</Details>
	<Shipment>
		<ShipmentKey/>
		<isChanged/>
		<Date>19.11.2013</Date>
		<Template>
			<TemplateName/>
			<TemplateUse>0</TemplateUse>
			<AmendTemplate>N</AmendTemplate>
		</Template>
		<Receiver>
			<Address>
				<ShortName/>
				<CompanyName>TNT ESPRESS ITALY</CompanyName>
				<ReceiverAccountNo/>
				<AddressLine1 action="nocheck">VIA SPINELLI</AddressLine1>
				<AddressLine2/>
				<AddressLine3/>
				<TownId/>
				<Town>PESCHIERA BORROMEO</Town>
				<ProvinceState>MI</ProvinceState>
				<Postcode>20068</Postcode>
				<CountryID>IT</CountryID>
				<ContactName/>
				<PhoneID1/>
				<PhoneID2/>
				<FaxID1/>
				<FaxID2/>
				<Email/>
				<PreAlert>N</PreAlert>
				<AmendAddress>N</AmendAddress>
			</Address>
		</Receiver>
		<Incomplete>N</Incomplete>
	</Shipment>
	<CMessage/>
	<ExtraCee>N</ExtraCee>
</Document>
"""

RateResponse = """<a></a>
"""
