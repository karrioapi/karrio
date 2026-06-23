"""DPD location finder (karrio.Location) + Shop2Shop sendingDepot tests.

References:
  - vendor/LoginService_V2_0_C0.pdf
  - vendor/DepotDataService_V1_0.pdf
"""

import json
import logging
import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dpd_meta as provider
import karrio.providers.dpd_meta.error as provider_error
import karrio.sdk as karrio

from .fixture import gateway

logger = logging.getLogger(__name__)


def _fresh_gateway():
    """A gateway with an empty connection cache.

    The public-WS auth token is cached on the gateway's connection cache;
    tests that assert on the getAuth call must start from an empty cache so
    they are independent of test execution order.
    """
    return karrio.gateway["dpd_meta"].create(
        dict(
            id="dpd_meta_fresh",
            test_mode=True,
            carrier_id="dpd_meta",
            dpd_login="TEST_USERNAME",
            dpd_password="TEST_PASSWORD",
            dpd_bucode="001",
        ),
        cache=lib.Cache(),
    )


GET_AUTH_RESPONSE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns2:getAuthResponse xmlns:ns2="http://dpd.com/common/service/types/LoginService/2.0">
      <return>
        <delisId>TEST_USERNAME</delisId>
        <customerUid>TEST_USERNAME</customerUid>
        <authToken>ws-token-abc123</authToken>
        <depot>0163</depot>
      </return>
    </ns2:getAuthResponse>
  </soap:Body>
</soap:Envelope>"""

# Real LoginService stage response for bad credentials — the specific error
# is an <authenticationFault> nested in <detail>, not a <LoginException>.
GET_AUTH_FAILURE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Server</faultcode>
      <faultstring>Fault occured</faultstring>
      <detail>
        <ns:authenticationFault xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0">
          <errorCode>LOGIN_8</errorCode>
          <errorMessage>The combination of user and password is invalid.</errorMessage>
        </ns:authenticationFault>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>"""

GET_DEPOT_DATA_RESPONSE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns2:getDepotDataResponse xmlns:ns2="http://dpd.com/common/service/types/DepotDataService/1.0">
      <DepotData>
        <depot>0163</depot>
        <name>DPD Deutschland GmbH</name>
        <street>Auhofstr. 25</street>
        <country>DE</country>
        <zipCode>63741</zipCode>
        <city>Aschaffenburg</city>
        <phone>1805 373 200</phone>
        <fax></fax>
        <email>Zentrale@depot163.dpd.de</email>
      </DepotData>
    </ns2:getDepotDataResponse>
  </soap:Body>
</soap:Envelope>"""

GET_DEPOT_DATA_FAULT_XML = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>soap:Server</faultcode>
      <faultstring>Fault occured</faultstring>
      <detail>
        <ns:dataFault xmlns:ns="http://dpd.com/common/service/types/DepotDataService/1.0">
          <errorCode>DEPOTDATA_MISMATCH_DEPOT_FOR_ZIP_CODE</errorCode>
          <errorMessage>The combination of postcode and depot number does not match.</errorMessage>
        </ns:dataFault>
      </detail>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>"""


class TestDPDLocationEnvelope(unittest.TestCase):
    """getDepotData SOAP envelope built by location_request."""

    def setUp(self):
        self.maxDiff = None

    def test_location_request_envelope(self):
        xml = gateway.mapper.create_location_request(
            models.LocationRequest(address=models.Address(country_code="de", postal_code="63741"))
        ).serialize()
        self.assertIn("<soapenv:Envelope", xml)
        self.assertIn("DepotDataService/1.0", xml)
        self.assertIn("Authentication/2.0", xml)
        # the <authentication> header carries an [AUTH_TOKEN] placeholder the
        # proxy substitutes once it holds a public-WS token
        self.assertIn("<ns:authentication", xml)
        self.assertIn("<authToken>[AUTH_TOKEN]</authToken>", xml)
        # the body carries the getDepotData query
        self.assertIn("<ns1:getDepotData", xml)
        self.assertIn("<country>DE</country>", xml)
        self.assertIn("<zipCode>63741</zipCode>", xml)
        # DPD WSDLs are elementFormDefault="unqualified": children stay unprefixed
        self.assertNotIn("<ns1:country>", xml)
        self.assertNotIn("<ns:delisId>", xml)
        self.assertNotIn("<ns:authToken>", xml)


