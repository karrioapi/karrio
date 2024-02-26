import unittest
import logging
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import TrackingRequest
from karrio import Tracking
from .fixture import gateway


logger = logging.getLogger(__name__)


class TestFeDexTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackRequest = TrackingRequest(tracking_numbers=["794887075005"])

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackRequest)

        self.assertEqual(request.serialize(), TrackingRequestXML)

    @patch("karrio.mappers.fedex_ws.proxy.lib.request", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/track")

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = Tracking.fetch(self.TrackRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedTrackingResponse)

    def test_tracking_auth_error_parsing(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = TrackingAuthErrorXML
            parsed_response = Tracking.fetch(self.TrackRequest).from_(gateway).parse()

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedAuthError))

    def test_parse_error_tracking_response(self):
        with patch("karrio.mappers.fedex_ws.proxy.lib.request") as mock:
            mock.return_value = TrackingErrorResponseXML
            parsed_response = Tracking.fetch(self.TrackRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponseError)
            )


if __name__ == "__main__":
    unittest.main()


ParsedAuthError = [
    [],
    [
        {
            "carrier_name": "fedex_ws",
            "carrier_id": "carrier_id",
            "code": "1000",
            "message": "Authentication Failed",
        }
    ],
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "carrier_id",
            "carrier_name": "fedex_ws",
            "delivered": False,
            "estimated_delivery": "2016-11-17",
            "events": [
                {
                    "code": "AE",
                    "date": "2022-12-02",
                    "description": "Shipment arriving early",
                    "location": "LETHBRIDGE, AB, T1H5K9, CA",
                    "time": "14:24",
                },
                {
                    "code": "PU",
                    "date": "2022-12-02",
                    "description": "Picked up",
                    "location": "LETHBRIDGE, AB, T1H5K9, CA",
                    "time": "14:21",
                },
                {
                    "code": "OC",
                    "date": "2022-12-02",
                    "description": "Shipment information sent to FedEx",
                    "location": "CUSTOMER",
                    "time": "09:56",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794887075005",
                "package_weight": 60.0,
                "package_weight_unit": "LB",
                "shipment_destination_country": "US",
                "shipment_origin_country": "US",
                "shipment_service": "FedEx Priority Overnight",
            },
            "status": "in_transit",
            "tracking_number": "794887075005",
        }
    ],
    [],
]

ParsedTrackingResponseError = [
    [],
    [
        {
            "carrier_name": "fedex_ws",
            "carrier_id": "carrier_id",
            "code": "6035",
            "message": "Invalid tracking numbers.   Please check the following numbers "
            "and resubmit.",
        }
    ],
]

TrackingErrorResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header />
   <SOAP-ENV:Body>
      <TrackReply xmlns="http://fedex.com/ws/track/v14">
         <HighestSeverity>SUCCESS</HighestSeverity>
         <Notifications>
            <Severity>SUCCESS</Severity>
            <Source>trck</Source>
            <Code>0</Code>
            <Message>Request was successfully processed.</Message>
            <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
         </Notifications>
         <TransactionDetail>
            <CustomerTransactionId>Track By Number_v14</CustomerTransactionId>
            <Localization>
               <LanguageCode>en</LanguageCode>
            </Localization>
         </TransactionDetail>
         <Version>
            <ServiceId>trck</ServiceId>
            <Major>14</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
         <CompletedTrackDetails>
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
               <Severity>SUCCESS</Severity>
               <Source>trck</Source>
               <Code>0</Code>
               <Message>Request was successfully processed.</Message>
               <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
            </Notifications>
            <DuplicateWaybill>false</DuplicateWaybill>
            <MoreData>false</MoreData>
            <TrackDetailsCount>0</TrackDetailsCount>
            <TrackDetails>
               <Notification>
                  <Severity>ERROR</Severity>
                  <Source>trck</Source>
                  <Code>6035</Code>
                  <Message>Invalid tracking numbers.   Please check the following numbers and resubmit.</Message>
                  <LocalizedMessage>Invalid tracking numbers.   Please check the following numbers and resubmit.</LocalizedMessage>
               </Notification>
               <TrackingNumber>1Z12345E1305277940</TrackingNumber>
               <StatusDetail>
                  <Location>
                     <Residential>false</Residential>
                  </Location>
               </StatusDetail>
               <PackageSequenceNumber>0</PackageSequenceNumber>
               <PackageCount>0</PackageCount>
               <DeliveryAttempts>0</DeliveryAttempts>
               <TotalUniqueAddressCountInConsolidation>0</TotalUniqueAddressCountInConsolidation>
               <DeliveryOptionEligibilityDetails>
                  <Option>INDIRECT_SIGNATURE_RELEASE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REDIRECT_TO_HOLD_AT_LOCATION</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REROUTE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>RESCHEDULE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
            </TrackDetails>
         </CompletedTrackDetails>
      </TrackReply>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

TrackingAuthErrorXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <v14:TrackReply xmlns:v14="http://fedex.com/ws/track/v14">
            <v14:HighestSeverity xmlns:v14="http://fedex.com/ws/track/v14">ERROR</v14:HighestSeverity>
            <v14:Notifications xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:Severity xmlns:v14="http://fedex.com/ws/track/v14">ERROR</v14:Severity>
                <v14:Source xmlns:v14="http://fedex.com/ws/track/v14">prof</v14:Source>
                <v14:Code xmlns:v14="http://fedex.com/ws/track/v14">1000</v14:Code>
                <v14:Message xmlns:v14="http://fedex.com/ws/track/v14">Authentication Failed</v14:Message>
            </v14:Notifications>
            <v14:TransactionDetail xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:CustomerTransactionId xmlns:v14="http://fedex.com/ws/track/v14">Track By Number_v14</v14:CustomerTransactionId>
                <v14:Localization xmlns:v14="http://fedex.com/ws/track/v14">
                    <v14:LanguageCode xmlns:v14="http://fedex.com/ws/track/v14">EN</v14:LanguageCode>
                    <v14:LocaleCode xmlns:v14="http://fedex.com/ws/track/v14">US</v14:LocaleCode>
                </v14:Localization>
            </v14:TransactionDetail>
            <v14:Version xmlns:v14="http://fedex.com/ws/track/v14">
                <v14:ServiceId xmlns:v14="http://fedex.com/ws/track/v14">trck</v14:ServiceId>
                <v14:Major xmlns:v14="http://fedex.com/ws/track/v14">14</v14:Major>
                <v14:Intermediate xmlns:v14="http://fedex.com/ws/track/v14">0</v14:Intermediate>
                <v14:Minor xmlns:v14="http://fedex.com/ws/track/v14">0</v14:Minor>
            </v14:Version>
        </v14:TrackReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

TrackingRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v18="http://fedex.com/ws/track/v18">
    <tns:Body>
        <v18:TrackRequest>
            <v18:WebAuthenticationDetail>
                <v18:UserCredential>
                    <v18:Key>user_key</v18:Key>
                    <v18:Password>password</v18:Password>
                </v18:UserCredential>
            </v18:WebAuthenticationDetail>
            <v18:ClientDetail>
                <v18:AccountNumber>2349857</v18:AccountNumber>
                <v18:MeterNumber>1293587</v18:MeterNumber>
            </v18:ClientDetail>
            <v18:TransactionDetail>
                <v18:CustomerTransactionId>Track By Number_v18</v18:CustomerTransactionId>
                <v18:Localization>
                    <v18:LanguageCode>en</v18:LanguageCode>
                </v18:Localization>
            </v18:TransactionDetail>
            <v18:Version>
                <v18:ServiceId>trck</v18:ServiceId>
                <v18:Major>18</v18:Major>
                <v18:Intermediate>0</v18:Intermediate>
                <v18:Minor>0</v18:Minor>
            </v18:Version>
            <v18:SelectionDetails>
                <v18:CarrierCode>FDXE</v18:CarrierCode>
                <v18:PackageIdentifier>
                    <v18:Type>TRACKING_NUMBER_OR_DOORTAG</v18:Type>
                    <v18:Value>794887075005</v18:Value>
                </v18:PackageIdentifier>
            </v18:SelectionDetails>
            <v18:ProcessingOptions>INCLUDE_DETAILED_SCANS</v18:ProcessingOptions>
        </v18:TrackRequest>
    </tns:Body>
