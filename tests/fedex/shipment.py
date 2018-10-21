import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pyfedex.ship_service_v21 import ProcessShipmentRequest
from purplship.domain.entities import Shipment
from tests.fedex.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestFedExShipment(unittest.TestCase):
    def setUp(self):
        self.ShipmentRequest = ProcessShipmentRequest()
        self.ShipmentRequest.build(get_node_from_xml(ShipmentRequestXml, 'ProcessShipmentRequest'))

    def test_create_shipment_request(self):
        payload = Shipment.create(**shipment_data)
        ShipmentRequest_ = proxy.mapper.create_shipment_request(payload)
        ShipmentRequest_.RequestedShipment.ShipTimestamp = None
        print(export(ShipmentRequest_))
        self.assertEqual(export(ShipmentRequest_), export(self.ShipmentRequest))

    @patch("purplship.mappers.fedex.fedex_proxy.http", return_value='<a></a>')
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.ShipmentRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXml))


if __name__ == '__main__':
    unittest.main()

ShipmentRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v21">
    <tns:Body>
        <ns:ProcessShipmentRequest>
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
                <ns:CustomerTransactionId>IE_v18_Ship</ns:CustomerTransactionId>
            </ns:TransactionDetail>
            <ns:Version>
                <ns:ServiceId>ship</ns:ServiceId>
                <ns:Major>21</ns:Major>
                <ns:Intermediate>0</ns:Intermediate>
                <ns:Minor>0</ns:Minor>
            </ns:Version>
            <ns:RequestedShipment>
                <ns:DropoffType>REGULAR_PICKUP</ns:DropoffType>
                <ns:ServiceType>INTERNATIONAL_PRIORITY</ns:ServiceType>
                <ns:PackagingType>YOUR_PACKAGING</ns:PackagingType>
                <ns:PreferredCurrency>USD</ns:PreferredCurrency>
                <ns:Shipper>
                    <ns:Contact>
                        <ns:PersonName>Input Your Information</ns:PersonName>
                        <ns:CompanyName>Input Your Information</ns:CompanyName>
                        <ns:PhoneNumber>Input Your Information</ns:PhoneNumber>
                        <ns:EMailAddress>Input Your Information</ns:EMailAddress>
                    </ns:Contact>
                    <ns:Address>
                        <ns:StreetLines>Input Your Information</ns:StreetLines>
                        <ns:StreetLines>Input Your Information</ns:StreetLines>
                        <ns:City>MEMPHIS</ns:City>
                        <ns:StateOrProvinceCode>TN</ns:StateOrProvinceCode>
                        <ns:PostalCode>38117</ns:PostalCode>
                        <ns:CountryCode>US</ns:CountryCode>
                    </ns:Address>
                </ns:Shipper>
                <ns:Recipient>
                    <ns:Contact>
                        <ns:PersonName>Input Your Information</ns:PersonName>
                        <ns:CompanyName>Input Your Information</ns:CompanyName>
                        <ns:PhoneNumber>Input Your Information</ns:PhoneNumber>
                        <ns:EMailAddress>Input Your Information</ns:EMailAddress>
                    </ns:Contact>
                    <ns:Address>
                        <ns:StreetLines>Input Your Information</ns:StreetLines>
                        <ns:StreetLines>Input Your Information</ns:StreetLines>
                        <ns:City>RICHMOND</ns:City>
                        <ns:StateOrProvinceCode>BC</ns:StateOrProvinceCode>
                        <ns:PostalCode>V7C4v7</ns:PostalCode>
                        <ns:CountryCode>CA</ns:CountryCode>
                    </ns:Address>
                </ns:Recipient>
                <ns:ShippingChargesPayment>
                    <ns:PaymentType>THIRD_PARTY</ns:PaymentType>
                    <ns:Payor>
                        <ns:ResponsibleParty>
                            <ns:AccountNumber>Input Your Information</ns:AccountNumber>
                            <ns:Tins>
                                <ns:TinType>BUSINESS_STATE</ns:TinType>
                                <ns:Number>213456</ns:Number>
                            </ns:Tins>
                            <ns:Contact>
                                <ns:ContactId>12345</ns:ContactId>
                                <ns:PersonName>Input Your Information</ns:PersonName>
                            </ns:Contact>
                        </ns:ResponsibleParty>
                    </ns:Payor>
                </ns:ShippingChargesPayment>
                <ns:SpecialServicesRequested>
                    <ns:SpecialServiceTypes>INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS</ns:SpecialServiceTypes>
                    <ns:InternationalTrafficInArmsRegulationsDetail>
                        <ns:LicenseOrExemptionNumber>12345</ns:LicenseOrExemptionNumber>
                    </ns:InternationalTrafficInArmsRegulationsDetail>
                </ns:SpecialServicesRequested>
                <ns:CustomsClearanceDetail>
                    <ns:DutiesPayment>
                        <ns:PaymentType>SENDER</ns:PaymentType>
                        <ns:Payor>
                            <ns:ResponsibleParty>
                                <ns:AccountNumber>Input Your Information</ns:AccountNumber>
                                <ns:Tins>
                                    <ns:TinType>BUSINESS_STATE</ns:TinType>
                                    <ns:Number>213456</ns:Number>
                                </ns:Tins>
                                <ns:Contact>
                                    <ns:ContactId>12345</ns:ContactId>
                                    <ns:PersonName>Input Your Information</ns:PersonName>
                                </ns:Contact>
                            </ns:ResponsibleParty>
                        </ns:Payor>
                    </ns:DutiesPayment>
                    <ns:CustomsValue>
                        <ns:Currency>USD</ns:Currency>
                        <ns:Amount>100.</ns:Amount>
                    </ns:CustomsValue>
                    <ns:Commodities>
                        <ns:NumberOfPieces>1</ns:NumberOfPieces>
                        <ns:Description>ABCD</ns:Description>
                        <ns:CountryOfManufacture>US</ns:CountryOfManufacture>
                        <ns:Weight>
                            <ns:Units>LB</ns:Units>
                            <ns:Value>1.</ns:Value>
                        </ns:Weight>
                        <ns:Quantity>1.</ns:Quantity>
                        <ns:QuantityUnits>cm</ns:QuantityUnits>
                        <ns:UnitPrice>
                            <ns:Currency>USD</ns:Currency>
                            <ns:Amount>1.</ns:Amount>
                        </ns:UnitPrice>
                        <ns:CustomsValue>
                            <ns:Currency>USD</ns:Currency>
                            <ns:Amount>100.</ns:Amount>
                        </ns:CustomsValue>
                    </ns:Commodities>
                    <ns:ExportDetail>
                        <ns:ExportComplianceStatement>30.37(f)</ns:ExportComplianceStatement>
                    </ns:ExportDetail>
                </ns:CustomsClearanceDetail>
                <ns:LabelSpecification>
                    <ns:LabelFormatType>COMMON2D</ns:LabelFormatType>
                    <ns:ImageType>PNG</ns:ImageType>
                    <ns:LabelStockType>PAPER_7X4.75</ns:LabelStockType>
                </ns:LabelSpecification>
                <ns:ShippingDocumentSpecification>
                    <ns:ShippingDocumentTypes>COMMERCIAL_INVOICE</ns:ShippingDocumentTypes>
                    <ns:CommercialInvoiceDetail>
                        <ns:Format>
                            <ns:ImageType>PDF</ns:ImageType>
                            <ns:StockType>PAPER_LETTER</ns:StockType>
                            <ns:ProvideInstructions>true</ns:ProvideInstructions>
                        </ns:Format>
                    </ns:CommercialInvoiceDetail>
                </ns:ShippingDocumentSpecification>
                <ns:RateRequestTypes>LIST</ns:RateRequestTypes>
                <ns:PackageCount>1</ns:PackageCount>
                <ns:RequestedPackageLineItems>
                    <ns:SequenceNumber>1</ns:SequenceNumber>
                    <ns:Weight>
                        <ns:Units>LB</ns:Units>
                        <ns:Value>20.</ns:Value>
                    </ns:Weight>
                    <ns:Dimensions>
                        <ns:Length>12</ns:Length>
                        <ns:Width>12</ns:Width>
                        <ns:Height>12</ns:Height>
                        <ns:Units>IN</ns:Units>
                    </ns:Dimensions>
                    <ns:CustomerReferences>
                        <ns:CustomerReferenceType>CUSTOMER_REFERENCE</ns:CustomerReferenceType>
                        <ns:Value>TC001_01_PT1_ST01_PK01_SNDUS_RCPCA_POS</ns:Value>
                    </ns:CustomerReferences>
                </ns:RequestedPackageLineItems>
            </ns:RequestedShipment>
        </ns:ProcessShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

