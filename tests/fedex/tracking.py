import unittest
from unittest.mock import patch
from pyfedex.track_service_v14 import TrackRequest
from gds_helpers import to_xml, to_dict, export
from purplship.core.models import TrackingRequest
from tests.fedex.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestFeDexTracking(unittest.TestCase):
    def setUp(self):
        req_xml = get_node_from_xml(TrackingRequestXML, "TrackRequest")
        self.TrackRequest = TrackRequest()
        self.TrackRequest.build(req_xml)

    def test_create_tracking_request(self):
        payload = TrackingRequest(tracking_numbers=["794887075005"])

        TrackRequest_ = proxy.mapper.create_tracking_request(payload)

        self.assertEqual(export(TrackRequest_), export(self.TrackRequest))

    @patch("purplship.carriers.fedex.fedex_proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        proxy.get_tracking(self.TrackRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(TrackingRequestXML))

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingResponseXML)
        )

        self.assertEqual(to_dict(parsed_response), to_dict(ParsedTrackingResponse))

    def test_tracking_auth_error_parsing(self):
        parsed_response = proxy.mapper.parse_error_response(
            to_xml(TrackingAuthErrorXML)
        )

        self.assertEqual(to_dict(parsed_response), to_dict(ParsedAuthError))

    def test_parse_error_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingErrorResponseXML)
        )

        self.assertEqual(to_dict(parsed_response), to_dict(ParsedTrackingResponseError))


if __name__ == "__main__":
    unittest.main()


ParsedAuthError = [
    {"carrier": "carrier_name", "code": "1000", "message": "Authentication Failed"}
]

ParsedTrackingResponse = [
    [
        {
            "carrier": "carrier_name",
            "events": [
                {
                    "code": "OC",
                    "date": "2016-11-17 03:13:01-06:00",
                    "description": "Shipment information sent to FedEx",
                    "location": "CUSTOMER",
                    "signatory": None,
                    "time": None,
                }
            ],
            "shipment_date": "2016-11-17 00:00:00",
            "tracking_number": "794887075005",
        }
    ],
    [],
]

ParsedTrackingResponseError = [
    [],
    [
        {
            "carrier": "carrier_name",
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

TrackingRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/track/v14">
    <tns:Body>
        <ns:TrackRequest>
            <ns:WebAuthenticationDetail>
                <ns:UserCredential>
                    <ns:Key>user_key</ns:Key>
                    <ns:Password>password</ns:Password>
                </ns:UserCredential>
            </ns:WebAuthenticationDetail>
            <ns:ClientDetail>
                <ns:AccountNumber>2349857</ns:AccountNumber>
                <ns:MeterNumber>1293587</ns:MeterNumber>
            </ns:ClientDetail>
            <ns:TransactionDetail>
                <ns:CustomerTransactionId>Track By Number_v14</ns:CustomerTransactionId>
                <ns:Localization>
                    <ns:LanguageCode>en</ns:LanguageCode>
                </ns:Localization>
            </ns:TransactionDetail>
            <ns:Version>
                <ns:ServiceId>trck</ns:ServiceId>
                <ns:Major>14</ns:Major>
                <ns:Intermediate>0</ns:Intermediate>
                <ns:Minor>0</ns:Minor>
            </ns:Version>
            <ns:SelectionDetails>
                <ns:CarrierCode>FDXE</ns:CarrierCode>
                <ns:PackageIdentifier>
                    <ns:Type>TRACKING_NUMBER_OR_DOORTAG</ns:Type>
                    <ns:Value>794887075005</ns:Value>
                </ns:PackageIdentifier>
            </ns:SelectionDetails>
        </ns:TrackRequest>
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
                  <Timestamp>2016-11-17T03:13:01-06:00</Timestamp>
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
