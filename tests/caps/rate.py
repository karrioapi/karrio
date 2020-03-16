import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.package import rating
from purplship.core.models import RateRequest
from tests.caps.fixture import gateway
from datetime import datetime


class TestCanadaPostQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), QuoteRequestXml)

    @patch("purplship.package.mappers.caps.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        rating.fetch(self.RateRequest).from_(gateway)

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(reqUrl, f"{gateway.proxy.settings.server_url}/rs/ship/price")

    def test_parse_rate_response(self):
        with patch("purplship.package.mappers.caps.proxy.http") as mock:
            mock.return_value = QuoteResponseXml
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteResponse))

    def test_parse_rate_parsing_error(self):
        with patch("purplship.package.mappers.caps.proxy.http") as mock:
            mock.return_value = QuoteParsingError
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteParsingError))

    def test_parse_rate_missing_args_error(self):
        with patch("purplship.package.mappers.caps.proxy.http") as mock:
            mock.return_value = QuoteMissingArgsError
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedQuoteMissingArgsError)
            )


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "postal_code": "H8Z2Z3",
        "country_code": "CA",
        "account_number": "1234567",
    },
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcel": {
        "height": 3,
        "length": 10,
        "width": 3,
        "weight": 4.0,
        "services": ["caps_expedited_parcel"],
        "dimension_unit": "CM",
        "weight_unit": "KG",
    },
}

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
            "message": "/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v4}parcel-characteristics with anonymous type, found </parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v4), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v4}weight, {http://www.canadapost.ca/ws/ship/rate-v4}dimensions, {http://www.canadapost.ca/ws/ship/rate-v4}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v4}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v4}oversized]",
        }
    ],
]
ParsedQuoteResponse = [[{'base_charge': 9.59, 'carrier': 'CanadaPost', 'currency': 'CAD', 'delivery_date': '2011-10-24', 'discount': 0.6200000000000001, 'duties_and_taxes': 0.0, 'extra_charges': [{'amount': -0.29, 'currency': 'CAD', 'name': 'Automation discount'}, {'amount': 0.91, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service_name': 'caps_expedited_parcel', 'service_type': 'DOM.EP', 'total_charge': 10.21}, {'base_charge': 22.64, 'carrier': 'CanadaPost', 'currency': 'CAD', 'delivery_date': '2011-10-21', 'discount': 2.56, 'duties_and_taxes': 0.0, 'extra_charges': [{'amount': -0.68, 'currency': 'CAD', 'name': 'Automation discount'}, {'amount': 3.24, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service_name': 'caps_priority', 'service_type': 'DOM.PC', 'total_charge': 25.2}, {'base_charge': 9.59, 'carrier': 'CanadaPost', 'currency': 'CAD', 'delivery_date': '2011-10-26', 'discount': 0.6200000000000001, 'duties_and_taxes': 0.0, 'extra_charges': [{'amount': -0.29, 'currency': 'CAD', 'name': 'Automation discount'}, {'amount': 0.91, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service_name': 'caps_regular_parcel', 'service_type': 'DOM.RP', 'total_charge': 10.21}, {'base_charge': 12.26, 'carrier': 'CanadaPost', 'currency': 'CAD', 'delivery_date': '2011-10-24', 'discount': 1.38, 'duties_and_taxes': 0.0, 'extra_charges': [{'amount': -0.37, 'currency': 'CAD', 'name': 'Automation discount'}, {'amount': 1.75, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service_name': 'caps_xpresspost', 'service_type': 'DOM.XP', 'total_charge': 13.64}], []]



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
        <description>/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v4}parcel-characteristics with anonymous type, found &lt;/parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v4), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v4}weight, {http://www.canadapost.ca/ws/ship/rate-v4}dimensions, {http://www.canadapost.ca/ws/ship/rate-v4}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v4}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v4}oversized]</description>
    </message>
</messages>
"""

QuoteRequestXml = f"""<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
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
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.EP?country=CA" media-type="application/vnd.cpc.ship.rate-v4+xml" />
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
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.PC?country=CA" media-type="application/vnd.cpc.ship.rate-v4+xml" />
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
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.RP?country=CA" media-type="application/vnd.cpc.ship.rate-v4+xml" />
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
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.XP?country=CA" media-type="application/vnd.cpc.ship.rate-v4+xml" />
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
