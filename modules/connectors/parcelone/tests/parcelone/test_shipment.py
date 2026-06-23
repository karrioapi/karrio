"""ParcelOne shipment tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.parcelone.units as provider_units
import karrio.sdk as karrio

from .fixture import gateway


class TestParcelOneShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_compact_phone(self):
        # ParcelOne rejects ShipmentContact.Phone > 15 chars (error 1014). The
        # connector must send the space-free form capped at 15 characters.
        self.assertEqual(provider_units.compact_phone("+33 1 42 00 00 00"), "+33142000000")
        self.assertEqual(provider_units.compact_phone("+49 30 1234560"), "+49301234560")
        self.assertEqual(len(provider_units.compact_phone("+1 234 567 890 1234")), 15)
        self.assertIsNone(provider_units.compact_phone(None))
        self.assertEqual(provider_units.compact_phone(""), "")

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        serialized = request.serialize()

        self.assertEqual(len(serialized), 1)
        self.assertDictEqual(serialized[0], ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)

        self.assertDictEqual(request.serialize(), ShipmentCancelRequestJSON)

    def test_create_shipment(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shippingapi/v1/shipment",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shippingapi/v1/shipment/trackingid/123456789012",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseJSON
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_shipment_error_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentErrorResponseJSON
            parsed_response = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentErrorResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponseJSON
            parsed_response = karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedCancelShipmentResponse)

    def test_create_shipment_request_with_insurance(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithInsurancePayload))
        self.assertDictEqual(request.serialize()[0], ShipmentWithInsuranceRequestJSON)

    def test_create_shipment_request_with_bulky_goods(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithBulkyGoodsPayload))
        self.assertDictEqual(request.serialize()[0], ShipmentWithBulkyGoodsRequestJSON)

    def test_create_shipment_request_with_return_label(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithReturnLabelPayload))
        self.assertDictEqual(request.serialize()[0], ShipmentWithReturnLabelRequestJSON)

    def test_create_shipment_request_zpl_alias_emits_zpl203(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithZPLPayload))
        self.assertDictEqual(request.serialize()[0], ShipmentWithZPLRequestJSON)

    def test_create_shipment_request_png_falls_back_to_pdf(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithPNGPayload))
        self.assertDictEqual(request.serialize()[0], ShipmentWithPNGRequestJSON)

    def test_create_intl_shipment_merchandise_item_category_5(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlMerchandisePayload))
        self.assertDictEqual(request.serialize()[0], IntlMerchandiseRequestJSON)

    def test_create_intl_shipment_documents_item_category_2(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlDocumentsPayload))
        self.assertDictEqual(request.serialize()[0], IntlDocumentsRequestJSON)

    def test_create_intl_return_shipment_item_category_4(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlReturnPayload))
        self.assertDictEqual(request.serialize()[0], IntlReturnRequestJSON)

    def test_create_intl_shipment_lb_commodity_weight_converted_to_kg(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlLBWeightPayload))
        self.assertDictEqual(request.serialize()[0], IntlLBWeightRequestJSON)

    def test_create_intl_shipment_kg_commodity_weight_unchanged(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlKGWeightPayload))
        self.assertDictEqual(request.serialize()[0], IntlKGWeightRequestJSON)

    def test_create_intl_shipment_emits_additional_info_passthrough(self):
        """AdditionalInfo metadata passthrough + ConsignerCustomsID. See SPECS.md."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**IntlEANPayload))
        self.assertDictEqual(request.serialize()[0], IntlEANRequestJSON)

    def test_create_multi_parcel_request(self):
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**MultiParcelPayload))
        self.assertListEqual(request.serialize(), MultiParcelRequestJSON)

    def test_create_multi_parcel_request_truncates_long_shipment_ref(self):
        """25-char reference truncates to 17 chars + ``-<index>`` so total ≤ 20."""
        request = gateway.mapper.create_shipment_request(
            models.ShipmentRequest(**{**MultiParcelPayload, "reference": "A" * 25})
        )
        refs = [entry["ShippingData"]["ShipmentRef"] for entry in request.serialize()]
        self.assertListEqual(refs, ["AAAAAAAAAAAAAAAAA-1", "AAAAAAAAAAAAAAAAA-2"])

    def test_create_single_parcel_request_truncates_long_shipment_ref(self):
        request = gateway.mapper.create_shipment_request(
            models.ShipmentRequest(**{**_BaseShipmentFields, "service": "parcelone_pa1_eco", "reference": "B" * 25})
        )
        self.assertEqual(request.serialize()[0]["ShippingData"]["ShipmentRef"], "B" * 20)

    def test_create_return_shipment_request(self):
        """Non-UPS return → SRO service + ``ReturnShipmentIndicator=0``.

        ReturnShipmentIndicator is UPS-exclusive (Mark Friebus, 2026-06); for
        non-UPS CEPs the SRO service alone drives the return, so the indicator
        stays 0. Full-body assertion proves both at once.
        """
        request = gateway.mapper.create_return_shipment_request(models.ShipmentRequest(**ReturnShipmentPayload))
        self.assertListEqual(request.serialize(), ReturnShipmentRequestJSON)

    def test_ups_return_uses_indicator_not_sro(self):
        """UPS return → ReturnShipmentIndicator (default 9), NO SRO service."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**UPSReturnPayload))
        sd = request.serialize()[0]["ShippingData"]
        self.assertEqual(sd["ReturnShipmentIndicator"], 9)
        self.assertEqual(sd["Packages"][0].get("Services"), None)

    def test_ups_return_indicator_custom_value(self):
        """``options.parcelone_return_indicator`` selects the UPS return type."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**UPSReturnIndicator2Payload))
        sd = request.serialize()[0]["ShippingData"]
        self.assertEqual(sd["ReturnShipmentIndicator"], 2)

    def test_ups_return_sets_package_remarks(self):
        """UPS returns need a goods description in Package.Remarks (UPS-9120201).

        Defaults to "Goods" when no parcel content/description is given (Mark
        Friebus, 2026-06). Non-UPS returns must not set Remarks.
        """
        ups = gateway.mapper.create_shipment_request(models.ShipmentRequest(**UPSReturnPayload))
        self.assertEqual(ups.serialize()[0]["ShippingData"]["Packages"][0]["Remarks"], "Goods")
        non_ups = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ReturnShipmentPayload))
        self.assertIsNone(non_ups.serialize()[0]["ShippingData"]["Packages"][0].get("Remarks"))

    def test_locker_shipment_sets_branch_id(self):
        """``options.parcelone_branch_id`` → ``ShipToData.BranchID`` (PUDO/locker)."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**LockerShipmentPayload))
        sd = request.serialize()[0]["ShippingData"]
        self.assertEqual(sd["ShipToData"]["BranchID"], "0481234567")

    def test_mfr_locker_shipment_sets_branch_id(self):
        """MFR (Mondial Relay) locker shipment → CEPID=MFR + ShipToData.BranchID."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**MFRLockerPayload))
        sd = request.serialize()[0]["ShippingData"]
        self.assertEqual(sd["CEPID"], "MFR")
        self.assertEqual(sd["ShipToData"]["BranchID"], "FR-12345")

    def test_create_shipment_request_with_cod(self):
        """``options.parcelone_cod`` → ServiceID="COD" with amount/currency."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**CODShipmentPayload))
        services = request.serialize()[0]["ShippingData"]["Packages"][0]["Services"]
        self.assertEqual(
            services,
            [{"ServiceID": "COD", "Value": {"Currency": "EUR", "Value": "49.9"}}],
        )

    def test_create_shipment_request_with_return_address_only(self):
        """``return_address`` alone must NOT attach SRL (paid vendor service).

        SRL is added only when ``options.parcelone_return_label=True`` —
        see ``test_create_shipment_request_with_return_label`` for the
        positive case.
        """
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentWithReturnAddressOnlyPayload))
        self.assertListEqual(request.serialize(), ShipmentWithReturnAddressOnlyRequestJSON)

    def test_create_shipment_request_pa1_plusz_no_auto_lmc(self):
        """PA1 plusZ must NOT auto-attach ServiceID="LMC" — ParcelOne advised
        against LMC for Shipping 2.0 (Mark Friebus, 2026-06). The last-mile
        tracking number arrives natively in PackageResults[].TrackingID."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentPA1PlusZPayload))
        self.assertListEqual(request.serialize(), ShipmentPA1PlusZRequestJSON)

    def test_create_shipment_request_mfr_24r_auto_lbl(self):
        """Non-PA1 CEP whose profile lists LBL → LBL auto-attached so the
        recipient gets the carrier-branded label."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentMFR24RPayload))
        self.assertListEqual(request.serialize(), ShipmentMFR24RRequestJSON)

    def test_create_shipment_request_consigner_override(self):
        """``options.parcelone_consigner_id`` overrides ``Settings.consigner_id``."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentConsignerOverridePayload))
        self.assertListEqual(request.serialize(), ShipmentConsignerOverrideRequestJSON)

    def test_create_shipment_request_mandator_override(self):
        """``options.parcelone_mandator_id`` overrides ``Settings.mandator_id`` —
        lets a shipping method point at a non-default mandator without
        spinning up a parallel connection."""
        request = gateway.mapper.create_shipment_request(models.ShipmentRequest(**ShipmentMandatorOverridePayload))
        self.assertListEqual(request.serialize(), ShipmentMandatorOverrideRequestJSON)

    def test_parse_shipment_response_with_lmc(self):
        """``PackageResults[].TrackingID`` is the customer-visible primary;
        the ParcelOne ``ActionResult.TrackingID`` is kept on the shipment for
        support reference under ``meta.parcelOne*``.
        """
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = LMCShipmentResponseJSON
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed), ParsedLMCShipmentResponse)

    def test_parse_srl_response_surfaces_return_label_in_extra_documents(self):
        """SRL (outbound + return) flow: the outbound label rides on
        ``docs.label`` (from ``PackageResults[].Label``) and the return label
        rides on ``docs.extra_documents`` (from ``DocumentsResults[]``).
        Without this, ParcelOne charges JTL for an SRL the merchant can never
        print — flagged on the 2026-05-22 sync with Christian."""
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = SRLShipmentResponseJSON
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed), ParsedSRLShipmentResponse)

    def test_parse_sro_response_promotes_return_label_to_docs_label(self):
        """SRO (return-only) flow: ``PackageResults[].Label`` is null and the
        return label is the only artefact — promote it to ``docs.label`` so
        callers without ``extra_documents`` support still get a usable label.
        Document IDs are mirrored onto meta so JTL can correlate against the
        ParcelOne portal."""
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = SROShipmentResponseJSON
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed), ParsedSROShipmentResponse)

    def test_parse_international_response_surfaces_customs_documents(self):
        """Non-EU shipments carry CN22 / commercial-invoice paperwork in
        ``InternationalDocumentsResults`` — surface them via extra_documents
        so the shipping app can print them alongside the label."""
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = InternationalShipmentResponseJSON
            parsed = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()

        self.assertListEqual(lib.to_dict(parsed), ParsedInternationalShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "email": "shipper@test.com",
        "phone_number": "+49301234567",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
        "email": "recipient@test.com",
        "phone_number": "+498912345678",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
            "length": 30.0,
            "width": 20.0,
            "height": 15.0,
            "dimension_unit": "CM",
        }
    ],
    "service": "parcelone_dhl_paket",
}

