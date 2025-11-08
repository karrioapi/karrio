"""Karrio MyDHL client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.mydhl.settings as provider_settings

# IMPLEMENTATION INSTRUCTIONS:
# 1. Import the schema types specific to your carrier API
# 2. Uncomment and adapt the request examples below to work with your carrier API
# 3. Replace the stub responses with actual API calls once you've tested with the example data
# 4. Update URLs, headers, and authentication methods as required by your carrier API


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
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
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/tracking",
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
    
    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # REPLACE THIS WITH YOUR ACTUAL API CALL IMPLEMENTATION
        # ---------------------------------------------------------
        # Example implementation:
        # response = lib.request(
        #     url=f"{self.settings.server_url}/address/validate",
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
    