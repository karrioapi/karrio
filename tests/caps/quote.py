import unittest
from unittest.mock import patch
from gds_helpers import to_xml, to_dict, export
from pycaps.rating import mailing_scenario
from purplship.domain.Types import RateRequest
from tests.caps.fixture import proxy
from tests.utils import strip, get_node_from_xml
from datetime import datetime


class TestCanadaPostQuote(unittest.TestCase):
    def setUp(self):
        self.mailing_scenario = mailing_scenario()
        self.mailing_scenario.build(to_xml(QuoteRequestXml))

    def test_create_quote_request(self):
        shipper = {
            "postal_code": "H8Z2Z3",
            "country_code": "CA",
            "account_number": "1234567",
        }
        recipient = {"postal_code": "H8Z2V4", "country_code": "CA"}
        shipment = {
            "items": [{"height": 3, "length": 10, "width": 3, "weight": 4.0}],
            "services": ["Expedited_Parcel"],
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "extra": {"options": []},
        }
        payload = RateRequest(shipper=shipper, recipient=recipient, shipment=shipment)

        mailing_scenario_ = proxy.mapper.create_quote_request(payload)

        self.assertEqual(export(mailing_scenario_), export(self.mailing_scenario))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_get_quotes(self, http_mock):
        proxy.get_quotes(self.mailing_scenario)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml))
        self.assertEqual(reqUrl, "%s/rs/ship/price" % (proxy.client.server_url))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(to_xml(QuoteResponseXml))
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteResponse))

    def test_parse_quote_parsing_error(self):
        parsed_response = proxy.mapper.parse_quote_response(to_xml(QuoteParsingError))
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteParsingError))

    def test_parse_quote_missing_args_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteMissingArgsError)
        )
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteMissingArgsError))


if __name__ == "__main__":
    unittest.main()


ParsedQuoteParsingError = [
    [],
    [
        {
            "carrier": "CanadaPost",
            "code": "AA004",
            "message": "You cannot mail on behalf of the requested customer.",
        }
    ],
]

ParsedQuoteMissingArgsError = [
    [],
    [
        {
            "carrier": "CanadaPost",
            "code": "Server",
            "message": "/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v3}parcel-characteristics with anonymous type, found </parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v3), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v3}weight, {http://www.canadapost.ca/ws/ship/rate-v3}dimensions, {http://www.canadapost.ca/ws/ship/rate-v3}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v3}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v3}oversized]",
        }
    ],
]

ParsedQuoteResponse = [
    [
        {
            "base_charge": 9.59,
            "carrier": "CanadaPost",
            "currency": "CAD",
            "delivery_date": "2011-10-24",
            "discount": 0.620_000_000_000_000_1,
            "duties_and_taxes": 0.0,
            "extra_charges": [
                {"amount": -0.29, "currency": "CAD", "name": "Automation discount"},
                {"amount": 0.91, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "service_name": "Expedited Parcel",
            "service_type": "DOM.EP",
            "total_charge": 10.21,
        },
        {
            "base_charge": 22.64,
            "carrier": "CanadaPost",
            "currency": "CAD",
            "delivery_date": "2011-10-21",
            "discount": 2.56,
            "duties_and_taxes": 0.0,
            "extra_charges": [
                {"amount": -0.68, "currency": "CAD", "name": "Automation discount"},
                {"amount": 3.24, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "service_name": "Priority Courier",
            "service_type": "DOM.PC",
            "total_charge": 25.2,
        },
        {
            "base_charge": 9.59,
            "carrier": "CanadaPost",
            "currency": "CAD",
            "delivery_date": "2011-10-26",
            "discount": 0.620_000_000_000_000_1,
            "duties_and_taxes": 0.0,
            "extra_charges": [
                {"amount": -0.29, "currency": "CAD", "name": "Automation discount"},
                {"amount": 0.91, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "service_name": "Regular Parcel",
            "service_type": "DOM.RP",
            "total_charge": 10.21,
        },
        {
            "base_charge": 12.26,
            "carrier": "CanadaPost",
            "currency": "CAD",
            "delivery_date": "2011-10-24",
            "discount": 1.38,
            "duties_and_taxes": 0.0,
            "extra_charges": [
                {"amount": -0.37, "currency": "CAD", "name": "Automation discount"},
                {"amount": 1.75, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "service_name": "Xpresspost",
            "service_type": "DOM.XP",
            "total_charge": 13.64,
        },
    ],
    [],
]


QuoteParsingError = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>AA004</code>
        <description>You cannot mail on behalf of the requested customer.</description>
    </message>
</messages>
"""

QuoteMissingArgsError = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>Server</code>
        <description>/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v3}parcel-characteristics with anonymous type, found &lt;/parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v3), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v3}weight, {http://www.canadapost.ca/ws/ship/rate-v3}dimensions, {http://www.canadapost.ca/ws/ship/rate-v3}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v3}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v3}oversized]</description>
    </message>
</messages>
"""

QuoteRequestXml = f"""<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v3">
    <customer-number>1234567</customer-number>
    <expected-mailing-date>{datetime.today().strftime('%Y-%m-%d')}</expected-mailing-date>
    <parcel-characteristics>
        <weight>4.</weight>
        <dimensions>
            <length>10.</length>
            <width>3.</width>
            <height>3.</height>
        </dimensions>
    </parcel-characteristics>
    <services>
        <service-code>DOM.EP</service-code>
    </services>
    <origin-postal-code>H8Z2Z3</origin-postal-code>
    <destination>
        <domestic>
            <postal-code>H8Z2V4</postal-code>
        </domestic>
    </destination>
</mailing-scenario>
"""

QuoteResponseXml = """<price-quotes>
   <price-quote>
      <service-code>DOM.EP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.EP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Expedited Parcel</service-name>
      <price-details>
         <base>9.59</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>10.21</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.29</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>0.91</adjustment-cost>
               <qualifier>
                  <percent>9.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>2</expected-transit-time>
         <expected-delivery-date>2011-10-24</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.PC</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.PC?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Priority Courier</service-name>
      <price-details>
         <base>22.64</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>25.20</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.68</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>3.24</adjustment-cost>
               <qualifier>
                  <percent>14.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>1</expected-transit-time>
         <expected-delivery-date>2011-10-21</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.RP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.RP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Regular Parcel</service-name>
      <price-details>
         <base>9.59</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>10.21</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
               <qualifier>
                  <included>true</included>
               </qualifier>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.29</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>0.91</adjustment-cost>
               <qualifier>
                  <percent>9.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>false</guaranteed-delivery>
         <expected-transit-time>4</expected-transit-time>
         <expected-delivery-date>2011-10-26</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.XP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.XP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Xpresspost</service-name>
      <price-details>
         <base>12.26</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>13.64</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.37</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>1.75</adjustment-cost>
               <qualifier>
                  <percent>14.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>2</expected-transit-time>
         <expected-delivery-date>2011-10-24</expected-delivery-date>
      </service-standard>
   </price-quote>
</price-quotes>
"""
