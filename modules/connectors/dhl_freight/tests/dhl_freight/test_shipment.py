"""DHL Freight shipment booking — full coverage.

4-method pattern per feature (see karrio testing.md):
  1. test_create_<feature>_request — payload → DHL on-wire payload
  2. test_create_<feature>          — proxy URL/method/headers assertion
  3. test_parse_<feature>_response  — DHL response → karrio model
  4. test_parse_error_response      — error path

Fixtures mirror the Sandbox Postman sample at
``vendors/DHL_Freight_Shipment_Booking_SANDBOX_2026_R03.postman_collection.json``.
"""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.schemas.dhl_freight.shipping_request as dhl_freight_req
import karrio.sdk as karrio

from .fixture import gateway


class TestDHLFreightShipment(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**SHIPMENT_PAYLOAD)
        self.DangerousGoodsRequest = models.ShipmentRequest(**DANGEROUS_GOODS_PAYLOAD)
        self.TempControlledRequest = models.ShipmentRequest(**TEMP_CONTROLLED_PAYLOAD)
        self.RomaniaRequest = models.ShipmentRequest(**ROMANIA_TAX_REF_PAYLOAD)
        self.MultiPieceRequest = models.ShipmentRequest(**MULTI_PIECE_PAYLOAD)

    # ------------------------------------------------------------------
    # Request building
    # ------------------------------------------------------------------

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertDictEqual(request.serialize(), ExpectedShipmentRequest)

    def test_create_shipment_request_builds_typed_dto(self):
        """The mapper holds the generated ShippingRequestType DTO, not a raw dict.

        Regression guard: if the schema codegen is skipped (e.g. someone
        commits ``schemas/*.json`` as JSON-Schema definitions instead of
        example payloads), this test fails immediately rather than at a
        future runtime crash.
        """
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertIsInstance(request.value, dhl_freight_req.ShippingRequestType)
        self.assertIsInstance(request.value.payerCode, dhl_freight_req.PayerCodeType)
        self.assertIsInstance(request.value.additionalServices, dhl_freight_req.AdditionalServicesType)
        self.assertTrue(all(isinstance(p, dhl_freight_req.PartyType) for p in request.value.parties))
        self.assertTrue(all(isinstance(p, dhl_freight_req.PieceType) for p in request.value.pieces))

    def test_create_shipment_request_uses_product_code(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize()["productCode"], "ECI")

    def test_create_shipment_request_has_consignor_and_consignee(self):
        """Booking sends the two mandatory party roles (Pickup/Delivery only when divergent)."""
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        types = sorted(p["type"] for p in request.serialize()["parties"])
        self.assertEqual(types, ["Consignee", "Consignor"])

    def test_create_shipment_request_sets_consignor_account_id(self):
        """Parties[Consignor].Id is the (mandatory) DHL Freight account number."""
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        consignor = next(p for p in request.serialize()["parties"] if p["type"] == "Consignor")
        self.assertEqual(consignor["id"], "62085855350106")

    def test_create_shipment_request_consignor_account_option_overrides(self):
        """The per-shipment consignor_account option overrides the connection account."""
        payload = {
            **SHIPMENT_PAYLOAD,
            "options": {**SHIPMENT_PAYLOAD["options"], "dhl_freight_consignor_account": "99999999999999"},
        }
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        consignor = next(p for p in request.serialize()["parties"] if p["type"] == "Consignor")
        self.assertEqual(consignor["id"], "99999999999999")

    def test_create_shipment_request_dangerous_goods_sets_flag(self):
        """If any piece declares ADR data, additionalServices.dangerousGoods must be true."""
        request = gateway.mapper.create_shipment_request(self.DangerousGoodsRequest)
        serialized = request.serialize()
        self.assertTrue(serialized["additionalServices"]["dangerousGoods"])
        self.assertIn("dangerousGoods", serialized["pieces"][0])
        self.assertEqual(serialized["pieces"][0]["dangerousGoods"]["unNumber"], 1380)

    def test_create_shipment_request_temperature_controlled(self):
        request = gateway.mapper.create_shipment_request(self.TempControlledRequest)
        temp = request.serialize()["additionalServices"]["temperatureControlled"]
        self.assertEqual(temp, {"type": "Custom", "min": 2, "max": 8})

    def test_create_shipment_request_romania_uit_number(self):
        request = gateway.mapper.create_shipment_request(self.RomaniaRequest)
        info = request.serialize()["additionalInformation"]
        self.assertEqual(info, [{"code": "UIT_NUMBER", "stringValue": "RO1M-A23N-4I5A-ROM6"}])

    def test_create_shipment_request_multi_piece_totals(self):
        """totalNumberOfPieces / totalPalletPlaces / totalLoadingMeters sum across pieces."""
        request = gateway.mapper.create_shipment_request(self.MultiPieceRequest)
        serialized = request.serialize()
        self.assertEqual(serialized["totalNumberOfPieces"], 5)  # 2 + 3
        self.assertEqual(serialized["totalPalletPlaces"], 4)  # 1 + 3
        self.assertEqual(serialized["totalLoadingMeters"], 2.4)

    def test_create_shipment_request_payer_code_falls_back_to_default(self):
        """When no per-shipment payerCode given, the connection default is used."""
        payload = {**SHIPMENT_PAYLOAD, "options": {"shipment_date": "2026-12-31"}}
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        # ``lib.to_dict`` strips empty `location`; assert only the code is set.
        self.assertEqual(request.serialize()["payerCode"]["code"], "DAP")

    def test_create_shipment_request_passes_vat_eori(self):
        """Tax id goes in vatEoriSocialSecurityNumber, not the typed `vat` field."""
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        consignor = next(p for p in request.serialize()["parties"] if p["type"] == "Consignor")
        self.assertEqual(consignor["vatEoriSocialSecurityNumber"], "NL0123456789")
        self.assertNotIn("vat", consignor)

    # ------------------------------------------------------------------
    # Proxy call shape
    # ------------------------------------------------------------------

    def test_create_shipment_proxy_call(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_RESPONSE_JSON
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            method = mock.call_args[1]["method"]
            headers = mock.call_args[1]["headers"]

            self.assertEqual(
                url,
                f"{gateway.settings.server_url}/sendtransportinstruction",
            )
            self.assertEqual(method, "POST")
            self.assertEqual(headers["content-type"], "application/json")
            self.assertIn("Bearer", headers["Authorization"])

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_RESPONSE_JSON
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_response_propagates_license_plates(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_RESPONSE_JSON
            details, _ = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertEqual(
                details.meta["license_plates"],
                ["00370000000000000001", "00370000000000000002"],
            )

    def test_parse_shipment_response_no_label_payload(self):
        """DHL Freight booking returns no label — docs.label must be empty."""
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_RESPONSE_JSON
            details, _ = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertEqual(details.docs.label, "")

    # ------------------------------------------------------------------
    # Error parsing
    # ------------------------------------------------------------------

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = ERROR_RESPONSE_JSON
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)

    def test_parse_429_rate_limit_response(self):
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.return_value = RATE_LIMIT_RESPONSE_JSON
            _, messages = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            self.assertEqual(messages[0].code, "429")
            self.assertIn("rate limit", messages[0].message.lower())


class TestDHLFreightFreightFeatures(unittest.TestCase):
    """PRD §6 follow-ups: billing/4-party, customs.options, ADR commodities, Print."""

    def setUp(self):
        self.maxDiff = None

    def test_billing_address_maps_to_consignor_and_shipper_to_pickup(self):
        """§6.2 billing_address → Consignor; divergent shipper → Pickup."""
        payload = {**SHIPMENT_PAYLOAD, "billing_address": _BILLING}
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload))
        parties = {p["type"]: p for p in request.serialize()["parties"]}
        self.assertEqual(sorted(parties), ["Consignee", "Consignor", "Pickup"])
        self.assertEqual(parties["Consignor"]["name"], "Billing Dept BV")
        self.assertEqual(parties["Pickup"]["name"], "Rower Gear NL")  # the shipper

    def test_no_billing_address_sends_two_parties(self):
        """Without billing_address, shipper == Consignor, so no Pickup is added."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**SHIPMENT_PAYLOAD))
        types = sorted(p["type"] for p in request.serialize()["parties"])
        self.assertEqual(types, ["Consignee", "Consignor"])

    def test_consignee_account_from_setting(self):
        """§6.2 consignee account resolves from the connection setting."""
        gw = karrio.gateway["dhl_freight"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="62085855350106",
                consignee_account_number="70000000000001",
                account_country_code="NL",
                test_mode=True,
            ),
        )
        request = gw.mapper.create_shipment_request(models.ShipmentRequest(**SHIPMENT_PAYLOAD))
        consignee = next(p for p in request.serialize()["parties"] if p["type"] == "Consignee")
        self.assertEqual(consignee["id"], "70000000000001")

    def test_customs_options_payer_and_tax_refs(self):
        """§6.6/§6.7 payerCode + RO/HU/PL refs read from customs.options."""
        payload = {
            **SHIPMENT_PAYLOAD,
            "options": {"shipment_date": "2026-12-31"},
            "customs": dict(
                commodities=[dict(quantity=2, description="Machinery", value_amount=7500, value_currency="EUR")],
                options=dict(
                    dhl_freight_payer_code="DDP",
                    dhl_freight_payer_code_location="BONN",
                    dhl_freight_uit_number="RO1M-A23N-4I5A-ROM6",
                ),
            ),
        }
        serialized = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload)).serialize()
        self.assertEqual(serialized["payerCode"], {"code": "DDP", "location": "BONN"})
        self.assertEqual(
            serialized["additionalInformation"], [{"code": "UIT_NUMBER", "stringValue": "RO1M-A23N-4I5A-ROM6"}]
        )

    def test_customs_incoterm_drives_payer_code(self):
        """§6.7 customs.incoterm is the payerCode fallback."""
        payload = {
            **SHIPMENT_PAYLOAD,
            "options": {"shipment_date": "2026-12-31"},
            "customs": dict(commodities=[dict(quantity=1, description="x")], incoterm="DDP"),
        }
        serialized = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload)).serialize()
        self.assertEqual(serialized["payerCode"]["code"], "DDP")

    def test_adr_from_commodity_metadata(self):
        """§6.4 ADR dangerous goods sourced from a parcel item's metadata."""
        payload = {
            **SHIPMENT_PAYLOAD,
            "parcels": [
                dict(
                    weight=550.0,
                    weight_unit="KG",
                    packaging_type="pallet",
                    items=[
                        dict(
                            quantity=1,
                            description="UN1380",
                            metadata=dict(dangerousGoods=dict(unNumber=1380, adrClass="4.2")),
                        )
                    ],
                )
            ],
        }
        serialized = gateway.mapper.create_shipment_request(models.ShipmentRequest(**payload)).serialize()
        self.assertTrue(serialized["additionalServices"]["dangerousGoods"])
        self.assertEqual(serialized["pieces"][0]["dangerousGoods"]["unNumber"], 1380)

    def test_print_followup_attaches_label_when_enabled(self):
        """§6.3 opt-in Print follow-up: booking → printdocumentsbyid → docs.label."""
        gw = karrio.gateway["dhl_freight"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="62085855350106",
                account_country_code="NL",
                test_mode=True,
                config=dict(auto_print_documents=True),
            ),
            cache=lib.Cache(
                **{
                    "dhl_freight|client_id|client_secret": dict(
                        access_token="t", expires_in="1799", expiry="2099-01-01 00:00:00"
                    )
                }
            ),
        )
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.side_effect = [SHIPMENT_RESPONSE_JSON, PRINT_RESPONSE_JSON]
            details, _ = karrio.Shipment.create(models.ShipmentRequest(**SHIPMENT_PAYLOAD)).from_(gw).parse()

            self.assertIn("printdocumentsbyid", mock.call_args_list[1][1]["url"])
            self.assertEqual(details.docs.label, "BASE64LABEL==")
            self.assertEqual(details.label_type, "PDF")

    def test_print_followup_fail_open(self):
        """A print failure never fails the booking (label stays empty)."""
        gw = karrio.gateway["dhl_freight"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
                account_number="62085855350106",
                account_country_code="NL",
                test_mode=True,
                config=dict(auto_print_documents=True),
            ),
            cache=lib.Cache(
                **{
                    "dhl_freight|client_id|client_secret": dict(
                        access_token="t", expires_in="1799", expiry="2099-01-01 00:00:00"
                    )
                }
            ),
        )
        with patch("karrio.mappers.dhl_freight.proxy.lib.request") as mock:
            mock.side_effect = [SHIPMENT_RESPONSE_JSON, Exception("print 500")]
            details, messages = karrio.Shipment.create(models.ShipmentRequest(**SHIPMENT_PAYLOAD)).from_(gw).parse()
            self.assertEqual(messages, [])
            self.assertEqual(details.tracking_number, "DHLF-2026-000001")
            self.assertEqual(details.docs.label, "")


