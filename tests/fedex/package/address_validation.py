import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import AddressValidationRequest
from purplship.package import Address
from tests.fedex.package.fixture import gateway


class TestFedexAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        self.assertEqual(request.serialize(), AddressValidationRequestXML,)

    @patch("purplship.package.mappers.fedex.proxy.http", return_value="<a></a>")
    def test_validated_address(self, http_mock):
        Address.validate(self.AddressValidationRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.settings.server_url)

    def test_parse_address_validation_response(self):
        with patch("purplship.package.mappers.fedex.proxy.http") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                Address.validate(self.AddressValidationRequest).from_(gateway).parse()
            )

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedAddressValidationResponse))


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {}

ParsedAddressValidationResponse = {}


AddressValidationRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v4="http://fedex.com/ws/addressvalidation/v4">
   <soapenv:Header/>
   <soapenv:Body>
      <v4:AddressValidationRequest>
         <v4:WebAuthenticationDetail>
            <v4:ParentCredential>
               <v4:Key>Input Your Information</v4:Key>
               <v4:Password>Input Your Information</v4:Password>
            </v4:ParentCredential>
            <v4:UserCredential>
               <v4:Key>Input Your Information</v4:Key>
               <v4:Password>Input Your Information</v4:Password>
            </v4:UserCredential>
         </v4:WebAuthenticationDetail>
         <v4:ClientDetail>
            <v4:AccountNumber>Input Your Information</v4:AccountNumber>
            <v4:MeterNumber>Input Your Information</v4:MeterNumber>
            <v4:Localization>
               <v4:LanguageCode>EN</v4:LanguageCode>
               <v4:LocaleCode>CA</v4:LocaleCode>
            </v4:Localization>
         </v4:ClientDetail>
         <v4:TransactionDetail>
            <v4:CustomerTransactionId>AddressValidationRequest_v4</v4:CustomerTransactionId>
            <v4:Localization>
               <v4:LanguageCode>EN</v4:LanguageCode>
               <v4:LocaleCode>CA</v4:LocaleCode>
            </v4:Localization>
         </v4:TransactionDetail>
         <v4:Version>
            <v4:ServiceId>aval</v4:ServiceId>
            <v4:Major>4</v4:Major>
            <v4:Intermediate>0</v4:Intermediate>
            <v4:Minor>0</v4:Minor>
         </v4:Version>
         <v4:InEffectAsOfTimestamp>2015-03-09T01:21:14+05:30</v4:InEffectAsOfTimestamp>
         <v4:AddressesToValidate>
            <v4:ClientReferenceId>ac vinclis et</v4:ClientReferenceId>
            <v4:Contact>
               <v4:ContactId>Input Your Information</v4:ContactId>
               <v4:PersonName>Input Your Information</v4:PersonName>
               <v4:CompanyName>Input Your Information</v4:CompanyName>
               <v4:PhoneNumber>Input Your Information</v4:PhoneNumber>
               <v4:EMailAddress>Input Your Information</v4:EMailAddress>
            </v4:Contact>
            <v4:Address>
               <v4:StreetLines>Input Your Information</v4:StreetLines>
               <v4:City>Input Your Information</v4:City>
               <v4:StateOrProvinceCode>Input Your Information</v4:StateOrProvinceCode>
               <v4:PostalCode>Input Your Information</v4:PostalCode>
               <v4:UrbanizationCode>Input Your Information</v4:UrbanizationCode>
               <v4:CountryCode>Input Your Information</v4:CountryCode>
               <v4:Residential>0</v4:Residential>
            </v4:Address>
         </v4:AddressesToValidate>
      </v4:AddressValidationRequest>
   </soapenv:Body>
</soapenv:Envelope>

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
