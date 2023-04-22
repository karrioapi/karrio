"""Karrio Deutsche Post DHL client proxy."""
import functools
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.mappers.dpdhl.settings as provider_settings

to_element = functools.partial(lib.to_element, encoding="ISO-8859-1")
decoder = lambda _: _.decode("ISO-8859-1")


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/soap",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.basic_authentication}",
                "SOAPAction": "urn:createShipmentOrder",
            },
            decoder=decoder,
        )

        return lib.Deserializable(response, to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/soap",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.basic_authentication}",
                "SOAPAction": "urn:deleteShipmentOrder",
            },
            decoder=decoder,
        )

        return lib.Deserializable(response, to_element)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        def _track(data):
            return lib.request(
                url=f"{self.settings.server_url}/rest/sendungsverfolgung",
                trace=self.trace_as("xml"),
                data=urllib.parse.urlencode(dict(xml=data)),
                method="POST",
                headers={
                    "Authorization": f"Basic {self.settings.basic_authentication}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )

        responses = lib.run_concurently(_track, requests.serialize())

        return lib.Deserializable(
            responses, lambda results: [lib.to_element(res) for res in results]
        )
