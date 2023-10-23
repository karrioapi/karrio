import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTNTShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse, ""]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/expressconnect/shipping/ship",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse, ""]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "tnt_global_express",
    "shipper": {
        "country_code": "GB",
        "city": "Atherstone",
        "postal_code": "CV9 2ry",
        "address_line1": "TEST DO NOT COLLECT1",
        "address_line2": "TEST DO NOT COLLECT2",
        "company_name": "Sender Co 01-008",
        "state_code": "Warwickshire",
        "person_name": "Mr Contact",
        "phone_number": "01827717733",
        "email": "contact@tnt.com",
    },
    "recipient": {
        "address_line1": "TEST DO NOT COLLECT7",
        "address_line2": "TEST DO NOT COLLECT8",
        "company_name": "Receiver Name",
        "postal_code": "1012 AA",
        "country_code": "NL",
        "city": "Amsterdam",
        "person_name": "Mr Bob",
        "phone_number": "1672987432",
        "email": "email@tnt.com",
        "state_tax_id": "VAT-0123",
    },
    "parcels": [
        {
            "height": 20,
            "length": 10,
            "width": 30,
            "weight": 0.4,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "description": "box 1",
            "reference_number": "ref01_008",
            "items": [
                {
                    "title": "paperclips",
                    "quantity": 1,
                    "weight": 0.03,
                    "hs_code": "ABC",
                    "value_amount": 2.30,
                    "description": "metal paperclips",
                    "origin_country": "GB",
                }
            ],
        },
        {
            "height": 60,
            "length": 50,
            "width": 70,
            "weight": 0.8,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "description": "box 2",
            "items": [
                {
                    "title": "paperclips",
                    "quantity": 3,
                    "weight": 0.03,
                    "hs_code": "ABC",
                    "value_amount": 2.30,
                    "description": "metal paperclips",
                    "origin_country": "GB",
                }
            ],
        },
    ],
    "options": {
        "currency": "GBP",
        "shipment_date": "2016-08-15",
        "insurance": 150.00,
        "declared_value": 180.00,
        "tnt_priority": True,
        "email_notification_to": "bob.yourname@tnt.com",
    },
    "reference": "DISKS",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "tnt",
        "carrier_name": "tnt",
        "docs": {},
        "shipment_identifier": "ref01_008",
        "tracking_number": "GE000003364GB",
    },
    [],
]