_BILLING = dict(
    company_name="Billing Dept BV",
    person_name="Pay Er",
    address_line1="Finance Straat 9",
    city="Amsterdam",
    postal_code="1011 AA",
    country_code="NL",
    federal_tax_id="NL9999999999",
)

PRINT_RESPONSE_JSON = """{"documents": [{"content": "BASE64LABEL=="}]}"""


if __name__ == "__main__":
    unittest.main()


# =============================================================================
# Fixtures
# =============================================================================

# ---- Payload helpers --------------------------------------------------------

_SHIPPER = dict(
    company_name="Rower Gear NL",
    person_name="John Doe",
    address_line1="Damrak Straat 1",
    city="Niemegen",
    postal_code="4651 SR",
    country_code="NL",
    phone_number="+31 63559867",
    email="NL.progidy@pgd-nl.com",
    federal_tax_id="NL0123456789",
)
_RECIPIENT = dict(
    company_name="Ford Romania",
    person_name="Gerardiu Pocamantiu",
    address_line1="Esma Sultan Street",
    city="MANKALYA",
    postal_code="905500",
    country_code="RO",
    phone_number="+40 921345871",
    email="RO.ford@fordromania.com",
    federal_tax_id="RO0123456789",
)

# ---- Payloads ---------------------------------------------------------------