class TestDPDSoapFaults(unittest.TestCase):
    """SOAP fault parsing in error.parse_soap_faults."""

    def setUp(self):
        self.maxDiff = None

    def test_parse_login_fault(self):
        messages = provider_error.parse_soap_faults(lib.to_element(GET_AUTH_FAILURE_XML), gateway.settings)
        # One Message per <soap:Fault> — the specific detail fault is surfaced.
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "LOGIN_8")
        self.assertEqual(messages[0].message, "The combination of user and password is invalid.")

    def test_parse_depot_data_fault(self):
        messages = provider_error.parse_soap_faults(lib.to_element(GET_DEPOT_DATA_FAULT_XML), gateway.settings)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "DEPOTDATA_MISMATCH_DEPOT_FOR_ZIP_CODE")
        self.assertEqual(messages[0].message, "The combination of postcode and depot number does not match.")

    def test_no_faults_on_success(self):
        messages = provider_error.parse_soap_faults(lib.to_element(GET_DEPOT_DATA_RESPONSE_XML), gateway.settings)
        self.assertEqual(messages, [])


class TestDPDLocation(unittest.TestCase):
    """The unified karrio.Location interface for dpd_meta."""

    def setUp(self):
        self.maxDiff = None

    def test_parse_location_response(self):
        """parse_location_response converts depot data to LocationDetails."""
        locations, messages = provider.parse_location_response(
            lib.Deserializable(GET_DEPOT_DATA_RESPONSE_XML), gateway.settings
        )
        self.assertEqual(messages, [])
        self.assertEqual(
            lib.to_dict(locations),
            [
                {
                    "carrier_id": "dpd_meta",
                    "carrier_name": "dpd_meta",
                    "location_id": "0163",
                    "location_type": "depot",
                    "name": "DPD Deutschland GmbH",
                    "address": {
                        "address_line1": "Auhofstr. 25",
                        "city": "Aschaffenburg",
                        "postal_code": "63741",
                        "country_code": "DE",
                        "phone_number": "1805 373 200",
                        "email": "Zentrale@depot163.dpd.de",
                        "residential": False,
                    },
                }
            ],
        )

    def test_parse_location_response_fault(self):
        """A depot dataFault surfaces as messages with no locations."""
        locations, messages = provider.parse_location_response(
            lib.Deserializable(GET_DEPOT_DATA_FAULT_XML), gateway.settings
        )
        self.assertEqual(locations, [])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "DEPOTDATA_MISMATCH_DEPOT_FOR_ZIP_CODE")

    def test_get_locations_proxy_call(self):
        """The proxy issues getAuth then getDepotData against the public WS URLs."""
        gateway = _fresh_gateway()
        request = gateway.mapper.create_location_request(
            models.LocationRequest(address=models.Address(country_code="DE", postal_code="63741"))
        )
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock_request:
            mock_request.side_effect = [GET_AUTH_RESPONSE_XML, GET_DEPOT_DATA_RESPONSE_XML]
            response = gateway.proxy.get_locations(request).deserialize()

        self.assertEqual(mock_request.call_count, 2)
        first_call, second_call = mock_request.call_args_list
        self.assertEqual(first_call[1]["url"], "https://public-ws-stage.dpd.com/services/LoginService/V2_0")
        self.assertEqual(second_call[1]["url"], "https://public-ws-stage.dpd.com/services/DepotDataService/V1_0")
        self.assertEqual(first_call[1]["headers"]["Content-Type"], "text/xml; charset=utf-8")
        self.assertEqual(
            second_call[1]["headers"]["SOAPAction"],
            "http://dpd.com/common/service/DepotDataService/1.0/getDepotData",
        )
        self.assertEqual(response, GET_DEPOT_DATA_RESPONSE_XML)

    def test_get_locations_caches_depot_lookup(self):
        """A resolved depot is cached 24h — a repeat lookup skips both SOAP calls."""
        gateway = _fresh_gateway()
        request = gateway.mapper.create_location_request(
            models.LocationRequest(address=models.Address(country_code="DE", postal_code="63741"))
        )
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock_request:
            mock_request.side_effect = [GET_AUTH_RESPONSE_XML, GET_DEPOT_DATA_RESPONSE_XML]
            first = gateway.proxy.get_locations(request).deserialize()
            second = gateway.proxy.get_locations(request).deserialize()

        # getAuth + getDepotData run once; the second lookup is served from cache.
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(first, second)
        self.assertEqual(first, GET_DEPOT_DATA_RESPONSE_XML)

    def test_location_search_interface(self):
        """karrio.Location.search() resolves a depot end-to-end."""
        with patch("karrio.mappers.dpd_meta.proxy.lib.request") as mock_request:
            mock_request.side_effect = [GET_AUTH_RESPONSE_XML, GET_DEPOT_DATA_RESPONSE_XML]
            locations, messages = (
                karrio.Location.search(
                    models.LocationRequest(address=models.Address(country_code="DE", postal_code="63741"))
                )
                .from_(_fresh_gateway())
                .parse()
            )

        self.assertEqual(messages, [])
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].location_id, "0163")
        self.assertEqual(locations[0].location_type, "depot")
        self.assertEqual(locations[0].address.city, "Aschaffenburg")


