import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.lib as lib
import karrio
import karrio.core.models as models


class TestCanadaPostRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        requests = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(requests.serialize()[0], RateRequestXML)

    def test_create_rate_request_with_package_preset(self):
        requests = gateway.mapper.create_rate_request(
            models.RateRequest(**RateWithPresetPayload)
        )

        self.assertEqual(requests.serialize()[0], RateRequestUsingPackagePresetXML)
        self.assertEqual(requests.serialize()[1], SecondParcelRateRequestXML)

    @patch("karrio.mappers.canadapost.proxy.lib.request", return_value="<a></a>")
    def test_create_rate_request_with_package_preset_missing_weight(self, _):
        processing_error = (
            karrio.Rating.fetch(
                models.RateRequest(**RateWithPresetMissingWeightPayload)
            )
            .from_(gateway)
            .parse()
        )

        self.assertListEqual(lib.to_dict(processing_error), ParsedProcessingError)

    @patch("karrio.mappers.canadapost.proxy.lib.request", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        karrio.Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]

        self.assertEqual(url, f"{gateway.proxy.settings.server_url}/rs/ship/price")

    def test_parse_rate_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = RateResponseXML
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRatingResponse)

    def test_parse_rate_parsing_error(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = RatingParsingErrorXML
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertEqual(lib.to_dict(parsed_response), ParsedRatingParsingError)

    def test_parse_rate_missing_args_error(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = RatingMissingArgsErrorXML
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertEqual(lib.to_dict(parsed_response), ParsedRatingMissingArgsError)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {"postal_code": "H8Z 2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "h8z2V4", "country_code": "CA"},
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
    "options": {
        "canadapost_leave_at_door": False,
        "signature_confirmation": True,
        "shipment_date": "2020-12-18",
        "insurance": 1000,
    },
}

RateWithPresetPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [
        {
            "package_preset": "canadapost_xexpresspost_certified_envelope",
        },
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {
                "signature_confirmation": True,
            },
        },
    ],
    "services": ["canadapost_xpresspost"],
}

RateWithPresetMissingWeightPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [
        {
            "package_preset": "canadapost_corrugated_small_box",
        }
    ],
    "services": ["canadapost_regular_parcel"],
}


ParsedProcessingError = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "SHIPPING_SDK_FIELD_ERROR",
            "message": "Invalid request payload",
            "details": {
                "parcel[0].weight": {
                    "code": "required",
                    "message": "This field is required",
                }
            },
        }
    ],
]

ParsedRatingParsingError = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "AA004",
            "message": "You cannot mail on behalf of the requested customer.",
            "details": {},
        }
    ],
]

ParsedRatingMissingArgsError = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "Server",
            "message": "/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v4}parcel-characteristics with anonymous type, found </parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v4), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v4}weight, {http://www.canadapost.ca/ws/ship/rate-v4}dimensions, {http://www.canadapost.ca/ws/ship/rate-v4}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v4}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v4}oversized]",
            "details": {},
        }
    ],
]

ParsedRatingResponse = [
    [
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 9.59, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "GST"},
                {"amount": 0.0, "currency": "CAD", "name": "PST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": -0.29, "currency": "CAD", "name": "Automation discount"},
                {"amount": 0.91, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {"service_name": "canadapost_expedited_parcel"},
            "service": "canadapost_expedited_parcel",
            "total_charge": 10.21,
            "transit_days": 2,
        },
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 22.64, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "GST"},
                {"amount": 0.0, "currency": "CAD", "name": "PST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": -0.68, "currency": "CAD", "name": "Automation discount"},
                {"amount": 3.24, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {"service_name": "canadapost_priority"},
            "service": "canadapost_priority",
            "total_charge": 25.2,
            "transit_days": 1,
        },
        {
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 9.59, "currency": "CAD", "name": "Base charge"},
                {"amount": 0.0, "currency": "CAD", "name": "GST"},
                {"amount": 0.0, "currency": "CAD", "name": "PST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": -0.29, "currency": "CAD", "name": "Automation discount"},
                {"amount": 0.91, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {"service_name": "canadapost_regular_parcel"},
            "service": "canadapost_regular_parcel",
            "total_charge": 10.21,
            "transit_days": 4,
        },
    ],
    [],
]


RatingParsingErrorXML = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>AA004</code>
        <description>You cannot mail on behalf of the requested customer.</description>
    </message>
</messages>
"""

RatingMissingArgsErrorXML = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>Server</code>
        <description>/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v4}parcel-characteristics with anonymous type, found &lt;/parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v4), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v4}weight, {http://www.canadapost.ca/ws/ship/rate-v4}dimensions, {http://www.canadapost.ca/ws/ship/rate-v4}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v4}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v4}oversized]</description>
    </message>
</messages>
"""

RateRequestXML = f"""<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
    <customer-number>2004381</customer-number>
    <contract-id>42708517</contract-id>
    <expected-mailing-date>2020-12-18</expected-mailing-date>
    <options>
        <option>
            <option-code>SO</option-code>
        </option>
        <option>
            <option-code>COV</option-code>
            <option-amount>1000</option-amount>
        </option>
    </options>
    <parcel-characteristics>
        <weight>4</weight>
        <dimensions>
            <length>10</length>
            <width>3</width>
            <height>3</height>
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

RateRequestUsingPackagePresetXML = f"""<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
    <customer-number>2004381</customer-number>
    <contract-id>42708517</contract-id>
    <parcel-characteristics>
        <weight>0.5</weight>
        <dimensions>
            <length>1.5</length>
            <width>26</width>
            <height>15.9</height>
        </dimensions>
    </parcel-characteristics>
    <services>
        <service-code>DOM.XP</service-code>
    </services>
    <origin-postal-code>H8Z2Z3</origin-postal-code>
    <destination>
        <domestic>
            <postal-code>H8Z2V4</postal-code>
        </domestic>
    </destination>
</mailing-scenario>
"""

SecondParcelRateRequestXML = f"""<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
    <customer-number>2004381</customer-number>
    <contract-id>42708517</contract-id>
    <options>
        <option>
            <option-code>SO</option-code>
        </option>
    </options>
    <parcel-characteristics>
        <weight>4</weight>
        <dimensions>
            <length>10</length>
            <width>3</width>
            <height>3</height>
        </dimensions>
    </parcel-characteristics>
    <services>
        <service-code>DOM.XP</service-code>
    </services>
    <origin-postal-code>H8Z2Z3</origin-postal-code>
    <destination>
        <domestic>
            <postal-code>H8Z2V4</postal-code>
        </domestic>
    </destination>
</mailing-scenario>
"""

RateResponseXML = """<price-quotes>
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