SHIPMENT_PAYLOAD = dict(
    service="dhl_freight_eurapid",
    reference="ORDER-9001",
    shipper=_SHIPPER,
    recipient=_RECIPIENT,
    parcels=[
        dict(
            weight=550.0,
            weight_unit="KG",
            length=100.0,
            width=90.0,
            height=140.0,
            dimension_unit="CM",
            packaging_type="pallet",
            description="Machinery parts",
            options=dict(
                numberOfPieces=2,
                palletPlaces=1,
                loadingMeters=0,
                stackable=True,
            ),
        )
    ],
    options=dict(
        shipment_date="2026-12-31",
        requested_delivery_date="2027-01-03",
        dhl_freight_pickup_instruction="to B... - MAX 512 chars",
        dhl_freight_delivery_instruction="from A... - MAX 512 chars",
        dhl_freight_pre_advice=True,
        dhl_freight_consignor_reference="Consignor-Ref123",
        dhl_freight_consignee_reference="Consignee-Ref456",
        dhl_freight_payer_code="DAP",
    ),
)

DANGEROUS_GOODS_PAYLOAD = dict(
    service="dhl_freight_euroconnect",
    shipper=_SHIPPER,
    recipient=_RECIPIENT,
    parcels=[
        dict(
            weight=750.0,
            weight_unit="KG",
            length=100.0,
            width=100.0,
            height=120.0,
            dimension_unit="CM",
            packaging_type="pallet",
            options=dict(
                numberOfPieces=2,
                palletPlaces=2,
                dangerousGoods=dict(
                    dgmId=979,
                    properShippingName="PENTABORANE",
                    adrClass="4.2",
                    unNumber=1380,
                    packageGroup="I",
                    tunnelCode="B/E",
                    grossWeight=700,
                ),
            ),
        )
    ],
    options=dict(shipment_date="2026-12-31"),
)

