import unittest
import logging
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCanparTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[0], TrackingRequestXML)

    def test_get_tracking(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanparAddonsService.CanparAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:trackByBarcodeV2"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.canpar.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response),
                ParsedTrackingResponse,
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "canpar",
            "carrier_name": "canpar",
            "delivered": True,
            "estimated_delivery": "2011-03-07",
            "events": [
                {
                    "code": "DEL",
                    "date": "2011-03-08",
                    "description": "DELIVERED",
                    "location": "1785 FROBISHER ST, UNIT C, SUDBURY, ON, CA",
                    "time": "09:14 AM",
                },
                {
                    "code": "INA",
                    "date": "2011-03-08",
                    "description": "ARRIVAL AT INTERLINE",
                    "location": "1785 FROBISHER ST, UNIT C, SUDBURY, ON, CA",
                    "time": "06:15 AM",
                },
                {
                    "code": "INO",
                    "date": "2011-03-07",
                    "description": "INTERLINE OUTBOUND",
                    "location": "JOHN CYOPECK CENTRE, 205 NEW TORONTO STREET, ETOBICOKE, ON, CA",
                    "time": "23:05 PM",
                },
                {
                    "code": "ARR",
                    "date": "2011-03-07",
                    "description": "ARRIVAL AT HUB/TERMINAL FROM BULK/CITY TRAILER",
                    "location": "JOHN CYOPECK CENTRE, 205 NEW TORONTO STREET, ETOBICOKE, ON, CA",
                    "time": "23:03 PM",
                },
                {
                    "code": "PIC",
                    "date": "2011-03-07",
                    "description": "PICKUP FROM CUSTOMER/SHIPPER",
                    "location": "JOHN CYOPECK CENTRE, 205 NEW TORONTO STREET, ETOBICOKE, ON, CA",
                    "time": "14:53 PM",
                },
            ],
            "info": {
                "carrier_tracking_link": "http://www.canpar.com/en/track/TrackingAction.do?locale=en&type=0&reference=D999999988030400000008",
                "shipment_destination_country": "CA",
                "shipment_destination_postal_code": "P3E5P9",
                "shipment_service": "GROUND",
                "shipping_date": "2011-03-07",
            },
            "tracking_number": "D999999988030400000008",
        }
    ],
    [],
]


TrackingRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:trackByBarcodeV2>
            <ws:request>
                <xsd:barcode>1Z12345E6205277936</xsd:barcode>
                <xsd:track_shipment>true</xsd:track_shipment>
            </ws:request>
        </ws:trackByBarcodeV2>
    </soap:Body>