ShipmentCancelPayload = {
    "shipment_identifier": "123456789012",
}

ShipmentRequestJSON = {
    "ShippingData": {
        "CEPID": "DHL",
        "ConsignerID": "TEST_CONSIGNER",
        "LabelFormat": {
            "Orientation": 0,
            "Size": "A6",
            "Type": "PDF",
        },
        "MandatorID": "TEST_MANDATOR",
        "Packages": [
            {
                "PackageDimensions": {
                    "Height": "15.0",
                    "Length": "30.0",
                    "Width": "20.0",
                },
                "PackageRef": "1",
                "PackageWeight": {
                    "Unit": "kg",
                    "Value": "5.0",
                },
            }
        ],
        "PrintDocuments": 0,
        "PrintLabel": 1,
        "ProductID": "101",
        "ReturnShipmentIndicator": 0,
        "ShipFromData": {
            "Name1": "Test Shipper",
            "ShipmentAddress": {
                "City": "Berlin",
                "Country": "DE",
                "PostalCode": "10115",
                "Street": "123 Teststrasse",
                "Streetno": "123",
            },
            "ShipmentContact": {
                "Email": "shipper@test.com",
                "Phone": "+49301234567",
            },
        },
        "ShipToData": {
            "Name1": "Test Recipient",
            "PrivateAddressIndicator": 0,
            "ShipmentAddress": {
                "City": "Munich",
                "Country": "DE",
                "PostalCode": "80331",
                "Street": "456 Empfangerweg",
                "Streetno": "456",
            },
            "ShipmentContact": {
                "AttentionName": "Test Recipient",
                "Email": "recipient@test.com",
                "Phone": "+498912345678",
            },
        },
        "Software": "JTL-Shipping",
    }
}