</tns:Envelope>
"""

TrackingResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <SOAP-ENV:Body>
      <TrackReply xmlns="http://fedex.com/ws/track/v14">
         <HighestSeverity>SUCCESS</HighestSeverity>
         <Notifications>
            <Severity>SUCCESS</Severity>
            <Source>trck</Source>
            <Code>0</Code>
            <Message>Request was successfully processed.</Message>
            <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
         </Notifications>
         <TransactionDetail>
            <CustomerTransactionId>Track By Number_v14</CustomerTransactionId>
            <Localization>
               <LanguageCode>EN</LanguageCode>
               <LocaleCode>US</LocaleCode>
            </Localization>
         </TransactionDetail>
         <Version>
            <ServiceId>trck</ServiceId>
            <Major>14</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
         <CompletedTrackDetails>
            <HighestSeverity>SUCCESS</HighestSeverity>
            <Notifications>
               <Severity>SUCCESS</Severity>
               <Source>trck</Source>
               <Code>0</Code>
               <Message>Request was successfully processed.</Message>
               <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
            </Notifications>
            <DuplicateWaybill>false</DuplicateWaybill>
            <MoreData>false</MoreData>
            <TrackDetailsCount>0</TrackDetailsCount>
            <TrackDetails>
               <Notification>
                  <Severity>SUCCESS</Severity>
                  <Source>trck</Source>
                  <Code>0</Code>
                  <Message>Request was successfully processed.</Message>
                  <LocalizedMessage>Request was successfully processed.</LocalizedMessage>
               </Notification>
               <TrackingNumber>794887075005</TrackingNumber>
               <TrackingNumberUniqueIdentifier>2457710000~794887075005~FX</TrackingNumberUniqueIdentifier>
               <StatusDetail>
                  <CreationTime>2016-11-17T00:00:00</CreationTime>
                  <Code>OC</Code>
                  <Description>Shipment information sent to FedEx</Description>
                  <Location>
                     <Residential>false</Residential>
                  </Location>
                  <AncillaryDetails>
                     <Reason>IN001</Reason>
                     <ReasonDescription>Please check back later for shipment status or subscribe for e-mail notifications</ReasonDescription>
                  </AncillaryDetails>
               </StatusDetail>
               <ServiceCommitMessage>Shipping label has been created. The status will be updated when shipment begins to travel.</ServiceCommitMessage>
               <DestinationServiceArea>OC</DestinationServiceArea>
               <CarrierCode>FDXE</CarrierCode>
               <OperatingCompanyOrCarrierDescription>FedEx Express</OperatingCompanyOrCarrierDescription>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>INVOICE</Type>
                     <Value>IO10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>PURCHASE_ORDER</Type>
                     <Value>PO10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <OtherIdentifiers>
                  <PackageIdentifier>
                     <Type>SHIPPER_REFERENCE</Type>
                     <Value>CUSTREF10570705</Value>
                  </PackageIdentifier>
               </OtherIdentifiers>
               <Service>
                  <Type>PRIORITY_OVERNIGHT</Type>
                  <Description>FedEx Priority Overnight</Description>
                  <ShortDescription>PO</ShortDescription>
               </Service>
               <PackageWeight>
                  <Units>LB</Units>
                  <Value>60.0</Value>
               </PackageWeight>
               <PackageDimensions>
                  <Length>12</Length>
                  <Width>12</Width>
                  <Height>12</Height>
                  <Units>IN</Units>
               </PackageDimensions>
               <ShipmentWeight>
                  <Units>LB</Units>
                  <Value>60.0</Value>
               </ShipmentWeight>
               <Packaging>Your Packaging</Packaging>
               <PackagingType>YOUR_PACKAGING</PackagingType>
               <PackageSequenceNumber>1</PackageSequenceNumber>
               <PackageCount>1</PackageCount>
               <SpecialHandlings>
                  <Type>DELIVER_WEEKDAY</Type>
                  <Description>Deliver Weekday</Description>
                  <PaymentType>OTHER</PaymentType>
               </SpecialHandlings>
               <Payments>
                  <Classification>TRANSPORTATION</Classification>
                  <Type>SHIPPER_ACCOUNT</Type>
                  <Description>Shipper</Description>
               </Payments>
               <ShipperAddress>
                  <City>COLORADO SPRINGS</City>
                  <StateOrProvinceCode>CO</StateOrProvinceCode>
                  <CountryCode>US</CountryCode>
                  <Residential>false</Residential>
               </ShipperAddress>
               <DatesOrTimes>
                  <Type>ANTICIPATED_TENDER</Type>
                  <DateOrTimestamp>2016-11-17T00:00:00</DateOrTimestamp>
               </DatesOrTimes>
               <DestinationAddress>
                  <City>DENVER</City>
                  <StateOrProvinceCode>CO</StateOrProvinceCode>
                  <CountryCode>US</CountryCode>
                  <Residential>false</Residential>
               </DestinationAddress>
               <DeliveryAttempts>0</DeliveryAttempts>
               <TotalUniqueAddressCountInConsolidation>0</TotalUniqueAddressCountInConsolidation>
               <NotificationEventsAvailable>ON_DELIVERY</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_EXCEPTION</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_ESTIMATED_DELIVERY</NotificationEventsAvailable>
               <NotificationEventsAvailable>ON_TENDER</NotificationEventsAvailable>
               <DeliveryOptionEligibilityDetails>
                  <Option>INDIRECT_SIGNATURE_RELEASE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REDIRECT_TO_HOLD_AT_LOCATION</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>REROUTE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <DeliveryOptionEligibilityDetails>
                  <Option>RESCHEDULE</Option>
                  <Eligibility>INELIGIBLE</Eligibility>
               </DeliveryOptionEligibilityDetails>
               <Events>
                  <Timestamp>2022-12-02T14:24:00-07:00</Timestamp>
                  <EventType>AE</EventType>
                  <EventDescription>Shipment arriving early</EventDescription>
                  <Address>
                        <City>LETHBRIDGE</City>
                        <StateOrProvinceCode>AB</StateOrProvinceCode>
                        <PostalCode>T1H5K9</PostalCode>
                        <CountryCode>CA</CountryCode>
                        <CountryName>Canada</CountryName>
                        <Residential>false</Residential>
                  </Address>
                  <ArrivalLocation>PICKUP_LOCATION</ArrivalLocation>
               </Events>
               <Events>
                  <Timestamp>2022-12-02T14:21:00-07:00</Timestamp>
                  <EventType>PU</EventType>
                  <EventDescription>Picked up</EventDescription>
                  <Address>
                        <City>LETHBRIDGE</City>
                        <StateOrProvinceCode>AB</StateOrProvinceCode>
                        <PostalCode>T1H5K9</PostalCode>
                        <CountryCode>CA</CountryCode>
                        <CountryName>Canada</CountryName>
                        <Residential>false</Residential>
                  </Address>
                  <ArrivalLocation>PICKUP_LOCATION</ArrivalLocation>
               </Events>
               <Events>
                  <Timestamp>2022-12-02T09:56:11-06:00</Timestamp>
                  <EventType>OC</EventType>
                  <EventDescription>Shipment information sent to FedEx</EventDescription>
                  <Address>
                        <Residential>false</Residential>
                  </Address>
                  <ArrivalLocation>CUSTOMER</ArrivalLocation>
               </Events>
            </TrackDetails>
         </CompletedTrackDetails>
      </TrackReply>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