TEMP_CONTROLLED_PAYLOAD = dict(
    service="dhl_freight_euroconnect",
    shipper=_SHIPPER,
    recipient=_RECIPIENT,
    parcels=[dict(weight=200.0, weight_unit="KG", packaging_type="pallet")],
    options=dict(
        shipment_date="2026-12-31",
        dhl_freight_temperature_controlled=dict(type="Custom", min=2, max=8),
    ),
)

ROMANIA_TAX_REF_PAYLOAD = dict(
    service="dhl_freight_euroconnect",
    shipper=_SHIPPER,
    recipient=_RECIPIENT,
    parcels=[dict(weight=200.0, weight_unit="KG", packaging_type="pallet")],
    options=dict(
        shipment_date="2026-12-31",
        dhl_freight_uit_number="RO1M-A23N-4I5A-ROM6",
    ),
)

MULTI_PIECE_PAYLOAD = dict(
    service="dhl_freight_euroconnect",
    shipper=_SHIPPER,
    recipient=_RECIPIENT,
    parcels=[
        dict(
            weight=400.0,
            weight_unit="KG",
            length=80.0,
            width=80.0,
            height=100.0,
            dimension_unit="CM",
            packaging_type="pallet",
            options=dict(numberOfPieces=2, palletPlaces=1, loadingMeters=0.8),
        ),
        dict(
            weight=600.0,
            weight_unit="KG",
            length=120.0,
            width=80.0,
            height=100.0,
            dimension_unit="CM",
            packaging_type="pallet",
            options=dict(numberOfPieces=3, palletPlaces=3, loadingMeters=1.6),
        ),
    ],
    options=dict(shipment_date="2026-12-31"),
)


