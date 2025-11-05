"""Karrio Teleship client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.teleship.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/rates/quotes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
                **({
                    "x-account-id": self.settings.connection_config.account_id.state
                } if self.settings.connection_config.account_id.state else {}),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/labels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
                **({
                    "x-account-id": self.settings.connection_config.account_id.state
                } if self.settings.connection_config.account_id.state else {}),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(
        self, request: lib.Serializable
    ) -> lib.Deserializable[str]:
        shipment_id = request.serialize().get("shipmentId")

        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/labels/{shipment_id}/void",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                **({
                    "x-account-id": self.settings.connection_config.account_id.state
                } if self.settings.connection_config.account_id.state else {}),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/api/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Authorization": f"Bearer {self.settings.api_key}",
                    **({
                        "x-account-id": self.settings.connection_config.account_id.state
                    } if self.settings.connection_config.account_id.state else {}),
                },
            )

        # Use concurrent requests for multiple tracking numbers
        responses = lib.run_concurently(_get_tracking, request.serialize())

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )
