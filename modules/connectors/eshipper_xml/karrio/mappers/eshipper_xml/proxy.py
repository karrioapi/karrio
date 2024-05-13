<<<<<<< HEAD:modules/connectors/eshipper/karrio/mappers/eshipper/proxy.py
"""Karrio eShipper client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.eshipper.settings as provider_settings
=======
from karrio.core.utils import XP, request as http
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.eshipper_xml.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable
>>>>>>> 3ccfd84c0 (feat: Rename legacy eshipper integration eshipper_xml):modules/connectors/eshipper_xml/karrio/mappers/eshipper_xml/proxy.py


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/quote",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/ship",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/ship/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = lib.to_query_string(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/track/events?{query}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
