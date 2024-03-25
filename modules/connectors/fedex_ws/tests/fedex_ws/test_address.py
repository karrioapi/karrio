import unittest
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import AddressValidationRequest
from .fixture import gateway


class TestDHLAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **address_validation_data
        )

    def test_create_AddressValidation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )

        self.assertEqual(request.serialize(), AddressValidationRequestXML)

    def test_validate_address(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/addressvalidation",
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedAddressValidationResponse)
            )


if __name__ == "__main__":
    unittest.main()

address_validation_data = {
    "address": {
        "address_line1": "333 Twin",
        "address_line2": "Suit 333",
        "postal_code": "94089",
        "city": "North Dakhota",
        "country_code": "US",
        "state_code": "CA",
    }
}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "fedex_ws",
        "complete_address": {
            "address_line1": "Input Your Information",
            "city": "Input Your Information",
            "country_code": "Input Your Information",
            "state_code": "Input Your Information",
        },
        "success": True,
    },
    [],
]


AddressValidationRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v4="http://fedex.com/ws/addressvalidation/v4">
    <tns:Body>
        <v4:AddressValidationRequest>
            <v4:WebAuthenticationDetail>
                <v4:UserCredential>
                    <v4:Key>user_key</v4:Key>
                    <v4:Password>password</v4:Password>
                </v4:UserCredential>
            </v4:WebAuthenticationDetail>
            <v4:ClientDetail>
                <v4:AccountNumber>2349857</v4:AccountNumber>
                <v4:MeterNumber>1293587</v4:MeterNumber>
            </v4:ClientDetail>
            <v4:TransactionDetail>
                <v4:CustomerTransactionId>AddressValidationRequest_v4</v4:CustomerTransactionId>
            </v4:TransactionDetail>
            <v4:Version>
                <v4:ServiceId>aval</v4:ServiceId>
                <v4:Major>4</v4:Major>
                <v4:Intermediate>0</v4:Intermediate>
                <v4:Minor>0</v4:Minor>
            </v4:Version>
            <v4:AddressesToValidate>
                <v4:Address>
                    <v4:StreetLines>333 Twin</v4:StreetLines>
                    <v4:StreetLines>Suit 333</v4:StreetLines>
                    <v4:City>North Dakhota</v4:City>
                    <v4:StateOrProvinceCode>North Dakhota</v4:StateOrProvinceCode>
                    <v4:PostalCode>94089</v4:PostalCode>
                    <v4:CountryCode>US</v4:CountryCode>
                </v4:Address>
            </v4:AddressesToValidate>
        </v4:AddressValidationRequest>
    </tns:Body>
</tns:Envelope>
"""

AddressValidationResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"/>
   <soapenv:Body>
      <v4:AddressValidationReply xmlns:v4="http://fedex.com/ws/addressvalidation/v4">
         <v4:HighestSeverity>SUCCESS</v4:HighestSeverity>
         <v4:Notifications>
            <v4:Severity>SUCCESS</v4:Severity>
            <v4:Source>wsi</v4:Source>
            <v4:Code>0</v4:Code>
            <v4:Message>Success</v4:Message>
         </v4:Notifications>
         <v4:TransactionDetail>
            <v4:CustomerTransactionId>AddressValidationRequest_v4</v4:CustomerTransactionId>
            <v4:Localization>
               <v4:LanguageCode>EN</v4:LanguageCode>
               <v4:LocaleCode>US</v4:LocaleCode>
            </v4:Localization>
         </v4:TransactionDetail>
         <v4:Version>
            <v4:ServiceId>aval</v4:ServiceId>
            <v4:Major>4</v4:Major>
            <v4:Intermediate>0</v4:Intermediate>
            <v4:Minor>0</v4:Minor>
         </v4:Version>
         <v4:ReplyTimestamp>2015-03-09T00:40:58.497-05:00</v4:ReplyTimestamp>
         <v4:AddressResults>
            <v4:ClientReferenceId>ac vinclis et</v4:ClientReferenceId>
            <v4:State>Input Your Information</v4:State>
            <v4:Classification>UNKNOWN</v4:Classification>
            <v4:EffectiveAddress>
               <v4:StreetLines>Input Your Information</v4:StreetLines>
               <v4:City>Input Your Information</v4:City>
               <v4:StateOrProvinceCode>Input Your Information</v4:StateOrProvinceCode>
               <v4:PostalCode>Input Your Information</v4:PostalCode>
               <v4:CountryCode>Input Your Information</v4:CountryCode>
            </v4:EffectiveAddress>
            <v4:ParsedAddressPartsDetail>
               <v4:ParsedStreetLine>
                  <v4:HouseNumber>Input Your Information</v4:HouseNumber>
                  <v4:LeadingDirectional>Input Your Information</v4:LeadingDirectional>
                  <v4:StreetName>Input Your Information</v4:StreetName>
                  <v4:StreetSuffix>Input Your Information</v4:StreetSuffix>
               </v4:ParsedStreetLine>
               <v4:ParsedPostalCode>
                  <v4:Base>Input Your Information</v4:Base>
                  <v4:AddOn>Input Your Information</v4:AddOn>
                  <v4:DeliveryPoint>Input Your Information</v4:DeliveryPoint>
               </v4:ParsedPostalCode>
            </v4:ParsedAddressPartsDetail>
            <v4:Attributes>
               <v4:Name>CountrySupported</v4:Name>
               <v4:Value>true</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>SuiteRequiredButMissing</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>InvalidSuiteNumber</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>Resolved</v4:Name>
               <v4:Value>true</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>ValidMultiUnit</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>POBox</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>MultiUnitBase</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>StreetRange</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>InterpolatedStreetAddress</v4:Name>
               <v4:Value>true</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>Intersection</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
            <v4:Attributes>
               <v4:Name>RRConversion</v4:Name>
               <v4:Value>false</v4:Value>
            </v4:Attributes>
         </v4:AddressResults>
      </v4:AddressValidationReply>
   </soapenv:Body>
</soapenv:Envelope>
"""
