import logging
import unittest
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from .fixture import gateway

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
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

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
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mocks:
            mocks.side_effect = [
                PickupAvailabilityResponseXML,
                PickupResponseXML,
                PickupCancelResponseXML,
            ]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

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
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_cancel_reply(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponseXML
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedPickupCancelResponse
            )


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
        "carrier_name": "fedex_ws",
        "confirmation_number": "0074698052",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "fedex_ws",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupAvailabilityRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v22="http://fedex.com/ws/pickup/v22">
    <tns:Body>
        <v22:PickupAvailabilityRequest>
            <v22:WebAuthenticationDetail>
                <v22:UserCredential>
                    <v22:Key>user_key</v22:Key>
                    <v22:Password>password</v22:Password>
                </v22:UserCredential>
            </v22:WebAuthenticationDetail>
            <v22:ClientDetail>
                <v22:AccountNumber>2349857</v22:AccountNumber>
                <v22:MeterNumber>1293587</v22:MeterNumber>
            </v22:ClientDetail>
            <v22:TransactionDetail>
                <v22:CustomerTransactionId>FTC</v22:CustomerTransactionId>
            </v22:TransactionDetail>
            <v22:Version>
                <v22:ServiceId>disp</v22:ServiceId>
                <v22:Major>22</v22:Major>
                <v22:Intermediate>0</v22:Intermediate>
                <v22:Minor>0</v22:Minor>
            </v22:Version>
            <v22:AccountNumber>
                <v22:Type>FEDEX_EXPRESS</v22:Type>
                <v22:AccountNumber>2349857</v22:AccountNumber>
            </v22:AccountNumber>
            <v22:PickupAddress>
                <v22:StreetLines>2271 Herring Cove</v22:StreetLines>
                <v22:City>Halifax</v22:City>
                <v22:StateOrProvinceCode>NS</v22:StateOrProvinceCode>
                <v22:PostalCode>B3L2C2</v22:PostalCode>
                <v22:CountryCode>CA</v22:CountryCode>
                <v22:Residential>true</v22:Residential>
            </v22:PickupAddress>
            <v22:PickupRequestType>FUTURE_DAY</v22:PickupRequestType>
            <v22:DispatchDate>2015-01-28</v22:DispatchDate>
            <v22:PackageReadyTime>15:00:00</v22:PackageReadyTime>
            <v22:CustomerCloseTime>17:00:00</v22:CustomerCloseTime>
            <v22:Carriers>FDXE</v22:Carriers>
        </v22:PickupAvailabilityRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v22="http://fedex.com/ws/pickup/v22">
    <tns:Body>
        <v22:CreatePickupRequest>
            <v22:WebAuthenticationDetail>
                <v22:UserCredential>
                    <v22:Key>user_key</v22:Key>
                    <v22:Password>password</v22:Password>
                </v22:UserCredential>
            </v22:WebAuthenticationDetail>
            <v22:ClientDetail>
                <v22:AccountNumber>2349857</v22:AccountNumber>
                <v22:MeterNumber>1293587</v22:MeterNumber>
            </v22:ClientDetail>
            <v22:TransactionDetail>
                <v22:CustomerTransactionId>FTC</v22:CustomerTransactionId>
            </v22:TransactionDetail>
            <v22:Version>
                <v22:ServiceId>disp</v22:ServiceId>
                <v22:Major>22</v22:Major>
                <v22:Intermediate>0</v22:Intermediate>
                <v22:Minor>0</v22:Minor>
            </v22:Version>
            <v22:AssociatedAccountNumber>
                <v22:Type>FEDEX_EXPRESS</v22:Type>
                <v22:AccountNumber>2349857</v22:AccountNumber>
            </v22:AssociatedAccountNumber>
            <v22:OriginDetail>
                <v22:PickupLocation>
                    <v22:Contact>
                        <v22:PersonName>John Doe</v22:PersonName>
                        <v22:CompanyName>Jim Duggan</v22:CompanyName>
                        <v22:PhoneNumber>800-555-1212</v22:PhoneNumber>
                        <v22:EMailAddress>john.doe@canadapost.ca</v22:EMailAddress>
                    </v22:Contact>
                    <v22:Address>
                        <v22:StreetLines>2271 Herring Cove</v22:StreetLines>
                        <v22:City>Halifax</v22:City>
                        <v22:StateOrProvinceCode>NS</v22:StateOrProvinceCode>
                        <v22:PostalCode>B3L2C2</v22:PostalCode>
                        <v22:CountryCode>CA</v22:CountryCode>
                        <v22:Residential>true</v22:Residential>
                    </v22:Address>
                </v22:PickupLocation>
                <v22:ReadyTimestamp>2015-01-28T15:00:00</v22:ReadyTimestamp>
                <v22:CompanyCloseTime>17:00:00</v22:CompanyCloseTime>
                <v22:PickupDateType>FUTURE_DAY</v22:PickupDateType>
            </v22:OriginDetail>
            <v22:PackageCount>1</v22:PackageCount>
            <v22:CarrierCode>FDXE</v22:CarrierCode>
            <v22:Remarks>Door at Back</v22:Remarks>
        </v22:CreatePickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateAvailabilityRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v22="http://fedex.com/ws/pickup/v22">
    <tns:Body>
        <v22:PickupAvailabilityRequest>
            <v22:WebAuthenticationDetail>
                <v22:UserCredential>
                    <v22:Key>user_key</v22:Key>
                    <v22:Password>password</v22:Password>
                </v22:UserCredential>
            </v22:WebAuthenticationDetail>
            <v22:ClientDetail>
                <v22:AccountNumber>2349857</v22:AccountNumber>
                <v22:MeterNumber>1293587</v22:MeterNumber>
            </v22:ClientDetail>
            <v22:TransactionDetail>
                <v22:CustomerTransactionId>FTC</v22:CustomerTransactionId>
            </v22:TransactionDetail>
            <v22:Version>
                <v22:ServiceId>disp</v22:ServiceId>
                <v22:Major>22</v22:Major>
                <v22:Intermediate>0</v22:Intermediate>
                <v22:Minor>0</v22:Minor>
            </v22:Version>
            <v22:AccountNumber>
                <v22:Type>FEDEX_EXPRESS</v22:Type>
                <v22:AccountNumber>2349857</v22:AccountNumber>
            </v22:AccountNumber>
            <v22:PickupAddress>
                <v22:Residential>false</v22:Residential>
            </v22:PickupAddress>
            <v22:PickupRequestType>FUTURE_DAY</v22:PickupRequestType>
            <v22:DispatchDate>2015-01-28</v22:DispatchDate>
            <v22:PackageReadyTime>15:00:00</v22:PackageReadyTime>
            <v22:CustomerCloseTime>17:00:00</v22:CustomerCloseTime>
            <v22:Carriers>FDXE</v22:Carriers>
        </v22:PickupAvailabilityRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupUpdateRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v22="http://fedex.com/ws/pickup/v22">
    <tns:Body>
        <v22:CreatePickupRequest>
            <v22:WebAuthenticationDetail>
                <v22:UserCredential>
                    <v22:Key>user_key</v22:Key>
                    <v22:Password>password</v22:Password>
                </v22:UserCredential>
            </v22:WebAuthenticationDetail>
            <v22:ClientDetail>
                <v22:AccountNumber>2349857</v22:AccountNumber>
                <v22:MeterNumber>1293587</v22:MeterNumber>
            </v22:ClientDetail>
            <v22:TransactionDetail>
                <v22:CustomerTransactionId>FTC</v22:CustomerTransactionId>
            </v22:TransactionDetail>
            <v22:Version>
                <v22:ServiceId>disp</v22:ServiceId>
                <v22:Major>22</v22:Major>
                <v22:Intermediate>0</v22:Intermediate>
                <v22:Minor>0</v22:Minor>
            </v22:Version>
            <v22:AssociatedAccountNumber>
                <v22:Type>FEDEX_EXPRESS</v22:Type>
                <v22:AccountNumber>2349857</v22:AccountNumber>
            </v22:AssociatedAccountNumber>
            <v22:OriginDetail>
                <v22:PickupLocation>
                    <v22:Contact>
                        <v22:PersonName>Jane Doe</v22:PersonName>
                        <v22:PhoneNumber>800-555-1212</v22:PhoneNumber>
                        <v22:EMailAddress>john.doe@canadapost.ca</v22:EMailAddress>
                    </v22:Contact>
                    <v22:Address>
                        <v22:Residential>false</v22:Residential>
                    </v22:Address>
                </v22:PickupLocation>
                <v22:ReadyTimestamp>2015-01-28T15:00:00</v22:ReadyTimestamp>
                <v22:CompanyCloseTime>17:00:00</v22:CompanyCloseTime>
                <v22:PickupDateType>FUTURE_DAY</v22:PickupDateType>
            </v22:OriginDetail>
            <v22:PackageCount>1</v22:PackageCount>
            <v22:TotalWeight>
                <v22:Units>LB</v22:Units>
                <v22:Value>52.92</v22:Value>
            </v22:TotalWeight>
            <v22:CarrierCode>FDXE</v22:CarrierCode>
            <v22:Remarks>Door at Back</v22:Remarks>
        </v22:CreatePickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v22="http://fedex.com/ws/pickup/v22">
    <tns:Body>
        <v22:CancelPickupRequest>
            <v22:WebAuthenticationDetail>
                <v22:UserCredential>
                    <v22:Key>user_key</v22:Key>
                    <v22:Password>password</v22:Password>
                </v22:UserCredential>
            </v22:WebAuthenticationDetail>
            <v22:ClientDetail>
                <v22:AccountNumber>2349857</v22:AccountNumber>
                <v22:MeterNumber>1293587</v22:MeterNumber>
            </v22:ClientDetail>
            <v22:TransactionDetail>
                <v22:CustomerTransactionId>FTC</v22:CustomerTransactionId>
            </v22:TransactionDetail>
            <v22:Version>
                <v22:ServiceId>disp</v22:ServiceId>
                <v22:Major>22</v22:Major>
                <v22:Intermediate>0</v22:Intermediate>
                <v22:Minor>0</v22:Minor>
            </v22:Version>
            <v22:CarrierCode>FDXE</v22:CarrierCode>
            <v22:PickupConfirmationNumber>0074698052</v22:PickupConfirmationNumber>
        </v22:CancelPickupRequest>
    </tns:Body>
