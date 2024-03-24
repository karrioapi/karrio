import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, LabelResponse as ManifestFile

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestCanadaPostManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)
        self.ManifestRequestWithIDs = models.ManifestRequest(**ManifestPayloadWithIDs)
        self.ManifestRequestWithShipments = models.ManifestRequest(
            **ManifestPayloadWithShipments
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [
                ManifestsResponse,
                ManifestResponse,
                ManifestResponse,
                ManifestFile,
                ManifestFile,
            ]
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            create, manifest1, manifest2, download1, download2 = mock.call_args_list
            self.assertEqual(
                create[1]["url"],
                f"{gateway.settings.server_url}/rs/2004381/2004381/manifest",
            )
            self.assertEqual(
                manifest1[1]["url"],
                f"https://XX/1111111111/222222222/manifest/444444444444",
            )
            self.assertEqual(
                manifest2[1]["url"],
                f"https://XX/1111111111/222222222/manifest/333333333333",
            )
            self.assertEqual(
                download1[1]["url"],
                f"https://ct.soa-gw.canadapost.ca/rs/artifact/6e93d53968881714/10005457526/0",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [
                ManifestsResponse,
                ManifestResponse,
                ManifestResponse,
                ManifestFile,
                ManifestFile,
            ]
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)

    def test_parse_manifest_response_from_identifiers(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [
                ShipmentResponse1,
                ShipmentResponse2,
                ManifestsResponse,
                ManifestResponse,
                ManifestResponse,
                ManifestFile,
                ManifestFile,
            ]
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequestWithIDs)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedManifestResponsWithIDs
            )

    def test_parse_manifest_response_from_shipments(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.side_effect = [
                ManifestsResponse,
                ManifestResponse,
                ManifestResponse,
                ManifestFile,
                ManifestFile,
            ]
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequestWithShipments)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedManifestResponseWithShipments
            )


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["545021584835957806", "1234567890123456"],
    "address": {
        "company_name": "my company",
        "person_name": "MajorShop",
        "address_line1": "1230 Tako RD.",
        "city": "Ottawa",
        "state_code": "ON",
        "postal_code": "K1A1A1",
        "country_code": "CA",
        "phone_number": "555 555 5555",
    },
    "options": {
        "group_ids": ["single-group"],
        "requested_shipping_point": "K1K4T3",
        "cpc_pickup_indicator": True,
    },
}

ManifestPayloadWithIDs = {
    "shipment_identifiers": ["545021584835957806", "1234567890123456"],
    "address": {
        "company_name": "my company",
        "person_name": "MajorShop",
        "address_line1": "1230 Tako RD.",
        "city": "Ottawa",
        "state_code": "ON",
        "postal_code": "K1A1A1",
        "country_code": "CA",
        "phone_number": "555 555 5555",
    },
    "options": {},
}

ManifestPayloadWithShipments = {
    "shipment_identifiers": ["545021584835957806", "1234567890123456"],
    "address": {
        "company_name": "my company",
        "person_name": "MajorShop",
        "address_line1": "1230 Tako RD.",
        "city": "Ottawa",
        "state_code": "ON",
        "postal_code": "K1A1A1",
        "country_code": "CA",
        "phone_number": "555 555 5555",
    },
    "options": {
        "shipments": [
            {
                "tracking_number": "545021584835957806",
                "meta": {"group_id": "group1"},
            },
            {
                "tracking_number": "1234567890123456",
                "meta": {"group_id": "group2"},
            },
        ]
    },
}


ParsedManifestResponse = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "doc": {"manifest": ANY},
        "meta": {
            "group_ids": ["single-group"],
            "links": [
                "https://XX/1111111111/222222222/manifest/444444444444",
                "https://XX/1111111111/222222222/manifest/333333333333",
            ],
        },
    },
    [],
]

ParsedManifestResponsWithIDs = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "doc": {"manifest": ANY},
        "meta": {
            "group_ids": ANY,
            "links": [
                "https://XX/1111111111/222222222/manifest/444444444444",
                "https://XX/1111111111/222222222/manifest/333333333333",
            ],
        },
    },
    [],
]

ParsedManifestResponseWithShipments = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "doc": {"manifest": ANY},
        "meta": {
            "group_ids": ANY,
            "links": [
                "https://XX/1111111111/222222222/manifest/444444444444",
                "https://XX/1111111111/222222222/manifest/333333333333",
            ],
        },
    },
    [],
]


ManifestRequest = """<transmit-set xmlns="http://www.canadapost.ca/ws/manifest-v8">
    <group-ids>
        <group-id>[GROUP_IDS]</group-id>
    </group-ids>
    <cpc-pickup-indicator>true</cpc-pickup-indicator>
    <requested-shipping-point>K1K4T3</requested-shipping-point>
    <detailed-manifests>true</detailed-manifests>
    <method-of-payment>Account</method-of-payment>
    <manifest-address>
        <manifest-company>my company</manifest-company>
        <manifest-name>MajorShop</manifest-name>
        <phone-number>555 555 5555</phone-number>
        <address-details>
            <address-line-1>1230 Tako RD.</address-line-1>
            <city>Ottawa</city>
            <prov-state>ON</prov-state>
            <country-code>CA</country-code>
            <postal-zip-code>K1A1A1</postal-zip-code>
        </address-details>
    </manifest-address>
</transmit-set>
"""

ManifestsResponse = """<manifests>
    <link rel="manifest" href="https://XX/1111111111/222222222/manifest/444444444444"
        media-type="application/vnd.cpc.manifest-v8+xml"></link>
    <link rel="manifest" href="https://XX/1111111111/222222222/manifest/333333333333"
        media-type="application/vnd.cpc.manifest-v8+xml"></link>
</manifests>
"""

