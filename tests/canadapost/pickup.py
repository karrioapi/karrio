import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import PickupRequest, PickupUpdateRequest, PickupCancellationRequest
from purplship.package import Pickup
from tests.canadapost.fixture import gateway


class TestCanadaPostPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancellationRequest(
            confirmation_number=pickup_update_data.get('confirmation_number')
        )

    # def test_create_pickup_request(self):
    #     requests = gateway.mapper.create_pickup_request(self.PickupRequest)
    #     pipeline = requests.serialize()
    #     request = pipeline['create_pickup'](PickupAvailabilityResponseXML)
    #     self.assertEqual(request.data.serialize(), PickupRequestXML)

    # def test_update_pickup_request(self):
    #     request = gateway.mapper.create_modify_pickup_request(self.PickupUpdateRequest)
    #     self.assertEqual(request.serialize(), PickupUpdateRequestXML)
    #
    # def test_cancel_pickup_request(self):
    #     request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
    #     self.assertEqual(request.serialize(), self.PickupCancelRequest.confirmation_number)
    #
    # def test_create_pickup(self):
    #     with patch("purplship.package.mappers.canadapost.proxy.http") as mocks:
    #         mocks.side_effect = ["<a></a>", ""]
    #         Pickup.book(self.PickupRequest).with_(gateway)
    #
    #         availability_url = mocks.call_args[1]["url"]
    #         create_url = mocks.call_args[2]["url"]
    #         self.assertEqual(
    #             availability_url,
    #             f"{gateway.settings.server_url}/ad/pickup/pickupavailability/{self.PickupRequest.address.postal_code}",
    #         )
    #         self.assertEqual(
    #             create_url,
    #             f"{gateway.settings.server_url}/enab/{gateway.settings.customer_number}/pickuprequest",
    #         )
    #
    # @patch("purplship.package.mappers.canadapost.proxy.http", return_value="<a></a>")
    # def test_update_pickup(self, http_mock):
    #     Pickup.update(self.PickupUpdateRequest).with_(gateway)
    #
    #     reqUrl = http_mock.call_args[1]["url"]
    #     self.assertEqual(
    #         reqUrl,
    #         f"{gateway.settings.server_url}/enab/{gateway.settings.customer_number}/pickuprequest/{self.PickupUpdateRequest.confirmation_number}",
    #     )
    #
    # @patch("purplship.package.mappers.canadapost.proxy.http", return_value="<a></a>")
    # def test_cancel_pickup(self, http_mock):
    #     Pickup.cancel(self.PickupCancelRequest).from_(gateway)
    #
    #     reqUrl = http_mock.call_args[1]["url"]
    #     self.assertEqual(
    #         reqUrl,
    #         f"{gateway.settings.server_url}/enab/{gateway.settings.customer_number}/pickuprequest/{self.PickupCancelRequest.confirmation_number}",
    #     )
    #
    # def test_parse_pickup_response(self):
    #     with patch("purplship.package.mappers.canadapost.proxy.http") as mocks:
    #         mocks.side_effect = [PickupResponseXML]
    #         parsed_response = (
    #             Pickup.book(self.PickupRequest).with_(gateway).parse()
    #         )
    #
    #         self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupResponse))
    #
    # def test_parse_pickup_error_response(self):
    #     with patch("purplship.package.mappers.canadapost.proxy.http") as mocks:
    #         mocks.side_effect = [PickupAvailabilityErrorResponseXML]
    #         parsed_response = (
    #             Pickup.book(self.PickupRequest).with_(gateway).parse()
    #         )
    #
    #         self.assertEqual(to_dict(parsed_response), to_dict(ParsedPickupResponse))


if __name__ == "__main__":
    unittest.main()

pickup_data = {

}

pickup_update_data = {**pickup_data, "confirmation_number": "0074698052"}

ParsedPickupResponse = []

ParsedPickupErrorResponse = []