</tns:Envelope>
"""

PickupCancelResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <CancelPickupReply xmlns="http://fedex.com/ws/pickup/v22">
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
                <Severity>SUCCESS</Severity>
                <Source>disp</Source>
                <Code>0000</Code>
                <Message>Success</Message>
                <LocalizedMessage>Success</LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>v22 CancelPickup_ExpUS</CustomerTransactionId>
                <Localization>
                    <LanguageCode>EN</LanguageCode>
                    <LocaleCode>US</LocaleCode>
                </Localization>
            </TransactionDetail>
            <Version>
                <ServiceId>disp</ServiceId>
                <Major>22</Major>
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
        <PickupAvailabilityReply xmlns="http://fedex.com/ws/pickup/v22">
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
                <Major>22</Major>
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
            <CreatePickupReply xmlns="http://fedex.com/ws/pickup/v22">
                <HighestSeverity>SUCCESS</HighestSeverity>
                <Notifications>
                    <Severity>SUCCESS</Severity>
                    <Source>disp</Source>
                    <Code>0000</Code>
                    <Message>Success</Message>
                    <LocalizedMessage>Success</LocalizedMessage>
                </Notifications>
                <TransactionDetail>
                    <CustomerTransactionId>CreatePickupRequest_v22</CustomerTransactionId>
                    <Localization>
                        <LanguageCode>EN</LanguageCode>
                        <LocaleCode>ES</LocaleCode>
                    </Localization>
                </TransactionDetail>
                <Version>
                    <ServiceId>disp</ServiceId>
                    <Major>22</Major>
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
