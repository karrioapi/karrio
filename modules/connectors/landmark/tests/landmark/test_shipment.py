"""Landmark Global carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestLandmarkGlobalShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**SHIPMENT_REQUEST_PAYLOAD)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **SHIPMENT_CANCEL_REQUEST_PAYLOAD
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), SHIPMENT_REQUEST_XML)

    def test_create_import_shipment_request(self):
        import_request = models.ShipmentRequest(**IMPORT_SHIPMENT_REQUEST_PAYLOAD)
        request = gateway.mapper.create_shipment_request(import_request)

        self.assertEqual(request.serialize(), IMPORT_SHIPMENT_REQUEST_XML)

    def test_create_shipment(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"], f"{gateway.settings.server_url}/Ship.php"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_RESPONSE_XML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), PARSED_SHIPMENT_RESPONSE)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), SHIPMENT_CANCEL_REQUEST_XML)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"], f"{gateway.settings.server_url}/Cancel.php"
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = SHIPMENT_CANCEL_RESPONSE_XML
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_CANCEL_SHIPMENT_RESPONSE
            )

    def test_parse_import_shipment_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = IMPORT_SHIPMENT_RESPONSE_XML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), PARSED_IMPORT_RESPONSE)

    def test_parse_error_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = ERROR_RESPONSE_XML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), PARSED_ERROR_RESPONSE)


if __name__ == "__main__":
    unittest.main()

SHIPMENT_CANCEL_REQUEST_PAYLOAD = {"shipment_identifier": "8724720680"}

IMPORT_SHIPMENT_REQUEST_PAYLOAD = {
    "shipper": {
        "address_line1": "123 Main Street",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
        "person_name": "Contact Person",
        "company_name": "Acme Retail Inc",
        "phone_number": "12125551234",
        "email": "contact@acme.com",
    },
    "recipient": {
        "address_line1": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "postal_code": "94043",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Purchasing Dept.",
        "company_name": "John Doe",
        "phone_number": "14085551234",
        "email": "orders@example.com",
    },
    "parcels": [
        {
            "weight": 4.5,
            "width": 12.0,
            "height": 12.0,
            "length": 12.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "reference_number": "98233310",
        }
    ],
    "service": "landmark_maxipak_scan_ddp",
    "reference": "3245325",
    "options": {
        "landmark_import_request": True,
        "insurance": 20.65,
        "currency": "USD",
    },
    "customs": {
        "duty": {
            "declared_value": 187.98,
            "currency": "USD",
        },
        "duty_billing_address": {
            "company_name": "Acme Retail Inc",
            "phone_number": "12125551234",
            "email": "contact@acme.com",
        },
        "commodities": [
            {
                "sku": "7224059",
                "description": "Women's Shoes",
                "quantity": 2,
                "value_amount": 93.99,
                "weight": 1.0,
                "weight_unit": "LB",
                "hs_code": "6403993000",
                "origin_country": "CN",
            }
        ],
    },
}

SHIPMENT_REQUEST_PAYLOAD = {
    "shipper": {
        "address_line1": "123 Main Street",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "state_code": "NY",
        "person_name": "Contact Person",
        "company_name": "Acme Corporation",
        "phone_number": "12125551234",
        "email": "contact@acme.com",
    },
    "recipient": {
        "address_line1": "1600 Amphitheatre Parkway",
        "city": "Mountain View",
        "postal_code": "94043",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Purchasing Dept.",
        "company_name": "Jane Smith",
        "phone_number": "14085551234",
        "email": "jane.smith@example.com",
    },
    "parcels": [
        {
            "weight": 4.5,
            "width": 12.0,
            "height": 12.0,
            "length": 12.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "service": "landmark_maxipak_scan_ddp",
    "reference": "TEST-ORDER-001",
    "customs": {
        "duty": {
            "declared_value": 187.98,
            "currency": "USD",
        },
        "commodities": [
            {
                "sku": "7224059",
                "description": "Women's Shoes",
                "quantity": 2,
                "value_amount": 93.99,
                "weight": 1.0,
                "weight_unit": "LB",
                "hs_code": "6403993000",
                "origin_country": "CN",
            }
        ],
    },
}

IMPORT_SHIPMENT_REQUEST_XML = """<ImportRequest>
    <Login>
        <Username>test_username</Username>
        <Password>test_password</Password>
    </Login>
    <Test>true</Test>
    <ClientID>2437</ClientID>
    <AccountNumber>TEST123</AccountNumber>
    <Reference>3245325</Reference>
    <ShipTo>
        <Name>John Doe</Name>
        <Attention>Purchasing Dept.</Attention>
        <Address1>1600 Amphitheatre Parkway</Address1>
        <City>Mountain View</City>
        <State>CA</State>
        <PostalCode>94043</PostalCode>
        <Country>US</Country>
        <Phone>14085551234</Phone>
        <Email>orders@example.com</Email>
    </ShipTo>
    <ShippingLane>
        <Region>Landmark CMH</Region>
    </ShippingLane>
    <ShipMethod>LGINTSTD</ShipMethod>
    <OrderTotal>187.98</OrderTotal>
    <ShipmentInsuranceFreight>20.65</ShipmentInsuranceFreight>
    <ItemsCurrency>USD</ItemsCurrency>
    <IsCommercialShipment>0</IsCommercialShipment>
    <ProduceLabel>false</ProduceLabel>
    <LabelEncoding>BASE64</LabelEncoding>
    <VendorInformation>
        <VendorName>Acme Retail Inc</VendorName>
        <VendorPhone>12125551234</VendorPhone>
        <VendorEmail>contact@acme.com</VendorEmail>
        <VendorAddress1>123 Main Street</VendorAddress1>
        <VendorCity>New York</VendorCity>
        <VendorState>NY</VendorState>
        <VendorPostalCode>10001</VendorPostalCode>
        <VendorCountry>US</VendorCountry>
    </VendorInformation>
    <FulfillmentAddress>
        <Name>Acme Retail Inc</Name>
        <Attention>Contact Person</Attention>
        <Address1>123 Main Street</Address1>
        <City>New York</City>
        <State>NY</State>
        <PostalCode>10001</PostalCode>
        <Country>US</Country>
    </FulfillmentAddress>
    <Packages>
        <Package>
            <WeightUnit>LB</WeightUnit>
            <Weight>4.5</Weight>
            <DimensionsUnit>IN</DimensionsUnit>
            <Length>12</Length>
            <Width>12</Width>
            <Height>12</Height>
            <PackageReference>98233310</PackageReference>
        </Package>
    </Packages>
    <Items>
        <Item>
            <Sku>7224059</Sku>
            <Quantity>2</Quantity>
            <UnitPrice>93.99</UnitPrice>
            <Description>Women's Shoes</Description>
            <HSCode>6403993000</HSCode>
            <CountryOfOrigin>CN</CountryOfOrigin>
            <ContentCategory>
                <ReturnCustomsInfo>
                    <HSCode>6403993000</HSCode>
                    <HSRegionCode>CN</HSRegionCode>
                </ReturnCustomsInfo>
            </ContentCategory>
        </Item>
    </Items>
