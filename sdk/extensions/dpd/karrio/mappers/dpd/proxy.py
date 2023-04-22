"""Karrio DPD client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/soap/services/ShipmentService/V3_3",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml;charset=UTF-8",
                "SOAPAction": "http://dpd.com/common/service/types/ShipmentService/3.3/storeOrders",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        def _track(payload):
            tracking_number, data = payload
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/soap/services/ParcelLifeCycleService/V2_0",
                trace=self.trace_as("xml"),
                method="POST",
                data=data,
                headers={
                    "Content-Type": "text/xml;charset=UTF-8",
                    "SOAPAction": "http://dpd.com/common/service/types/ParcelLifeCycleService/2.0/getTrackingData",
                },
            )

        responses = lib.run_concurently(_track, requests.serialize().items())

        return lib.Deserializable(
            responses,
            lambda results: [(res[0], lib.to_element(res[1])) for res in results],
        )