ShipmentCancelRequestJSON = {
    "ref_field": "trackingid",
    "ref_value": "123456789012",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {
            "label": "JVBERi0xLjMKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PAo+PgovTWVkaWFCb3ggWyAwIDAgNTk1IDg0MiBdCi9QYXJlbnQgMSAwIFIKPj4KZW5kb2JqCnhyZWYKMCA1CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMDc0IDAwMDAwIG4gCjAwMDAwMDAxMTQgMDAwMDAgbiAKMDAwMDAwMDE2MyAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDUKL1Jvb3QgMyAwIFIKL0luZm8gMiAwIFIKPj4Kc3RhcnR4cmVmCjI1MwolJUVPRgo="
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://parcel.one/tracking?trackno=123456789012",
            "currency": "EUR",
            "parcelOneShipmentID": "SHIP001",
            "parcelOneTrackingID": "123456789012",
            "shipment_id": "SHIP001",
            "total_charge": 5.99,
            "tracking_numbers": ["123456789012"],
        },
        "shipment_identifier": "SHIP001",
        "tracking_number": "123456789012",
    },
    [],
]

ParsedShipmentErrorResponse = [
    None,
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "code": "E001",
            "details": {
                "shipment_id": "SHIP001",
                "tracking_id": "123456789012",
            },
            "message": "Invalid postal code",
        }
    ],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "SHIP001",
            "TrackingID": "123456789012"
        },
        "PackageResults": [
            {
                "PackageID": "PKG001",
                "TrackingID": "123456789012",
                "Label": "JVBERi0xLjMKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PAo+PgovTWVkaWFCb3ggWyAwIDAgNTk1IDg0MiBdCi9QYXJlbnQgMSAwIFIKPj4KZW5kb2JqCnhyZWYKMCA1CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxNSAwMDAwMCBuIAowMDAwMDAwMDc0IDAwMDAwIG4gCjAwMDAwMDAxMTQgMDAwMDAgbiAKMDAwMDAwMDE2MyAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDUKL1Jvb3QgMyAwIFIKL0luZm8gMiAwIFIKPj4Kc3RhcnR4cmVmCjI1MwolJUVPRgo="
            }
        ],
        "TotalCharges": {
            "Value": "5.99",
            "Currency": "EUR"
        },
        "LabelsAvailable": 1
    }
}"""

ShipmentErrorResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 0,
            "ShipmentID": "SHIP001",
            "TrackingID": "123456789012",
            "Errors": [
                {
                    "ErrorNo": "E001",
                    "Message": "Invalid postal code"
                }
            ]
        }
    }
}"""

ShipmentCancelResponseJSON = """{
    "success": 1,
    "results": {
        "Success": 1,
        "ShipmentID": "SHIP001",
        "TrackingID": "123456789012"
    }
}"""

# --- Option-specific fixtures ---

_BaseShipmentFields = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "email": "shipper@test.com",
        "phone_number": "+49301234567",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
        "email": "recipient@test.com",
        "phone_number": "+498912345678",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "KG",
        }
    ],
}