ManifestResponse = """<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="http://www.canadapost.ca/ws/manifest-v8">
    <po-number>P123456789</po-number>
    <links>
        <link rel="self"
            href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/manifest/732071711235567991"
            media-type="application/vnd.cpc.manifest-v8+xml" />
        <link rel="details"
            href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/manifest/732071711235567991/details"
            media-type="application/vnd.cpc.manifest-v8+xml" />
        <link rel="manifestShipments"
            href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment?manifestId=732071711235567991"
            media-type="application/vnd.cpc.shipment-v8+xml" />
        <link rel="artifact"
            href="https://ct.soa-gw.canadapost.ca/rs/artifact/6e93d53968881714/10005457526/0"
            media-type="application/pdf" />
    </links>
</manifest>
"""

ShipmentResponse1 = """<shipment-details>
    <shipment-status>reconciled</shipment-status>
    <final-shipping-point>K1G1C0</final-shipping-point>
    <shipping-point-id>0015</shipping-point-id>
    <tracking-pin>545021584835957806</tracking-pin>
    <shipment-detail>
        <group-id>group1</group-id>
        <requested-shipping-point>K1G1C0</requested-shipping-point>
        <expected-mailing-date>2011-09-01</expected-mailing-date>
        <delivery-spec>
            <service-code>DOM.EP</service-code>
            <sender>
                <name>Bob</name>
                <company>CGI</company>
                <address-details>
                    <address-line-1>502 MAIN ST N</address-line-1>
                    <city>MONTREAL</city>
                    <prov-state>QC</prov-state>
                    <country-code>CA</country-code>
                    <postal-zip-code>H2B1A0</postal-zip-code>
                </address-details>
            </sender>
            <destination>
                <name>Jain</name>
                <company>CGI</company>
                <address-details>
                    <address-line-1>23 jardin private</address-line-1>
                    <city>Ottawa</city>
                    <prov-state>ON</prov-state>
                    <country-code>CA</country-code>
                    <postal-zip-code>K1K4T3</postal-zip-code>
                </address-details>
            </destination>
            <options>
                <option>
                    <option-code>DC</option-code>
                </option>
            </options>
            <parcel-characteristics>
                <weight>20.000</weight>
                <dimensions>
                    <length>12</length>
                    <width>9</width>
                    <height>6</height>
                </dimensions>
                <unpackaged>true</unpackaged>
                <mailing-tube>false</mailing-tube>
                <oversized>false</oversized>
            </parcel-characteristics>
            <notification>
                <email>john.doe@yahoo.com</email>
                <on-shipment>true</on-shipment>
                <on-exception>false</on-exception>
                <on-delivery>true</on-delivery>
            </notification>
            <print-preferences>
                <output-format>8.5x11</output-format>
            </print-preferences>
            <preferences>
                <show-packing-instructions>true</show-packing-instructions>
                <show-postage-rate>false</show-postage-rate>
                <show-insured-value>true</show-insured-value>
            </preferences>
            <settlement-info>
                <paid-by-customer>0001234567</paid-by-customer>
                <contract-id>0012345678</contract-id>
                <intended-method-of-payment>Account</intended-method-of-payment>
            </settlement-info>
        </delivery-spec>
    </shipment-detail>
</shipment-details>
"""

ShipmentResponse2 = """<shipment-details>
    <shipment-status>reconciled</shipment-status>
    <final-shipping-point>K1G1C0</final-shipping-point>
    <shipping-point-id>0015</shipping-point-id>
    <tracking-pin>1234567890123456</tracking-pin>
    <shipment-detail>
        <group-id>group2</group-id>
        <requested-shipping-point>K1G1C0</requested-shipping-point>
        <expected-mailing-date>2011-09-01</expected-mailing-date>
        <delivery-spec>
            <service-code>DOM.EP</service-code>
            <sender>
                <name>Bob</name>
                <company>CGI</company>
                <address-details>
                    <address-line-1>502 MAIN ST N</address-line-1>
                    <city>MONTREAL</city>
                    <prov-state>QC</prov-state>
                    <country-code>CA</country-code>
                    <postal-zip-code>H2B1A0</postal-zip-code>
                </address-details>
            </sender>
            <destination>
                <name>Jain</name>
                <company>CGI</company>
                <address-details>
                    <address-line-1>23 jardin private</address-line-1>
                    <city>Ottawa</city>
                    <prov-state>ON</prov-state>
                    <country-code>CA</country-code>
                    <postal-zip-code>K1K4T3</postal-zip-code>
                </address-details>
            </destination>
            <options>
                <option>
                    <option-code>DC</option-code>
                </option>
            </options>
            <parcel-characteristics>
                <weight>20.000</weight>
                <dimensions>
                    <length>12</length>
                    <width>9</width>
                    <height>6</height>
                </dimensions>
                <unpackaged>true</unpackaged>
                <mailing-tube>false</mailing-tube>
                <oversized>false</oversized>
            </parcel-characteristics>
            <notification>
                <email>john.doe@yahoo.com</email>
                <on-shipment>true</on-shipment>
                <on-exception>false</on-exception>
                <on-delivery>true</on-delivery>
            </notification>
            <print-preferences>
                <output-format>8.5x11</output-format>
            </print-preferences>
            <preferences>
                <show-packing-instructions>true</show-packing-instructions>
                <show-postage-rate>false</show-postage-rate>
                <show-insured-value>true</show-insured-value>
            </preferences>
            <settlement-info>
                <paid-by-customer>0001234567</paid-by-customer>
                <contract-id>0012345678</contract-id>
                <intended-method-of-payment>Account</intended-method-of-payment>
            </settlement-info>
        </delivery-spec>
    </shipment-detail>
</shipment-details>
"""
