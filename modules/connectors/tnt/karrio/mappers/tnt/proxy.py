import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.tnt.error as provider_error
import karrio.providers.tnt.utils as provider_utils
import karrio.mappers.tnt.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    """ Proxy Methods """

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
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

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        ctx: dict = {}
        shipment_response = lib.request(
            url=f"{self.settings.server_url}/expressconnect/shipping/ship",
            data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        label_request = provider_utils.create_label_request(
            shipment_response, self.settings, request.ctx
        )

        if label_request is not None:
            label_response = lib.request(
                url=f"{self.settings.server_url}/expresslabel/documentation/getlabel",
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                data=urllib.parse.urlencode(dict(xml_in=label_request.serialize())),
            )

            label_errors = provider_error.parse_error_response(
                lib.to_element(label_response), self.settings
            )

            if not any(label_errors):
                label = lib.request(
                    url=f"{self.settings.server_url}/expresswebservices-website/app/render.html",
                    trace=self.trace_as("xml"),
                    method="POST",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Authorization": f"Basic {self.settings.authorization}",
                    },
                    data=urllib.parse.urlencode(
                        dict(
                            responseXml=label_response,
                            documentType="routingLabel",
                            contentType="pdf",
                        ),
                    ),
                    decoder=lib.encode_base64,
                )

                ctx.update(label=label)

        return lib.Deserializable(shipment_response, lib.to_element, ctx=ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url="https://necta.az.fxei.fedex.com/ectrack/track",
            data=urllib.parse.urlencode(dict(xml_in=request.serialize())),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "accept": "text/xml; charset=UTF-8",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_element)
