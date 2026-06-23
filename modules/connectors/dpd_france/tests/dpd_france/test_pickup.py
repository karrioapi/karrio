"""DPD France pickup tests (CreateCollectionRequestBc + TerminateCollectionRequestBc)."""

import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

from .fixture import gateway


class TestDPDFrancePickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(request.serialize(), PickupRequestXML)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.server_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/CreateCollectionRequestBc",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = PickupResponseXML
            parsed = karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedPickupResponse)

    def test_parse_pickup_error_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseXML
            parsed = karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedPickupErrorResponse)

    def test_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
        self.assertEqual(request.serialize(), PickupCancelRequestXML)

    def test_cancel_pickup(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.server_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/TerminateCollectionRequestBc",
            )

    def test_parse_pickup_cancel_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponseXML
            parsed = karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedPickupCancelResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2026-04-25",
    "ready_time": "10:00",
    "closing_time": "17:00",
    "instruction": "Ring at gate",
    "address": {
        "company_name": "Chef Royale",
        "person_name": "Jean Dupont",
        "address_line1": "28 rue du Clair Bocage",
        "city": "La Seyne-sur-mer",
        "postal_code": "83500",
        "country_code": "FR",
        "phone_number": "+330447110494",
    },
    "parcels": [{"weight": 5.0, "weight_unit": "KG"}],
}

PickupCancelPayload = {
    "confirmation_number": "CR250000001",
    "pickup_date": "2026-04-25",
    "address": {"country_code": "FR", "person_name": "Jean Dupont"},
}

ParsedPickupResponse = [
    {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "confirmation_number": "CR250000001",
    },
    [],
]

ParsedPickupErrorResponse = [
    None,
    [
        {
            "carrier_id": "dpd_france",
            "carrier_name": "dpd_france",
            "code": "IpPermissionDenied",
            "details": {},
            "message": "Caller IP not whitelisted",
        }
    ],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "dpd_france",
        "carrier_name": "dpd_france",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:CreateCollectionRequestBc>
            <imt:request>
                <imt:shipperaddress>
                    <imt:countryPrefix>FR</imt:countryPrefix>
                    <imt:zipCode>83500</imt:zipCode>
                    <imt:city>La Seyne-sur-mer</imt:city>
                    <imt:street>28 rue du Clair Bocage</imt:street>
                    <imt:name>Chef Royale</imt:name>
                    <imt:phoneNumber>+330447110494</imt:phoneNumber>
                </imt:shipperaddress>
                <imt:customer_countrycode>250</imt:customer_countrycode>
                <imt:customer_centernumber>123</imt:customer_centernumber>
                <imt:customer_number>456789</imt:customer_number>
                <imt:parcel_count>1</imt:parcel_count>
                <HideCustomerAddress xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
                <imt:pick_date>2026-04-25</imt:pick_date>
                <imt:time_from>10:00</imt:time_from>
                <imt:time_to>17:00</imt:time_to>
                <imt:pick_remark>Ring at gate</imt:pick_remark>
                <dayCheckDone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
            </imt:request>
        </imt:CreateCollectionRequestBc>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupCancelRequestXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:TerminateCollectionRequestBc>
            <imt:request>
                <imt:customer>
                    <imt:centernumber>123</imt:centernumber>
                    <imt:number>456789</imt:number>
                    <imt:countrycode>250</imt:countrycode>
                </imt:customer>
                <imt:parcel>
                    <imt:Parcel>
                        <imt:Barcode>
                            <imt:Identifier>Bic3</imt:Identifier>
                            <imt:BarcodeValue>CR250000001</imt:BarcodeValue>
                        </imt:Barcode>
                    </imt:Parcel>
                </imt:parcel>
            </imt:request>
        </imt:TerminateCollectionRequestBc>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateCollectionRequestBcResponse xmlns="http://www.cargonet.software">
      <CreateCollectionRequestBcResult>CR250000001</CreateCollectionRequestBcResult>
    </CreateCollectionRequestBcResponse>
  </soap:Body>
</soap:Envelope>"""

PickupCancelResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TerminateCollectionRequestBcResponse xmlns="http://www.cargonet.software"/>
  </soap:Body>
</soap:Envelope>"""

ErrorResponseXML = """<?xml version="1.0"?>
<Error><ErrorId>IpPermissionDenied</ErrorId><ErrorMessage>Caller IP not whitelisted</ErrorMessage></Error>"""
