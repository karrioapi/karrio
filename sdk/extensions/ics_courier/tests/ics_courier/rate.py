import re
import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Rating
from karrio.core.models import RateRequest
from tests.ics_courier.fixture import gateway


class TestICSCourierRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        serialized_request = re.sub(
            "<shipping_date>[^>]+</shipping_date>",
            "",
            request.serialize(),
        )

        self.assertEqual(serialized_request, RateRequestXML)

    def test_get_rates(self):
        with patch("karrio.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"], gateway.settings.server_url,
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "http://www.icscourier.ca/GetEstimatedCharges"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedQuoteResponse)
            )


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "residential": False,
    },
    "recipient": {
        "address_line1": "1 TEST ST",
        "city": "TORONTO",
        "company_name": "TEST ADDRESS",
        "phone_number": "4161234567",
        "postal_code": "M4X1W7",
        "state_code": "ON",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "services": ["ics_courier_ground"],
    "options": {
        "ics_courier_extra_care": True,
    },
}

ParsedQuoteResponse = [
]


RateRequestXML = f"""<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <GetEstimatedCharges xmlns="http://www.icscourier.ca/">
            <AuthenicateAccount>
                <AccountID>555555</AccountID>
                <Password>555555</Password>
            </AuthenicateAccount>
            <PkgInfo>
                <Product>GR</Product>
                <Pieces>
                    <PieceInfo>
                        <Weight>1</Weight>
                        <WeightUnit>LB</WeightUnit>
                        <Length>4</Length>
                        <Width>4</Width>
                        <Height>4</Height>
                        <DeclaredValue>100</DeclaredValue>
                    </PieceInfo>
                </Pieces>
                <FromPost>H3E1W6</FromPost>
                <ToPost>E1C4Z8</ToPost>
            </PkgInfo>
        </GetEstimatedCharges>
    </soap12:Body>
</soap12:Envelope>
"""

RateResponseXml = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <GetEstimatedChargesResponse xmlns="http://www.icscourier.ca/">
            <GetEstimatedChargesResult>
                <BaseCharges>13.28</BaseCharges>
                <InsuranceCharges>0</InsuranceCharges>
                <SurCharges>
                    <SurCharge>
                        <SurChargeName>Consolidation Fee</SurChargeName>
                        <SurChargeAmount>0</SurChargeAmount>
                    </SurCharge>
                    <SurCharge>
                        <SurChargeName>Furtherance Charges</SurChargeName>
                        <SurChargeAmount>0</SurChargeAmount>
                    </SurCharge>
                    <SurCharge>
                        <SurChargeName>Oversize Charges</SurChargeName>
                        <SurChargeAmount>0</SurChargeAmount>
                    </SurCharge>
                    <SurCharge>
                        <SurChargeName>Pilot Fatigue Charges</SurChargeName>
                        <SurChargeAmount>0</SurChargeAmount>
                    </SurCharge>
                </SurCharges>
                <FuelCharges>1.66</FuelCharges>
                <Zone>14</Zone>
            </GetEstimatedChargesResult>
        </GetEstimatedChargesResponse>
    </soap:Body>
</soap:Envelope>
"""
