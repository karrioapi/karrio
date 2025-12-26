"""Karrio Hermes client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.hermes.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments",
        #     data=lib.to_json(request.serialize()),
        #     trace=self.trace_as("json"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.settings.api_key}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = lib.to_json({})

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/shipments/cancel",
        #     data=lib.to_json(request.serialize()),
        #     trace=self.trace_as("json"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.settings.api_key}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = lib.to_json({})

        return lib.Deserializable(response, lib.to_dict)
    
    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups",
        #     data=lib.to_json(request.serialize()),
        #     trace=self.trace_as("json"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.settings.api_key}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = lib.to_json({})

        return lib.Deserializable(response, lib.to_dict)
    
    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups/modify",
        #     data=lib.to_json(request.serialize()),
        #     trace=self.trace_as("json"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.settings.api_key}"
        #     },
        # )

        # DEVELOPMENT ONLY: Remove this stub response and uncomment the API call above when implementing the real carrier API
        response = lib.to_json({})

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/pickups/cancel",
        #     data=lib.to_json(request.serialize()),
        #     trace=self.trace_as("json"),
        #     method="POST",
        #     headers={
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {self.settings.api_key}"
        #     },
        # )

        # During development, use stub response from schema examples
        response = lib.to_json({})

        return lib.Deserializable(response, lib.to_dict)
    
    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        # REPLACE THIS WITH YOUR ACTUAL AUTHENTICATION IMPLEMENTATION
        # ------------------------------------------------------------
        # Example OAuth2 implementation:
        # cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"
        #
        # def get_token():
        #     response = lib.request(
        #         url=f"{self.settings.server_url}/oauth/token",
        #         method="POST",
        #         headers={"content-Type": "application/x-www-form-urlencoded"},
        #         data=lib.to_query_string({
        #             "grant_type": "client_credentials",
        #             "client_id": self.settings.client_id,
        #             "client_secret": self.settings.client_secret,
        #         }),
        #         decoder=lib.to_dict,
        #     )
        #
        #     messages = provider_error.parse_error_response(response, self.settings)
        #     if any(messages):
        #         raise errors.ParsedMessagesError(messages)
        #
        #     expiry = datetime.datetime.now() + datetime.timedelta(
        #         seconds=float(response.get("expires_in", 3600))
        #     )
        #
        #     return {**response, "expiry": lib.fdatetime(expiry)}
        #
        # token = self.settings.connection_cache.thread_safe(
        #     refresh_func=get_token,
        #     cache_key=cache_key,
        #     buffer_minutes=30,
        #     token_field="access_token",
        # )
        #
        # return lib.Deserializable(token.get_state())

        # DEVELOPMENT ONLY: Remove this stub and implement actual authentication
        return lib.Deserializable({"access_token": "STUB_TOKEN", "expires_in": 3600})
