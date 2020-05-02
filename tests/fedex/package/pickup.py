import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import PickupRequest, PickupCancellationRequest, PickupUpdateRequest
from purplship.package import Pickup
from .fixture import gateway


class TestFedExPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
    #     self.PickupRequest = PickupRequest(**PickupRequestData)
    #     self.PickupUpdateRequest = PickupUpdateRequest(**PickupUpdateRequestData)
    #     self.PickupCancelRequest = PickupCancellationRequest(**PickupCancelRequestData)
    #
    # def test_create_pickup_request(self):
    #     request = gateway.mapper.create_pickup_request(self.PickupRequest)
    #
    #     pipeline = request.serialize()
    #     availability_request = pipeline["availability"]().data
    #     create_pickup = pipeline["create_pickup"](PickupAvailabilityResponseXML).data
    #
    #     self.assertEqual(availability_request, PickupAvailabilityRequestXML)
    #     self.assertEqual(create_pickup, PickupRequestXML)
    #
    # def test_update_pickup_request(self):
    #     request = gateway.mapper.create_pickup_request(self.PickupRequest)
    #
    #     pipeline = request.serialize()
    #     availability_request = pipeline["availability"]().data
    #     cancel_pickup = pipeline["cancel_pickup"](PickupAvailabilityResponseXML).data
    #     create_pickup = pipeline["create_pickup"](PickupAvailabilityResponseXML).data
    #
    #     self.assertEqual(availability_request, PickupAvailabilityRequestXML)
    #     self.assertEqual(cancel_pickup, PickupCancelRequestXML)
    #     self.assertEqual(create_pickup, PickupRequestXML)
    #
    # def test_cancel_pickup_request(self):
    #     request = gateway.mapper.create_pickup_request(self.PickupRequest)
    #
    #     self.assertEqual(request.serialize(), PickupCancelRequestXML)
    #
    # def test_create_pickup(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mocks:
    #         mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
    #         Pickup.book(self.PickupRequest).with_(gateway)
    #
    #         availability_call, create_call = mocks.call_args_list
    #
    #         self.assertEqual(
    #             availability_call[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
    #         )
    #         self.assertEqual(
    #             create_call[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
    #         )
    #
    # def test_update_pickup(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mocks:
    #         mocks.side_effect = [PickupAvailabilityResponseXML, PickupCancelResponseXML, PickupResponseXML]
    #         Pickup.book(self.PickupRequest).with_(gateway)
    #
    #         availability_call, cancel_call, create_call = mocks.call_args_list
    #
    #         self.assertEqual(
    #             availability_call[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
    #         )
    #         self.assertEqual(
    #             cancel_call[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
    #         )
    #         self.assertEqual(
    #             create_call[1]["url"],
    #             f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
    #         )
    #
    # def test_cancel_pickup(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mock:
    #         mock.return_value = "<a></a>"
    #         Pickup.cancel(self.PickupCancelRequest).with_(gateway)
    #
    #         url = mock.call_args[1]["url"]
    #         self.assertEqual(url, gateway.settings.server_url)
    #
    # def test_parse_pickup_cancel_response(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mock:
    #         mock.return_value = PickupCancelResponseXML
    #         parsed_response = Pickup.cancel(self.PickupCancelRequest).with_(gateway).parse()
    #
    #         self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupCancelResponse))
    #
    # def test_parse_pickup_response(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mocks:
    #         mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
    #         parsed_response = Pickup.book(self.PickupRequest).with_(gateway).parse()
    #
    #         self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupResponse))
    #
    # def test_parse_pickup_unavailable_response(self):
    #     with patch("purplship.package.mappers.fedex.proxy.http") as mocks:
    #         mocks.side_effect = [PickupAvailabilityErrorResponseXML]
    #         parsed_response = Pickup.book(self.PickupRequest).with_(gateway).parse()
    #
    #         self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupErrorResponse))


if __name__ == "__main__":
    unittest.main()


PickupRequestData = {}

