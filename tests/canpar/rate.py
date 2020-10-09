import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship import Rating
from purplship.core.models import RateRequest
from tests.canpar.fixture import gateway
from datetime import datetime


class TestCanparRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    # def test_create_rate_request(self):
    #     request = gateway.mapper.create_rate_request(self.RateRequest)
    #
    #     self.assertEqual(request.serialize(), RateRequestXML)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "services": ["canadapost_expedited_parcel"],
}

ParsedQuoteResponse = []


RateRequestXML = """<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns3:rateShipment xmlns:ns3="http://ws.onlinerating.canshipws.canpar.com">
            <ns3:request>
                <ns1:apply_association_discount xmlns:ns1="http://ws.dto.canshipws.canpar.com/xsd">false</ns1:apply_association_discount>
                <ns1:apply_individual_discount xmlns:ns1="http://ws.dto.canshipws.canpar.com/xsd">false</ns1:apply_individual_discount>
                <ns1:apply_invoice_discount xmlns:ns1="http://ws.dto.canshipws.canpar.com/xsd">false</ns1:apply_invoice_discount>
                <ns1:password xmlns:ns1="http://ws.dto.canshipws.canpar.com/xsd">password</ns1:password>
                <shipment xmlns="http://ws.dto.canshipws.canpar.com/xsd">
                    <ns2:billed_weight xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:billed_weight>
                    <ns2:billed_weight_unit xmlns:ns2="http://dto.canshipws.canpar.com/xsd">L</ns2:billed_weight_unit>
                    <ns2:cod_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:cod_charge>
                    <ns2:cod_type xmlns:ns2="http://dto.canshipws.canpar.com/xsd">N</ns2:cod_type>
                    <ns2:collect_shipper_num xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:consolidation_type xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:cos xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:cos>
                    <ns2:cos_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:cos_charge>
                    <delivery_address xmlns="http://dto.canshipws.canpar.com/xsd">
                        <address_id>A1</address_id>
                        <address_line_1>1 TEST ST</address_line_1>
                        <address_line_2 />
                        <address_line_3 />
                        <attention />
                        <city>TORONTO</city>
                        <country>CA</country>
                        <email>1@1.COM,2@2.COM</email>
                        <extension>23</extension>
                        <id>-1</id>
                        <name>TEST ADDRESS</name>
                        <phone>4161234567</phone>
                        <postal_code>M4X1W7</postal_code>
                        <province>ON</province>
                        <residential>false</residential>
                    </delivery_address>
                    <ns2:description xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:dg xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:dg>
                    <ns2:dg_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:dg_charge>
                    <ns2:dimention_unit xmlns:ns2="http://dto.canshipws.canpar.com/xsd">I</ns2:dimention_unit>
                    <ns2:dv_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:dv_charge>
                    <ns2:ea_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:ea_charge>
                    <ns2:ea_zone xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0</ns2:ea_zone>
                    <ns2:freight_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:freight_charge>
                    <ns2:fuel_surcharge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:fuel_surcharge>
                    <ns2:handling xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:handling>
                    <ns2:handling_type xmlns:ns2="http://dto.canshipws.canpar.com/xsd">$</ns2:handling_type>
                    <ns2:id xmlns:ns2="http://dto.canshipws.canpar.com/xsd">-1</ns2:id>
                    <ns2:instruction xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:manifest_num xmlns:ns2="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="1" />
                    <ns2:nsr xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:nsr>
                    <packages xmlns="http://dto.canshipws.canpar.com/xsd">
                        <alternative_reference />
                        <barcode />
                        <billed_weight>0.0</billed_weight>
                        <cod xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="1" />
                        <cost_centre />
                        <declared_value>0.0</declared_value>
                        <dim_weight>0.0</dim_weight>
                        <dim_weight_flag>false</dim_weight_flag>
                        <height>0.0</height>
                        <id>-1</id>
                        <length>0.0</length>
                        <min_weight_flag>false</min_weight_flag>
                        <package_num>0</package_num>
                        <package_reference>0</package_reference>
                        <reference />
                        <reported_weight>1.0</reported_weight>
                        <store_num />
                        <width>0.0</width>
                        <xc>false</xc>
                    </packages>
                    <pickup_address xmlns="http://dto.canshipws.canpar.com/xsd">
                        <address_id>A1</address_id>
                        <address_line_1>1 TEST ST</address_line_1>
                        <address_line_2 />
                        <address_line_3 />
                        <attention />
                        <city>TORONTO</city>
                        <country>CA</country>
                        <email>1@1.COM,2@2.COM</email>
                        <extension>23</extension>
                        <id>-1</id>
                        <name>TEST ADDRESS</name>
                        <phone>4161234567</phone>
                        <postal_code>M4X1W7</postal_code>
                        <province>ON</province>
                        <residential>false</residential>
                    </pickup_address>
                    <ns2:premium xmlns:ns2="http://dto.canshipws.canpar.com/xsd">N</ns2:premium>
                    <ns2:premium_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:premium_charge>
                    <ns2:proforma xmlns:ns2="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="1" />
                    <ns2:ra_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:ra_charge>
                    <ns2:reported_weight_unit xmlns:ns2="http://dto.canshipws.canpar.com/xsd">L</ns2:reported_weight_unit>
                    <ns2:rural_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:rural_charge>
                    <ns2:send_email_to_delivery xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:send_email_to_delivery>
                    <ns2:send_email_to_pickup xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:send_email_to_pickup>
                    <ns2:service_type xmlns:ns2="http://dto.canshipws.canpar.com/xsd">1</ns2:service_type>
                    <ns2:shipment_status xmlns:ns2="http://dto.canshipws.canpar.com/xsd">R</ns2:shipment_status>
                    <ns2:shipper_num xmlns:ns2="http://dto.canshipws.canpar.com/xsd">99999999</ns2:shipper_num>
                    <ns2:shipping_date xmlns:ns2="http://dto.canshipws.canpar.com/xsd">2012-06-15T00:00:00.000-04:00</ns2:shipping_date>
                    <ns2:tax_charge_1 xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:tax_charge_1>
                    <ns2:tax_charge_2 xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:tax_charge_2>
                    <ns2:tax_code_1 xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:tax_code_2 xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:transit_time xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0</ns2:transit_time>
                    <ns2:transit_time_guaranteed xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:transit_time_guaranteed>
                    <ns2:user_id xmlns:ns2="http://dto.canshipws.canpar.com/xsd" />
                    <ns2:voided xmlns:ns2="http://dto.canshipws.canpar.com/xsd">false</ns2:voided>
                    <ns2:xc_charge xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0.0</ns2:xc_charge>
                    <ns2:zone xmlns:ns2="http://dto.canshipws.canpar.com/xsd">0</ns2:zone>
                </shipment>
                <ns1:user_id xmlns:ns1="http://ws.dto.canshipws.canpar.com/xsd">user_id</ns1:user_id>
            </ns3:request>
        </ns3:rateShipment>
    </soapenv:Body>
</soapenv:Envelope>
"""

