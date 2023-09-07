import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.tnt.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    """ Proxy Methods """

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/expressconnect/pricing/getprice",
            data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/expressconnect/shipping/ship",
            data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url="https://necta.az.fxei.fedex.com/ectrack/jtrack",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
