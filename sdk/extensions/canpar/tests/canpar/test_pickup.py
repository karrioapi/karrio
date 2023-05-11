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


class TestCanparPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequestXML)

    def test_create_modify_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        pipeline = request.serialize()
        cancel_request = pipeline["cancel"]()
        schedule_request = pipeline["schedule"](PickupCancelResponseXML)

        self.assertEqual(cancel_request.data.serialize(), PickupCancelRequestXML)
        self.assertEqual(schedule_request.data.serialize(), PickupUpdateRequestXML)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequestXML)

    def test_request_pickup(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:schedulePickupV2"
            )

    def test_modify_pickup(self):
        with patch("karrio.mappers.canpar.proxy.http") as mocks:
            mocks.side_effect = [
                PickupCancelResponseXML,
                PickupResponseXML,
            ]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            cancel_call, schedule_call = mocks.call_args_list

            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                cancel_call[1]["headers"]["soapaction"], "urn:cancelPickup"
            )
            self.assertEqual(
                schedule_call[1]["url"],
                f"{gateway.settings.server_url}/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                schedule_call[1]["headers"]["soapaction"], "urn:schedulePickupV2"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:cancelPickup"
            )

    def test_parse_request_pickup_response(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = PickupResponseXML
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupResponse)
            )

    def test_parse_modify_pickup_response(self):
        with patch("karrio.mappers.canpar.proxy.http") as mocks:
            mocks.side_effect = [
                PickupCancelResponseXML,
                PickupResponseXML,
            ]
            parsed_response = (
                karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupResponse)
            )

    def test_parse_void_shipment_response(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = PickupCancelResponseXML
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedPickupCancelResponse)
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
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canpar.ca",
    },
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
}

pickup_update_data = {
    "confirmation_number": "10000696",
    "pickup_date": "2015-01-28",
    "address": {
        "person_name": "Jane Doe",
        "email": "john.doe@canpar.ca",
        "phone_number": "1 514 5555555",
    },
    "parcels": [{"weight": 4, "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"LoadingDockAvailable": False, "TrailerAccessible": False},
}

pickup_cancel_data = {"confirmation_number": "10000696"}

ParsedPickupResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "confirmation_number": "10000696",
        "pickup_date": "2015-01-28 15:00:00",
    },
    [],
]

ParsedPickupCancelResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" xmlns:xsd1="http://dto.canshipws.canpar.com/xsd">
    <soap:Header/>
    <soap:Body>
        <ws:schedulePickupV2>
            <ws:request>
                <xsd:password>password</xsd:password>
                <xsd:pickup>
                    <xsd1:comments>Door at Back</xsd1:comments>
                    <xsd1:created_by>John Doe</xsd1:created_by>
                    <xsd1:pickup_address>
                        <xsd1:address_line_1>2271 Herring Cove</xsd1:address_line_1>
                        <xsd1:attention>John Doe</xsd1:attention>
                        <xsd1:city>Halifax</xsd1:city>
                        <xsd1:country>CA</xsd1:country>
                        <xsd1:email>john.doe@canpar.ca</xsd1:email>
                        <xsd1:name>Jim Duggan</xsd1:name>
                        <xsd1:phone>1 514 5555555</xsd1:phone>
                        <xsd1:postal_code>B3L2C2</xsd1:postal_code>
                        <xsd1:province>NS</xsd1:province>
                        <xsd1:residential>true</xsd1:residential>
                    </xsd1:pickup_address>
                    <xsd1:pickup_date>2015-01-28T15:00:00</xsd1:pickup_date>
                    <xsd1:pickup_phone>1 514 5555555</xsd1:pickup_phone>
                </xsd:pickup>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:schedulePickupV2>
    </soap:Body>
</soap:Envelope>
"""

PickupUpdateRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" xmlns:xsd1="http://dto.canshipws.canpar.com/xsd">
    <soap:Header/>
    <soap:Body>
        <ws:schedulePickupV2>
            <ws:request>
                <xsd:password>password</xsd:password>
                <xsd:pickup>
                    <xsd1:comments>Door at Back</xsd1:comments>
                    <xsd1:created_by>Jane Doe</xsd1:created_by>
                    <xsd1:pickup_address>
                        <xsd1:attention>Jane Doe</xsd1:attention>
                        <xsd1:email>john.doe@canpar.ca</xsd1:email>
                        <xsd1:phone>1 514 5555555</xsd1:phone>
                        <xsd1:residential>false</xsd1:residential>
                    </xsd1:pickup_address>
                    <xsd1:pickup_date>2015-01-28T15:00:00</xsd1:pickup_date>
                    <xsd1:pickup_phone>1 514 5555555</xsd1:pickup_phone>
                    <xsd1:unit_of_measure>K</xsd1:unit_of_measure>
                    <xsd1:weight>4.</xsd1:weight>
                </xsd:pickup>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:schedulePickupV2>
    </soap:Body>
</soap:Envelope>
"""

PickupCancelRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:cancelPickup>
            <ws:request>
                <xsd:id>10000696</xsd:id>
                <xsd:password>password</xsd:password>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:cancelPickup>
    </soap:Body>
</soap:Envelope>
"""

PickupCancelResponseXML = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:cancelPickupResponse xmlns:ns="http://ws.business.canshipws.canpar.com">
            <ns:return xmlns:ax211="http://dto.canshipws.canpar.com/xsd"
                xmlns:ax29="http://ws.dto.canshipws.canpar.com/xsd"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:CancelPickupRs">
                <ax29:error xsi:nil="true"/>
            </ns:return>
        </ns:cancelPickupResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

PickupResponseXML = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope  xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope" xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns="http://ws.dto.canshipws.canpar.com/xsd" xmlns:xsd1="http://dto.canshipws.canpar.com/xsd">
    <soapenv:Body>
        <ws:schedulePickupResponse>
            <ws:request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:CancelPickupRs">
                <error xsi:nil="true"/>
                <pickup>
                    <id>10000696</id>
                    <comments>Door at Back</comments>
                    <created_by>John Doe</created_by>
                    <pickup_address>
                        <address_line_1>2271 Herring Cove</address_line_1>
                        <address_line_2></address_line_2>
                        <attention>John Doe</attention>
                        <city>Halifax</city>
                        <country>CA</country>
                        <email>john.doe@canpar.ca</email>
                        <name>Jim Duggan</name>
                        <phone>1 514 5555555</phone>
                        <postal_code>B3L2C2</postal_code>
                        <province>NS</province>
                        <residential>true</residential>
                    </pickup_address>
                    <pickup_date>2015-01-28T15:00:00</pickup_date>
                    <pickup_phone>1 514 5555555</pickup_phone>
                    <unit_of_measure>L</unit_of_measure>
                </pickup>
            </ws:request>
        </ws:schedulePickupResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