</ImportRequest>
"""

SHIPMENT_REQUEST_XML = """<ShipRequest>
    <Login>
        <Username>test_username</Username>
        <Password>test_password</Password>
    </Login>
    <Test>true</Test>
    <ClientID>2437</ClientID>
    <AccountNumber>TEST123</AccountNumber>
    <Reference>TEST-ORDER-001</Reference>
    <ShipTo>
        <Name>Jane Smith</Name>
        <Attention>Purchasing Dept.</Attention>
        <Address1>1600 Amphitheatre Parkway</Address1>
        <City>Mountain View</City>
        <State>CA</State>
        <PostalCode>94043</PostalCode>
        <Country>US</Country>
        <Phone>14085551234</Phone>
        <Email>jane.smith@example.com</Email>
    </ShipTo>
    <ShippingLane>
        <Region>Landmark CMH</Region>
    </ShippingLane>
    <ShipMethod>LGINTSTD</ShipMethod>
    <OrderTotal>187.98</OrderTotal>
    <IsCommercialShipment>0</IsCommercialShipment>
    <LabelEncoding>BASE64</LabelEncoding>
    <VendorInformation>
        <VendorName>Acme Corporation</VendorName>
        <VendorPhone>12125551234</VendorPhone>
        <VendorEmail>contact@acme.com</VendorEmail>
        <VendorAddress1>123 Main Street</VendorAddress1>
        <VendorCity>New York</VendorCity>
        <VendorState>NY</VendorState>
        <VendorPostalCode>10001</VendorPostalCode>
        <VendorCountry>US</VendorCountry>
    </VendorInformation>
    <FulfillmentAddress>
        <Name>Acme Corporation</Name>
        <Attention>Contact Person</Attention>
        <Address1>123 Main Street</Address1>
        <City>New York</City>
        <State>NY</State>
        <PostalCode>10001</PostalCode>
        <Country>US</Country>
    </FulfillmentAddress>
    <Packages>
        <Package>
            <WeightUnit>LB</WeightUnit>
            <Weight>4.5</Weight>
            <DimensionsUnit>IN</DimensionsUnit>
            <Length>12</Length>
            <Width>12</Width>
            <Height>12</Height>
        </Package>
    </Packages>
    <Items>
        <Item>
            <Sku>7224059</Sku>
            <Quantity>2</Quantity>
            <UnitPrice>93.99</UnitPrice>
            <Description>Women's Shoes</Description>
            <HSCode>6403993000</HSCode>
            <CountryOfOrigin>CN</CountryOfOrigin>
            <ReturnCustomsInfo>
                <HSCode>6403993000</HSCode>
                <HSRegionCode>CN</HSRegionCode>
            </ReturnCustomsInfo>
        </Item>
    </Items>