_BaseRequestShippingData = {
    "CEPID": "PA1",
    "ConsignerID": "TEST_CONSIGNER",
    "LabelFormat": {"Orientation": 0, "Size": "A6", "Type": "PDF"},
    "MandatorID": "TEST_MANDATOR",
    "Packages": [
        {
            "PackageRef": "1",
            "PackageWeight": {"Unit": "kg", "Value": "5.0"},
        }
    ],
    "PrintDocuments": 0,
    "PrintLabel": 1,
    "ReturnShipmentIndicator": 0,
    "ShipFromData": {
        "Name1": "Test Shipper",
        "ShipmentAddress": {
            "City": "Berlin",
            "Country": "DE",
            "PostalCode": "10115",
            "Street": "123 Teststrasse",
            "Streetno": "123",
        },
        "ShipmentContact": {
            "Email": "shipper@test.com",
            "Phone": "+49301234567",
        },
    },
    "ShipToData": {
        "Name1": "Test Recipient",
        "PrivateAddressIndicator": 0,
        "ShipmentAddress": {
            "City": "Munich",
            "Country": "DE",
            "PostalCode": "80331",
            "Street": "456 Empfangerweg",
            "Streetno": "456",
        },
        "ShipmentContact": {
            # AttentionName mirrors Name1 even when the recipient is a person —
            # ParcelOne expects it for label rendering (Mark Friebus, 2026-06).
            "AttentionName": "Test Recipient",
            "Email": "recipient@test.com",
            "Phone": "+498912345678",
        },
    },
    "Software": "JTL-Shipping",
}

ShipmentWithInsurancePayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_plus",
    "options": {"insurance": 200},
}

ShipmentWithInsuranceRequestJSON = {
    "ShippingData": {
        **_BaseRequestShippingData,
        "ProductID": "plus",
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "5.0"},
                "Services": [
                    {
                        "ServiceID": "EI",
                        "Value": {"Currency": "EUR", "Value": "200.0"},
                    }
                ],
            }
        ],
    }
}

ShipmentWithBulkyGoodsPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_plus",
    "options": {"parcelone_bulky_goods": True},
}

ShipmentWithBulkyGoodsRequestJSON = {
    "ShippingData": {
        **_BaseRequestShippingData,
        "ProductID": "plus",
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "5.0"},
                "Services": [{"ServiceID": "BSC"}],
            }
        ],
    }
}

ShipmentWithReturnLabelPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "options": {"parcelone_return_label": True},
}

ShipmentWithReturnLabelRequestJSON = {
    "ShippingData": {
        **_BaseRequestShippingData,
        "ProductID": "eco",
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "5.0"},
                "Services": [{"ServiceID": "SRL"}],
            }
        ],
    }
}

ShipmentWithZPLPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_plus",
    "label_type": "ZPL",
}

ShipmentWithZPLRequestJSON = {
    "ShippingData": {
        **_BaseRequestShippingData,
        "ProductID": "plus",
        "LabelFormat": {"Orientation": 0, "Size": "A6", "Type": "ZPL203"},
    }
}

ShipmentWithPNGPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_plus",
    "label_type": "PNG",
}

ShipmentWithPNGRequestJSON = {
    "ShippingData": {
        **_BaseRequestShippingData,
        "ProductID": "plus",
        "LabelFormat": {"Orientation": 0, "Size": "A6", "Type": "PDF"},
    }
}

_IntlShipmentFields = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
        "email": "shipper@test.com",
        "phone_number": "+49301234567",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "123 Test Street",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
        "email": "recipient@test.com",
        "phone_number": "+441234567890",
    },
    "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
    "service": "parcelone_dhl_paket",
    "customs": {
        "invoice": "INV-001",
        "commodities": [
            {
                "description": "Test Item",
                "quantity": 1,
                "value_amount": 50.0,
                "weight": 1.0,
                "origin_country": "DE",
            }
        ],
    },
}

_IntlBaseRequestShippingData = {
    "CEPID": "DHL",
    "ConsignerID": "TEST_CONSIGNER",
    "DocumentFormat": {"Orientation": 0, "Type": "PDF"},
    "LabelFormat": {"Orientation": 0, "Size": "A6", "Type": "PDF"},
    "MandatorID": "TEST_MANDATOR",
    "PrintDocuments": 1,
    "PrintLabel": 1,
    "ReturnShipmentIndicator": 0,
    "ProductID": "101",
    "ShipFromData": {
        "Name1": "Test Shipper",
        "ShipmentAddress": {
            "City": "Berlin",
            "Country": "DE",
            "PostalCode": "10115",
            "Street": "123 Teststrasse",
            "Streetno": "123",
        },
        "ShipmentContact": {
            "Email": "shipper@test.com",
            "Phone": "+49301234567",
        },
    },
    "ShipToData": {
        "Name1": "Test Recipient",
        "PrivateAddressIndicator": 0,
        "ShipmentAddress": {
            "City": "London",
            "Country": "GB",
            "PostalCode": "SW1A 1AA",
            "Street": "123 Test Street",
            "Streetno": "123",
        },
        "ShipmentContact": {
            "AttentionName": "Test Recipient",
            "Email": "recipient@test.com",
            "Phone": "+441234567890",
        },
    },
    "Software": "JTL-Shipping",
}


def _IntlPackagesWithCategory(category):
    return [
        {
            "PackageRef": "1",
            "PackageWeight": {"Unit": "kg", "Value": "1.0"},
            "IntDocData": {
                "Invoice": 1,
                "InvoiceNo": "INV-001",
                "PrintInternationalDocuments": 1,
                "InternationalDocumentFormat": {
                    "Orientation": 0,
                    "Size": "CN23",
                    "Type": "PDF",
                },
                "ItemCategory": category,
                # DHL Weltpaket requires these aggregate totals — without
                # them the carrier rejects with 1099 CustomsDetails::
                # getPostalCharges() returned null.
                "Postage": 0.0,
                "TotalValue": 50.0,
                "Currency": "EUR",
                "TotalWeightkg": 1.0,
                "CustomDetails": [
                    {
                        "Contents": "Test Item",
                        "Quantity": 1,
                        "ItemValuePerItem": 50.0,
                        "NetWeightPerItem": 1.0,
                        "Origin": "DE",
                    }
                ],
            },
        }
    ]


