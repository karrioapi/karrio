"""Karrio Australia Post client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.australiapost.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipping/v1/prices/items",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        responses: list = []
        responses.append(
            lib.request(
                url=f"{self.settings.server_url}/shipping/v1/shipments",
                data=lib.to_json(payload["shipment"]),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Account-Number": self.settings.account_number,
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            )
        )

        shipment_id = (lib.to_dict(responses[0]).get("shipments") or [{}])[0].get(
            "shipment_id"
        )

        if shipment_id is not None:
            responses.append(
                lib.request(
                    url=f"{self.settings.server_url}/shipping/v1/labels",
                    trace=self.trace_as("json"),
                    data=lib.to_json(payload["label"]).replace(
                        "[SHIPMENT_ID]", shipment_id
                    ),
                    method="POST",
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Account-Number": self.settings.account_number,
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                )
            )

            label_url = (lib.to_dict(responses[1]).get("labels") or [{}])[0].get("url")

            if label_url is not None:
                responses.append(
                    lib.request(
                        decoder=lib.encode_base64,
                        url=label_url,
                        method="GET",
                    )
                )

        return lib.Deserializable(
            responses,
            lambda _: [
                # parse create shipment response
                lib.to_dict(_[0]),
                # parse create label response if exists
                lib.to_dict(_[1] if len(_) > 1 else "{}"),
                # return label image if exists
                (_[2] if len(_) > 2 else None),
            ],
            request.ctx,
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/shipping/v1/shipments/{payload['shipment_id']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
            decoder=lambda _: dict(ok=True),
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = request.serialize()
        tracking_ids = ",".join(query["tracking_ids"])
        response = lib.request(
            url=f"{self.settings.server_url}/shipping/v1/track?tracking_ids={tracking_ids}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable:
        ctx: dict = {}
        response = lib.request(
            url=f"{self.settings.server_url}/shipping/v1/orders",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        order_id = lib.to_dict(response).get("order", {}).get("order_id")

        if order_id is not None:
            ctx.update(
                manifest=lib.request(
                    url=f"{self.settings.server_url}/shipping/v1/accounts/{self.settings.account_number}/orders/{order_id}/summary",
                    decoder=lib.encode_base64,
                    method="GET",
                )
            )

        return lib.Deserializable(response, lib.to_dict, ctx=ctx)
