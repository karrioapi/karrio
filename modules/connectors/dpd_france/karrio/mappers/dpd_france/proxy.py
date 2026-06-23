"""Karrio DPD France client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd_france.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _send(data: str) -> str:
            return lib.request(
                url=self.settings.server_url,
                data=data,
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": f"{self.settings.shipping_namespace}/CreateShipmentWithLabelsBc",
                },
            )

        responses = lib.run_concurently(_send, request.serialize())

        return lib.Deserializable(
            responses,
            lambda results: [lib.to_element(res) for res in results],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": f"{self.settings.shipping_namespace}/TerminateShipment",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _fetch(payload):
            tracking_number, data = payload
            return tracking_number, lib.request(
                url=self.settings.tracking_url,
                data=data,
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": f"{self.settings.tracking_namespace}GetShipmentTrace",
                },
            )

        responses = lib.run_concurently(_fetch, request.serialize())

        return lib.Deserializable(
            responses,
            lambda results: [(num, lib.to_element(res)) for num, res in results],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": f"{self.settings.shipping_namespace}/CreateCollectionRequestBc",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": f"{self.settings.shipping_namespace}/TerminateCollectionRequestBc",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _send(data: str) -> str:
            return lib.request(
                url=self.settings.server_url,
                data=data,
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": f"{self.settings.shipping_namespace}/CreateReverseInverseShipmentWithLabelsBc",
                },
            )

        responses = lib.run_concurently(_send, request.serialize())

        return lib.Deserializable(
            responses,
            lambda results: [lib.to_element(res) for res in results],
        )