</ShipRequest>
"""

SHIPMENT_CANCEL_REQUEST_XML = """<CancelRequest>
    <Login>
        <Username>test_username</Username>
        <Password>test_password</Password>
    </Login>
    <Test>true</Test>
    <ClientID>2437</ClientID>
    <TrackingNumber>8724720680</TrackingNumber>
    <DeleteShipment>true</DeleteShipment>
    <Reason>Consignee canceled shipment.</Reason>
</CancelRequest>
"""

SHIPMENT_RESPONSE_XML = """<?xml version="1.0"?>
<ShipResponse>
	<Result>
		<Success>true</Success>
		<ResultMessage>Shipment TEST-ORDER-001 successfully created and processed</ResultMessage>
		<ShippingCarrier>Canada Post</ShippingCarrier>
		<Packages>
			<Package>
				<LabelImages>
					<LabelImage>JVBERi0xLjMKJeLjz9MKNiAwIG9iago8PCAvVHlwZSAvUGFnZSAvUGFyZW50IDEgMCBSIC9MYXN0TW9kaWZpZWQgKEQ6MjAxNTAxMDUxMDU2MDUtMDgnMDAnKSAvUmVzb3VyY2VzIDIgMCBSIC9NZWRpYUJveCBbMC4wMDAwMDAgMC4wMDAwMDAgMjg4LjAwMDAwMCA0MzIuMDAwMDAwXSAvQ3JvcEJveCBbMC4wMDAwMDAgMC4wMDAwMDAgMjg4LjAwMDAwMCA0MzIuMDAwMDAwXSAvQmxlZWRCb3ggWzAuMDAwMDAwIDAuMDAwMDAwIDI4OC4wMDAwMDAgNDMyLjAwMDAwMF0gL1RyaW1Cb3ggWzAuMDAwMDAwIDAuMDAwMDAwIDI4OC4wMDAwMDAgNDMyLjAwMDAwMF0gL0FydEJveCBbMC4wMDAwMDAgMC4wMDAwMDAgMjg4LjAwMDAwMCA0MzIuMDAwMDAwXSAvQ29udGVudHMgNyAwIFIgL1JvdGF0ZSAwIC9Hcm91cCA8PCAvVHlwZSAvR3JvdXAgL1MgL1RyYW5zcGFyZW5jeSAvQ1MgL0RldmljZVJHQiA+PiAvQW5ub3RzIFsgNSAwIFIgXSAvUFogMSA+PgplbmRvYmoKNyAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlIC9MZW5ndGggNTg2Pj4gc3RyZWFtCnicxZfRbtowFIbv+xRH2k2RlvTYjmOXO5MYmi4EGtz1ovSmBSpNm9jYpGhvP8OEg4FWhYXVyCKybP+fD/7PCRhygbZBBQjXtn+B+wf7NbG9Z/vzWcfARZcAISGuGpgZaHOGxy5cDVMg9Ij97OQF4HphZdeBHbVbScaXIxHhIV7Gq10ncH+eqyLtq/IT9HShyyyBXHV03noAc72BIk5AwmQURow4km456Le3hQk2psxErWwjK3E3BkaPDBR3pzv9BoPwTx/RCOFKlZ8tgi6hTB1EM3Kx8ORui8wAbVoDPY3ObZlnRc8Mio+DAnKRo5YNK3LmKZJAShkwSYJY4iFaS1P8FWGRcx3lbjSIHMViCiM4dP76JtHmLE3rKBARErFh6V6irJshgET5V5mAPFS/Pim9FPtOevlSZN42/59yiQsBlbEXgtFVNgQzaG8ff2+mJU1mmQ0m63BKsWZS/WGuYYnW14XZQcP/iBb7aC8nn/eA4z7cVqp6D6LIJ3o1sZ0UhPkgiSpUqg7IcycoqzUdkcIrqysTlrrbtkWfRdtF9eBM9AqB906BceQQUmV0G5AEyAOKhDdRfjblhC+39jZkaRsoIcg4j5vWjH3NYaYTDXcGxudfH3+OWzbaq9VNy/J9sh+sGsxnQJzaD2Do9ll+SH3X3AOP109P3+AiI5DO4cbVSH6Cu8lISLG+mus3vhrb+fYIcba/QDtfWM/yOnDzarqYTuDxN5hkmHbt71ZVVfjr6ftkFs4Xz+OWg7p561+I3aDZdvTaPzVYxSsKZW5kc3RyZWFtCmVuZG9iagoxIDAgb2JqCjw8IC9UeXBlIC9QYWdlcyAvS2lkcyBbIDYgMCBSIF0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwvVHlwZSAvRm9udCAvU3VidHlwZSAvVHlwZTEgL0Jhc2VGb250IC9IZWx2ZXRpY2EgL05hbWUgL0YxIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nID4+CmVuZG9iago0IDAgb2JqCjw8L1R5cGUgL0ZvbnQgL1N1YnR5cGUgL1R5cGUxIC9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGQgL05hbWUgL0YyIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nID4+CmVuZG9iago4IDAgb2JqCjw8L1R5cGUgL1hPYmplY3QgL1N1YnR5cGUgL0ltYWdlIC9XaWR0aCAzMDAgL0hlaWdodCAxMTAgL0NvbG9yU3BhY2UgWy9JbmRleGVkIC9EZXZpY2VSR0IgMSA5IDAgUl0gL0JpdHNQZXJDb21wb25lbnQgMSAvRmlsdGVyIC9GbGF0ZURlY29kZSAvRGVjb2RlUGFybXMgPDwgL1ByZWRpY3RvciAxNSAvQ29sb3JzIDEgL0JpdHNQZXJDb21wb25lbnQgMSAvQ29sdW1ucyAzMDAgPj4gL0xlbmd0aCAyNDUgPj4gc3RyZWFtCliF7dChiwJBFAbw93gwW+a0rihetg1s0r9lw25RLMfC1YObKwZBESwLgtWqxTzJZrVoEATzxgty3MxZDp1tF4R7X3z84ON9AJzHiZiM9sNTr7VtL7rxYTbtxP3tZLVjxowZM2bMmDFjxuwXuz34r3/MDF2kaoICI+CNPp9NEwc4uGeQVFQEGZoqbAhCiHBDXlZVqS7I1DQ5luI5KGGobakygrK6TvDsL31aEvywBuUN84LrMiauTICE5NXHwDJZyCsjx9KPOWovy0LH3AsytGxcxpRjdhDMpYnQx74sU+/6QoWdF4pA23mD4x3jcP55vgGOCnt9CmVuZHN0cmVhbQplbmRvYmoKOSAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlIC9MZW5ndGggMTQ+PiBzdHJlYW0KeJz7//8/AwMDAA73Av4KZW5kc3RyZWFtCmVuZG9iagoyIDAgb2JqCjw8IC9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXSAvRm9udCA8PCAvRjEgMyAwIFIgL0YyIDQgMCBSID4+IC9YT2JqZWN0IDw8IC9JMSA4IDAgUiA+PiA+PgplbmRvYmoKNSAwIG9iago8PC9UeXBlIC9Bbm5vdCAvU3VidHlwZSAvTGluayAvUmVjdCBbMi44MzUwMDAgMS4wMDAwMDAgMTkuMDA1MDAwIDIuMTU2MDAwXSAvQ29udGVudHMgKGh0dHA6Ly93d3cudGNwZGYub3JnKSAvUCA2IDAgUiAvTk0gKDAwMDEtMDAwMCkgL00gKEQ6MjAxNTAxMDUxMDU2MDUtMDgnMDAnKSAvRiA0IC9Cb3JkZXIgWzAgMCAwXSAvQSA8PC9TIC9VUkkgL1VSSSAoaHR0cDovL3d3dy50Y3BkZi5vcmcpPj4gL0ggL0k+PgplbmRvYmoKMTAgMCBvYmoKPDwgL1Byb2R1Y2VyIChUQ1BERiA1LjkuMTk4IFwoaHR0cDovL3d3dy50Y3BkZi5vcmdcKSkgL0NyZWF0aW9uRGF0ZSAoRDoyMDE1MDEwNTEwNTYwNS0wOCcwMCcpIC9Nb2REYXRlIChEOjIwMTUwMTA1MTA1NjA1LTA4JzAwJykgL1RyYXBwZWQgL0ZhbHNlID4+CmVuZG9iagoxMSAwIG9iago8PCAvVHlwZSAvTWV0YWRhdGEgL1N1YnR5cGUgL1hNTCAvTGVuZ3RoIDQyMzEgPj4gc3RyZWFtCjw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDQuMi4xLWMwNDMgNTIuMzcyNzI4LCAyMDA5LzAxLzE4LTE1OjA4OjA0Ij4KCTxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CgkJPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIj4KCQkJPGRjOmZvcm1hdD5hcHBsaWNhdGlvbi9wZGY8L2RjOmZvcm1hdD4KCQkJPGRjOnRpdGxlPgoJCQkJPHJkZjpBbHQ+CgkJCQkJPHJkZjpsaSB4bWw6bGFuZz0ieC1kZWZhdWx0Ij48L3JkZjpsaT4KCQkJCTwvcmRmOkFsdD4KCQkJPC9kYzp0aXRsZT4KCQkJPGRjOmNyZWF0b3I+CgkJCQk8cmRmOlNlcT4KCQkJCQk8cmRmOmxpPjwvcmRmOmxpPgoJCQkJPC9yZGY6U2VxPgoJCQk8L2RjOmNyZWF0b3I+CgkJCTxkYzpkZXNjcmlwdGlvbj4KCQkJCTxyZGY6QWx0PgoJCQkJCTxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+PC9yZGY6bGk+CgkJCQk8L3JkZjpBbHQ+CgkJCTwvZGM6ZGVzY3JpcHRpb24+CgkJCTxkYzpzdWJqZWN0PgoJCQkJPHJkZjpCYWc+CgkJCQkJPHJkZjpsaT48L3JkZjpsaT4KCQkJCTwvcmRmOkJhZz4KCQkJPC9kYzpzdWJqZWN0PgoJCTwvcmRmOkRlc2NyaXB0aW9uPgoJCTxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CgkJCTx4bXA6Q3JlYXRlRGF0ZT4yMDE1LTAxLTA1VDEwOjU2OjA1KzA4OjAwPC94bXA6Q3JlYXRlRGF0ZT4KCQkJPHhtcDpDcmVhdG9yVG9vbD48L3htcDpDcmVhdG9yVG9vbD4KCQkJPHhtcDpNb2RpZnlEYXRlPjIwMTUtMDEtMDVUMTA6NTY6MDUrMDg6MDA8L3htcDpNb2RpZnlEYXRlPgoJCQk8eG1wOk1ldGFkYXRhRGF0ZT4yMDE1LTAxLTA1VDEwOjU2OjA1KzA4OjAwPC94bXA6TWV0YWRhdGFEYXRlPgoJCTwvcmRmOkRlc2NyaXB0aW9uPgoJCTxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnBkZj0iaHR0cDovL25zLmFkb2JlLmNvbS9wZGYvMS4zLyI+CgkJCTxwZGY6S2V5d29yZHM+IFRDUERGPC9wZGY6S2V5d29yZHM+CgkJCTxwZGY6UHJvZHVjZXI+VENQREYgNS45LjE5OCAoaHR0cDovL3d3dy50Y3BkZi5vcmcpPC9wZGY6UHJvZHVjZXI+CgkJPC9yZGY6RGVzY3JpcHRpb24+CgkJPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iPgoJCQk8eG1wTU06RG9jdW1lbnRJRD51dWlkOjMzYzYzOWRjLWU1ZDktY2Y4Zi1kYzI1LTBlMDAzMzEyNGM1NDwveG1wTU06RG9jdW1lbnRJRD4KCQkJPHhtcE1NOkluc3RhbmNlSUQ+dXVpZDozM2M2MzlkYy1lNWQ5LWNmOGYtZGMyNS0wZTAwMzMxMjRjNTQ8L3htcE1NOkluc3RhbmNlSUQ+CgkJPC9yZGY6RGVzY3JpcHRpb24+CgkJPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6cGRmYUV4dGVuc2lvbj0iaHR0cDovL3d3dy5haWltLm9yZy9wZGZhL25zL2V4dGVuc2lvbi8iIHhtbG5zOnBkZmFTY2hlbWE9Imh0dHA6Ly93d3cuYWlpbS5vcmcvcGRmYS9ucy9zY2hlbWEjIiB4bWxuczpwZGZhUHJvcGVydHk9Imh0dHA6Ly93d3cuYWlpbS5vcmcvcGRmYS9ucy9wcm9wZXJ0eSMiPgoJCQk8cGRmYUV4dGVuc2lvbjpzY2hlbWFzPgoJCQkJPHJkZjpCYWc+CgkJCQkJPHJkZjpsaSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CgkJCQkJCTxwZGZhU2NoZW1hOm5hbWVzcGFjZVVSST5odHRwOi8vbnMuYWRvYmUuY29tL3BkZi8xLjMvPC9wZGZhU2NoZW1hOm5hbWVzcGFjZVVSST4KCQkJCQkJPHBkZmFTY2hlbWE6cHJlZml4PnBkZjwvcGRmYVNjaGVtYTpwcmVmaXg+CgkJCQkJCTxwZGZhU2NoZW1hOnNjaGVtYT5BZG9iZSBQREYgU2NoZW1hPC9wZGZhU2NoZW1hOnNjaGVtYT4KCQkJCQk8L3JkZjpsaT4KCQkJCQk8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KCQkJCQkJPHBkZmFTY2hlbWE6bmFtZXNwYWNlVVJJPmh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS88L3BkZmFTY2hlbWE6bmFtZXNwYWNlVVJJPgoJCQkJCQk8cGRmYVNjaGVtYTpwcmVmaXg+eG1wTU08L3BkZmFTY2hlbWE6cHJlZml4PgoJCQkJCQk8cGRmYVNjaGVtYTpzY2hlbWE+WE1QIE1lZGlhIE1hbmFnZW1lbnQgU2NoZW1hPC9wZGZhU2NoZW1hOnNjaGVtYT4KCQkJCQkJPHBkZmFTY2hlbWE6cHJvcGVydHk+CgkJCQkJCQk8cmRmOlNlcT4KCQkJCQkJCQk8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KCQkJCQkJCQkJPHBkZmFQcm9wZXJ0eTpjYXRlZ29yeT5pbnRlcm5hbDwvcGRmYVByb3BlcnR5OmNhdGVnb3J5PgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OmRlc2NyaXB0aW9uPlVVSUQgYmFzZWQgaWRlbnRpZmllciBmb3Igc3BlY2lmaWMgaW5jYXJuYXRpb24gb2YgYSBkb2N1bWVudDwvcGRmYVByb3BlcnR5OmRlc2NyaXB0aW9uPgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5Om5hbWU+SW5zdGFuY2VJRDwvcGRmYVByb3BlcnR5Om5hbWU+CgkJCQkJCQkJCTxwZGZhUHJvcGVydHk6dmFsdWVUeXBlPlVSSTwvcGRmYVByb3BlcnR5OnZhbHVlVHlwZT4KCQkJCQkJCQk8L3JkZjpsaT4KCQkJCQkJCTwvcmRmOlNlcT4KCQkJCQkJPC9wZGZhU2NoZW1hOnByb3BlcnR5PgoJCQkJCTwvcmRmOmxpPgoJCQkJCTxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgoJCQkJCQk8cGRmYVNjaGVtYTpuYW1lc3BhY2VVUkk+aHR0cDovL3d3dy5haWltLm9yZy9wZGZhL25zL2lkLzwvcGRmYVNjaGVtYTpuYW1lc3BhY2VVUkk+CgkJCQkJCTxwZGZhU2NoZW1hOnByZWZpeD5wZGZhaWQ8L3BkZmFTY2hlbWE6cHJlZml4PgoJCQkJCQk8cGRmYVNjaGVtYTpzY2hlbWE+UERGL0EgSUQgU2NoZW1hPC9wZGZhU2NoZW1hOnNjaGVtYT4KCQkJCQkJPHBkZmFTY2hlbWE6cHJvcGVydHk+CgkJCQkJCQk8cmRmOlNlcT4KCQkJCQkJCQk8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KCQkJCQkJCQkJPHBkZmFQcm9wZXJ0eTpjYXRlZ29yeT5pbnRlcm5hbDwvcGRmYVByb3BlcnR5OmNhdGVnb3J5PgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OmRlc2NyaXB0aW9uPlBhcnQgb2YgUERGL0Egc3RhbmRhcmQ8L3BkZmFQcm9wZXJ0eTpkZXNjcmlwdGlvbj4KCQkJCQkJCQkJPHBkZmFQcm9wZXJ0eTpuYW1lPnBhcnQ8L3BkZmFQcm9wZXJ0eTpuYW1lPgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OnZhbHVlVHlwZT5JbnRlZ2VyPC9wZGZhUHJvcGVydHk6dmFsdWVUeXBlPgoJCQkJCQkJCTwvcmRmOmxpPgoJCQkJCQkJCTxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OmNhdGVnb3J5PmludGVybmFsPC9wZGZhUHJvcGVydHk6Y2F0ZWdvcnk+CgkJCQkJCQkJCTxwZGZhUHJvcGVydHk6ZGVzY3JpcHRpb24+QW1lbmRtZW50IG9mIFBERi9BIHN0YW5kYXJkPC9wZGZhUHJvcGVydHk6ZGVzY3JpcHRpb24+CgkJCQkJCQkJCTxwZGZhUHJvcGVydHk6bmFtZT5hbWQ8L3BkZmFQcm9wZXJ0eTpuYW1lPgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OnZhbHVlVHlwZT5UZXh0PC9wZGZhUHJvcGVydHk6dmFsdWVUeXBlPgoJCQkJCQkJCTwvcmRmOmxpPgoJCQkJCQkJCTxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgoJCQkJCQkJCQk8cGRmYVByb3BlcnR5OmNhdGVnb3J5PmludGVybmFsPC9wZGZhUHJvcGVydHk6Y2F0ZWdvcnk+CgkJCQkJCQkJCTxwZGZhUHJvcGVydHk6ZGVzY3JpcHRpb24+Q29uZm9ybWFuY2UgbGV2ZWwgb2YgUERGL0Egc3RhbmRhcmQ8L3BkZmFQcm9wZXJ0eTpkZXNjcmlwdGlvbj4KCQkJCQkJCQkJPHBkZmFQcm9wZXJ0eTpuYW1lPmNvbmZvcm1hbmNlPC9wZGZhUHJvcGVydHk6bmFtZT4KCQkJCQkJCQkJPHBkZmFQcm9wZXJ0eTp2YWx1ZVR5cGU+VGV4dDwvcGRmYVByb3BlcnR5OnZhbHVlVHlwZT4KCQkJCQkJCQk8L3JkZjpsaT4KCQkJCQkJCTwvcmRmOlNlcT4KCQkJCQkJPC9wZGZhU2NoZW1hOnByb3BlcnR5PgoJCQkJCTwvcmRmOmxpPgoJCQkJPC9yZGY6QmFnPgoJCQk8L3BkZmFFeHRlbnNpb246c2NoZW1hcz4KCQk8L3JkZjpEZXNjcmlwdGlvbj4KCTwvcmRmOlJERj4KPC94OnhtcG1ldGE+Cjw/eHBhY2tldCBlbmQ9InciPz4KZW5kc3RyZWFtCmVuZG9iagoxMiAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvVmVyc2lvbiAvMS4zIC9QYWdlcyAxIDAgUiAvTmFtZXMgPDwgPj4gL1ZpZXdlclByZWZlcmVuY2VzIDw8IC9EaXJlY3Rpb24gL0wyUiA+PiAvUGFnZUxheW91dCAvU2luZ2xlUGFnZSAvUGFnZU1vZGUgL1VzZU5vbmUgL09wZW5BY3Rpb24gWzYgMCBSIC9GaXRIIG51bGxdIC9NZXRhZGF0YSAxMSAwIFIgPj4KZW5kb2JqCnhyZWYKMCAxMwowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDExMzkgMDAwMDAgbiAKMDAwMDAwMjAwNiAwMDAwMCBuIAowMDAwMDAxMTk4IDAwMDAwIG4gCjAwMDAwMDEzMDQgMDAwMDAgbiAKMDAwMDAwMjEzMCAwMDAwMCBuIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDA0ODMgMDAwMDAgbiAKMDAwMDAwMTQxNSAwMDAwMCBuIAowMDAwMDAxOTIzIDAwMDAwIG4gCjAwMDAwMDIzNzkgMDAwMDAgbiAKMDAwMDAwMjU0MyAwMDAwMCBuIAowMDAwMDA2ODU3IDAwMDAwIG4gCnRyYWlsZXIKPDwgL1NpemUgMTMgL1Jvb3QgMTIgMCBSIC9JbmZvIDEwIDAgUiAvSUQgWyA8MzNjNjM5ZGNlNWQ5Y2Y4ZmRjMjUwZTAwMzMxMjRjNTQ+IDwzM2M2MzlkY2U1ZDljZjhmZGMyNTBlMDAzMzEyNGM1ND4gXSA+PgpzdGFydHhyZWYKNzA2NgolJUVPRgo=</LabelImage>
				</LabelImages>
				<TrackingNumber>58949576860</TrackingNumber>
				<LandmarkTrackingNumber>LTN_test35364527N1</LandmarkTrackingNumber>
				<PackageID>xxx1</PackageID>
				<BarcodeData>xxx492104000000412001</BarcodeData>
				<PackageReference>PKG-001</PackageReference>
			</Package>
		</Packages>
	</Result>
