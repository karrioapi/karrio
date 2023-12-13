"""Karrio Allied Express client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.allied_express.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/calculatePrice",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/GetLabelfull",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/cancelJob/{payload['shipment_no']}/{payload['postal_code']}",
            trace=self.trace_as("json"),
            method="POST",
            headers={"Authorization": f"Basic {self.settings.authorization}"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda shipment_no: (
                shipment_no,
                lib.request(
                    url=f"{self.settings.server_url}/getShipmentsStatus/{shipment_no}",
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={"Authorization": f"Basic {self.settings.authorization}"},
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(response, lib.to_dict)