PickupRequestXML = """<pickup-request-details>
    <pickup-type>OnDemand</pickup-type>
    <pickup-location>
        <business-address-flag>false</business-address-flag>
        <alternate-address>
            <company>Jim Duggan</company>
            <address-line-1>2271 Herring Cove</address-line-1>
            <city>Halifax</city><province>NS</province>
            <postal-code>B3L2C2</postal-code>
        </alternate-address>
    </pickup-location>
    <contact-info>
        <contact-name>John Doe</contact-name>
        <email>john.doe@canadapost.ca</email>
        <contact-phone>800-555-1212</contact-phone>
        <opt-out-email-updates-flag>true</opt-out-email-updates-flag>
        <receive-email-updates-flag>true</ receive-email-updates-flag>
    </contact-info>
    <location-details>
        <five-ton-flag>false</five-ton-flag>
        <loading-dock-flag>true</loading-dock-flag>
        <pickup-instructions>Door at Back</pickup-instructions>
    </location-details>
    <items-characteristics>
        <pww-flag>true</pww-flag>
        <priority-flag>false</priority-flag>
        <returns-flag>true</returns-flag>
        <heavy-item-flag>true</heavy-item-flag>
    </items-characteristics>
    <pickup-volume>50</pickup-volume>
    <pickup-times>
        <on-demand-pickup-time>
            <date>2015-01-28</date>
            <preferred-time>15:00</preferred-time>
            <closing-time>17:00</closing-time>
        </on-demand-pickup-time>
    </pickup-times>
</pickup-request-details>
"""

PickupUpdateRequestXML = """<pickup-request-update>
    <contact-info>
        <contact-name>Jane Doe</contact-name>
        <email>john.doe@canadapost.ca</email>
        <contact-phone>800-555-1212</contact-phone>
        <receive-email-updates-flag>true</receive-email-updates-flag>
    </contact-info>
    <location-details>
        <five-ton-flag>false</five-ton-flag>
        <loading-dock-flag>true</loading-dock-flag>
        <pickup-instructions>Door at Back</pickup-instructions>
    </location-details>
    <items-characteristics>
        <heavy-item-flag>true</heavy-item-flag>
    </items-characteristics>
        <pickup-volume>50</pickup-volume>
        <pickup-times>
        <on-demand-pickup-time>
        <date>2015-01-28</date>
        <preferred-time>15:00</preferred-time>
        <closing-time>17:00</closing-time>
    </on-demand-pickup-time>
    </pickup-times>
</pickup-request-update>
"""

PickupAvailabilityResponseXML = """<pickup-availability>
    <postal-code>K2B 8J6</postal-code>
    <on-demand-cutoff>16:00</on-demand-cutoff>
    <on-demand-tour>true</on-demand-tour>
    <prority-world-cutoff>14:00</prority-world-cutoff>
    <scheduled-pickups-available>true</scheduled-pickups-available>
</pickup-availability>
"""

PickupResponseXML = f"""<wrapper>
    {PickupAvailabilityResponseXML}
    <pickup-request-info>
        <pickup-request-header>
            <request-id>0074698052</request-id>
            <request-status>Active</request-status>
            <pickup-type>OnDemand</pickup-type>
            <request-date>2015-01-01</request-date>
        </pickup-request-header>
        <pickup-request-price>
            <pre-tax-amount>3.50</pre-tax-amount>
            <hst-amount>0.46</hst-amount>
            <due-amount>3.96</due-amount>
        </pickup-request-price>
        <links>
            <link rel="self" href="https://ct.soa-gw.canadapost.ca/enab/1234567/pickuprequest/0074698052" media-type="application/vnd.cpc.pickuprequest+xml"></link>
            <link rel="details" href="https://ct.soa-gw.canadapost.ca/enab/1234567/pickuprequest/0074698052/details" media-type="application/vnd.cpc.pickuprequest+xml"></link>
        </links>
    </pickup-request-info>
</wrapper>
"""

PickupAvailabilityErrorResponseXML = """<get-pickup-availability-response>
    <error-list>
        <status-message>
        <code>No_Record_Found</code>
        <message></message>
    </error-list>
</get-pickup-availability-response>
"""