# ---- Expected request body --------------------------------------------------

ExpectedShipmentRequest = {
    "productCode": "ECI",
    "pickupDate": "2026-12-31T00:00:00.000Z",
    "requestedDeliveryDate": "2027-01-03T00:00:00.000Z",
    "pickupInstruction": "to B... - MAX 512 chars",
    "deliveryInstruction": "from A... - MAX 512 chars",
    "totalNumberOfPieces": 2,
    "totalWeight": 550.0,
    "totalVolume": 2.52,
    "totalLoadingMeters": 0,
    "totalPalletPlaces": 1,
    "goodsDescription": "Machinery parts",
    "goodsValueCurrency": "EUR",
    "references": [
        {"qualifier": "CNR", "value": "Consignor-Ref123"},
        {"qualifier": "CNZ", "value": "Consignee-Ref456"},
        {"qualifier": "SHP", "value": "ORDER-9001"},
    ],
    "payerCode": {"code": "DAP"},
    "parties": [
        {
            "type": "Consignor",
            "id": "62085855350106",
            "name": "Rower Gear NL",
            "vatEoriSocialSecurityNumber": "NL0123456789",
            "contactName": "John Doe",
            "address": {
                "street": "Damrak Straat 1",
                "cityName": "Niemegen",
                "postalCode": "4651 SR",
                "countryCode": "NL",
            },
            "phone": "+31 63559867",
            "email": "NL.progidy@pgd-nl.com",
        },
        {
            "type": "Consignee",
            "name": "Ford Romania",
            "vatEoriSocialSecurityNumber": "RO0123456789",
            "contactName": "Gerardiu Pocamantiu",
            "address": {
                "street": "Esma Sultan Street",
                "cityName": "MANKALYA",
                "postalCode": "905500",
                "countryCode": "RO",
            },
            "phone": "+40 921345871",
            "email": "RO.ford@fordromania.com",
        },
    ],
    "additionalServices": {
        "preAdvice": True,
    },
    "pieces": [
        {
            "id": [""],
            "goodsType": "Machinery parts",
            "packageType": "PAL",
            "numberOfPieces": 2,
            "weight": 550.0,
            "volume": 2.52,
            "loadingMeters": 0,
            "palletPlaces": 1,
            "width": 90.0,
            "height": 140.0,
            "length": 100.0,
            "stackable": True,
        }
    ],
}


# ---- DHL responses (mocked HTTP) -------------------------------------------

SHIPMENT_RESPONSE_JSON = """{
    "shipmentId": "DHLF-2026-000001",
    "status": "BOOKED",
    "licensePlates": [
        {"licensePlate": "00370000000000000001"},
        {"licensePlate": "00370000000000000002"}
    ]
}"""

ERROR_RESPONSE_JSON = """{
    "type": "https://api.dhl.com/freight/problem",
    "title": "Bad Request",
    "statusCode": 400,
    "detail": "Missing required field: totalWeight",
    "instance": "/freight/shipping/orders/v1/sendtransportinstruction",
    "invalidParams": [
        {"name": "totalWeight", "reason": "must be > 0"}
    ]
}"""

RATE_LIMIT_RESPONSE_JSON = """{
    "title": "Too Many Requests",
    "statusCode": 429,
    "detail": "Daily rate limit exceeded"
}"""


# ---- Parsed karrio output --------------------------------------------------

ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_freight",
        "carrier_name": "dhl_freight",
        "tracking_number": "DHLF-2026-000001",
        "shipment_identifier": "DHLF-2026-000001",
        # ``lib.to_dict`` strips empty ``label`` → empty ``docs`` dict.
        "docs": {},
        "meta": {
            "carrier_tracking_link": gateway.settings.tracking_url.format("DHLF-2026-000001"),
            "tracking_numbers": ["DHLF-2026-000001"],
            "shipment_identifiers": [
                "DHLF-2026-000001",
                "00370000000000000001",
                "00370000000000000002",
            ],
            "license_plates": [
                "00370000000000000001",
                "00370000000000000002",
            ],
            "product_code": "dhl_freight_eurapid",
        },
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_freight",
            "carrier_name": "dhl_freight",
            "code": "400",
            "message": "Missing required field: totalWeight",
            "details": {
                "title": "Bad Request",
                "instance": "/freight/shipping/orders/v1/sendtransportinstruction",
                "invalidParams": [{"name": "totalWeight", "reason": "must be > 0"}],
            },
        }
    ],
]