IntlMerchandisePayload = {
    **_IntlShipmentFields,
    "customs": {**_IntlShipmentFields["customs"], "content_type": "merchandise"},
}

IntlMerchandiseRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "Packages": _IntlPackagesWithCategory(5),
    }
}

IntlDocumentsPayload = {
    **_IntlShipmentFields,
    "customs": {**_IntlShipmentFields["customs"], "content_type": "documents"},
}

IntlDocumentsRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "Packages": _IntlPackagesWithCategory(2),
    }
}

IntlReturnPayload = {
    **_IntlShipmentFields,
    "customs": {**_IntlShipmentFields["customs"], "content_type": "merchandise"},
    "options": {"is_return": True},
}

IntlReturnRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "ReturnShipmentIndicator": 0,
        "Packages": [
            {
                **_IntlPackagesWithCategory(4)[0],
                "Services": [{"ServiceID": "SRO"}],
            }
        ],
    }
}

# 2.2046 LB ≈ 1.0 KG — wire must show 1.0
IntlLBWeightPayload = {
    **_IntlShipmentFields,
    "customs": {
        "invoice": "INV-002",
        "content_type": "merchandise",
        "commodities": [
            {
                "description": "Heavy Item",
                "quantity": 1,
                "value_amount": 100.0,
                "weight": 2.2046,
                "weight_unit": "LB",
                "origin_country": "DE",
            }
        ],
    },
}

IntlLBWeightRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "1.0"},
                "IntDocData": {
                    "Invoice": 1,
                    "InvoiceNo": "INV-002",
                    "PrintInternationalDocuments": 1,
                    "InternationalDocumentFormat": {
                        "Orientation": 0,
                        "Size": "CN23",
                        "Type": "PDF",
                    },
                    "ItemCategory": 5,
                    "Postage": 0.0,
                    "TotalValue": 100.0,
                    "Currency": "EUR",
                    "TotalWeightkg": 1.0,
                    "CustomDetails": [
                        {
                            "Contents": "Heavy Item",
                            "Quantity": 1,
                            "ItemValuePerItem": 100.0,
                            "NetWeightPerItem": 1.0,
                            "Origin": "DE",
                        }
                    ],
                },
            }
        ],
    }
}

IntlKGWeightPayload = {
    **_IntlShipmentFields,
    "customs": {
        "invoice": "INV-003",
        "content_type": "merchandise",
        "commodities": [
            {
                "description": "KG Item",
                "quantity": 2,
                "value_amount": 75.0,
                "weight": 0.5,
                "weight_unit": "KG",
                "origin_country": "DE",
            }
        ],
    },
}

IntlKGWeightRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "1.0"},
                "IntDocData": {
                    "Invoice": 1,
                    "InvoiceNo": "INV-003",
                    "PrintInternationalDocuments": 1,
                    "InternationalDocumentFormat": {
                        "Orientation": 0,
                        "Size": "CN23",
                        "Type": "PDF",
                    },
                    "ItemCategory": 5,
                    "Postage": 0.0,
                    # 2 items × 75.0 = 150.0
                    "TotalValue": 150.0,
                    "Currency": "EUR",
                    "TotalWeightkg": 1.0,
                    "CustomDetails": [
                        {
                            "Contents": "KG Item",
                            "Quantity": 2,
                            "ItemValuePerItem": 75.0,
                            "NetWeightPerItem": 0.5,
                            "Origin": "DE",
                        }
                    ],
                },
            }
        ],
    }
}

# AdditionalInfo passthrough + ConsignerCustomsID coverage (see SPECS.md).
# Item 1: EAN alias + Barcode_* + Document0 + product_url→urlPath.
# Item 2: GTIN alias + Barcode_UPC_1. Item 3: no metadata → AdditionalInfo omitted.
IntlEANPayload = {
    **_IntlShipmentFields,
    "customs": {
        "invoice": "INV-EAN",
        "content_type": "merchandise",
        "duty": {"paid_by": "sender", "account_number": "DE284968554884383"},
        "commodities": [
            {
                "description": "Tart cherry juice concentrate",
                "quantity": 2,
                "value_amount": 7.83,
                "weight": 1.234,
                "weight_unit": "KG",
                "origin_country": "US",
                "hs_code": "2009899690",
                "product_url": "spielzeug/kartenspiele/tart-cherry",
                "metadata": {
                    "ean": "00850029592327",
                    "Barcode_EAN_13": "00850029592327",
                    "Document0": '{"type": "invoice", "ref": "INV-1"}',
                },
            },
            {
                "description": "Gummies",
                "quantity": 2,
                "value_amount": 17.19,
                "weight": 0.24,
                "weight_unit": "KG",
                "origin_country": "US",
                "hs_code": "17049065",
                "metadata": {"GTIN": "4262491030133", "Barcode_UPC_1": "012345678905"},
            },
            {
                # No metadata — verifies AdditionalInfo is omitted (not [None]).
                "description": "Unboxed sample",
                "quantity": 1,
                "value_amount": 1.0,
                "weight": 0.1,
                "weight_unit": "KG",
                "origin_country": "US",
            },
        ],
    },
}

