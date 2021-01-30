import logging
import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from tests.ups_package.fixture import gateway

logger = logging.getLogger(__name__)


class TestUPSPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        pipeline = request.serialize()
        rate_request = pipeline["rate"]()
        create_request = pipeline["create"](PickupRateResponseXML)

        self.assertEqual(rate_request.data.serialize(), PickupRateRequestXML)
        self.assertEqual(create_request.data.serialize(), PickupRequestXML)

    def test_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        pipeline = request.serialize()
        rate_request = pipeline["rate"]()
        create_request = pipeline["create"](PickupRateResponseXML)
        cancel_request = pipeline["cancel"](PickupResponseXML)

        self.assertEqual(rate_request.data.serialize(), PickupUpdateRateRequestXML)
        self.assertEqual(create_request.data.serialize(), PickupUpdateRequestXML)
        self.assertEqual(cancel_request.data.serialize(), PickupCancelRequestXML)

    def test_create_pickup(self):
        with patch("purplship.mappers.ups_package.proxy.http") as mocks:
            mocks.side_effect = [PickupRateResponseXML, PickupResponseXML]
            purplship.Pickup.schedule(self.PickupRequest).from_(gateway)

            rate_call, create_call = mocks.call_args_list
            self.assertEqual(
                rate_call[1]["url"],
                f"{gateway.settings.server_url}/Pickup",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/Pickup",
            )

    def test_update_pickup(self):
        with patch("purplship.mappers.ups_package.proxy.http") as mocks:
            mocks.side_effect = [
                PickupRateResponseXML,
                PickupResponseXML,
                PickupCancelResponseXML,
            ]
            purplship.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            rate_call, create_call, cancel_call = mocks.call_args_list
            self.assertEqual(
                rate_call[1]["url"],
                f"{gateway.settings.server_url}/Pickup",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/Pickup",
            )
            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}/Pickup",
            )

    def test_parse_pickup_reply(self):
        with patch("purplship.mappers.ups_package.proxy.http") as mocks:
            mocks.side_effect = [PickupRateResponseXML, PickupResponseXML]
            parsed_response = (
                purplship.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_cancel_reply(self):
        with patch("purplship.mappers.ups_package.proxy.http") as mock:
            mock.return_value = PickupCancelResponseXML
            parsed_response = (
                purplship.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupCancelResponse)


if __name__ == "__main__":
    unittest.main()

pickup_data = {
    "pickup_date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canadapost.ca",
    },
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_update_data = {
    "confirmation_number": "0074698052",
    "pickup_date": "2015-01-28",
    "address": {
        "person_name": "Jane Doe",
        "email": "john.doe@canadapost.ca",
        "phone_number": "1 514 5555555",
    },
    "parcels": [{"weight": 14, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_cancel_data = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "ups_package",
        "carrier_name": "ups_package",
        "confirmation_number": "2923843QRO0",
        "pickup_charge": {"amount": 9.28, "currency": "USD", "name": "FD"},
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "ups_package",
        "carrier_name": "ups_package",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRateRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <v11:PickupRateRequest>
            <common:Request/>
            <v11:PickupAddress>
                <v11:CompanyName>Jim Duggan</v11:CompanyName>
                <v11:ContactName>John Doe</v11:ContactName>
                <v11:AddressLine>2271 Herring Cove</v11:AddressLine>
                <v11:City>Halifax</v11:City>
                <v11:StateProvince>NS</v11:StateProvince>
                <v11:PostalCode>B3L2C2</v11:PostalCode>
                <v11:CountryCode>CA</v11:CountryCode>
                <v11:ResidentialIndicator>Y</v11:ResidentialIndicator>
                <v11:Phone>
                    <v11:Number>1 514 5555555</v11:Number>
                </v11:Phone>
            </v11:PickupAddress>
            <v11:AlternateAddressIndicator>Y</v11:AlternateAddressIndicator>
            <v11:ServiceDateOption>02</v11:ServiceDateOption>
            <v11:PickupDateInfo>
                <v11:CloseTime>1700</v11:CloseTime>
                <v11:ReadyTime>1500</v11:ReadyTime>
                <v11:PickupDate>20150128</v11:PickupDate>
            </v11:PickupDateInfo>
            <TaxInformationIndicator></TaxInformationIndicator>
            <UserLevelDiscountIndicator></UserLevelDiscountIndicator>
        </v11:PickupRateRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <v11:PickupCreationRequest>
            <common:Request/>
            <v11:RatePickupIndicator>N</v11:RatePickupIndicator>
            <TaxInformationIndicator></TaxInformationIndicator>
            <UserLevelDiscountIndicator></UserLevelDiscountIndicator>
            <v11:Shipper>
                <v11:Account>
                    <v11:AccountNumber>Your Account Number</v11:AccountNumber>
                    <v11:AccountCountryCode>CA</v11:AccountCountryCode>
                </v11:Account>
            </v11:Shipper>
            <v11:PickupDateInfo>
                <v11:CloseTime>1700</v11:CloseTime>
                <v11:ReadyTime>1500</v11:ReadyTime>
                <v11:PickupDate>20150128</v11:PickupDate>
            </v11:PickupDateInfo>
            <v11:PickupAddress>
                <v11:CompanyName>Jim Duggan</v11:CompanyName>
                <v11:ContactName>John Doe</v11:ContactName>
                <v11:AddressLine>2271 Herring Cove</v11:AddressLine>
                <v11:City>Halifax</v11:City>
                <v11:StateProvince>NS</v11:StateProvince>
                <v11:PostalCode>B3L2C2</v11:PostalCode>
                <v11:CountryCode>CA</v11:CountryCode>
                <v11:ResidentialIndicator>Y</v11:ResidentialIndicator>
                <v11:Phone>
                    <v11:Number>1 514 5555555</v11:Number>
                </v11:Phone>
            </v11:PickupAddress>
            <v11:AlternateAddressIndicator>Y</v11:AlternateAddressIndicator>
            <v11:TotalWeight>
                <v11:UnitOfMeasurement>LBS</v11:UnitOfMeasurement>
            </v11:TotalWeight>
            <v11:PaymentMethod>01</v11:PaymentMethod>
            <v11:SpecialInstruction>Door at Back</v11:SpecialInstruction>
            <v11:ShippingLabelsAvailable>Y</v11:ShippingLabelsAvailable>
        </v11:PickupCreationRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateRateRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <v11:PickupRateRequest>
            <common:Request/>
            <v11:PickupAddress>
                <v11:ContactName>Jane Doe</v11:ContactName>
                <v11:ResidentialIndicator>N</v11:ResidentialIndicator>
                <v11:Phone>
                    <v11:Number>1 514 5555555</v11:Number>
                </v11:Phone>
            </v11:PickupAddress>
            <v11:AlternateAddressIndicator>Y</v11:AlternateAddressIndicator>
            <v11:ServiceDateOption>02</v11:ServiceDateOption>
            <v11:PickupDateInfo>
                <v11:CloseTime>1700</v11:CloseTime>
                <v11:ReadyTime>1500</v11:ReadyTime>
                <v11:PickupDate>20150128</v11:PickupDate>
            </v11:PickupDateInfo>
            <TaxInformationIndicator></TaxInformationIndicator>
            <UserLevelDiscountIndicator></UserLevelDiscountIndicator>
        </v11:PickupRateRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <v11:PickupCreationRequest>
            <common:Request/>
            <v11:RatePickupIndicator>N</v11:RatePickupIndicator>
            <TaxInformationIndicator></TaxInformationIndicator>
            <UserLevelDiscountIndicator></UserLevelDiscountIndicator>
            <v11:Shipper>
                <v11:Account>
                    <v11:AccountNumber>Your Account Number</v11:AccountNumber>
                    <v11:AccountCountryCode></v11:AccountCountryCode>
                </v11:Account>
            </v11:Shipper>
            <v11:PickupDateInfo>
                <v11:CloseTime>1700</v11:CloseTime>
                <v11:ReadyTime>1500</v11:ReadyTime>
                <v11:PickupDate>20150128</v11:PickupDate>
            </v11:PickupDateInfo>
            <v11:PickupAddress>
                <v11:ContactName>Jane Doe</v11:ContactName>
                <v11:ResidentialIndicator>N</v11:ResidentialIndicator>
                <v11:Phone>
                    <v11:Number>1 514 5555555</v11:Number>
                </v11:Phone>
            </v11:PickupAddress>
            <v11:AlternateAddressIndicator>Y</v11:AlternateAddressIndicator>
            <v11:TotalWeight>
                <v11:Weight>30.87</v11:Weight>
                <v11:UnitOfMeasurement>LBS</v11:UnitOfMeasurement>
            </v11:TotalWeight>
            <v11:PaymentMethod>01</v11:PaymentMethod>
            <v11:SpecialInstruction>Door at Back</v11:SpecialInstruction>
            <v11:ShippingLabelsAvailable>Y</v11:ShippingLabelsAvailable>
        </v11:PickupCreationRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:v11="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <v11:PickupCancelRequest>
            <common:Request/>
            <v11:CancelBy>02</v11:CancelBy>
            <v11:PRN>0074698052</v11:PRN>
        </v11:PickupCancelRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <pkup:PickupCancelResponse xmlns:pkup="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext />
                </common:TransactionReference>
            </common:Response>
            <pkup:PickupType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true" />
        </pkup:PickupCancelResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupRateResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header />
   <soapenv:Body>
      <pkup:PickupRateResponse xmlns:pkup="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
         <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
            <common:ResponseStatus>
               <common:Code>1</common:Code>
               <common:Description>Success</common:Description>
            </common:ResponseStatus>
            <common:TransactionReference>
               <common:CustomerContext>Your Customer Context</common:CustomerContext>
            </common:TransactionReference>
         </common:Response>
         <pkup:RateResult>
            <pkup:RateType>FD</pkup:RateType>
            <pkup:CurrencyCode>USD</pkup:CurrencyCode>
            <pkup:ChargeDetail>
               <pkup:ChargeCode>B</pkup:ChargeCode>
               <pkup:ChargeDescription>BASE CHARGE</pkup:ChargeDescription>
               <pkup:ChargeAmount>5.65</pkup:ChargeAmount>
               <pkup:TaxAmount>0.00</pkup:TaxAmount>
            </pkup:ChargeDetail>
            <pkup:ChargeDetail>
               <pkup:ChargeCode>S</pkup:ChargeCode>
               <pkup:ChargeDescription>REMOTE AREA SURCHARGE</pkup:ChargeDescription>
               <pkup:ChargeAmount>0.00</pkup:ChargeAmount>
               <pkup:TaxAmount>0.00</pkup:TaxAmount>
            </pkup:ChargeDetail>
            <pkup:ChargeDetail>
               <pkup:ChargeCode>S</pkup:ChargeCode>
               <pkup:ChargeDescription>RESIDENTIAL SURCHARGE</pkup:ChargeDescription>
               <pkup:ChargeAmount>3.25</pkup:ChargeAmount>
               <pkup:TaxAmount>0.00</pkup:TaxAmount>
            </pkup:ChargeDetail>
            <pkup:ChargeDetail>
               <pkup:ChargeCode>S</pkup:ChargeCode>
               <pkup:ChargeDescription>FUEL SURCHARGE</pkup:ChargeDescription>
               <pkup:ChargeAmount>0.38</pkup:ChargeAmount>
               <pkup:TaxAmount>0.00</pkup:TaxAmount>
            </pkup:ChargeDetail>
            <pkup:GrandTotalOfAllCharge>9.28</pkup:GrandTotalOfAllCharge>
         </pkup:RateResult>
      </pkup:PickupRateResponse>
   </soapenv:Body>
</soapenv:Envelope>
"""

PickupResponseXML = f"""<wrapper>
    {PickupRateResponseXML}
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header />
        <soapenv:Body>
            <pkup:PickupCreationResponse xmlns:pkup="http://www.ups.com/XMLSchema/XOLTWS/Pickup/v1.1">
                <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                    <common:ResponseStatus>
                        <common:Code>1</common:Code>
                        <common:Description>Success</common:Description>
                    </common:ResponseStatus>
                    <common:TransactionReference>
                        <common:CustomerContext>Your Customer Context</common:CustomerContext>
                    </common:TransactionReference>
                </common:Response>
                <pkup:PRN>2923843QRO0</pkup:PRN>
                <pkup:RateStatus>
                    <pkup:Code>01</pkup:Code>
                    <pkup:Description>Rate available</pkup:Description>
                </pkup:RateStatus>
                <pkup:RateResult>
                    <pkup:Disclaimer>
                        <pkup:Code>05</pkup:Code>
                        <pkup:Description>Rate excludes VAT. Rate includes a fuel surcharge, but excludes taxes, duties and other charges that may apply to the shipment.</pkup:Description>
                    </pkup:Disclaimer>
                    <pkup:RateType>FD</pkup:RateType>
                    <pkup:CurrencyCode>USD</pkup:CurrencyCode>
                    <pkup:ChargeDetail>
                        <pkup:ChargeCode>B</pkup:ChargeCode>
                        <pkup:ChargeDescription>BASE CHARGE</pkup:ChargeDescription>
                        <pkup:ChargeAmount>5.65</pkup:ChargeAmount>
                        <pkup:TaxAmount>0.00</pkup:TaxAmount>
                    </pkup:ChargeDetail>
                    <pkup:ChargeDetail>
                        <pkup:ChargeCode>S</pkup:ChargeCode>
                        <pkup:ChargeDescription>REMOTE AREA SURCHARGE</pkup:ChargeDescription>
                        <pkup:ChargeAmount>0.00</pkup:ChargeAmount>
                        <pkup:TaxAmount>0.00</pkup:TaxAmount>
                    </pkup:ChargeDetail>
                    <pkup:ChargeDetail>
                        <pkup:ChargeCode>S</pkup:ChargeCode>
                        <pkup:ChargeDescription>RESIDENTIAL SURCHARGE</pkup:ChargeDescription>
                        <pkup:ChargeAmount>3.25</pkup:ChargeAmount>
                        <pkup:TaxAmount>0.00</pkup:TaxAmount>
                    </pkup:ChargeDetail>
                    <pkup:ChargeDetail>
                        <pkup:ChargeCode>S</pkup:ChargeCode>
                        <pkup:ChargeDescription>FUEL SURCHARGE</pkup:ChargeDescription>
                        <pkup:ChargeAmount>0.38</pkup:ChargeAmount>
                        <pkup:TaxAmount>0.00</pkup:TaxAmount>
                    </pkup:ChargeDetail>
                    <pkup:GrandTotalOfAllCharge>9.28</pkup:GrandTotalOfAllCharge>
                </pkup:RateResult>
            </pkup:PickupCreationResponse>
        </soapenv:Body>
    </soapenv:Envelope>
</wrapper>
"""