</ShipResponse>
"""

IMPORT_SHIPMENT_RESPONSE_XML = """<?xml version="1.0"?>
<ImportResponse>
	<Result>
		<Success>true</Success>
		<ResultMessage>Shipment 3245325 successfully created</ResultMessage>
		<Packages>
			<Package>
				<TrackingNumber>LTNtest48741737N1</TrackingNumber>
				<LandmarkTrackingNumber>LTNtest48741737N1</LandmarkTrackingNumber>
				<PackageReference>98233310</PackageReference>
			</Package>
		</Packages>
	</Result>
</ImportResponse>
"""

SHIPMENT_CANCEL_RESPONSE_XML = """<?xml version="1.0"?>
<CancelResponse>
	<Test>true</Test>
	<Result>
		<Success>true</Success>
		<ResultMessage>Successfully unprocessed shipment 1234</ResultMessage>
	</Result>
</CancelResponse>"""

ERROR_RESPONSE_XML = """<?xml version="1.0"?>
<ShipResponse>
	<Result>
		<Success>false</Success>
		<ResultMessage>See Errors element for error details</ResultMessage>
	</Result>
	<Errors>
		<Error>
			<ErrorCode>unprocess</ErrorCode>
			<ErrorMessage>Already assigned to Shipment Group</ErrorMessage>
		</Error>
	</Errors>