IntlEANRequestJSON = {
    "ShippingData": {
        **_IntlBaseRequestShippingData,
        "Packages": [
            {
                "PackageRef": "1",
                "PackageWeight": {"Unit": "kg", "Value": "1.0"},
                "IntDocData": {
                    "Invoice": 1,
                    "InvoiceNo": "INV-EAN",
                    "ConsignerCustomsID": "DE284968554884383",
                    "PrintInternationalDocuments": 1,
                    "InternationalDocumentFormat": {
                        "Orientation": 0,
                        "Size": "CN23",
                        "Type": "PDF",
                    },
                    "ItemCategory": 5,
                    "Postage": 0.0,
                    # (7.83 × 2) + (17.19 × 2) + (1.0 × 1) = 51.04
                    "TotalValue": 51.04,
                    "Currency": "EUR",
                    "TotalWeightkg": 1.0,
                    "CustomDetails": [
                        {
                            "Contents": "Tart cherry juice concentrate",
                            "Quantity": 2,
                            "ItemValuePerItem": 7.83,
                            # lib.units.Weight rounds KG to 2 decimal places.
                            "NetWeightPerItem": 1.23,
                            "Origin": "US",
                            "TariffNumber": "2009899690",
                            "AdditionalInfo": [
                                {"Key": "EAN", "Value": "00850029592327"},
                                {"Key": "Barcode_EAN_13", "Value": "00850029592327"},
                                {"Key": "Document0", "Value": '{"type": "invoice", "ref": "INV-1"}'},
                                {"Key": "urlPath", "Value": "spielzeug/kartenspiele/tart-cherry"},
                            ],
                        },
                        {
                            "Contents": "Gummies",
                            "Quantity": 2,
                            "ItemValuePerItem": 17.19,
                            "NetWeightPerItem": 0.24,
                            "Origin": "US",
                            "TariffNumber": "17049065",
                            "AdditionalInfo": [
                                {"Key": "EAN", "Value": "4262491030133"},
                                {"Key": "Barcode_UPC_1", "Value": "012345678905"},
                            ],
                        },
                        {
                            "Contents": "Unboxed sample",
                            "Quantity": 1,
                            "ItemValuePerItem": 1.0,
                            "NetWeightPerItem": 0.1,
                            "Origin": "US",
                        },
                    ],
                },
            }
        ],
    }
}

# --- Multi-parcel (Pattern B) fixtures ---

MultiParcelPayload = {
    "shipper": {
        "company_name": "Test Shipper",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
    "recipient": {
        "person_name": "Test Recipient",
        "address_line1": "Empfangerweg 456",
        "city": "Munich",
        "postal_code": "80331",
        "country_code": "DE",
    },
    "parcels": [
        {"weight": 2.0, "weight_unit": "KG"},
        {"weight": 3.0, "weight_unit": "KG"},
    ],
    "service": "parcelone_pa1_eco",
    "reference": "REF",
}

# --- Return shipment fixtures ---

ReturnShipmentPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
}

# UPS returns use ReturnShipmentIndicator (UPS-exclusive), not the SRO service.
UPSReturnPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_ups_11",
    "options": {"parcelone_return_only": True},
}
UPSReturnIndicator2Payload = {
    **_BaseShipmentFields,
    "service": "parcelone_ups_11",
    "options": {"parcelone_return_only": True, "parcelone_return_indicator": 2},
}
# Locker / parcel-shop delivery — the PUDO id rides ShipToData.BranchID.
LockerShipmentPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "options": {"parcelone_branch_id": "0481234567"},
}
# MFR (Mondial Relay) point-relais locker shipment via ShipToData.BranchID.
MFRLockerPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_mfr_24r",
    "options": {"parcelone_branch_id": "FR-12345"},
}
CODShipmentPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "options": {"parcelone_cod": 49.90, "parcelone_cod_currency": "EUR"},
}

ReturnShipmentRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "ProductID": "eco",
            "ReturnShipmentIndicator": 0,
            "Packages": [
                {
                    "PackageRef": "1",
                    "PackageWeight": {"Unit": "kg", "Value": "5.0"},
                    "Services": [{"ServiceID": "SRO"}],
                }
            ],
        }
    }
]

# Sanity: an outbound shipment that only carries a return_address (no
# parcelone_return_label option). Must NOT add SRL or SRO — SRL is a paid
# service and the unified return_address field is used by many flows that
# do not opt into the ParcelOne return label.
ShipmentWithReturnAddressOnlyPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "return_address": {
        "person_name": "Returns Desk",
        "address_line1": "Teststrasse 123",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
}

ShipmentWithReturnAddressOnlyRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "ProductID": "eco",
        }
    }
]

# PA1 plusZ — the static profile lists LMC for this product, but we no
# longer auto-attach it (ParcelOne advised against LMC for Shipping 2.0).
# The request carries no Services array; the last-mile tracking number is
# returned natively in PackageResults[].TrackingID.
ShipmentPA1PlusZPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_plusZ",
}

ShipmentPA1PlusZRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "ProductID": "plusZ",
        }
    }
]

# Mondial Relay 24R — non-PA1 CEP that lists LBL in its profile, so
# force_carrier_label (default True) attaches ServiceID="LBL" so the
# recipient sees the Mondial Relay-branded label.
ShipmentMFR24RPayload = {
    **_BaseShipmentFields,
    "service": "parcelone_mfr_24r",
}

