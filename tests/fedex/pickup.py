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
from tests.fedex.fixture import gateway

logger = logging.getLogger(__name__)


class TestFedExPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        pipeline = request.serialize()
        get_availability_request = pipeline["get_availability"]()
        create_pickup_request = pipeline["create_pickup"](PickupAvailabilityResponseXML)

        self.assertEqual(
            get_availability_request.data.serialize(), PickupAvailabilityRequestXML
        )
        self.assertEqual(create_pickup_request.data.serialize(), PickupRequestXML)

    def test_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        pipeline = request.serialize()
        get_availability_request = pipeline["get_availability"]()
        create_pickup_request = pipeline["create_pickup"](PickupAvailabilityResponseXML)
        cancel_pickup_request = pipeline["cancel_pickup"](PickupResponseXML)

        self.assertEqual(
            get_availability_request.data.serialize(),
            PickupUpdateAvailabilityRequestXML,
        )
        self.assertEqual(create_pickup_request.data.serialize(), PickupUpdateRequestXML)
        self.assertEqual(cancel_pickup_request.data.serialize(), PickupCancelRequestXML)

    def test_create_pickup(self):
        with patch("purplship.mappers.fedex.proxy.http") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            purplship.Pickup.schedule(self.PickupRequest).from_(gateway)

            availability_call, create_call = mocks.call_args_list
            self.assertEqual(
                availability_call[1]["url"],
                f"{gateway.settings.server_url}/pickup",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/pickup",
            )

    def test_update_pickup(self):
        with patch("purplship.mappers.fedex.proxy.http") as mocks:
            mocks.side_effect = [
                PickupAvailabilityResponseXML,
                PickupResponseXML,
                PickupCancelResponseXML,
            ]
            purplship.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            availability_call, create_call, cancel_call = mocks.call_args_list
            self.assertEqual(
                availability_call[1]["url"],
                f"{gateway.settings.server_url}/pickup",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/pickup",
            )
            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}/pickup",
            )

    def test_parse_pickup_reply(self):
        with patch("purplship.mappers.fedex.proxy.http") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            parsed_response = (
                purplship.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_cancel_reply(self):
        with patch("purplship.mappers.fedex.proxy.http") as mock:
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
        "phone_number": "800-555-1212",
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
        "phone_number": "800-555-1212",
    },
    "parcels": [{"weight": 24, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_cancel_data = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "fedex",
        "confirmation_number": "0074698052",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "fedex",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupAvailabilityRequestXML = """<tns:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <tns:Body>
        <v17:PickupAvailabilityRequest>
            <v17:WebAuthenticationDetail>
                <v17:UserCredential>
                    <v17:Key>user_key</v17:Key>
                    <v17:Password>password</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>2349857</v17:AccountNumber>
                <v17:MeterNumber>1293587</v17:MeterNumber>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>FTC</v17:CustomerTransactionId>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:AccountNumber>
                <v17:Type>FEDEX_EXPRESS</v17:Type>
                <v17:AccountNumber>2349857</v17:AccountNumber>
            </v17:AccountNumber>
            <v17:PickupAddress>
                <v17:StreetLines>2271 Herring Cove</v17:StreetLines>
                <v17:City>Halifax</v17:City>
                <v17:StateOrProvinceCode>NS</v17:StateOrProvinceCode>
                <v17:PostalCode>B3L2C2</v17:PostalCode>
                <v17:CountryCode>CA</v17:CountryCode>
                <v17:Residential>true</v17:Residential>
            </v17:PickupAddress>
            <v17:PickupRequestType>FUTURE_DAY</v17:PickupRequestType>
            <v17:DispatchDate>2015-01-28</v17:DispatchDate>
            <v17:PackageReadyTime>15:00:00</v17:PackageReadyTime>
            <v17:CustomerCloseTime>17:00:00</v17:CustomerCloseTime>
            <v17:Carriers>FDXE</v17:Carriers>
        </v17:PickupAvailabilityRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupRequestXML = """<tns:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <tns:Body>
        <v17:CreatePickupRequest>
            <v17:WebAuthenticationDetail>
                <v17:UserCredential>
                    <v17:Key>user_key</v17:Key>
                    <v17:Password>password</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>2349857</v17:AccountNumber>
                <v17:MeterNumber>1293587</v17:MeterNumber>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>FTC</v17:CustomerTransactionId>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:AssociatedAccountNumber>
                <v17:Type>FEDEX_EXPRESS</v17:Type>
                <v17:AccountNumber>2349857</v17:AccountNumber>
            </v17:AssociatedAccountNumber>
            <v17:OriginDetail>
                <v17:PickupLocation>
                    <v17:Contact>
                        <v17:PersonName>John Doe</v17:PersonName>
                        <v17:CompanyName>Jim Duggan</v17:CompanyName>
                        <v17:PhoneNumber>800-555-1212</v17:PhoneNumber>
                        <v17:EMailAddress>john.doe@canadapost.ca</v17:EMailAddress>
                    </v17:Contact>
                    <v17:Address>
                        <v17:StreetLines>2271 Herring Cove</v17:StreetLines>
                        <v17:City>Halifax</v17:City>
                        <v17:StateOrProvinceCode>NS</v17:StateOrProvinceCode>
                        <v17:PostalCode>B3L2C2</v17:PostalCode>
                        <v17:CountryCode>CA</v17:CountryCode>
                        <v17:Residential>true</v17:Residential>
                    </v17:Address>
                </v17:PickupLocation>
                <v17:ReadyTimestamp>2015-01-28T15:00:00</v17:ReadyTimestamp>
                <v17:CompanyCloseTime>17:00:00</v17:CompanyCloseTime>
                <v17:PickupDateType>FUTURE_DAY</v17:PickupDateType>
            </v17:OriginDetail>
            <v17:PackageCount>1</v17:PackageCount>
            <v17:CarrierCode>FDXE</v17:CarrierCode>
            <v17:Remarks>Door at Back</v17:Remarks>
        </v17:CreatePickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateAvailabilityRequestXML = """<tns:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <tns:Body>
        <v17:PickupAvailabilityRequest>
            <v17:WebAuthenticationDetail>
                <v17:UserCredential>
                    <v17:Key>user_key</v17:Key>
                    <v17:Password>password</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>2349857</v17:AccountNumber>
                <v17:MeterNumber>1293587</v17:MeterNumber>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>FTC</v17:CustomerTransactionId>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:AccountNumber>
                <v17:Type>FEDEX_EXPRESS</v17:Type>
                <v17:AccountNumber>2349857</v17:AccountNumber>
            </v17:AccountNumber>
            <v17:PickupAddress>
                <v17:Residential>false</v17:Residential>
            </v17:PickupAddress>
            <v17:PickupRequestType>FUTURE_DAY</v17:PickupRequestType>
            <v17:DispatchDate>2015-01-28</v17:DispatchDate>
            <v17:PackageReadyTime>15:00:00</v17:PackageReadyTime>
            <v17:CustomerCloseTime>17:00:00</v17:CustomerCloseTime>
            <v17:Carriers>FDXE</v17:Carriers>
        </v17:PickupAvailabilityRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateRequestXML = """<tns:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <tns:Body>
        <v17:CreatePickupRequest>
            <v17:WebAuthenticationDetail>
                <v17:UserCredential>
                    <v17:Key>user_key</v17:Key>
                    <v17:Password>password</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>2349857</v17:AccountNumber>
                <v17:MeterNumber>1293587</v17:MeterNumber>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>FTC</v17:CustomerTransactionId>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:AssociatedAccountNumber>
                <v17:Type>FEDEX_EXPRESS</v17:Type>
                <v17:AccountNumber>2349857</v17:AccountNumber>
            </v17:AssociatedAccountNumber>
            <v17:OriginDetail>
                <v17:PickupLocation>
                    <v17:Contact>
                        <v17:PersonName>Jane Doe</v17:PersonName>
                        <v17:PhoneNumber>800-555-1212</v17:PhoneNumber>
                        <v17:EMailAddress>john.doe@canadapost.ca</v17:EMailAddress>
                    </v17:Contact>
                    <v17:Address>
                        <v17:Residential>false</v17:Residential>
                    </v17:Address>
                </v17:PickupLocation>
                <v17:ReadyTimestamp>2015-01-28T15:00:00</v17:ReadyTimestamp>
                <v17:CompanyCloseTime>17:00:00</v17:CompanyCloseTime>
                <v17:PickupDateType>FUTURE_DAY</v17:PickupDateType>
            </v17:OriginDetail>
            <v17:PackageCount>1</v17:PackageCount>
            <v17:TotalWeight>
                <v17:Units>LB</v17:Units>
                <v17:Value>52.92</v17:Value>
            </v17:TotalWeight>
            <v17:CarrierCode>FDXE</v17:CarrierCode>
            <v17:Remarks>Door at Back</v17:Remarks>
        </v17:CreatePickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelRequestXML = """<tns:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v17="http://fedex.com/ws/pickup/v17">
    <tns:Body>
        <v17:CancelPickupRequest>
            <v17:WebAuthenticationDetail>
                <v17:UserCredential>
                    <v17:Key>user_key</v17:Key>
                    <v17:Password>password</v17:Password>
                </v17:UserCredential>
            </v17:WebAuthenticationDetail>
            <v17:ClientDetail>
                <v17:AccountNumber>2349857</v17:AccountNumber>
                <v17:MeterNumber>1293587</v17:MeterNumber>
            </v17:ClientDetail>
            <v17:TransactionDetail>
                <v17:CustomerTransactionId>FTC</v17:CustomerTransactionId>
            </v17:TransactionDetail>
            <v17:Version>
                <v17:ServiceId>disp</v17:ServiceId>
                <v17:Major>17</v17:Major>
                <v17:Intermediate>0</v17:Intermediate>
                <v17:Minor>0</v17:Minor>
            </v17:Version>
            <v17:CarrierCode>FDXE</v17:CarrierCode>
            <v17:PickupConfirmationNumber>0074698052</v17:PickupConfirmationNumber>
        </v17:CancelPickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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

PickupAvailabilityResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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

PickupResponseXML = f"""<wrapper>
    {PickupAvailabilityResponseXML}
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
                <PickupConfirmationNumber>0074698052</PickupConfirmationNumber>
                <Location>NQAA</Location>
            </CreatePickupReply>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    {PickupCancelResponseXML}
</wrapper>
"""
