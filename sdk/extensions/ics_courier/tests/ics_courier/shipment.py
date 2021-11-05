import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from tests.ics_courier.fixture import gateway


class TestICSCourierShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.VoidShipmentRequest = ShipmentCancelRequest(**void_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_void_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.VoidShipmentRequest
        )

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
                ShipmentLabelResponseXML,
            ]
            purplship.Shipment.create(self.ShipmentRequest).from_(gateway)

            process_shipment_call, get_label_call = mocks.call_args_list

            self.assertEqual(
                process_shipment_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                process_shipment_call[1]["headers"]["soapaction"], "urn:processShipment"
            )
            self.assertEqual(
                get_label_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )

    def test_void_shipment(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Shipment.cancel(self.VoidShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:voidShipment"
            )

    def test_parse_void_shipment_response(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = VoidShipmentResponseXML
            parsed_response = (
                purplship.Shipment.cancel(self.VoidShipmentRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedVoidShipmentResponse)
            )


if __name__ == "__main__":
    unittest.main()


void_shipment_data = {"shipment_identifier": "10000696"}

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "residential": False,
    },
    "recipient": {
        "address_line1": "1 TEST ST",
        "city": "TORONTO",
        "company_name": "TEST ADDRESS",
        "phone_number": "4161234567",
        "postal_code": "M4X1W7",
        "state_code": "ON",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "service": "ics_courier_ground",
    "options": {
        "ics_courier_extra_care": True,
    },
}

ParsedShipmentResponse = []

ParsedVoidShipmentResponse = [
    {
        "carrier_id": "ics_courier",
        "carrier_name": "ics_courier",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ShipmentLabelResponseXML = "<label></label>"

ShipmentRequestXML = f"""<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <CreateShipment xmlns="http://www.icscourier.ca/">
            <AuthenicateAccount>
                <AccountID>string</AccountID>
                <Password>string</Password>
            </AuthenicateAccount>
            <ConsigneeInfo>
                <ID>string</ID>
                <Name>string</Name>
                <Address1>string</Address1>
                <Address2>string</Address2>
                <City>string</City>
                <Province>string</Province>
                <Postcode>string</Postcode>
                <Contact>string</Contact>
                <Phone>string</Phone>
            </ConsigneeInfo>
            <PackageInfo>
                <Product>string</Product>
                <Pieces>
                    <PieceInfo>
                        <Weight>double</Weight>
                        <WeightUnit>string</WeightUnit>
                        <Length>double</Length>
                        <Width>double</Width>
                        <Height>double</Height>
                        <DeclaredValue>double</DeclaredValue>
                    </PieceInfo>
                    <PieceInfo>
                        <Weight>double</Weight>
                        <WeightUnit>string</WeightUnit>
                        <Length>double</Length>
                        <Width>double</Width>
                        <Height>double</Height>
                        <DeclaredValue>double</DeclaredValue>
                    </PieceInfo>
                </Pieces>
                <Contact>string</Contact>
                <Phone>string</Phone>
                <CostCenter>string</CostCenter>
                <Refereces>
                    <string>string</string>
                    <string>string</string>
                </Refereces>
                <NotificationEmail>string</NotificationEmail>
                <SpecialInstruction>string</SpecialInstruction>
                <NoSignatureRequired>boolean</NoSignatureRequired>
                <ShipDate>string</ShipDate>
            </PackageInfo>
        </CreateShipment>
    </soap12:Body>
</soap12:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <CreateShipmentResponse xmlns="http://www.icscourier.ca/">
      <CreateShipmentResult>
        <Err>
          <_ErrCode>string</_ErrCode>
          <_ErrDescription>string</_ErrDescription>
        </Err>
        <ManifestNumber>string</ManifestNumber>
        <PackageIDAndLink>string</PackageIDAndLink>
        <PackageID>
          <string>string</string>
          <string>string</string>
        </PackageID>
      </CreateShipmentResult>
    </CreateShipmentResponse>
  </soap12:Body>
</soap12:Envelope>
"""

VoidShipmentRequestXML = """<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <VoidPackages xmlns="http://www.icscourier.ca/">
            <AuthenicateAccount>
                <AccountID>string</AccountID>
                <Password>string</Password>
            </AuthenicateAccount>
            <Packages>
                <string>string</string>
            </Packages>
        </VoidPackages>
    </soap12:Body>
</soap12:Envelope>
"""

VoidShipmentResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <VoidPackagesResponse xmlns="http://www.icscourier.ca/">
            <VoidPackagesResult>
                <err>
                    <_ErrCode>string</_ErrCode>
                    <_ErrDescription>string</_ErrDescription>
                </err>
                <PackageVoidStatus>
                    <PackageVoidStatus>
                        <HeaderPin>string</HeaderPin>
                        <VoidStatus>string</VoidStatus>
                        <Err xsi:nil="true" />
                        <Packages xsi:nil="true" />
                    </PackageVoidStatus>
                    <PackageVoidStatus>
                        <HeaderPin>string</HeaderPin>
                        <VoidStatus>string</VoidStatus>
                        <Err xsi:nil="true" />
                        <Packages xsi:nil="true" />
                    </PackageVoidStatus>
                </PackageVoidStatus>
            </VoidPackagesResult>
        </VoidPackagesResponse>
    </soap12:Body>
</soap12:Envelope>
"""
