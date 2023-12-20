"""Karrio Allied Express client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.allied_express.utils as provider_utils
import karrio.mappers.allied_express.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/calculatePrice",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, provider_utils.parse_response, request.ctx)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/GetLabelfull",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, provider_utils.parse_response, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/cancelJob/{payload['shipmentno']}/{payload['postalcode']}",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, provider_utils.parse_response)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda payload: (
                payload["shipmentno"],
                lib.request(
                    url=f"{self.settings.server_url}/getShipmentsStatus/{payload['shipmentno']}",
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={
                        "Authorization": f"Basic {self.settings.authorization}",
                        "Content-Type": "application/json",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(no, provider_utils.parse_response(_)) for no, _ in __],
        )
