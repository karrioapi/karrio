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


class TestPurolatorPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        pipeline = request.serialize()
        validate_request = pipeline["validate"]()
        schedule_request = pipeline["schedule"](PickupValidationResponseXML)

        self.assertEqual(validate_request.data.serialize(), PickupValidationRequestXML)
        self.assertEqual(schedule_request.data.serialize(), PickupRequestXML)

    def test_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        pipeline = request.serialize()
        validate_request = pipeline["validate"]()
        modify_request = pipeline["modify"](PickupValidationResponseXML)

        self.assertEqual(
            validate_request.data.serialize(), PickupUpdateValidationRequestXML
        )
        self.assertEqual(modify_request.data.serialize(), PickupUpdateRequestXML)

    def test_create_pickup(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [PickupValidationResponseXML, PickupResponseXML]
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            validate_call, schedule_call = mocks.call_args_list
            self.assertEqual(
                validate_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V1/PickUp/PickUpService.asmx",
            )
            self.assertEqual(
                validate_call[1]["headers"]["soapaction"],
                "http://purolator.com/pws/service/v1/ValidatePickUp",
            )
            self.assertEqual(
                schedule_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V1/PickUp/PickUpService.asmx",
            )
            self.assertEqual(
                schedule_call[1]["headers"]["soapaction"],
                "http://purolator.com/pws/service/v1/SchedulePickUp",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [
                PickupValidationResponseXML,
                PickupResponseXML,
                PickupCancelResponseXML,
            ]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            validate_call, modify_call = mocks.call_args_list
            self.assertEqual(
                validate_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V1/PickUp/PickUpService.asmx",
            )
            self.assertEqual(
                validate_call[1]["headers"]["soapaction"],
                "http://purolator.com/pws/service/v1/ValidatePickUp",
            )
            self.assertEqual(
                modify_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V1/PickUp/PickUpService.asmx",
            )
            self.assertEqual(
                modify_call[1]["headers"]["soapaction"],
                "http://purolator.com/pws/service/v1/ModifyPickUp",
            )

    def test_parse_pickup_reply(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [PickupValidationResponseXML, PickupResponseXML]
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_cancel_reply(self):
        with patch("karrio.mappers.purolator.proxy.http") as mock:
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
        "phone_number": "15145555555",
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
        "phone_number": "15145555555",
    },
    "parcels": [{"weight": 24, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"LoadingDockAvailable": False, "TrailerAccessible": False},
}

pickup_cancel_data = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "purolator",
        "carrier_name": "purolator",
        "confirmation_number": "01365863",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "purolator",
        "carrier_name": "purolator",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupValidationRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.2</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:ValidatePickUpRequest>
            <v1:BillingAccountNumber>12398576956</v1:BillingAccountNumber>
            <v1:PickupInstruction>
                <v1:Date>2015-01-28</v1:Date>
                <v1:AnyTimeAfter>1500</v1:AnyTimeAfter>
                <v1:UntilTime>1700</v1:UntilTime>
                <v1:TotalWeight>
                    <v1:WeightUnit>lb</v1:WeightUnit>
                </v1:TotalWeight>
                <v1:TotalPieces>1</v1:TotalPieces>
                <v1:AdditionalInstructions>Door at Back</v1:AdditionalInstructions>
            </v1:PickupInstruction>
            <v1:Address>
                <v1:Name>John Doe</v1:Name>
                <v1:Company>Jim Duggan</v1:Company>
                <v1:StreetNumber>2271</v1:StreetNumber>
                <v1:StreetName>2271 Herring Cove</v1:StreetName>
                <v1:City>Halifax</v1:City>
                <v1:Province>NS</v1:Province>
                <v1:Country>CA</v1:Country>
                <v1:PostalCode>B3L2C2</v1:PostalCode>
                <v1:PhoneNumber>
                    <v1:CountryCode>1</v1:CountryCode>
                    <v1:AreaCode>514</v1:AreaCode>
                    <v1:Phone>5555555</v1:Phone>
                </v1:PhoneNumber>
            </v1:Address>
            <v1:NotificationEmails>
                <v1:NotificationEmail>john.doe@canadapost.ca</v1:NotificationEmail>
            </v1:NotificationEmails>
        </v1:ValidatePickUpRequest>
    </soap:Body>
</soap:Envelope>
"""

PickupRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.2</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:SchedulePickUpRequest>
            <v1:BillingAccountNumber>12398576956</v1:BillingAccountNumber>
            <v1:PickupInstruction>
                <v1:Date>2015-01-28</v1:Date>
                <v1:AnyTimeAfter>1500</v1:AnyTimeAfter>
                <v1:UntilTime>1700</v1:UntilTime>
                <v1:TotalWeight>
                    <v1:WeightUnit>lb</v1:WeightUnit>
                </v1:TotalWeight>
                <v1:TotalPieces>1</v1:TotalPieces>
                <v1:AdditionalInstructions>Door at Back</v1:AdditionalInstructions>
            </v1:PickupInstruction>
            <v1:Address>
                <v1:Name>John Doe</v1:Name>
                <v1:Company>Jim Duggan</v1:Company>
                <v1:StreetNumber>2271</v1:StreetNumber>
                <v1:StreetName>2271 Herring Cove</v1:StreetName>
                <v1:City>Halifax</v1:City>
                <v1:Province>NS</v1:Province>
                <v1:Country>CA</v1:Country>
                <v1:PostalCode>B3L2C2</v1:PostalCode>
                <v1:PhoneNumber>
                    <v1:CountryCode>1</v1:CountryCode>
                    <v1:AreaCode>514</v1:AreaCode>
                    <v1:Phone>5555555</v1:Phone>
                </v1:PhoneNumber>
            </v1:Address>
            <v1:NotificationEmails>
                <v1:NotificationEmail>john.doe@canadapost.ca</v1:NotificationEmail>
            </v1:NotificationEmails>
        </v1:SchedulePickUpRequest>
    </soap:Body>
</soap:Envelope>
"""

PickupUpdateValidationRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.2</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:ValidatePickUpRequest>
            <v1:BillingAccountNumber>12398576956</v1:BillingAccountNumber>
            <v1:PickupInstruction>
                <v1:Date>2015-01-28</v1:Date>
                <v1:AnyTimeAfter>1500</v1:AnyTimeAfter>
                <v1:UntilTime>1700</v1:UntilTime>
                <v1:TotalWeight>
                    <v1:Value>52.92</v1:Value>
                    <v1:WeightUnit>lb</v1:WeightUnit>
                </v1:TotalWeight>
                <v1:TotalPieces>1</v1:TotalPieces>
                <v1:AdditionalInstructions>Door at Back</v1:AdditionalInstructions>
                <v1:TrailerAccessible>false</v1:TrailerAccessible>
                <v1:LoadingDockAvailable>false</v1:LoadingDockAvailable>
            </v1:PickupInstruction>
            <v1:Address>
                <v1:Name>Jane Doe</v1:Name>
                <v1:StreetNumber></v1:StreetNumber>
                <v1:PhoneNumber>
                    <v1:CountryCode>1</v1:CountryCode>
                    <v1:AreaCode>514</v1:AreaCode>
                    <v1:Phone>5555555</v1:Phone>
                </v1:PhoneNumber>
            </v1:Address>
            <v1:NotificationEmails>
                <v1:NotificationEmail>john.doe@canadapost.ca</v1:NotificationEmail>
            </v1:NotificationEmails>
        </v1:ValidatePickUpRequest>
    </soap:Body>
</soap:Envelope>
"""

PickupUpdateRequestXML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.2</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:ModifyPickUpRequest>
            <v1:BillingAccountNumber>12398576956</v1:BillingAccountNumber>
            <v1:ConfirmationNumber>0074698052</v1:ConfirmationNumber>
            <v1:ModifyPickupInstruction>
                <v1:UntilTime>1700</v1:UntilTime>
                <v1:TrailerAccessible>false</v1:TrailerAccessible>
                <v1:LoadingDockAvailable>false</v1:LoadingDockAvailable>
            </v1:ModifyPickupInstruction>
        </v1:ModifyPickUpRequest>
    </soap:Body>
</soap:Envelope>
"""

PickupCancelRequestXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1">
   <SOAP-ENV:Header>
      <ns1:RequestContext>
         <ns1:Version>1.0</ns1:Version>
         <ns1:Language>en</ns1:Language>
         <ns1:GroupID>xxx</ns1:GroupID>
         <ns1:RequestReference>Rating Example</ns1:RequestReference>
      </ns1:RequestContext>
   </SOAP-ENV:Header>
   <SOAP-ENV:Body>
      <ns1:VoidPickUpRequest>
         <ns1:PickUpConfirmationNumber>12312312</ns1:PickUpConfirmationNumber>
      </ns1:VoidPickUpRequest>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

PickupCancelResponseXML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Header>
      <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <h:ResponseReference>Rating Example</h:ResponseReference>
      </h:ResponseContext>
   </s:Header>
   <s:Body>
      <VoidPickUpResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <ResponseInformation i:nil="true" />
         <PickUpVoided>true</PickUpVoided>
      </VoidPickUpResponse>
   </s:Body>
</s:Envelope>
"""

PickupValidationResponseXML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Header>
      <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <h:ResponseReference>Rating Example</h:ResponseReference>
      </h:ResponseContext>
   </s:Header>
   <s:Body>
      <ValidatePickUpResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <ResponseInformation i:nil="true" />
         <IsBulkdRequired>false</IsBulkdRequired>
         <CutOffTime>17:30</CutOffTime>
         <CutOffWindow>60</CutOffWindow>
         <BulkMaxWeight>0</BulkMaxWeight>
         <BulkMaxPackages>0</BulkMaxPackages>
      </ValidatePickUpResponse>
   </s:Body>
</s:Envelope>
"""

PickupResponseXML = f"""<wrapper>
    {PickupValidationResponseXML}
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
       <s:Header>
          <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
             <h:ResponseReference>Rating Example</h:ResponseReference>
          </h:ResponseContext>
       </s:Header>
       <s:Body>
          <SchedulePickUpResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
             <ResponseInformation i:nil="true" />
             <PickUpConfirmationNumber>01365863</PickUpConfirmationNumber>
          </SchedulePickUpResponse>
       </s:Body>
    </s:Envelope>
</wrapper>
"""
