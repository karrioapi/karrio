"""Karrio Belgian Post client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.bpost.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        ctx: dict = {**request.ctx}

        response = lib.request(
            url=f"{self.settings.server_url}/{self.settings.account_id}/orders/",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-type": "application/vnd.bpost.shm-order-v5+XML",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        if not any(response):
            reference = ctx["reference"]
            label_format = ctx["label_format"]
            label_header = ctx["label_header"]
            label = lib.request(
                url=f"{self.settings.server_url}/{self.settings.account_id}/orders/{reference}/labels/{label_format}",
                trace=self.trace_as("xml"),
                method="GET",
                headers={
                    "Content-type": "application/vnd.bpost.shm-labelRequest-v5+XML",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept": f"{label_header}",
                },
            )

            ctx.update(label=lib.to_element(label))
            response = "<success>true</success>"

        return lib.Deserializable(response, lib.to_element, ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        reference = request.ctx["reference"]
        response = lib.request(
            url=f"{self.settings.server_url}/{self.settings.account_id}/orders/{reference}",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-type": "application/vnd.bpost.shm-orderUpdate-v3+XML",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        response = response if any(response) else "<success>true</success>"

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda item_nb: (
                item_nb,
                lib.request(
                    url=f"https://api.parcel.bpost.cloud/services/trackedmail/item/{item_nb}/trackingInfo",
                    trace=self.trace_as("xml"),
                    method="GET",
                    headers={"Authorization": f"Basic {self.settings.authorization}"},
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda results: [
                (result[0], lib.to_element(result[1])) for result in results
            ],
        )
