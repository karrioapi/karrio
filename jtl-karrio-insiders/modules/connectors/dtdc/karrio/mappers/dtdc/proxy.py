"""Karrio DTDC client proxy."""

import urllib.parse

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dtdc.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # Step 1: Create shipment using DTDC Order Upload API
        response = lib.request(
            url=f"{self.settings.server_url}/api/customer/integration/consignment/softdata",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": self.settings.api_key,
            },
        )

        consignment = lib.identity(
            lib.failsafe(lambda: lib.to_dict(response)["data"][0]) or {}
        )
        is_success = lib.identity(
            consignment.get("success") and consignment.get("reference_number")
        )

        # Step 2: Get label from DTDC Label API
        label = lib.identity(
            lib.request(
                url=lib.identity(
                    f"{self.settings.label_server_url}/api/customer/integration/consignment/shippinglabel/stream?"
                    + urllib.parse.urlencode(
                        dict(
                            reference_number=consignment.get("reference_number"),
                            label_format=request.ctx.get("label_format"),
                            label_code=request.ctx.get("label_type"),
                        )
                    )
                ),
                headers={
                    "Content-Type": "application/json",
                    "api-key": self.settings.api_key,
                },
                trace=self.trace_as("json"),
            )
            if is_success
            else None
        )

        return lib.Deserializable(
            [response, label],
            lambda __: (lib.to_dict(_) for _ in __),
            request.ctx,
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/customer/integration/consignment/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.run_asynchronously(
            lambda payload: (
                payload["strcnno"],
                lib.request(
                    url=f"{self.settings.tracking_server_url}/dtdc-api/rest/JSONCnTrk/getTrackDetails",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Accept": "application/json",
                        "Content-type": "application/json",
                        "x-access-token": self.settings.access_token,
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(ref, lib.to_dict(_)) for ref, _ in __],
        )
