"""Karrio USPS client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.usps.utils as provider_utils
import karrio.mappers.usps.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=f"{self.settings.server_url}/shipments/v3/options/search",
                data=lib.to_json(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.access_token}",
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda _: [lib.to_dict(_) for _ in _],
            request.ctx,
        )

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=f"{self.settings.server_url}/labels/v3/label",
                data=lib.to_json(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.access_token}",
                    "X-Payment-Authorization-Token": f"{self.settings.payment_token}",
                },
                on_error=provider_utils.parse_error_response,
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda _: [provider_utils.parse_response(_) for _ in _],
            request.ctx,
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda _: (
                _["trackingNumber"],
                lib.request(
                    url=f"{self.settings.server_url}/labels/v3/label/{_['trackingNumber']}",
                    trace=self.trace_as("json"),
                    method="DELETE",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.settings.access_token}",
                        "X-Payment-Authorization-Token": f"{self.settings.payment_token}",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.run_asynchronously(
            lambda trackingNumber: (
                trackingNumber,
                lib.request(
                    url=f"{self.settings.server_url}/tracking/v3/tracking/{trackingNumber}?expand=DETAIL",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.settings.access_token}",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup/{request.ctx['confirmationNumber']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup/{request.serialize()['confirmationNumber']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_ok=lambda _: '{"ok": true}',
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/scan-forms/v3/scan-form",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
