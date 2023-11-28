import unittest
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import (
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from .fixture import gateway


class TestCanadaPostPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**pickup_data)
        self.PickupUpdateRequest = PickupUpdateRequest(**pickup_update_data)
        self.PickupCancelRequest = PickupCancelRequest(**pickup_cancel_data)

    def test_create_pickup_request(self):
        requests = gateway.mapper.create_pickup_request(self.PickupRequest)
        pipeline = requests.serialize()
        request = pipeline["create_pickup"](PickupAvailabilityResponseXML)

        self.assertEqual(request.data.serialize(), PickupRequestXML)

    def test_update_pickup_request(self):
        requests = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        pipeline = requests.serialize()
        update = pipeline["update_pickup"]()
        details = pipeline["get_pickup"]("")

        self.assertEqual(update.data.serialize()["data"], PickupUpdateRequestXML)
        self.assertEqual(
            update.data.serialize()["pickuprequest"],
            pickup_update_data["confirmation_number"],
        )
        self.assertEqual(
            details.data.serialize(), "/enab/2004381/pickuprequest/0074698052/details"
        )

    def test_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
        self.assertEqual(
            request.serialize(), self.PickupCancelRequest.confirmation_number
        )

    def test_create_pickup(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            availability_call, create_call = mocks.call_args_list

            self.assertEqual(
                availability_call[1]["url"],
                f"{gateway.settings.server_url}/ad/pickup/pickupavailability/B3L2C2",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/enab/2004381/pickuprequest",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mocks:
            mocks.side_effect = ["", PickupDetailseResponseXML]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            update_call, get_call = mocks.call_args_list

            self.assertEqual(
                update_call[1]["url"],
                f"{gateway.settings.server_url}/enab/2004381/pickuprequest/0074698052",
            )
            self.assertEqual(
                get_call[1]["url"],
                f"{gateway.settings.server_url}/enab/2004381/pickuprequest/0074698052/details",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(
                url,
                f"{gateway.settings.server_url}/enab/2004381/pickuprequest/0074698052",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mocks:
            mocks.side_effect = [PickupAvailabilityResponseXML, PickupResponseXML]
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_pickup_update_response(self):
        with patch("karrio.mappers.canadapost.proxy.lib.request") as mocks:
            mocks.side_effect = [None, PickupDetailseResponseXML]
            parsed_response = (
                karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedPickupUpdateResponse
            )


if __name__ == "__main__":
    unittest.main()

pickup_data = {
    "pickup_date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "800-555-1212",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canadapost.ca",
    },
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"loading_dock_flag": True},
}

pickup_update_data = {
    "confirmation_number": "0074698052",
    "pickup_date": "2015-01-28",
    "address": {
        "person_name": "Jane Doe",
        "email": "john.doe@canadapost.ca",
        "phone_number": "800-555-1212",
    },
    "parcels": [{"weight": "24", "weight_unit": "KG"}],
    "instruction": "Door at Back",
    "ready_time": "15:00",
    "closing_time": "17:00",
    "options": {"loading_dock_flag": True},
}

pickup_cancel_data = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "confirmation_number": "0074698052",
        "pickup_charge": {"amount": 4.42, "currency": "CAD", "name": "Pickup fees"},
    },
    [],
]

ParsedPickupUpdateResponse = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "confirmation_number": "0074698052",
    },
    [],
]

PickupRequestXML = """<pickup-request-details xmlns="http://www.canadapost.ca/ws/pickuprequest">
    <customer-request-id>2004381</customer-request-id>
    <pickup-type>OnDemand</pickup-type>
    <pickup-location>
        <business-address-flag>false</business-address-flag>
        <alternate-address>
            <company>Jim Duggan</company>
            <address-line-1>2271 Herring Cove</address-line-1>
            <city>Halifax</city>
            <province>NS</province>
            <postal-code>B3L2C2</postal-code>
        </alternate-address>
    </pickup-location>
    <contact-info>
        <contact-name>John Doe</contact-name>
        <email>john.doe@canadapost.ca</email>
        <contact-phone>800-555-1212</contact-phone>
        <receive-email-updates-flag>true</receive-email-updates-flag>
    </contact-info>
    <location-details>
        <loading-dock-flag>true</loading-dock-flag>
        <pickup-instructions>Door at Back</pickup-instructions>
    </location-details>
    <pickup-volume>1</pickup-volume>
    <pickup-times>
        <on-demand-pickup-time>
            <date>2015-01-28</date>
            <preferred-time>15:00</preferred-time>
            <closing-time>17:00</closing-time>
        </on-demand-pickup-time>
    </pickup-times>
</pickup-request-details>
"""

PickupUpdateRequestXML = """<pickup-request-update xmlns="http://www.canadapost.ca/ws/pickuprequest">
    <contact-info>
        <contact-name>Jane Doe</contact-name>
        <email>john.doe@canadapost.ca</email>
        <contact-phone>800-555-1212</contact-phone>
        <receive-email-updates-flag>true</receive-email-updates-flag>
    </contact-info>
    <location-details>
        <loading-dock-flag>true</loading-dock-flag>
        <pickup-instructions>Door at Back</pickup-instructions>
    </location-details>
    <items-characteristics>
        <heavy-item-flag>true</heavy-item-flag>
    </items-characteristics>
    <pickup-volume>1</pickup-volume>
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

PickupDetailseResponseXML = f"""<pickup-request-detailed-info>
    <pickup-request-header>
        <request-id>0074698052</request-id>
        <request-status>Active</request-status>
        <pickup-type>OnDemand</pickup-type>
        <request-date>2015-01-01</request-date>
    </pickup-request-header>
    <pickup-request-details>
        <pickup-location>
            <business-address-flag>false</business-address-flag>
            <alternate-address>
                <company>Jim Duggan</company>
                <address-line-1>2271 Herring Cove</address-line-1>
                <city>Halifax</city>
                <province>NS</province>
                <postal-code>B3L2C2</postal-code>
            </alternate-address>
        </pickup-location>
        <contact-info>
            <contact-name>John Doe</contact-name>
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
</pickup-request-detailed-info>
"""