ShipmentRequest = """<ESHIPPER>
    <LOGIN>
        <COMPANY>username</COMPANY>
        <PASSWORD>password</PASSWORD>
        <APPID>EC</APPID>
        <APPVERSION>3.1</APPVERSION>
    </LOGIN>
    <CONSIGNMENTBATCH>
        <SENDER>
            <COMPANYNAME>Sender Co 01-008</COMPANYNAME>
            <STREETADDRESS1>TEST DO NOT COLLECT1</STREETADDRESS1>
            <STREETADDRESS2>TEST DO NOT COLLECT2</STREETADDRESS2>
            <CITY>Atherstone</CITY>
            <PROVINCE>Warwickshire</PROVINCE>
            <POSTCODE>CV9 2ry</POSTCODE>
            <COUNTRY>GB</COUNTRY>
            <ACCOUNT>3230493849304</ACCOUNT>
            <CONTACTNAME>Mr Contact</CONTACTNAME>
            <CONTACTTELEPHONE>01827717733</CONTACTTELEPHONE>
            <CONTACTEMAIL>contact@tnt.com</CONTACTEMAIL>
            <COLLECTION>
                <SHIPDATE>15/08/2016</SHIPDATE>
            </COLLECTION>
        </SENDER>
        <CONSIGNMENT>
            <CONREF>ref01_008</CONREF>
            <DETAILS>
                <RECEIVER>
                    <COMPANYNAME>Receiver Name</COMPANYNAME>
                    <STREETADDRESS1>TEST DO NOT COLLECT7</STREETADDRESS1>
                    <STREETADDRESS2>TEST DO NOT COLLECT8</STREETADDRESS2>
                    <CITY>Amsterdam</CITY>
                    <POSTCODE>1012 AA</POSTCODE>
                    <COUNTRY>NL</COUNTRY>
                    <VAT>VAT-0123</VAT>
                    <CONTACTNAME>Mr Bob</CONTACTNAME>
                    <CONTACTTELEPHONE>1672987432</CONTACTTELEPHONE>
                    <CONTACTEMAIL>email@tnt.com</CONTACTEMAIL>
                </RECEIVER>
                <CUSTOMERREF>DISKS</CUSTOMERREF>
                <CONTYPE>N</CONTYPE>
                <PAYMENTIND>S</PAYMENTIND>
                <ITEMS>2</ITEMS>
                <TOTALWEIGHT>1.2</TOTALWEIGHT>
                <TOTALVOLUME>0.22</TOTALVOLUME>
                <CURRENCY>GBP</CURRENCY>
                <GOODSVALUE>180</GOODSVALUE>
                <INSURANCEVALUE>150</INSURANCEVALUE>
                <INSURANCECURRENCY>GBP</INSURANCECURRENCY>
                <SERVICE>15N</SERVICE>
                <OPTION>IN</OPTION>
                <OPTION>PR</OPTION>
                <PACKAGE>
                    <ITEMS>1</ITEMS>
                    <DESCRIPTION>box 1</DESCRIPTION>
                    <LENGTH>0.1</LENGTH>
                    <HEIGHT>0.2</HEIGHT>
                    <WIDTH>0.3</WIDTH>
                    <WEIGHT>0.4</WEIGHT>
                    <ARTICLE>
                        <ITEMS>1</ITEMS>
                        <DESCRIPTION>paperclips</DESCRIPTION>
                        <WEIGHT>0.03</WEIGHT>
                        <INVOICEVALUE>2.3</INVOICEVALUE>
                        <INVOICEDESC>metal paperclips</INVOICEDESC>
                        <HTS>ABC</HTS>
                        <COUNTRY>GB</COUNTRY>
                    </ARTICLE>
                </PACKAGE>
                <PACKAGE>
                    <ITEMS>3</ITEMS>
                    <DESCRIPTION>box 2</DESCRIPTION>
                    <LENGTH>0.5</LENGTH>
                    <HEIGHT>0.6</HEIGHT>
                    <WIDTH>0.7</WIDTH>
                    <WEIGHT>0.8</WEIGHT>
                    <ARTICLE>
                        <ITEMS>3</ITEMS>
                        <DESCRIPTION>paperclips</DESCRIPTION>
                        <WEIGHT>0.03</WEIGHT>
                        <INVOICEVALUE>2.3</INVOICEVALUE>
                        <INVOICEDESC>metal paperclips</INVOICEDESC>
                        <HTS>ABC</HTS>
                        <COUNTRY>GB</COUNTRY>
                    </ARTICLE>
                </PACKAGE>
            </DETAILS>
        </CONSIGNMENT>
    </CONSIGNMENTBATCH>
    <ACTIVITY>
        <CREATE>
            <CONREF>ref01_008</CONREF>
        </CREATE>
        <RATE>
            <CONREF>ref01_008</CONREF>
        </RATE>
        <BOOK>
            <CONREF>ref01_008</CONREF>
        </BOOK>
        <SHIP>
            <CONREF>ref01_008</CONREF>
        </SHIP>
        <PRINT>
            <REQUIRED>
                <CONREF>ref01_008</CONREF>
            </REQUIRED>
            <CONNOTE>
                <CONREF>ref01_008</CONREF>
            </CONNOTE>
            <LABEL>
                <CONREF>ref01_008</CONREF>
            </LABEL>
            <MANIFEST>
                <CONREF>ref01_008</CONREF>
            </MANIFEST>
            <INVOICE>
                <CONREF>ref01_008</CONREF>
            </INVOICE>
            <EMAILTO>bob.yourname@tnt.com</EMAILTO>
        </PRINT>
        <SHOW_GROUPCODE/>
    </ACTIVITY>
</ESHIPPER>
"""

