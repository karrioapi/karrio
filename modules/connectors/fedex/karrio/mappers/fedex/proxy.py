import typing
import typing
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.fedex.utils as provider_utils
import karrio.mappers.fedex.settings as provider_settings
import karrio.schemas.fedex.tracking_document_request as fedex
import logging

logger = logging.getLogger(__name__)

class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/rate/v1/rates/quotes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/track/v1/trackingnumbers",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.track_access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        responses = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(responses, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, requests: lib.Serializable) -> lib.Deserializable:
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=(
                    "https://documentapitest.prod.fedex.com/sandbox/documents/v1/etds/upload"
                    if self.settings.test_mode
                    else "https://documentapi.prod.fedex.com/documents/v1/etds/upload"
                ),
                data=urllib.parse.urlencode(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "content-Type": "multipart/form-data",
                    "authorization": f"Bearer {self.settings.access_token}",
                },
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx["cancel"]))
        confirmation = response.deserialize().get("output") or {}

        if confirmation.get("pickupConfirmationCode") is not None:
            return self.schedule_pickup(request)

        return response

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)
    
    def get_proof_of_delivery(self, tracking_number: str) -> typing.Optional[str]:
        import karrio.providers.fedex.error as error

        # Construct the request
        request = fedex.TrackingDocumentRequestType(
            trackDocumentSpecification=[
                fedex.TrackDocumentSpecificationType(
                    trackingNumberInfo=fedex.TrackingNumberInfoType(
                        trackingNumber=tracking_number
                    )
                )
            ],
            trackDocumentDetail=fedex.TrackDocumentDetailType(
                documentType="SIGNATURE_PROOF_OF_DELIVERY",
                documentFormat="PNG",
            ),
        )

        try:
            # Send the request
            response = lib.to_dict(
                lib.request(
                    url=f"{self.settings.server_url}/track/v1/trackingdocuments",
                    data=lib.to_json(request),
                    method="POST",
                    headers={
                        "x-locale": "en_US",
                        "content-type": "application/json",
                        "authorization": f"Bearer {self.settings.track_access_token}",
                    },
                    decoder=provider_utils.parse_response,
                    on_error=lambda b: self.log_request_error(b),  # Custom error handler
                )
            )
            messages = error.parse_error_response(response, self.settings)
            if any(messages):
                logger.error(f"FedEx SPOD Error for tracking number {tracking_number}: {messages}")
                return None

            # Check if the documents are present in the response
            documents = response.get("output", {}).get("documents")
            if not documents:
                logger.error(f"No POD documents found in the response for tracking number {tracking_number}")
                return None

            # Convert documents to base64
            return lib.failsafe(lambda: lib.bundle_base64(documents, format="PNG"))
        
        except Exception as e:
            # Catch any other exceptions and log the details
            logger.error(f"An error occurred while fetching POD for tracking number {tracking_number}: {e}")
            return None

    def log_request_error(self, response_body):
        # Custom handler for logging errors during the request
        error_content = response_body.read().decode()
        logger.error(f"FedEx API Request Error: {error_content}")
        return provider_utils.parse_response(error_content)