</soap:Envelope>
"""

TrackingResponseXML = """<wrapper>
    <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
        <soapenv:Body>
            <ns:trackByBarcodeResponse xmlns:ns="http://ws.canparaddons.canpar.com">
                <ns:return xmlns:ax21="http://ws.dto.canshipws.canpar.com/xsd" xmlns:ax23="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax21:TrackByBarcodeRs">
                    <ax21:error xsi:nil="true" />
                    <ax21:result xsi:type="ax23:TrackingResult">
                        <ax23:barcode>D999999988030400000008</ax23:barcode>
                        <ax23:consignee_address xsi:type="ax23:Address">
                            <ax23:address_id />
                            <ax23:address_line_1>199 LARCH ST</ax23:address_line_1>
                            <ax23:address_line_2>3RD FLOOR (PRINT SHOP)</ax23:address_line_2>
                            <ax23:address_line_3 />
                            <ax23:attention />
                            <ax23:city>SUDBURY</ax23:city>
                            <ax23:country>CA</ax23:country>
                            <ax23:email />
                            <ax23:extension />
                            <ax23:id>-1</ax23:id>
                            <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                            <ax23:name />
                            <ax23:phone />
                            <ax23:postal_code>P3E5P9</ax23:postal_code>
                            <ax23:province>ON</ax23:province>
                            <ax23:residential>false</ax23:residential>
                            <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                        </ax23:consignee_address>
                        <ax23:delivered>false</ax23:delivered>
                        <ax23:estimated_delivery_date>20110307</ax23:estimated_delivery_date>
                        <ax23:events xsi:type="ax23:TrackingEvent">
                            <ax23:address xsi:type="ax23:Address">
                                <ax23:address_id />
                                <ax23:address_line_1>1785 FROBISHER ST, UNIT C</ax23:address_line_1>
                                <ax23:address_line_2 />
                                <ax23:address_line_3 />
                                <ax23:attention />
                                <ax23:city>SUDBURY</ax23:city>
                                <ax23:country>CA</ax23:country>
                                <ax23:email />
                                <ax23:extension />
                                <ax23:id>-1</ax23:id>
                                <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                                <ax23:name />
                                <ax23:phone />
                                <ax23:postal_code>P3A6C8</ax23:postal_code>
                                <ax23:province>ON</ax23:province>
                                <ax23:residential>false</ax23:residential>
                                <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                            </ax23:address>
                            <ax23:code>DEL</ax23:code>
                            <ax23:code_description_en>DELIVERED</ax23:code_description_en>
                            <ax23:code_description_fr>LIVR…</ax23:code_description_fr>
                            <ax23:comment xsi:nil="true" />
                            <ax23:local_date_time>20110308 091442</ax23:local_date_time>
                            <ax23:time_shift>3</ax23:time_shift>
                        </ax23:events>
                        <ax23:events xsi:type="ax23:TrackingEvent">
                            <ax23:address xsi:type="ax23:Address">
                                <ax23:address_id />
                                <ax23:address_line_1>1785 FROBISHER ST, UNIT C</ax23:address_line_1>
                                <ax23:address_line_2 />
                                <ax23:address_line_3 />
                                <ax23:attention />
                                <ax23:city>SUDBURY</ax23:city>
                                <ax23:country>CA</ax23:country>
                                <ax23:email />
                                <ax23:extension />
                                <ax23:id>-1</ax23:id>
                                <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                                <ax23:name />
                                <ax23:phone />
                                <ax23:postal_code>P3A6C8</ax23:postal_code>
                                <ax23:province>ON</ax23:province>
                                <ax23:residential>false</ax23:residential>
                                <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                            </ax23:address>
                            <ax23:code>INA</ax23:code>
                            <ax23:code_description_en>ARRIVAL AT INTERLINE</ax23:code_description_en>
                            <ax23:code_description_fr>ARRIV… ¿ LA FIRME DE TRANSPORT DE LIAISON</ax23:code_description_fr>
                            <ax23:comment xsi:nil="true" />
                            <ax23:local_date_time>20110308 061542</ax23:local_date_time>
                            <ax23:time_shift>3</ax23:time_shift>
                        </ax23:events>
                        <ax23:events xsi:type="ax23:TrackingEvent">
                            <ax23:address xsi:type="ax23:Address">
                                <ax23:address_id />
                                <ax23:address_line_1>JOHN CYOPECK CENTRE</ax23:address_line_1>
                                <ax23:address_line_2>205 NEW TORONTO STREET</ax23:address_line_2>
                                <ax23:address_line_3 />
                                <ax23:attention />
                                <ax23:city>ETOBICOKE</ax23:city>
                                <ax23:country>CA</ax23:country>
                                <ax23:email />
                                <ax23:extension />
                                <ax23:id>-1</ax23:id>
                                <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                                <ax23:name />
                                <ax23:phone />
                                <ax23:postal_code>M8V0A1</ax23:postal_code>
                                <ax23:province>ON</ax23:province>
                                <ax23:residential>false</ax23:residential>
                                <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                            </ax23:address>
                            <ax23:code>INO</ax23:code>
                            <ax23:code_description_en>INTERLINE OUTBOUND</ax23:code_description_en>
                            <ax23:code_description_fr>COLIS REMIS ¿ UNE FIRME DE TRANSPORT DE LIAISON</ax23:code_description_fr>
                            <ax23:comment xsi:nil="true" />
                            <ax23:local_date_time>20110307 230559</ax23:local_date_time>
                            <ax23:time_shift>3</ax23:time_shift>
                        </ax23:events>
                        <ax23:events xsi:type="ax23:TrackingEvent">
                            <ax23:address xsi:type="ax23:Address">
                                <ax23:address_id />
                                <ax23:address_line_1>JOHN CYOPECK CENTRE</ax23:address_line_1>
                                <ax23:address_line_2>205 NEW TORONTO STREET</ax23:address_line_2>
                                <ax23:address_line_3 />
                                <ax23:attention />
                                <ax23:city>ETOBICOKE</ax23:city>
                                <ax23:country>CA</ax23:country>
                                <ax23:email />
                                <ax23:extension />
                                <ax23:id>-1</ax23:id>
                                <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                                <ax23:name />
                                <ax23:phone />
                                <ax23:postal_code>M8V0A1</ax23:postal_code>
                                <ax23:province>ON</ax23:province>
                                <ax23:residential>false</ax23:residential>
                                <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                            </ax23:address>
                            <ax23:code>ARR</ax23:code>
                            <ax23:code_description_en>ARRIVAL AT HUB/TERMINAL FROM BULK/CITY TRAILER</ax23:code_description_en>
                            <ax23:code_description_fr>COLIS ARRIV… AU CENTRE PAR REMORQUE DE TRANSPORT EN VRAC OU LOCAL</ax23:code_description_fr>
                            <ax23:comment xsi:nil="true" />
                            <ax23:local_date_time>20110307 230314</ax23:local_date_time>
                            <ax23:time_shift>3</ax23:time_shift>
                        </ax23:events>
                        <ax23:events xsi:type="ax23:TrackingEvent">
                            <ax23:address xsi:type="ax23:Address">
                                <ax23:address_id />
                                <ax23:address_line_1>JOHN CYOPECK CENTRE</ax23:address_line_1>
                                <ax23:address_line_2>205 NEW TORONTO STREET</ax23:address_line_2>
                                <ax23:address_line_3 />
                                <ax23:attention />
                                <ax23:city>ETOBICOKE</ax23:city>
                                <ax23:country>CA</ax23:country>
                                <ax23:email />
                                <ax23:extension />
                                <ax23:id>-1</ax23:id>
                                <ax23:inserted_on>2015-01-22T23:17:26.681Z</ax23:inserted_on>
                                <ax23:name />
                                <ax23:phone />
                                <ax23:postal_code>M8V0A1</ax23:postal_code>
                                <ax23:province>ON</ax23:province>
                                <ax23:residential>false</ax23:residential>
                                <ax23:updated_on>2015-01-22T23:17:26.681Z</ax23:updated_on>
                            </ax23:address>
                            <ax23:code>PIC</ax23:code>
                            <ax23:code_description_en>PICKUP FROM CUSTOMER/SHIPPER</ax23:code_description_en>
                            <ax23:code_description_fr>CUEILLETTE EFFECTU…E PAR LE CLIENT, L'EXP…DITEUR.</ax23:code_description_fr>
                            <ax23:comment xsi:nil="true" />
                            <ax23:local_date_time>20110307 145353</ax23:local_date_time>
                            <ax23:time_shift>3</ax23:time_shift>
                        </ax23:events>
                        <ax23:reference_num xsi:nil="true" />
                        <ax23:service_description_en>GROUND</ax23:service_description_en>
                        <ax23:service_description_fr>GROUND (fr)</ax23:service_description_fr>
                        <ax23:shipping_date>20110307</ax23:shipping_date>
                        <ax23:signature xsi:nil="true" />
                        <ax23:signed_by xsi:nil="true" />
                        <ax23:tracking_url_en>http://www.canpar.com/en/track/TrackingAction.do?locale=en&amp;type=0&amp;reference=D999999988030400000008</ax23:tracking_url_en>
                        <ax23:tracking_url_fr>http://www.canpar.com/fr/track/TrackingAction.do?locale=fr&amp;type=0&amp;reference=D999999988030400000008</ax23:tracking_url_fr>
                    </ax21:result>
                </ns:return>
            </ns:trackByBarcodeResponse>
        </soapenv:Body>
    </soapenv:Envelope>
</wrapper>
"""