RateResponseXml = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:rateShipmentResponse xmlns:ns="http://ws.onlinerating.canshipws.canpar.com">
            <ns:return xmlns:ax25="http://ws.dto.canshipws.canpar.com/xsd" xmlns:ax27="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax25:RateShipmentRs">
                <ax25:error xsi:nil="true" />
                <ax25:processShipmentResult xsi:type="ax27:ProcessShipmentResult">
                    <ax27:shipment xsi:type="ax27:Shipment">
                        <ax27:airport_code />
                        <ax27:billed_weight>1.0</ax27:billed_weight>
                        <ax27:billed_weight_unit>L</ax27:billed_weight_unit>
                        <ax27:cod_charge>0.0</ax27:cod_charge>
                        <ax27:cod_type>N</ax27:cod_type>
                        <ax27:collect_shipper_num />
                        <ax27:consolidation_type />
                        <ax27:cos>false</ax27:cos>
                        <ax27:cos_charge>0.0</ax27:cos_charge>
                        <ax27:delivery_address xsi:type="ax27:Address">
                            <ax27:address_id>A1</ax27:address_id>
                            <ax27:address_line_1>1 TEST ST</ax27:address_line_1>
                            <ax27:address_line_2 />
                            <ax27:address_line_3 />
                            <ax27:attention />
                            <ax27:city>TORONTO</ax27:city>
                            <ax27:country>CA</ax27:country>
                            <ax27:email>1@1.COM,2@2.COM</ax27:email>
                            <ax27:extension>23</ax27:extension>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:name>TEST ADDRESS</ax27:name>
                            <ax27:phone>4161234567</ax27:phone>
                            <ax27:postal_code>M4X1W7</ax27:postal_code>
                            <ax27:province>ON</ax27:province>
                            <ax27:residential>false</ax27:residential>
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        </ax27:delivery_address>
                        <ax27:description />
                        <ax27:dg>false</ax27:dg>
                        <ax27:dg_charge>0.0</ax27:dg_charge>
                        <ax27:dimention_unit>I</ax27:dimention_unit>
                        <ax27:dv_charge>0.0</ax27:dv_charge>
                        <ax27:ea_charge>0.0</ax27:ea_charge>
                        <ax27:ea_zone>0</ax27:ea_zone>
                        <ax27:estimated_delivery_date>2012-06-18T04:00:00.000Z</ax27:estimated_delivery_date>
                        <ax27:freight_charge>7.57</ax27:freight_charge>
                        <ax27:fuel_surcharge>0.0</ax27:fuel_surcharge>
                        <ax27:handling>0.0</ax27:handling>
                        <ax27:handling_type>$</ax27:handling_type>
                        <ax27:id>-1</ax27:id>
                        <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                        <ax27:instruction />
                        <ax27:manifest_num xsi:nil="true" />
                        <ax27:nsr>false</ax27:nsr>
                        <ax27:packages xsi:type="ax27:Package">
                            <ax27:alternative_reference />
                            <ax27:barcode />
                            <ax27:billed_weight>1.0</ax27:billed_weight>
                            <ax27:cod xsi:nil="true" />
                            <ax27:cost_centre />
                            <ax27:declared_value>0.0</ax27:declared_value>
                            <ax27:dim_weight>0.0</ax27:dim_weight>
                            <ax27:dim_weight_flag>false</ax27:dim_weight_flag>
                            <ax27:height>0.0</ax27:height>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:length>0.0</ax27:length>
                            <ax27:min_weight_flag>false</ax27:min_weight_flag>
                            <ax27:package_num>0</ax27:package_num>
                            <ax27:package_reference>0</ax27:package_reference>
                            <ax27:reference />
                            <ax27:reported_weight>1.0</ax27:reported_weight>
                            <ax27:store_num />
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                            <ax27:width>0.0</ax27:width>
                            <ax27:xc>false</ax27:xc>
                        </ax27:packages>
                        <ax27:pickup_address xsi:type="ax27:Address">
                            <ax27:address_id>A1</ax27:address_id>
                            <ax27:address_line_1>1 TEST ST</ax27:address_line_1>
                            <ax27:address_line_2 />
                            <ax27:address_line_3 />
                            <ax27:attention />
                            <ax27:city>TORONTO</ax27:city>
                            <ax27:country>CA</ax27:country>
                            <ax27:email>1@1.COM,2@2.COM</ax27:email>
                            <ax27:extension>23</ax27:extension>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:name>TEST ADDRESS</ax27:name>
                            <ax27:phone>4161234567</ax27:phone>
                            <ax27:postal_code>M4X1W7</ax27:postal_code>
                            <ax27:province>ON</ax27:province>
                            <ax27:residential>false</ax27:residential>
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        </ax27:pickup_address>
                        <ax27:premium>N</ax27:premium>
                        <ax27:premium_charge>0.0</ax27:premium_charge>
                        <ax27:proforma xsi:nil="true" />
                        <ax27:ra_charge>2.75</ax27:ra_charge>
                        <ax27:reported_weight_unit>L</ax27:reported_weight_unit>
                        <ax27:rural_charge>0.0</ax27:rural_charge>
                        <ax27:send_email_to_delivery>false</ax27:send_email_to_delivery>
                        <ax27:send_email_to_pickup>false</ax27:send_email_to_pickup>
                        <ax27:service_type>1</ax27:service_type>
                        <ax27:shipment_status>R</ax27:shipment_status>
                        <ax27:shipper_num>99999999</ax27:shipper_num>
                        <ax27:shipping_date>2012-06-15T04:00:00.000Z</ax27:shipping_date>
                        <ax27:tax_charge_1>1.34</ax27:tax_charge_1>
                        <ax27:tax_charge_2>0.0</ax27:tax_charge_2>
                        <ax27:tax_code_1>ONHST</ax27:tax_code_1>
                        <ax27:tax_code_2 />
                        <ax27:transit_time>1</ax27:transit_time>
                        <ax27:transit_time_guaranteed>false</ax27:transit_time_guaranteed>
                        <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        <ax27:user_id>WSADMIN@DEMO.COM</ax27:user_id>
                        <ax27:voided>false</ax27:voided>
                        <ax27:xc_charge>0.0</ax27:xc_charge>
                        <ax27:zone>1</ax27:zone>
                    </ax27:shipment>
                </ax25:processShipmentResult>
            </ns:return>
        </ns:rateShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