shipment_data = {
    "shipper": {
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email_address": "Input Your Information",
        "address_lines": ["Input Your Information", "Input Your Information"],
        "city": "MEMPHIS",
        "state_code": "TN",
        "postal_code": "38117",
        "country_code": "US"
    },
    "recipient": {
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email_address": "Input Your Information",
        "address_lines": ["Input Your Information", "Input Your Information"],
        "city": "RICHMOND",
        "state_code": "BC",
        "postal_code": "V7C4v7",
        "country_code": "CA"
    },
    "shipment": {
        "number_of_packages": 1,
        "paid_by": "THIRD_PARTY",
        "packaging_type": "YOUR_PACKAGING",
        "services": ["INTERNATIONAL_PRIORITY"],
        "billing_account_number": "Input Your Information",
        "duty_paid_by": "SENDER",
        "declared_value": "100.",
        "currency": "USD",
        "weight_unit": "LB",
        "dimension_unit": "IN",
        "packages": [
            {
                "id": "1",
                "weight": 20.0,
                "length": 12,
                "width": 12,
                "height": 12,
                "extra": {
                    "CustomerReferences": [
                        {
                            "CustomerReferenceType": "CUSTOMER_REFERENCE",
                            "Value": "TC001_01_PT1_ST01_PK01_SNDUS_RCPCA_POS"
                        }
                    ]
                }
            }
        ],
        "label": {
            "format": "COMMON2D",
            "type": "PNG",
            "extra": {
                "LabelStockType": "PAPER_7X4.75"
            }
        },
        "commodities": [
            {
                "description": "ABCD",
                "extra": {
                    "NumberOfPieces": 1,
                    "CountryOfManufacture": "US",
                    "QuantityUnits": "cm",
                    "Quantity": 1.0,
                    "Weight": {
                        "Unit": "LB",
                        "Value": "1."
                    },
                    "UnitPrice": {
                        "Currency": "USD",
                        "Amount": 1.0
                    },
                    "CustomsVallue": {
                        "Currency": "USD",
                        "Amount": 100.0
                    }
                }
            }
        ],
        "extra": {
            "Payor": {
                "person_name": "Input Your Information",
                "extra": {
                    "ContactId": "12345",
                    "Tins": [
                        {
                            "TinType": "BUSINESS_STATE",
                            "Number": "213456"
                        }
                    ]
                }
            },
            "ExportDetail": {
                "ExportComplianceStatement": "30.37(f)"
            },
            "DropoffType": "REGULAR_PICKUP",
            "SpecialServicesRequested": {
                "SpecialServiceTypes": ["INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS"],
                "InternationalTrafficInArmsRegulationsDetail": {
                    "LicenseOrExemptionNumber": 12345
                }
            },
            "ShippingDocumentSpecification": {
                "ShippingDocumentTypes": "COMMERCIAL_INVOICE",
                "CommercialInvoiceDetail": {
                    "Format": {
                        "ImageType": "PDF",
                        "StockType": "PAPER_LETTER",
                        "ProvideInstructions": True
                    }
                }
            }
        }
    }
}