PickupUpdateRequestData = {}

PickupCancelRequestData = {}


ParsedPickupResponse = []

ParsedPickupErrorResponse = []

ParsedPickupCancelResponse = []


PickupAvailabilityRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <soapenv:Header />
    <soapenv:Body>
        <v17:PickupAvailabilityRequest>
            <v17:WebAuthenticationDetail>
                <v17:ParentCredential>
                    <v17:Key>INPUT YOUR INFORMATION</v17:Key>
                    <v17:Password>INPUT YOUR INFORMATION</v17:Password>
                </v17:ParentCredential>
                <v17:UserCredential>
                    <v17:Key>INPUT YOUR INFORMATION</v17:Key>
                    <v17:Password>INPUT YOUR INFORMATION</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>XXXXXXXXX</v17:AccountNumber>
                <v17:MeterNumber>XXXXXXX</v17:MeterNumber>
                <v17:Localization>
                    <v17:LanguageCode>EN</v17:LanguageCode>
                    <v17:LocaleCode>ES</v17:LocaleCode>
                </v17:Localization>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>pickup_availability</v17:CustomerTransactionId>
                <v17:Localization>
                    <v17:LanguageCode>EN</v17:LanguageCode>
                    <v17:LocaleCode>ES</v17:LocaleCode>
                </v17:Localization>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:PickupAddress>
                <v17:StreetLines>INPUT YOUR INFORMATION</v17:StreetLines>
                <v17:City>HAMBURG</v17:City>
                <v17:StateOrProvinceCode>HH</v17:StateOrProvinceCode>
                <v17:PostalCode>22415</v17:PostalCode>
                <v17:CountryCode>DE</v17:CountryCode>
                <v17:Residential>1</v17:Residential>
                <v17:GeographicCoordinates>ac vinclis</v17:GeographicCoordinates>
            </v17:PickupAddress>
            <v17:PickupRequestType>SAME_DAY</v17:PickupRequestType>
            <v17:DispatchDate>2016-02-26</v17:DispatchDate>
            <v17:NumberOfBusinessDays>3</v17:NumberOfBusinessDays>
            <v17:PackageReadyTime>15:00:00</v17:PackageReadyTime>
            <v17:CustomerCloseTime>17:00:00</v17:CustomerCloseTime>
            <v17:Carriers>FDXE</v17:Carriers>
            <v17:ShipmentAttributes>
                <v17:ServiceType>PRIORITY_OVERNIGHT</v17:ServiceType>
                <v17:PackagingType>YOUR_PACKAGING</v17:PackagingType>
                <v17:Dimensions>
                    <v17:Length>12</v17:Length>
                    <v17:Width>12</v17:Width>
                    <v17:Height>12</v17:Height>
                    <v17:Units>IN</v17:Units>
                </v17:Dimensions>
                <v17:Weight>
                    <v17:Units>LB</v17:Units>
                    <v17:Value>150.0</v17:Value>
                </v17:Weight>
            </v17:ShipmentAttributes>
        </v17:PickupAvailabilityRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupCancelRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://fedex.com/ws/pickup/v17">
    <soapenv:Header />
    <soapenv:Body>
        <CancelPickupRequest>
            <WebAuthenticationDetail>
                <ParentCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </ParentCredential>
                <UserCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>XXXXXXXXX</AccountNumber>
                <MeterNumber>XXXXXXX</MeterNumber>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>US</LocaleCode>
                </Localization>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>v17 CancelPickup_ExpUS</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>US</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <CarrierCode>FDXE</CarrierCode>
            <PickupConfirmationNumber>INPUT YOUR INFORMATION</PickupConfirmationNumber>
            <ScheduledDate>${= String.format('%tF', new Date() )}</ScheduledDate>
            <Location>NQAA</Location>
            <Remarks>Preet</Remarks>
            <Reason>TXT</Reason>
            <ContactName>Radhika</ContactName>
        </CancelPickupRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://fedex.com/ws/pickup/v17">
    <soapenv:Header />
    <soapenv:Body>
        <CreatePickupRequest>
            <WebAuthenticationDetail>
                <ParentCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </ParentCredential>
                <UserCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>XXXXXXXXX</AccountNumber>
                <MeterNumber>XXXXXXX</MeterNumber>
                <IntegratorId>12345</IntegratorId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>CreatePickupRequest_v17</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <AssociatedAccountNumber>
                <Type>FEDEX_EXPRESS</Type>
                <AccountNumber>XXXXXXXXXXX</AccountNumber>
            </AssociatedAccountNumber>
            <OriginDetail>
                <PickupLocation>
                    <Contact>
                        <ContactId>KR1059</ContactId>
                        <PersonName>INPUT YOUR INFORMATION</PersonName>
                        <Title>Mr.</Title>
                        <CompanyName>DEOYAROHIT0905$</CompanyName>
                        <PhoneNumber>INPUT YOUR INFORMATION</PhoneNumber>
                        <PhoneExtension>INPUT YOUR INFORMATION</PhoneExtension>
                        <PagerNumber>XXXXXXXXXX</PagerNumber>
                        <FaxNumber>XXXXXXXXXX</FaxNumber>
                        <EMailAddress>kaustubha_ramdasi@syntelinc.com</EMailAddress>
                    </Contact>
                    <Address>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <City>Memphis</City>
                        <StateOrProvinceCode>TN</StateOrProvinceCode>
                        <PostalCode>38125</PostalCode>
                        <CountryCode>US</CountryCode>
                    </Address>
                </PickupLocation>
                <PackageLocation>FRONT</PackageLocation>
                <BuildingPart>DEPARTMENT</BuildingPart>
                <BuildingPartDescription>BuildingPartDescription</BuildingPartDescription>
                <ReadyTimestamp>${=String.format('%tF', new Date())}T12:34:56-06:00</ReadyTimestamp>
                <CompanyCloseTime>19:00:00</CompanyCloseTime>
                <Location>NQAA</Location>
                <SuppliesRequested>SuppliesRequested</SuppliesRequested>
            </OriginDetail>
            <PackageCount>1</PackageCount>
            <TotalWeight>
                <Units>LB</Units>
                <Value>50.0</Value>
            </TotalWeight>
            <CarrierCode>FDXE</CarrierCode>
            <OversizePackageCount>0</OversizePackageCount>
            <Remarks>Remarks</Remarks>
            <CommodityDescription>TEST ENVIRONMENT - PLEASE DO NOT PROCESS PICKUP</CommodityDescription>
            <CountryRelationship>DOMESTIC</CountryRelationship>
        </CreatePickupRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupUpdateRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://fedex.com/ws/pickup/v17">
    <soapenv:Header />
    <soapenv:Body>
        <CreatePickupRequest>
            <WebAuthenticationDetail>
                <ParentCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </ParentCredential>
                <UserCredential>
                    <Key>INPUT YOUR INFORMATION</Key>
                    <Password>INPUT YOUR INFORMATION</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>XXXXXXXXX</AccountNumber>
                <MeterNumber>XXXXXXX</MeterNumber>
                <IntegratorId>12345</IntegratorId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>CreatePickupRequest_v17</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <AssociatedAccountNumber>
                <Type>FEDEX_EXPRESS</Type>
                <AccountNumber>XXXXXXXXXXX</AccountNumber>
            </AssociatedAccountNumber>
            <OriginDetail>
                <PickupLocation>
                    <Contact>
                        <ContactId>KR1059</ContactId>
                        <PersonName>INPUT YOUR INFORMATION</PersonName>
                        <Title>Mr.</Title>
                        <CompanyName>DEOYAROHIT0905$</CompanyName>
                        <PhoneNumber>INPUT YOUR INFORMATION</PhoneNumber>
                        <PhoneExtension>INPUT YOUR INFORMATION</PhoneExtension>
                        <PagerNumber>XXXXXXXXXX</PagerNumber>
                        <FaxNumber>XXXXXXXXXX</FaxNumber>
                        <EMailAddress>kaustubha_ramdasi@syntelinc.com</EMailAddress>
                    </Contact>
                    <Address>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <StreetLines>INPUT YOUR INFORMATION</StreetLines>
                        <City>Memphis</City>
                        <StateOrProvinceCode>TN</StateOrProvinceCode>
                        <PostalCode>38125</PostalCode>
                        <CountryCode>US</CountryCode>
                    </Address>
                </PickupLocation>
                <PackageLocation>FRONT</PackageLocation>
                <BuildingPart>DEPARTMENT</BuildingPart>
                <BuildingPartDescription>BuildingPartDescription</BuildingPartDescription>
                <ReadyTimestamp>${=String.format('%tF', new Date())}T12:34:56-06:00</ReadyTimestamp>
                <CompanyCloseTime>19:00:00</CompanyCloseTime>
                <Location>NQAA</Location>
                <SuppliesRequested>SuppliesRequested</SuppliesRequested>
            </OriginDetail>
            <PackageCount>1</PackageCount>
            <TotalWeight>
                <Units>LB</Units>
                <Value>50.0</Value>
            </TotalWeight>
            <CarrierCode>FDXE</CarrierCode>
            <OversizePackageCount>0</OversizePackageCount>
            <Remarks>Remarks</Remarks>
            <CommodityDescription>TEST ENVIRONMENT - PLEASE DO NOT PROCESS PICKUP</CommodityDescription>
            <CountryRelationship>DOMESTIC</CountryRelationship>
        </CreatePickupRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""


PickupCancelResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <CancelPickupReply xmlns="http://fedex.com/ws/pickup/v17">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>disp</Source>
                <Code>0000</Code>
                <Message>Success</Message>
                <LocalizedMessage>Success</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>v17 CancelPickup_ExpUS</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>US</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
        </CancelPickupReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

PickupAvailabilityResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <PickupAvailabilityReply xmlns="http://fedex.com/ws/pickup/v17">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>disp</Source>
                <Code>0000</Code>
                <Message>Success</Message>
                <LocalizedMessage>Success</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>pickup_availability</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <RequestTimestamp>2017-12-13T08:28:00</RequestTimestamp>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-13</PickupDate>
                <CutOffTime>17:01:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>DOMESTIC</CountryRelationship>
            </Options>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-13</PickupDate>
                <CutOffTime>17:01:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>INTERNATIONAL</CountryRelationship>
            </Options>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-14</PickupDate>
                <CutOffTime>17:01:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>DOMESTIC</CountryRelationship>
            </Options>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-14</PickupDate>
                <CutOffTime>17:01:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>INTERNATIONAL</CountryRelationship>
            </Options>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-15</PickupDate>
                <CutOffTime>17:00:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>INTERNATIONAL</CountryRelationship>
            </Options>
            <Options>
                <Carrier>FDXE</Carrier>
                <ScheduleDay>SAME_DAY</ScheduleDay>
                <Available>true</Available>
                <PickupDate>2017-12-15</PickupDate>
                <CutOffTime>17:01:00</CutOffTime>
                <AccessTime>PT1H30M</AccessTime>
                <ResidentialAvailable>false</ResidentialAvailable>
                <CountryRelationship>DOMESTIC</CountryRelationship>
            </Options>
        </PickupAvailabilityReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

PickupAvailabilityErrorResponseXML = """
"""

PickupResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <CreatePickupReply xmlns="http://fedex.com/ws/pickup/v17">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>disp</Source>
                <Code>0000</Code>
                <Message>Success</Message>
                <LocalizedMessage>Success</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>CreatePickupRequest_v17</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>ES</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>17</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <PickupConfirmationNumber>INPUT YOUR INFORMATION</PickupConfirmationNumber>
            <Location>NQAA</Location>
        </CreatePickupReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
