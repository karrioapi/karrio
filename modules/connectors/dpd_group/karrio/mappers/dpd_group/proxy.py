"""Karrio DPD Group client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd_group.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Retrieve access token using thread-safe token manager.

        Returns the cached token if available and not expired,
        otherwise fetches a new token from the DPD META-API login endpoint.
        """
        from karrio.providers.dpd_group.utils import login

        # Build cache key (same logic as before)
        identity = (
            f"u:{self.settings.username}"
            if any([self.settings.username, self.settings.password])
            else f"c:{self.settings.client_id}"
        )
        env = "test" if self.settings.test_mode else "prod"
        cache_key = f"{self.settings.carrier_name}|{identity}|{self.settings.bucode}|{env}"

        def get_token():
            return login(self.settings)

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
        )

        return lib.Deserializable(token.get_state())

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """
        Create a shipment with DPD META-API.
        POST /shipping/v1/shipment
        """
        access_token = self.authenticate(request).deserialize()

        # Get label format from request options or default to PDF
        label_format = getattr(request, "label_format", "PDF") or "PDF"

        response = lib.request(
            url=f"{self.settings.server_url}/shipment?LabelPrintFormat={label_format}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """
        Schedule a pickup with DPD META-API.
        POST /shipping/v1/pickupscheduling
        """
        access_token = self.authenticate(request).deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/pickupscheduling",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