SHOP2SHOP_PAYLOAD = {
    "shipper": {
        "address_line1": "Auhofstr.",
        "street_number": "25",
        "city": "Aschaffenburg",
        "postal_code": "63741",
        "country_code": "DE",
        "person_name": "John Sender",
        "company_name": "Sender Corp",
        "phone_number": "+49301234567",
        "email": "sender@example.com",
    },
    "recipient": {
        "address_line1": "Konrad-Adenauer-Allee",
        "street_number": "1",
        "city": "Aschaffenburg",
        "postal_code": "63739",
        "country_code": "DE",
        "person_name": "Jane Receiver",
        "company_name": "Receiver Inc",
        "phone_number": "+49301234567",
        "email": "receiver@example.com",
    },
    "parcels": [
        {
            "weight": 3.0,
            "width": 20.0,
            "height": 15.0,
            "length": 30.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "Shop2Shop parcel",
        }
    ],
    "service": "dpd_meta_shop2shop_domestic",
    "reference": "S2S-1",
    "options": {"dpd_meta_parcel_shop_id": "DE40501"},
}


class TestShop2ShopDepotInjection(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**SHOP2SHOP_PAYLOAD)

    def test_create_shipment_request_stamps_depot_placeholder(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = request.serialize()[0]
        self.assertEqual(serialized["shipmentInfos"]["productCode"], "345")
        # Shop2Shop: the [DEPOT] placeholder is stamped at mapping time; the
        # proxy resolves the real depot before posting.
        self.assertEqual(serialized["sendingDepot"], "[DEPOT]")

    def test_resolve_shipper_depot_can_be_disabled(self):
        """The resolve_shipper_depot option opts out of depot resolution."""
        payload = dict(
            SHOP2SHOP_PAYLOAD,
            options={**SHOP2SHOP_PAYLOAD["options"], "dpd_meta_resolve_shipper_depot": False},
        )
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        serialized = request.serialize()[0]
        self.assertNotIn("sendingDepot", serialized)

    def test_proxy_injects_sending_depot_for_shop2shop(self):
        """For Shop2Shop, the proxy resolves the sender's depot via
        DepotDataService and injects it as `sendingDepot` before posting."""

        def fake_request(**kwargs):
            url = kwargs.get("url", "")
            if "LoginService" in url:
                return GET_AUTH_RESPONSE_XML
            if "DepotDataService" in url:
                return GET_DEPOT_DATA_RESPONSE_XML
            # Shipment endpoint
            return json.dumps(
                {
                    "shipmentId": "S2S-1",
                    "parcelIds": ["0987654321"],
                    "networkShipmentId": "NET-1",
                    "networkParcelIds": ["0987654321"],
                    "parcelBarcodes": [],
                    "label": {"base64Data": "Zm9v", "media-type": "application/pdf"},
                }
            )

        with patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=fake_request) as mock_request:
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

        shipment_call = next(call for call in mock_request.call_args_list if "/shipment?" in call.kwargs["url"])
        body = json.loads(shipment_call.kwargs["data"])
        # shipments carry the 7-digit GeoRouting code (BU code 001 + depot 0163)
        self.assertEqual(body[0]["sendingDepot"], "0010163")
        self.assertEqual(body[0]["shipmentInfos"]["productCode"], "345")

    def test_proxy_skips_depot_lookup_when_resolution_disabled(self):
        """With resolve_shipper_depot off, the proxy performs no depot lookup."""
        payload = dict(
            SHOP2SHOP_PAYLOAD,
            options={**SHOP2SHOP_PAYLOAD["options"], "dpd_meta_resolve_shipper_depot": False},
        )

        def fake_request(**kwargs):
            return "{}"

        with patch("karrio.mappers.dpd_meta.proxy.lib.request", side_effect=fake_request) as mock_request:
            karrio.Shipment.create(models.ShipmentRequest(**payload)).from_(gateway).parse()

        urls = [call.kwargs["url"] for call in mock_request.call_args_list]
        self.assertFalse(any("DepotDataService" in u or "LoginService" in u for u in urls), urls)


if __name__ == "__main__":
    unittest.main()