</ShipResponse>
"""

PARSED_SHIPMENT_RESPONSE = [
    {
        "carrier_id": "landmark",
        "carrier_name": "landmark",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {
            "barcode_datas": ["xxx492104000000412001"],
            "last_mile_carrier": "Canada Post",
            "last_mile_tracking_number": "58949576860",
            "last_mile_tracking_numbers": ["58949576860"],
            "package_references": ["PKG-001"],
            "shipment_identifiers": ["xxx1"],
            "tracking_numbers": ["LTN_test35364527N1"],
        },
        "shipment_identifier": "xxx1",
        "tracking_number": "LTN_test35364527N1",
    },
    [],
]

PARSED_IMPORT_RESPONSE = [
    {
        "carrier_id": "landmark",
        "carrier_name": "landmark",
        "docs": {},
        "label_type": "PDF",
        "meta": {
            "package_references": ["98233310"],
            "shipment_identifiers": ["LTNtest48741737N1"],
            "tracking_numbers": ["LTNtest48741737N1"],
        },
        "shipment_identifier": "LTNtest48741737N1",
        "tracking_number": "LTNtest48741737N1",
    },
    [],
]

PARSED_CANCEL_SHIPMENT_RESPONSE = [
    {
        "carrier_id": "landmark",
        "carrier_name": "landmark",
        "success": True,
        "operation": "Shipment Cancellation",
    },
    [],
]

PARSED_ERROR_RESPONSE = [
    None,
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "code": "unprocess",
            "details": {},
            "message": "Already assigned to Shipment Group",
        }
    ],
]
