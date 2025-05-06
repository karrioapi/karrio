import re
import unittest
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio.sdk import Shipment
from .fixture import gateway


class TestPurolatorShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**SHIPMENT_REQUEST_PAYLOAD)
        self.ShipmentCancelRequest = ShipmentCancelRequest(
            **SHIPMENT_CANCEL_REQUEST_PAYLOAD
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        pipeline = request.serialize()
        create_request = pipeline["create"]()
        document_request = pipeline["document"](SHIPMENT_RESPONSE_XML)

        self.assertEqual(create_request.data.serialize(), SHIPMENT_REQUEST_XML)
        self.assertEqual(
            document_request.data.serialize(), SHIPMENT_DOCUMENT_REQUEST_XML
        )

    def test_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), SHIPMENT_CANCEL_REQUEST_XML)

    def test_request_shipment(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [
                SHIPMENT_RESPONSE_XML,
                SHIPMENT_DOCUMENT_RESPONSE_XML,
            ]
            Shipment.create(self.ShipmentRequest).from_(gateway)

            create_call, document_call = mocks.call_args_list

            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
            )
            self.assertEqual(
                document_call[1]["url"],
                f"{gateway.settings.server_url}/EWS/V1/ShippingDocuments/ShippingDocumentsService.asmx",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.purolator.proxy.http") as mock:
            mock.return_value = ""
            Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            url = mock.call_args[1]["url"]

            self.assertEqual(
                url,
                f"{gateway.settings.server_url}/EWS/V2/Shipping/ShippingService.asmx",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.side_effect = [
                SHIPMENT_RESPONSE_XML,
                SHIPMENT_DOCUMENT_RESPONSE_XML,
            ]
            parsed_response = (
                Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), PARSED_SHIPMENT_RESPONSE)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.purolator.proxy.http") as mocks:
            mocks.return_value = SHIPMENT_CANCEL_RESPONSE_XML
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(PARSED_CANCEL_SHIPMENT_RESPONSE)
            )


if __name__ == "__main__":
    unittest.main()

SHIPMENT_CANCEL_REQUEST_PAYLOAD = {"shipment_identifier": "329014521622"}

SHIPMENT_REQUEST_PAYLOAD = {
    "shipper": {
        "person_name": "Aaron Summer",
        "state_code": "ON",
        "city": "Mississauga",
        "country_code": "CA",
        "postal_code": "L4W5M8",
        "address_line1": "Main Street",
        "phone_number": "1 514 5555555",
    },
    "recipient": {
        "person_name": "Aaron Summer",
        "state_code": "BC",
        "city": "Burnaby",
        "country_code": "CA",
        "postal_code": "V5C5A9",
        "address_line1": "Douglas Road",
        "phone_number": "1 514 2982181",
    },
    "parcels": [
        {
            "weight": 10,
            "weight_unit": "LB",
        }
    ],
    "reference": "Reference For Shipment",
    "service": "purolator_express",
    "label_type": "PDF",
    "options": {"shipment_date": "2021-02-04"},
}

PARSED_SHIPMENT_RESPONSE = [
    {
        "carrier_name": "purolator",
        "carrier_id": "purolator",
        "tracking_number": "329014521622",
        "shipment_identifier": "329014521622",
        "docs": {"label": ANY},
        "meta": {
            "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=329014521622"
        },
    },
    [],
]

