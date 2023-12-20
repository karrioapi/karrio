import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTNTRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/expressconnect/pricing/getprice",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "country_code": "NL",
        "city": "Amsterdam",
        "postal_code": "1100 KG",
    },
    "recipient": {
        "address_line1": "Piazza del Colosseo, 1",
        "postal_code": "00184",
        "country_code": "IT",
        "city": "Roma",
    },
    "parcels": [
        {
            "height": 3,
            "length": 1,
            "width": 2,
            "weight": 1.25,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "services": ["tnt_special_express"],
    "options": {
        "currency": "GBP",
        "shipment_date": "2023-10-16",
        "insurance": 110.00,
        "declared_value": 100.00,
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "currency": "GBP",
            "extra_charges": [
                {"amount": 238.4, "currency": "GBP", "name": "Base charge"},
                {"amount": 50.07, "currency": "GBP", "name": "VAT"},
                {
                    "amount": 0.86,
                    "currency": "GBP",
                    "name": "ENHANCED SECURITY SURCHARGE",
                },
                {
                    "amount": 43.22,
                    "currency": "GBP",
                    "name": "FUEL SURCHARGE REFERENCIADO",
                },
                {"amount": 55.35, "currency": "GBP", "name": "IVA 21%"},
            ],
            "meta": {"service_name": "9:00 Express"},
            "service": "tnt_9_00_express",
            "total_charge": 288.47,
        }
    ],
    [
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "code": "P13",
            "details": {"messageType": "W"},
            "message": "Standard Rates",
        }
    ],
]


RateRequest = """<priceRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <appId>PC</appId>
    <appVersion>3.2</appVersion>
    <priceCheck>
        <sender>
            <country>NL</country>
            <town>Amsterdam</town>
            <postcode>1100 KG</postcode>
        </sender>
        <delivery>
            <country>IT</country>
            <town>Roma</town>
            <postcode>00184</postcode>
        </delivery>
        <collectionDateTime>2023-10-16T00:00:00</collectionDateTime>
        <product>
            <id>1N</id>
            <division>G</division>
            <type>N</type>
            <options>
                <option>
                    <optionCode>IN</optionCode>
                </option>
            </options>
        </product>
        <account>
            <accountNumber>3230493849304</accountNumber>
        </account>
        <termsOfPayment>S</termsOfPayment>
        <currency>GBP</currency>
        <priceBreakDown>true</priceBreakDown>
        <consignmentDetails>
            <totalWeight>1.25</totalWeight>
            <totalVolume>6e-06</totalVolume>
            <totalNumberOfPieces>1</totalNumberOfPieces>
        </consignmentDetails>
        <pieceLine>
            <numberOfPieces>1</numberOfPieces>
            <pieceMeasurements>
                <length>0.01</length>
                <width>0.02</width>
                <height>0.03</height>
                <weight>1.25</weight>
            </pieceMeasurements>
            <pallet>false</pallet>
        </pieceLine>
    </priceCheck>
</priceRequest>
"""

RateResponse = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<document>
    <requestId>28817</requestId>
    <errors>
        <brokenRule>
            <rateId>rate2</rateId>
            <messageType>W</messageType>
            <code>P13</code>
            <description>Standard Rates</description>
        </brokenRule>
    </errors>
    <priceResponse>
        <ratedServices>
            <rateId>rate2</rateId>
            <currency>GBP</currency>
            <ratedService>
                <product>
                    <id>09N</id>
                    <productDesc>9:00 Express</productDesc>
                </product>
                <totalPrice>288.47</totalPrice>
                <totalPriceExclVat>238.40</totalPriceExclVat>
                <vatAmount>50.07</vatAmount>
                <chargeElements>
                    <chargeElement>
                        <chargeItem>1</chargeItem>
                        <chargeCategory>SURCHARGE</chargeCategory>
                        <chargeCode>ESS00</chargeCode>
                        <description>ENHANCED SECURITY SURCHARGE</description>
                        <chargeValue>0.86</chargeValue>
                        <vatIndicator>true</vatIndicator>
                    </chargeElement>
                    <chargeElement>
                        <chargeItem>2</chargeItem>
                        <chargeCategory>SURCHARGE</chargeCategory>
                        <chargeCode>FSI00</chargeCode>
                        <description>FUEL SURCHARGE REFERENCIADO</description>
                        <chargeValue>43.22</chargeValue>
                        <vatIndicator>true</vatIndicator>
                    </chargeElement>
                    <chargeElement>
                        <chargeItem>3</chargeItem>
                        <chargeCategory>VAT</chargeCategory>
                        <chargeCode>VAT02</chargeCode>
                        <description>IVA 21%</description>
                        <chargeValue>55.35</chargeValue>
                        <vatIndicator>false</vatIndicator>
                    </chargeElement>
                </chargeElements>
            </ratedService>
        </ratedServices>
    </priceResponse>
</document>
"""
