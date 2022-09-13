import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.ups.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def _send_request(self, path: str, request: lib.Serializable[typing.Any]) -> str:
        return lib.request(
            url=f"{self.settings.server_url}{path}",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={"Content-Type": "application/xml"},
        )

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request("/webservices/AV", request)

        return lib.Deserializable(response, lib.to_element)

    def get_rates(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/webservices/Rate", request)

        return lib.Deserializable(response, lib.to_element)

    def create_shipment(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/webservices/Ship", request)

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request("/webservices/Void", request)

        return lib.Deserializable(response, lib.to_element)

    def schedule_pickup(
        self, request: lib.Serializable[lib.Pipeline]
    ) -> lib.Deserializable[str]:
        def process(job: lib.Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/webservices/Pickup", job.data)

        pipeline: lib.Pipeline = request.serialize()
        response = pipeline.apply(process)
        return lib.Deserializable(response, lib.to_element)

    def modify_pickup(
        self, request: lib.Serializable[lib.Pipeline]
    ) -> lib.Deserializable[str]:
        def process(job: lib.Job):
            if job.data is None:
                return job.fallback

            return self._send_request("/webservices/Pickup", job.data)

        pipeline: lib.Pipeline = request.serialize()
        response = pipeline.apply(process)

        return lib.Deserializable(response, lib.to_element)

    def cancel_pickup(
        self, request: lib.Serializable[lib.Envelope]
    ) -> lib.Deserializable[str]:
        response = self._send_request("/webservices/Pickup", request)

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(
        self, request: lib.Serializable[typing.List[str]]
    ) -> lib.Deserializable[typing.List[typing.Tuple[str, dict]]]:
        """
        get_tracking makes background requests for each tracking number
        """

        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/track/v1/details/{tracking_number}",
                trace=self.trace_as("json"),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "AccessLicenseNumber": self.settings.access_license_number,
                    "Username": self.settings.username,
                    "Password": self.settings.password,
                },
                method="GET",
            )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            _get_tracking, request.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable:
        url = (
            "https://wwwcie.ups.com/rest/PaperlessDocumentAPI"
            if self.settings.test_mode
            else "https://filexfer.ups.com/rest/PaperlessDocumentAPI"
        )

        def _upload(data: dict):
            name = data["UploadRequest"]["UserCreatedForm"]["UserCreatedFormFileName"]
            return name, lib.request(
                url=url,
                data=lib.to_json(data),
                trace=self.trace_as("json"),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "AccessLicenseNumber": self.settings.access_license_number,
                    "Username": self.settings.username,
                    "Password": self.settings.password,
                },
                method="POST",
            )

        responses = lib.run_concurently(_upload, request.serialize())
        return lib.Deserializable(
            responses, lambda values: [(n, lib.to_dict(r)) for n, r in values]
        )