PARSED_CANCEL_SHIPMENT_RESPONSE = [
    {
        "carrier_id": "purolator",
        "carrier_name": "purolator",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


SHIPMENT_REQUEST_XML = f"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2">
    <soap:Header>
        <v2:RequestContext>
            <v2:Version>2.1</v2:Version>
            <v2:Language>en</v2:Language>
            <v2:GroupID></v2:GroupID>
            <v2:RequestReference></v2:RequestReference>
            <v2:UserToken>token</v2:UserToken>
        </v2:RequestContext>
    </soap:Header>
    <soap:Body>
        <v2:CreateShipmentRequest>
            <v2:Shipment>
                <v2:SenderInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetNumber></v2:StreetNumber>
                        <v2:StreetName>Main Street</v2:StreetName>
                        <v2:City>Mississauga</v2:City>
                        <v2:Province>ON</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>L4W5M8</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>5555555</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:SenderInformation>
                <v2:ReceiverInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetNumber></v2:StreetNumber>
                        <v2:StreetName>Douglas Road</v2:StreetName>
                        <v2:City>Burnaby</v2:City>
                        <v2:Province>BC</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>V5C5A9</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>2982181</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:ReceiverInformation>
                <v2:ShipmentDate>2021-02-04</v2:ShipmentDate>
                <v2:PackageInformation>
                    <v2:ServiceID>PurolatorExpress</v2:ServiceID>
                    <v2:TotalWeight>
                        <v2:Value>10</v2:Value>
                        <v2:WeightUnit>lb</v2:WeightUnit>
                    </v2:TotalWeight>
                    <v2:TotalPieces>1</v2:TotalPieces>
                    <v2:PiecesInformation>
                        <v2:Piece>
                            <v2:Weight>
                                <v2:Value>10.</v2:Value>
                                <v2:WeightUnit>lb</v2:WeightUnit>
                            </v2:Weight>
                        </v2:Piece>
                    </v2:PiecesInformation>
                </v2:PackageInformation>
                <v2:PickupInformation>
                    <v2:PickupType>DropOff</v2:PickupType>
                </v2:PickupInformation>
                <v2:TrackingReferenceInformation>
                    <v2:Reference1>Reference For Shipment</v2:Reference1>
                </v2:TrackingReferenceInformation>
            </v2:Shipment>
            <v2:PrinterType>Regular</v2:PrinterType>
        </v2:CreateShipmentRequest>
    </soap:Body>
</soap:Envelope>
"""

SHIPMENT_DOCUMENT_REQUEST_XML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.3</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:GetDocumentsRequest>
            <v1:OutputType>PDF</v1:OutputType>
            <v1:Synchronous>true</v1:Synchronous>
            <v1:DocumentCriterium>
                <v1:DocumentCriteria>
                    <v1:PIN>
                        <v1:Value>329014521622</v1:Value>
                    </v1:PIN>
                    <v1:DocumentTypes>
                        <v1:DocumentType>DomesticBillOfLading</v1:DocumentType>
                    </v1:DocumentTypes>
                </v1:DocumentCriteria>
            </v1:DocumentCriterium>
        </v1:GetDocumentsRequest>
    </soap:Body>
</soap:Envelope>
"""

SHIPMENT_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <CreateShipmentResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <ShipmentPIN>
                <Value>329014521622</Value>
            </ShipmentPIN>
            <PiecePINs>
                <PIN>
                    <Value>329014521622</Value>
                </PIN>
            </PiecePINs>
            <ReturnShipmentPINs/>
            <ExpressChequePIN>
                <Value/>
            </ExpressChequePIN>
        </CreateShipmentResponse>
    </s:Body>
</s:Envelope>
"""

SHIPMENT_DOCUMENT_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Header>
      <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <h:ResponseReference>Example Code</h:ResponseReference>
      </h:ResponseContext>
   </s:Header>
   <s:Body>
      <GetDocumentsResponse xmlns="http://purolator.com/pws/datatypes/v1" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
         <ResponseInformation>
            <Errors />
            <InformationalMessages i:nil="true" />
         </ResponseInformation>
         <Documents>
            <Document>
               <PIN>
                  <Value>329015010179</Value>
               </PIN>
               <DocumentDetails>
                  <DocumentDetail>
                     <DocumentType>DomesticBillOfLadingThermal</DocumentType>
                     <Description>Domestic Bill of Lading - Thermal</Description>
                     <DocumentStatus>Completed</DocumentStatus>
                     <Data>JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS40Ci9QYWdlcyAyIDAgUgo+PgplbmRvYmoKMyAwIG9iago8PAovUHJvZHVjZXIgKGlUZXh0IDIuMS43IGJ5IDFUM1hUKQovTW9kRGF0ZSAoRDoyMDE4MDIyNzA4MDg0OSswMScwMCcpCi9DcmVhdGlvbkRhdGUgKEQ6MjAxODAyMjcwODA4NDkrMDEnMDAnKQo+PgplbmRvYmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzQgMCBSIDUgMCBSXQovQ291bnQgMgo+PgplbmRvYmoKNCAwIG9iago8PAovUGFyZW50IDIgMCBSCi9Db250ZW50cyA2IDAgUgovVHlwZSAvUGFnZQovUmVzb3VyY2VzIDcgMCBSCi9NZWRpYUJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovQ3JvcEJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovUm90YXRlIDAKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL1BhcmVudCAyIDAgUgovQ29udGVudHMgOCAwIFIKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA5IDAgUgovTWVkaWFCb3ggWzAuMCAwLjAgODQxLjg5IDU5NS4yOF0KL0Nyb3BCb3ggWzAuMCAwLjAgODQxLjg5IDU5NS4yOF0KL1JvdGF0ZSAwCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9MZW5ndGggNTEKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtDQp4nCvkcgrhMlAwtTTVM7JQCEnhcg3hCuQqVDBUMABCCJmcq6AfkWao4JKvEMgFAP2hClYNCmVuZHN0cmVhbQplbmRvYmoKNyAwIG9iago8PAovWE9iamVjdCA8PAovWGYxIDEwIDAgUgo+PgovUHJvY1NldCBbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KPj4KZW5kb2JqCjggMCBvYmoKPDwKL0xlbmd0aCA1MQovRmlsdGVyIC9GbGF0ZURlY29kZQo+PgpzdHJlYW0NCnicK+RyCuEyUDC1NNUzslAISeFyDeEK5CpUMFQwAEIImZyroB+RZqjgkq8Q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74WUwoWAXyykecYrIv7HHFQlq+3XXSON0ttX+3a12ft0+DUQ/lcEdnj18OVLyduuF5t2vZmvbkW3Wux/brP7cPjNvjznKO9VfhP80oizRTtdt+K6E6vuBaODPJTi8EXSxvw+vxHru/n904cP5ROOavvwUfQ/PGTml13lzfa7J+Sd8t3z/XzWrvCr2YI+03Y34p5ewsR8Rf3ja92zH4/x0laWxcSQ8oPO9ycSrvXGOxPhgqKTN+E5D9xY5EByhmRlyg6wMbjsuANxP71twQiGq8QBp/0If/4PWx5djw0KZW5kc3RyZWFtCmVuZG9iagoxMiAwIG9iago8PAovTGVuZ3RoIDcxNTUKL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9Db2xvclNwYWNlIFsvSW5kZXhlZCAvRGV2aWNlUkdCIDI1NSA8RDJFNTlDQkNENzZCRTlGMkNFRkFGQ0YzQUJDRDQ1QzdERTg0RERFQkI1RjRGOUU3QjZENDVFQjBEMTUyRUVGNURCRDhFOEE5Q0RFMTkwRTNFRkMyQzFEQjc3QkJENzZBQUFDRDQ1RThGMUNERjlGQkYyQzZERDgzQjVEMzVFRjNGOEU2RUVGNUQ5RDJFNDlDRERFQkI0QzFEQTc2RDdFN0E4QjBEMDUxQ0NFMThGRTJFRUMxQTVDQTM5RkZGRkZGMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw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q3/orhbLw28n393sXfKHKtar1X7xYr9ajbjIbrW6fX0Ri9VK+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQ2v8B4fNgUg0KZW5kc3RyZWFtCmVuZG9iagoxMyAwIG9iago8PAovRjEgMTYgMCBSCi9GMiAxNyAwIFIKPj4KZW5kb2JqCjE0IDAgb2JqCjw8Ci9MZW5ndGggNzE1NQovVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL0NvbG9yU3BhY2UgWy9JbmRleGVkIC9EZXZpY2VSR0IgMjU1IDxEMkU1OUNCQ0Q3NkJFOUYyQ0VGQUZDRjNBQkNENDVDN0RFODREREVCQjVGNEY5RTdCNkQ0NUVCMEQxNTJFRUY1REJEOEU4QTlDREUxOTBFM0VGQzJDMURCNzdCQkQ3NkFBQUNENDVFOEYxQ0RGOUZCRjJDNkREODNCNUQzNUVGM0Y4RTZFRUY1RDlEMkU0OUNEREVCQjRDMURBNzZEN0U3QThCMEQwNTFDQ0UxOEZFMkVFQzFBNUNBMzlGRkZGRkYwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA+XQovV2lkdGggMTAyNAovQml0c1BlckNvbXBvbmVudCA4Ci9IZWlnaHQgNzY4Ci9GaWx0ZXIgL0ZsYXRlRGVjb2RlCj4+CnN0cmVhbQ0KeJzt3VlD48a2gFFPYIyBJJ3xDKH//7+8cAi3sZGNLe0qqbbWesyD4vbmkzWU5e/fAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACASVst9vdjv4Zito+Lx/XYLwKm6nH3/GKZcw+wfnj9xz0/jP06YJpun99sUu4Alv/8657GfiEwRevNP4U8L8d+KQW879yen2/HfikwQT8KSZjIj53b893YrwUmaPGj/93YryXch3/c89ivBSboYyL7sV9MsO1G/3DO/kMim2T3yW4+/Nsc/8Nn2w+NPC/GfjWhEv/TIMjDx0q2Y7+aSMsP/7BdskMbiLH+eJJ8M/arCbT6uGPLd28DQny8AvicaBHQwcf/2C8Gpmr3IZQ8i4BuP+7WVmO/GpiqnKXk3KtBuLuE98kWKXdqEC/hlbK0VzUhXL47ZQcf/6nuakK0+4+1ZFgpY+kPXO7jStkMq4Cz/XugpINvyrT/sJx0xzNQVK7zZUt/4BqprpcnvJ8BRX38HnDr98s/Lv3Jsp4BisqzXi7nekYo6aCax7FfzQDrPHsyqCbLRbNclzKhjiRXzVJdyYRqPh4AtLto5uPzjDY+/uFCKRbNpvhHwAgyrJp9SvBvgDEkOHU+uIiR7fcMoKj2L51nuYkB9R0cALR46/wxxz0MGEXrS+cs/YEB2g6o9d0XjKvpA+iD05ensV8NtKflC2jtX76EcTV8A23b/u1LGFn8IqD1arVavLhZHnt6/c+Pq1XMZ3WG5UswrrAFtNvV7eJh+fF84py75c1ivxry84NW/sJww38Q/CX85d1zP7vlw37V68M7x9eXYFxDVgFvHxfL3XHSPWyWD7dXHgsk+foyjKzfD4KvX9LfPIdaPjxefvzR8o0LmI7rH6C1vb3pe7z/ld3T/qJdkKU/EOOqlta3NxFH/OdsnvZfHge0vXARJuTiHwRfPZT63D+2u3k8d00v0+PLYVwXXUt7+eAPPt//yunDgARPLoDJ+PIHwde3T8d1VnHXvQuw8hfinP8BzbHif9OxCzhY+tP+z5fCyM6spR01/jd3t+tLXy1wtVOfqPe1z/lPefrwE0V+7htidZ1Rr/el7/RdY7d4Pw+w9Adifb6ifn9zXODo3g4CrPyFaEd31G9r3ei/zm6xvny1AnCpj8f6u4mc9XfYHHzD2NIfCHF7qrgJs/IXglz66I4JGfL8EOCD1de9TYyVvxCmtQMAP/cNYbat9b9z9Q9ibKd3u/9rS3sAGG798HVsk/TkHAAGWkz3fv+XHnwBCAZYTWmZ//U2bf1sEUxJc5f9PrtzGQD6WC++zqsBN04C4GqNH/r/4CQArrQe/9E+cZYWA8MVHhu+6t/Fo4DgUqk+/N/cOQSAi2T78H/jEAC+lvDD/41DAPjKKuWH//+4EQDntbrY/zJP1gLASdtpPtozzsZyQDgh54W/Qy4DQqfcx/7vls4B4JN19mP/dzv3AeDI/QyO/d/5ZSA40OIj/vvzdGD4oMUn/A3hIgC8W7f/nI9rWQwIb9Lf9e+ysQOA7/O68veRq4Awi0U/3XwdgNmb14X/Q24DMHNzzt8OgJmb232/Y+4DMmNzz//5+c4OgLmSvx0AsyX/V3YAzJL839gBMEPyf2cHwOzI/wc7AGZG/h/ZATAr8j90N/ZAoJ792L1NjpWAzMa8F/12swNgJh7Hbm2SPBicWZjr9/2/4nkAzMBW/ic8jj0aKG02j/m/nkeCkd78HvV5uZ1lAOTmxv85lgGQmjt/57kLSGL3Y/c1eZ4JSlprl/6/5BogWQ279vfbTy9+C8qsjP+8vsSfBm1i4xogOT0MyOJff3/7Zyt///rzoMCK+emv3/95iX/8d8BLXI41HihpwLLfX3//uKFvf/bfUjE//XLwj/13/z2AhcAk1H/d38+/HG/rj6mdBvz87+OX+O1fvTe2qjMQqKj3yf9v3z5vbEBdJfz8R8c/+Ne+W3MJgHQWfWvoyv/FsKtssTrzH7ADcAmAZHrf+f/59+4NfpvQKcCn85N/9D5IsQqAVNa7vin8fWqTf/TdYrj/nnqJ3/peBPRNIFLpfevvp9Pb7H14Hezn7hOUV3/13aYvApDIqndcpw6tX/zee6Ox/jzzD/9P3426CUga/Y/+/3NusxO5B3D64//79/4rFZwBkEX/hX8nT61f9T66DnXmDGXIMYozAJLof/R/7vB/KicA5w7/v3+3DJC56330f/7Y+vv3/tsNdHYXNWCZwmYbOQMYSe+VPy/Ob3kSa4DO9//f/hu2CogEtkPiOr/pBvof8lUlzwOmfYO+9H9+08n79zhQmjfsx37Ob3sSS4DP9z/oHqVLgLRuwMW/F91frHk3aNNR/jr7EocdorgESNuGXPz7Kq5pfAPg7BKFgbuop9BZQGVDn/j567mN/3vYtoOcXaL498CNexQILRv6cx9nvlszYHF9rHMXAIZ+R8kqQBo26N7f/5xZXffL4I3HOHOMMnyFoh8Fpl1Pg//+zxwATOLq/6vTBwDDv6K8KzEWqGHAwv//969TG5/OQ4B/O/USI45QHADQqpDf+j1xC2AaF//fnDgD+D3ihwo8DJRGRXz8P5/YAfwxqR8B6dwBBD2h0CIg2hTy8f/cuQP4e1L5d+4Aon6jwAEATQr6+H/xr6OLgN8GfKuukN+OVyoO+AGgIw4AaFHUx/+Ln//88BTwb3FpRTr4jbK/AtcmbKpPDgbr/cT/bj/9+ctLYL//8u+JPPWvw29//vJyFPDtl7+Cf6HULQDaM3TpH++sAaA5w5f+8c4BAK3p/8xfjnkSGI0Z+sU/PvI1QNqyHzuZVG7GHidcZdhjfzjiQUC0JG7tD6+sAaIlw7/4y0duAdIQN/+i+S0A2uHqXzRPAqUdrv6FcwWQVgQv/efFfuyhwoUs/Y/nScC0wtq/Au7HnipcZNhP/tHtYeyxwkUc/pdgCQBtcPhfhBMAWuDwvwwnALTA4X8ZTgBogcP/QpwAMH0O/0uxBIjp8+CvUiwBYvqs/S/GLwExdb76W47nADN1vvpbjscAMnWe/FOOXwJj6tz9K8gdQKbNV/9LcgeQaXP6X5KngDFtTv9LcgGAaXP6X5SnADJl7v6XZQUAU3Y7diDJ+Q4wU2bxf1m+AsCULccOJLuxBwxnjJ1HequxJwwnWf1TmhVATJfLf6W5AMh0LcbOI73l2COGk1z+K80KQKbLs3+K8wwgJmvsOGbADQCmyuX/8twAYKpWY8cxA4uxhwwnuPxfnhsATJXV/+Xpn6ly+6+CsYcMJ+i/grGHDCeMncYseAYwEzV2GrNgAQDT5OFfNTyOPWbo5PZ/DRYAME36r0H/TJNv/9fgCQBMk+V/NVgAxDTpvwb9M036r0H/TNPN2GnMgv6ZJst/a/AEMKZJ/1WMPWbopP8qxh4zdNJ/FWOPGTrpv4qxxwyd9F/F2GOGTg9LKhh7zAAAAAAAADRjtX9Yvt/Fv1s+LFZ+bbpx97eL5XLzNtHd8max2o79ipim+0XX+p27B8+bbtV2/7T5PNHdjScIc2S72J1cb7Z58JMT7Vnv705P9MZOnR9WT18sOV3ejv0Sucr2q2ex7EyUN6tL1u3vHDS248v6/3cQsB/7ZTIB268++98tnQW0YX3pcxh3zgJmb99xhegUvzzRgtXpKzmfPLm/M2vr676ye3f+EGC1oILzE324aqIbp3Uztrriw//tz+XsVSPP/67i3Ai2py/6n+Cgbrb6/F7XuV+f0n8VZyZwf+0O/dk5wGz1y/UmeoNc6fQA+v0A450dwBz1/bWO0zsA/Vdx8v3v+/urdgAzdN11oo9O7gD0X8Wpt7//zy/bAczOkN/qPrUD0H8VJ979+wGbtAOYmcdBf4EnVo7pv4ruN7/Ppb8fzlzVIZ/toD+W5+fuhWP6r6LzvV9ffePvkMXAczLwj+V503m8qP8qOic6+LeXre6ej+GhPpXZLBfoeuuHnc+92rkEMBdDrhS961o3qv8qOt759cDzuVfnVnaRScTvdHWdAei/io6J9r+Z+4EzgHkYcuvvh4514/qv4vMbvw3Zrh8Wm4crvh96zucHSeq/is8TDfrhVY8DmIOYj/+uW8b6r+LT+x5xPeeVA4A5CPr477gCoP8qPk108L2/dw4A8ht+p+jdpyUj+q/i+G2POft/ZRVgfpc+7u9ru+NN67+Kgm+7NQDZreP+WD7dMNJ/FccjjTqhe7YKOL+oq3+vjleM6L+Ko3c96urfq7taf4aMJO7w//MJgP6rKPmu+3XA5CL/WI5PAPRfxdFEh36X64BfBcptFfnHcny6qP8qDt/0yAs67gBkF5voTcmNc8Lhmx67R/90T4dUIk//P10u0n8VRd/0en+KjCD0ZLHwnyLdDt/0sMV/bywBTC32j+XoAqD+qzicaNB3f965AJhZ3FLRN4efFvqv4nCkAU/++MjPgWUWe7Ho+NNC/1UcjjR44/rPLLr/w78W/VdxONLgjXc+2JEk9J/A4UiDN+4ZAJnpP4GD9zxy9f8r/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TKDpR/Wem/wSKTlT/mek/gaIT1X9m+k+g6ET1n5n+Eyg6Uf1npv8Eik5U/5npP4GiE9V/ZvpPoOhE9Z+Z/hMoOlH9Z6b/BIpOVP+Z6T+BohPVf2b6T6DoRPWfmf4TOHjP18Eb139m+k/gcKTBG9d/ZvpP4HCkwRt/qPjXSG3R/a8Otq7/Kg5HGrzxwz06yQT/teh/BIcTvYvduP5T28T+tawPNq7/Kg4nuozd+OEenWRi/1o2hxvXfxVF3/Rtvb9F6nsI/WM5ulis/yoO3/Tb0G0f7dFJJvav5ehkUf9VHL7p96Hbdvsvt23oX8vj4cb1X8XRSEMv6bj8l9wu8q/l8PKf/us4muhN5Lbvq/0hMorICwBPR9vWfxVH73rkKZ3T/+wiTxdvj7at/yqO3vXIbwDc1PozZCyBJwBHh//6r+N4ok9xm3b3P724SD99WOi/iuO3/TFsy7s6f4KMKO4OwKcPC/1X8WmkYYd0+yp/gYwq6nrx51vF+q/i0/sedQVwc3xCR0JRBwCPn7as/yo+jzToAMDN/1mIOQDoWCmm/yo+v/ExBwA+/udhG7JirONSsf6r6BhpyAGAs/+ZiOi0606x/qvoeOcjnutyV/rPjqkY/syIzmNF/VfRNdGANQDu/c/G8EWAny/+fdd/JV1v/XrwGYCLfzOyH/jH0r1OVP9VdL73Q88AHP3PyrB7AHfdV4r1X0X3RIft0jee+zMr6yGXAE7dKNJ/FSdGOmiX7nu/MzNgB7A59cei/ypOjXTAsx2Pv8lJevd9VwGczF//dZx6+/vv0uU/Q/f9Lhmfzl//dZx8//vuAOQ/S73+XM7kr/86zoy0zzWAjfxnan39qpETV/7f6L+KcyO9/vFu53boJHdtsTdnvyKi/yrOTvTxyss6S1/6mbOrLgJsOlf9/aD/Ks4PYXvVbQCr/mZufXm05z/8v+u/kq9Gur/4EGDp2J8LPzCWX38/RP9VfDmH9WVXAXYu/PFq9fUe4IL69V/JBZPYfn0jQP38v+3N2WPGm8u+G6r/Ki6axXpx9srOUv0cuD21C3i6vfQSsf6ruHSijzcndgF3e9/24bPV4unwL2azXFzzVAj9V3HFRO73N0eLvJYPj+74cdpqdbt4tV9d/UAY/Vdx7Vju/5noYrWSPuXov4qxxwyd9F/F2GOGTvqvYuwxQyf9VzH2mKGT/qsYe8zQSf9VjD1m6KT/KsYeM3TSfxVjjxk66b+KsccMnfRfxdhjhk76r2LsMUMn/Vcx9pihk/6rGHvM0En/VYw9Zuik/yrGHjN00n8VY48ZOum/irHHDJ30X8XYY4ZO+q9i7DFDJ/1XMfaYoZP+a1iOPWbodDt2GrOgf6ZpNXYas6B/pkn/NTyNPWbotB47jVlYjD1m6DZ2GrOwH3vK0O3r3xFnsKt/lg3q+PpX5xnMb/gxUfux25iB3dhDhhPux45jBm7GHjKcshm7jvxux54xnOICQHFO/5msx7HrSO9u7BHDaU4ACnP3nwlzAlCYw38mzB2Aslz9Z9Luxi4kN4v/mDTPACjJd3+ZuN3YjWTm45+JcwBQjo9/Js+XAIvx8c/keQpQKS7+04CHsTtJauPePw1YuwRYxOPYg4VLOAMowXM/aYQfAom3c/RPK57GriWdzf3YM4VLrS0DDubkn4bYAcTy1B+acu9JAIHkT2Pu3QUMI3+a4xQgivxp0NpdgAgbq/5pk3UAw9258UerVq4CDvRg2Q/tcg4wyM6xP21buQ/Q28KHP83bOwno5WY79uQgwHrvGOBq6iePW9cBrrFbqJ9UtnsPBrzM7sEtPxJaPz7YB5x3d7MXP4ltV7eLr0RX9eX/sEv0rurmy//jSvrw/Xtwec+9XkT0XsitfLhIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhgSXp39oSHB5+oeGBJenf2hIcHn6h4YEl6d/aEhwefqHhiyD0+v1IvQPowjuf9nrRegfRjGJ/vexL6LfQQjMz0NseU+9XsQq9kXoHy4TfOi96PUi7mNfxF3wewRZBX/03vZ7FbEvot9BCMzPNja9+36vIvYqRL+DEJihTWh6PV9E7FUIl//hQk+R5fW7/P/9+23ki3heh75BkFhoevueL2Id+SJc/oNLhV4A2PZ9FXeBL6LvTghmKDC9Xe8XEbkCqPdOCOYnML3+n7yBRyEO/+FygefeAz554y5D9lyCAPN0E1XezYAX8Rj1Ijau/sMVwo69B9133wW9CIt/4CpBBwB9b/6/CboP6eMfrhN0ADBw2V3MAYCPf7hSyAHAkLP/VyHfRPLxD9daB3wJYDP4tnvELQAX/+FqAVffh6+62w7fCw27BAEzNfizN6K8wZcAhx+DwBytB159iznvHnod4jHiRcD8DHwEV8xX7tfDvovwEPIiYIYGHXxHXXYbdAnAyT/0NuB7QENv/f1w338HcOfWH/TX++w7Lv8BOwD5wyA9n8IXmX/vHYD8YaBe1wCiV9z22gHIHwZ7vLq9TfyKu+31dwFiD0Fgpu6vbO+u5wP/z1pfeSWiwD4I5umqiwAPhQ67rzoOKbIPgnlaXXwIsCv3QxuXHwJsfOMXIt1e9OlbOLzVZb8JdmPJP8RaL77cA2wWxa+4X7AHUD+UcHv2LOCuzhW31dmzgN1C/VDIdn9iF3D3UK+79e2JbyZvbnzZD4paPz4cHYMvH26rf+iuFsvDbyff3exd8ocq1qvVfvFiv1qNuMhutbp9fRGL1Ur6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJDa/wHh82BSDQplbmRzdHJlYW0KZW5kb2JqCjE1IDAgb2JqCjw8Ci9GMSAxOCAwIFIKL0YyIDE5IDAgUgo+PgplbmRvYmoKMTYgMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAovVHlwZSAvRm9udAovRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwovU3VidHlwZSAvVHlwZTEKPj4KZW5kb2JqCjE3IDAgb2JqCjw8Ci9CYXNlRm9udCAvSGVsdmV0aWNhCi9UeXBlIC9Gb250Ci9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCi9TdWJ0eXBlIC9UeXBlMQo+PgplbmRvYmoKMTggMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAovVHlwZSAvRm9udAovRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwovU3VidHlwZSAvVHlwZTEKPj4KZW5kb2JqCjE5IDAgb2JqCjw8Ci9CYXNlRm9udCAvSGVsdmV0aWNhCi9UeXBlIC9Gb250Ci9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCi9TdWJ0eXBlIC9UeXBlMQo+PgplbmRvYmoKeHJlZgowIDIwCjAwMDAwMDAwMDAgNjU1MzUgZg0KMDAwMDAwMDAxNSAwMDAwMCBuDQowMDAwMDAwMjA3IDAwMDAwIG4NCjAwMDAwMDAwNzggMDAwMDAgbg0KMDAwMDAwMDI3MCAwMDAwMCBuDQowMDAwMDAwNDI3IDAwMDAwIG4NCjAwMDAwMDA1ODQgMDAwMDAgbg0KMDAwMDAwMDcwOCAwMDAwMCBuDQowMDAwMDAwODAyIDAwMDAwIG4NCjAwMDAwMDA5MjYgMDAwMDAgbg0KMDAwMDAwMTAyMCAwMDAwMCBuDQowMDAwMDA1NzcxIDAwMDAwIG4NCjAwMDAwMDkyMzkgMDAwMDAgbg0KMDAwMDAxODEyMiAwMDAwMCBuDQowMDAwMDE4MTY2IDAwMDAwIG4NCjAwMDAwMjcwNDkgMDAwMDAgbg0KMDAwMDAyNzA5MyAwMDAwMCBuDQowMDAwMDI3MTk2IDAwMDAwIG4NCjAwMDAwMjcyOTQgMDAwMDAgbg0KMDAwMDAyNzM5NyAwMDAwMCBuDQp0cmFpbGVyCjw8Ci9Sb290IDEgMCBSCi9JbmZvIDMgMCBSCi9JRCBbPDcxMjU2RkRCMTNFNzhCQUQ3QkM2RjBGOUZBRDQ1NjFEPiA8NzEyNTZGREIxM0U3OEJBRDdCQzZGMEY5RkFENDU2MUQ+XQovU2l6ZSAyMAo+PgpzdGFydHhyZWYKMjc0OTUKJSVFT0YK</Data>
                 </DocumentDetail>
               </DocumentDetails>
            </Document>
         </Documents>
      </GetDocumentsResponse>
   </s:Body>
</s:Envelope>
"""

SHIPMENT_CANCEL_REQUEST_XML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2">
    <soap:Header>
        <v2:RequestContext>
            <v2:Version>2.0</v2:Version>
            <v2:Language>en</v2:Language>
            <v2:GroupID></v2:GroupID>
            <v2:RequestReference></v2:RequestReference>
            <v2:UserToken>token</v2:UserToken>
        </v2:RequestContext>
    </soap:Header>
    <soap:Body>
        <v2:VoidShipmentRequest>
            <v2:PIN>
                <v2:Value>329014521622</v2:Value>
            </v2:PIN>
        </v2:VoidShipmentRequest>
    </soap:Body>
</soap:Envelope>
"""

SHIPMENT_CANCEL_RESPONSE_XML = """
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1"
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <VoidShipmentResponse xmlns="http://purolator.com/pws/datatypes/v1"
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <ShipmentVoided>true</ShipmentVoided>
        </VoidShipmentResponse>
    </s:Body>
</s:Envelope>
"""