ShipmentMFR24RRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "CEPID": "MFR",
            "ProductID": "24R",
            "Packages": [
                {
                    "PackageRef": "1",
                    "PackageWeight": {"Unit": "kg", "Value": "5.0"},
                    "Services": [{"ServiceID": "LBL"}],
                }
            ],
        }
    }
]

# Per-shipment consigner_id override.
ShipmentConsignerOverridePayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "options": {"parcelone_consigner_id": "ALT_CONSIGNER_42"},
}

ShipmentConsignerOverrideRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "ConsignerID": "ALT_CONSIGNER_42",
            "ProductID": "eco",
        }
    }
]

# Per-shipment mandator_id override.
ShipmentMandatorOverridePayload = {
    **_BaseShipmentFields,
    "service": "parcelone_pa1_eco",
    "options": {"parcelone_mandator_id": "ALT_MANDATOR_99"},
}

ShipmentMandatorOverrideRequestJSON = [
    {
        "ShippingData": {
            **_BaseRequestShippingData,
            "MandatorID": "ALT_MANDATOR_99",
            "ProductID": "eco",
        }
    }
]

# Response where ActionResult.TrackingID is the ParcelOne number and
# PackageResults[0].TrackingID is the LMC/carrier number — the documented
# behaviour when service LMC (or LBL) is active. Used to verify that the
# parser selects the package-level ID as the customer-visible primary.
LMCShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "SHIP001",
            "ShipmentRef": "REF-XYZ",
            "TrackingID": "PA000001"
        },
        "PackageResults": [
            {
                "PackageID": "PKG001",
                "TrackingID": "LMC9999",
                "Label": "JVBER"
            }
        ],
        "TotalCharges": {"Value": "5.99", "Currency": "EUR"},
        "LabelsAvailable": 1
    }
}"""

ParsedLMCShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {"label": "JVBER"},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://parcel.one/tracking?trackno=PA000001",
            "currency": "EUR",
            "parcelOneShipmentID": "SHIP001",
            "parcelOneShipmentRef": "REF-XYZ",
            "parcelOneTrackingID": "PA000001",
            "shipment_id": "SHIP001",
            "shipment_ref": "REF-XYZ",
            "total_charge": 5.99,
            "tracking_numbers": ["LMC9999"],
        },
        "shipment_identifier": "SHIP001",
        "tracking_number": "LMC9999",
    },
    [],
]

# Multi-parcel: 2 parcels in one shipment → 2 separate ShipIT payloads,
# each carrying ShipmentRef "REF-1" / "REF-2".
MultiParcelRequestJSON = [
    {
        "ShippingData": {
            **{k: v for k, v in _BaseRequestShippingData.items() if k != "ShipFromData" and k != "ShipToData"},
            "ProductID": "eco",
            "Packages": [{"PackageRef": "1", "PackageWeight": {"Unit": "kg", "Value": "2.0"}}],
            "ShipFromData": {
                "Name1": "Test Shipper",
                "ShipmentAddress": {
                    "City": "Berlin",
                    "Country": "DE",
                    "PostalCode": "10115",
                    "Street": "123 Teststrasse",
                    "Streetno": "123",
                },
                "ShipmentContact": {},
            },
            "ShipToData": {
                "Name1": "Test Recipient",
                "PrivateAddressIndicator": 0,
                "Reference": "REF-1",
                "ShipmentAddress": {
                    "City": "Munich",
                    "Country": "DE",
                    "PostalCode": "80331",
                    "Street": "456 Empfangerweg",
                    "Streetno": "456",
                },
                "ShipmentContact": {"AttentionName": "Test Recipient"},
            },
            "ShipmentRef": "REF-1",
        }
    },
    {
        "ShippingData": {
            **{k: v for k, v in _BaseRequestShippingData.items() if k != "ShipFromData" and k != "ShipToData"},
            "ProductID": "eco",
            "Packages": [{"PackageRef": "2", "PackageWeight": {"Unit": "kg", "Value": "3.0"}}],
            "ShipFromData": {
                "Name1": "Test Shipper",
                "ShipmentAddress": {
                    "City": "Berlin",
                    "Country": "DE",
                    "PostalCode": "10115",
                    "Street": "123 Teststrasse",
                    "Streetno": "123",
                },
                "ShipmentContact": {},
            },
            "ShipToData": {
                "Name1": "Test Recipient",
                "PrivateAddressIndicator": 0,
                "Reference": "REF-2",
                "ShipmentAddress": {
                    "City": "Munich",
                    "Country": "DE",
                    "PostalCode": "80331",
                    "Street": "456 Empfangerweg",
                    "Streetno": "456",
                },
                "ShipmentContact": {"AttentionName": "Test Recipient"},
            },
            "ShipmentRef": "REF-2",
        }
    },
]

# SRL response (outbound + return label, EU shipment) — mirrors the vendor
# spec example "ResultSuccess - Parcel.One EU Shipment with ReturnLabel in
# DocumentResults". Outbound rides on PackageResults[].Label and the return
# label rides on DocumentsResults[].Document; the parser must surface both.
SRLShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "107443",
            "ShipmentRef": "CustRef 9998898",
            "TrackingID": "1234501074436"
        },
        "PackageResults": [
            {
                "ShipmentID": "107443",
                "PackageID": 1,
                "PackageRef": "123-AB",
                "TrackingID": "1234501074436",
                "DocType": "LABEL",
                "Format": {"Type": "PDF", "Size": "A6"},
                "Label": "OUTBOUND_LABEL_BASE64",
                "TrackingURL": "https://parcel.one/tracking?trackno=1234501074436&zip=14150"
            }
        ],
        "DocumentsResults": [
            {
                "ShipmentID": "107443",
                "PackageID": "",
                "TrackingID": "1234501074436",
                "DocType": "Retourelabel",
                "Format": {"Type": "PDF", "Size": "A6"},
                "Document": "RETURN_LABEL_BASE64",
                "DocumentID": "94902717593SE"
            }
        ],
        "LabelsAvailable": 1,
        "DocumentsAvailable": 1
    }
}"""

ParsedSRLShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {
            "label": "OUTBOUND_LABEL_BASE64",
            "extra_documents": [
                {
                    "category": "Retourelabel",
                    "format": "PDF",
                    "base64": "RETURN_LABEL_BASE64",
                }
            ],
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://parcel.one/tracking?trackno=1234501074436",
            "currency": "EUR",
            "parcelOneShipmentID": "107443",
            "parcelOneShipmentRef": "CustRef 9998898",
            "parcelOneTrackingID": "1234501074436",
            "return_document_ids": ["94902717593SE"],
            "shipment_id": "107443",
            "shipment_ref": "CustRef 9998898",
            "tracking_numbers": ["1234501074436"],
            "tracking_urls": ["https://parcel.one/tracking?trackno=1234501074436&zip=14150"],
        },
        "shipment_identifier": "107443",
        "tracking_number": "1234501074436",
    },
    [],
]

# SRO response (return-only) — PackageResults entry exists for tracking
# correlation but `Label` is null; the return label lives in
# DocumentsResults. Parser must promote the return document to docs.label.
SROShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "107500",
            "ShipmentRef": "RetourRef 1234",
            "TrackingID": "9876504107500"
        },
        "PackageResults": [
            {
                "ShipmentID": "107500",
                "PackageID": 1,
                "PackageRef": "RET-AB",
                "TrackingID": "9876504107500",
                "DocType": "LABEL",
                "Format": {"Type": "PDF", "Size": "A6"},
                "Label": null
            }
        ],
        "DocumentsResults": [
            {
                "ShipmentID": "107500",
                "PackageID": "",
                "TrackingID": "9876504107500",
                "DocType": "Retourelabel",
                "Format": {"Type": "PDF", "Size": "A6"},
                "Document": "SRO_RETURN_LABEL_BASE64",
                "DocumentID": "RETDOC-100"
            }
        ],
        "DocumentsAvailable": 1
    }
}"""

ParsedSROShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {
            "label": "SRO_RETURN_LABEL_BASE64",
            "extra_documents": [
                {
                    "category": "Retourelabel",
                    "format": "PDF",
                    "base64": "SRO_RETURN_LABEL_BASE64",
                }
            ],
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://parcel.one/tracking?trackno=9876504107500",
            "currency": "EUR",
            "parcelOneShipmentID": "107500",
            "parcelOneShipmentRef": "RetourRef 1234",
            "parcelOneTrackingID": "9876504107500",
            "return_document_ids": ["RETDOC-100"],
            "shipment_id": "107500",
            "shipment_ref": "RetourRef 1234",
            "tracking_numbers": ["9876504107500"],
        },
        "shipment_identifier": "107500",
        "tracking_number": "9876504107500",
    },
    [],
]

# International response — outbound rides on PackageResults as usual,
# customs paperwork (CN22, commercial invoice, …) rides on
# InternationalDocumentsResults. Same vendor-spec example, EU → non-EU.
InternationalShipmentResponseJSON = """{
    "success": 1,
    "results": {
        "ActionResult": {
            "Success": 1,
            "ShipmentID": "107435",
            "ShipmentRef": "CustRef 9998898",
            "TrackingID": "1234501074344"
        },
        "PackageResults": [
            {
                "ShipmentID": "107434",
                "PackageID": 1,
                "PackageRef": "123-AB",
                "TrackingID": "1234501074344",
                "DocType": "LABEL",
                "Format": {"Type": "PDF", "Size": "A6"},
                "Label": "INTL_OUTBOUND_LABEL_BASE64",
                "TrackingURL": "https://parcel.one/tracking?trackno=1234501074344&zip=14150"
            }
        ],
        "InternationalDocumentsResults": [
            {
                "ShipmentID": "107435",
                "PackageID": "1",
                "TrackingID": "1234501074344",
                "DocType": "CN22",
                "Document": "CN22_DOCUMENT_BASE64"
            }
        ],
        "LabelsAvailable": 1,
        "InternationalDocumentsAvailable": 1,
        "InternationalDocumentsNeeded": 1
    }
}"""

ParsedInternationalShipmentResponse = [
    {
        "carrier_id": "parcelone",
        "carrier_name": "parcelone",
        "docs": {
            "label": "INTL_OUTBOUND_LABEL_BASE64",
            "extra_documents": [
                {
                    "category": "CN22",
                    "format": "PDF",
                    "base64": "CN22_DOCUMENT_BASE64",
                }
            ],
        },
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://parcel.one/tracking?trackno=1234501074344",
            "currency": "EUR",
            "parcelOneShipmentID": "107435",
            "parcelOneShipmentRef": "CustRef 9998898",
            "parcelOneTrackingID": "1234501074344",
            "shipment_id": "107435",
            "shipment_ref": "CustRef 9998898",
            "tracking_numbers": ["1234501074344"],
            "tracking_urls": ["https://parcel.one/tracking?trackno=1234501074344&zip=14150"],
        },
        "shipment_identifier": "107435",
        "tracking_number": "1234501074344",
    },
    [],
]