LabelRequest = """<labelRequest>
    <consignment key="CON1">
        <consignmentIdentity>
            <consignmentNumber>123456782</consignmentNumber>
            <customerReference>Robert's computer</customerReference>
        </consignmentIdentity>
        <collectionDateTime>2008-06-12T13:00:00</collectionDateTime>
        <sender>
            <name>Karen Bradley</name>
            <addressLine1>TNT Express</addressLine1>
            <addressLine2>TNT House</addressLine2>
            <addressLine3>Holly Lane</addressLine3>
            <town>Atherstone</town>
            <exactMatch>Y</exactMatch>
            <province>Warks</province>
            <postcode>CV9 1TT</postcode>
            <country>GB</country>
        </sender>
        <delivery>
            <name>TNT Corporate Head Office</name>
            <addressLine1>Neptunusstraat 41-63</addressLine1>
            <addressLine2>2132 JA Hoofddorp</addressLine2>
            <town>Amsterdam</town>
            <exactMatch>Y</exactMatch>
            <province />
            <postcode>1011 AA</postcode>
            <country>NL</country>
        </delivery>
        <product>
            <lineOfBusiness>2</lineOfBusiness>
            <groupId>0</groupId>
            <subGroupId>0</subGroupId>
            <id>EX</id>
            <type>N</type>
            <option>PR</option>
        </product>
        <account>
            <accountNumber>100445</accountNumber>
            <accountCountry>GB</accountCountry>
        </account>
        <totalNumberOfPieces>3</totalNumberOfPieces>
        <pieceLine>
            <identifier>1</identifier>
            <goodsDescription>piecelinegoods desc</goodsDescription>
            <pieceMeasurements>
                <length>1.11</length>
                <width>1.11</width>
                <height>1.11</height>
                <weight>1.11</weight>
            </pieceMeasurements>
            <pieces>
                <sequenceNumbers>1,2</sequenceNumbers>
                <pieceReference>keyboard and mouse</pieceReference>
            </pieces>
            <pieces>
                <sequenceNumbers>3</sequenceNumbers>
                <pieceReference>computer tower</pieceReference>
            </pieces>
        </pieceLine>
    </consignment>
</labelRequest>
"""

ShipmentResponse = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<document>
    <GROUPCODE>1736</GROUPCODE>
    <CREATE>
        <CONREF>ref01_008</CONREF>
        <CONNUMBER>GE000003364GB</CONNUMBER>
        <SUCCESS>Y</SUCCESS>
    </CREATE>
    <RATE>
        <PRICE>
            <RATEID>ref01_008</RATEID>
            <SERVICE>15N</SERVICE>
            <SERVICEDESC>Express</SERVICEDESC>
            <OPTION>IN</OPTION>
            <OPTIONDESC>Insurance</OPTIONDESC>
            <CURRENCY>GBP</CURRENCY>
            <RATE>996.61</RATE>
            <RESULT>Y</RESULT>
        </PRICE>
    </RATE>
    <BOOK>
        <CONSIGNMENT>
            <CONREF>ref01_008</CONREF>
            <CONNUMBER>GE000003364GB</CONNUMBER>
            <SUCCESS>Y</SUCCESS>
            <FIRSTTIMETRADER>Y</FIRSTTIMETRADER>
        </CONSIGNMENT>
    </BOOK>
    <SHIP>
        <CONSIGNMENT>
            <CONREF>ref01_008</CONREF>
            <CONNUMBER>GE000003364GB</CONNUMBER>
            <SUCCESS>Y</SUCCESS>
        </CONSIGNMENT>
    </SHIP>
    <PRINT>
        <CONNOTE>CREATED</CONNOTE>
        <LABEL>CREATED</LABEL>
        <MANIFEST>CREATED</MANIFEST>
        <INVOICE>CREATED</INVOICE>
    </PRINT>
</document>
"""

LabelResponse = """<?xml version="1.0" encoding="UTF-8"?>
<labelResponse>
    <consignment key="CON1">
        <pieceLabelData>
            <pieceNumber>1</pieceNumber>
            <weightDisplay code="1.11" renderInstructions="yes">1.11kg</weightDisplay>
            <pieceReference><![CDATA[piece1]]></pieceReference>
            <barcode symbology="128C">0000000000000000000000000000</barcode>
            <twoDBarcode symbology="pdf417"><![CDATA[123456782|123456782||1|100445|John Smith|TNT Express|HOOFDDORP|2132 LS|NL|S|TNT Corporate Head Office|Neptunusstraat 41-63|HOOFDDORP|2132 LS|NL|100|EX|N|PR||||0|12.34|EUR|N|||piecelinegoods desc|3|1.11|1.3676310000000003|N|16 Oct 2023|07:24:00]]></twoDBarcode>
        </pieceLabelData>
        <pieceLabelData>
            <pieceNumber>2</pieceNumber>
            <weightDisplay code="1.11" renderInstructions="yes">1.11kg</weightDisplay>
            <pieceReference><![CDATA[piece1]]></pieceReference>
            <barcode symbology="128C">0000000000000000000000000000</barcode>
            <twoDBarcode symbology="pdf417"><![CDATA[123456782|123456782||2|100445|John Smith|TNT Express|HOOFDDORP|2132 LS|NL|S|TNT Corporate Head Office|Neptunusstraat 41-63|HOOFDDORP|2132 LS|NL|100|EX|N|PR||||0|12.34|EUR|N|||piecelinegoods desc|3|1.11|1.3676310000000003|N|16 Oct 2023|07:24:00]]></twoDBarcode>
        </pieceLabelData>
        <pieceLabelData>
            <pieceNumber>3</pieceNumber>
            <weightDisplay code="1.11" renderInstructions="yes">1.11kg</weightDisplay>
            <pieceReference><![CDATA[piece3]]></pieceReference>
            <barcode symbology="128C">0000000000000000000000000000</barcode>
            <twoDBarcode symbology="pdf417"><![CDATA[123456782|123456782||3|100445|John Smith|TNT Express|HOOFDDORP|2132 LS|NL|S|TNT Corporate Head Office|Neptunusstraat 41-63|HOOFDDORP|2132 LS|NL|100|EX|N|PR||||0|12.34|EUR|N|||piecelinegoods desc|3|1.11|1.3676310000000003|N|16 Oct 2023|07:24:00]]></twoDBarcode>
        </pieceLabelData>
        <consignmentLabelData>
            <consignmentNumber>123456782</consignmentNumber>
            <sender>
                <name><![CDATA[John Smith]]></name>
                <addressLine1><![CDATA[TNT Express]]></addressLine1>
                <addressLine2><![CDATA[TNT House]]></addressLine2>
                <town><![CDATA[HOOFDDORP]]></town>
                <province />
                <postcode><![CDATA[2132 LS]]></postcode>
                <country><![CDATA[NL]]></country>
            </sender>
            <delivery>
                <name><![CDATA[**TEST LABEL - DO NOT SHIP**]]></name>
                <addressLine1><![CDATA[ ]]></addressLine1>
                <addressLine2><![CDATA[ ]]></addressLine2>
                <town><![CDATA[ ]]></town>
                <province><![CDATA[ ]]></province>
                <postcode><![CDATA[ ]]></postcode>
                <country><![CDATA[ ]]></country>
            </delivery>
            <account>
                <accountNumber>100445</accountNumber>
                <accountCountry>GB</accountCountry>
            </account>
            <totalNumberOfPieces>3</totalNumberOfPieces>
            <product id="EX">Express (ND)</product>
            <option id="PR"><![CDATA[PR]]></option>
            <collectionDate>2023-10-16</collectionDate>
            <marketDisplay code="1" renderInstructions="yes"><![CDATA[DOM]]></marketDisplay>
            <transportDisplay code="3" renderInstructions="yes"><![CDATA[ROAD]]></transportDisplay>
            <freeCirculationDisplay code="" renderInstructions="no" />
            <sortSplitText><![CDATA[2]]></sortSplitText>
            <xrayDisplay code="" renderInstructions="no" />
            <originDepot>
                <depotCode>SP8</depotCode>
            </originDepot>
            <transitDepots />
            <destinationDepot>
                <depotCode>SP8</depotCode>
                <dueDayOfMonth>17</dueDayOfMonth>
                <dueDate>2023-10-17</dueDate>
            </destinationDepot>
            <microzone code="" renderInstructions="no" />
            <clusterCode>26</clusterCode>
            <legalComments />
            <cashAmount code="12.34" renderInstructions="yes">GBP 12.34</cashAmount>
            <specialInstructions />
            <bulkShipment code="Y" renderInstructions="yes">BSH</bulkShipment>
        </consignmentLabelData>
    </consignment>
</labelResponse>
"""
