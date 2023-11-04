import time
import typing
import base64
import karrio.lib as lib
import karrio.core.errors as errors
import karrio.api.proxy as proxy
import karrio.mappers.boxknight.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, requests: lib.Serializable) -> lib.Deserializable:
        responses = lib.run_asynchronously(
            lambda data: lib.request(
                url=f"{self.settings.server_url}/rs/ship/price",
                trace=self.trace_as("xml"),
                method="POST",
                data=data,
                headers={
                    "Content-Type": "application/vnd.cpc.ship.rate-v4+xml",
                    "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_element(_) for _ in __],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """get_tracking make parallel request for each pin"""
        _throttle = 0.0

        def _track(tracking_pin: str) -> str:
            nonlocal _throttle
            time.sleep(_throttle)
            _throttle += 0.025

            return lib.request(
                url=f"{self.settings.server_url}/vis/track/pin/{tracking_pin}/detail",
                trace=self.trace_as("xml"),
                method="GET",
                headers={
                    "Accept": "application/vnd.cpc.track-v2+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        responses: typing.List[str] = lib.run_asynchronously(
            _track,
            request.serialize(),
        )

        return lib.Deserializable(responses, lib.to_element)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        def _contract_shipment(job: lib.Job):
            return lib.request(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment",
                data=job.data.serialize(),
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                    "Accept": "application/vnd.cpc.shipment-v8+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _non_contract_shipment(job: lib.Job):
            return lib.request(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/ncshipment",
                data=job.data.serialize(),
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Accept": "application/vnd.cpc.ncshipment-v4+xml",
                    "Content-Type": "application/vnd.cpc.ncshipment-v4+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _get_label(job: lib.Job):
            label_string = lib.request(
                decoder=lib.encode_base64,
                url=job.data["href"],
                method="GET",
                headers={
                    "Accept": job.data["media"],
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            )
            return f"<label>{label_string}</label>"

        def _process(job: lib.Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "contract_shipment": _contract_shipment,
                "non_contract_shipment": _non_contract_shipment,
                "shipment_label": _get_label,
            }
            if job.id not in subprocess:
                raise errors.ShippingSDKError(
                    f"Unknown shipment request job id: {job.id}"
                )

            return subprocess[job.id](job)

        pipeline: lib.Pipeline = request.serialize()
        responses = pipeline.apply(_process)

        return lib.Deserializable(responses, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        def _request(method: str, shipment_id: str, path: str = "", **kwargs):
            return lib.request(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment/{shipment_id}{path}",
                trace=self.trace_as("xml"),
                method=method,
                headers={
                    "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                    "Accept": "application/vnd.cpc.shipment-v8+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
                **kwargs,
            )

        def _process(job: lib.Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "info": lambda _: _request("GET", job.data.serialize()),
                "refund": lambda _: _request(
                    "POST",
                    job.data["id"],
                    "/refund",
                    data=job.data["payload"].serialize(),
                ),
                "cancel": lambda _: _request("DELETE", job.data.serialize()),
            }
            if job.id not in subprocess:
                raise lib.ShippingSDKError(
                    f"Unknown shipment cancel request job id: {job.id}"
                )

            return subprocess[job.id](job)

        pipeline: lib.Pipeline = request.serialize()
        responses = pipeline.apply(_process)

        return lib.Deserializable(responses, lib.to_element)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        def _availability(job: lib.Job) -> str:
            return lib.request(
                url=f"{self.settings.server_url}/ad/pickup/pickupavailability/{job.data}",
                trace=self.trace_as("xml"),
                method="GET",
                headers={
                    "Accept": "application/vnd.cpc.pickup+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _create_pickup(job: lib.Job) -> str:
            return lib.request(
                url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest",
                data=job.data.serialize(),
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Accept": "application/vnd.cpc.pickuprequest+xml",
                    "Content-Type": "application/vnd.cpc.pickuprequest+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _process(job: lib.Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "create_pickup": _create_pickup,
                "availability": _availability,
            }
            if job.id not in subprocess:
                raise lib.ShippingSDKError(f"Unknown pickup request job id: {job.id}")

            return subprocess[job.id](job)

        pipeline: lib.Pipeline = request.serialize()
        responses = pipeline.apply(_process)

        return lib.Deserializable(responses, lib.to_element)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        def _get_pickup(job: lib.Job) -> str:
            return lib.request(
                url=f"{self.settings.server_url}{job.data.serialize()}",
                trace=self.trace_as("xml"),
                method="GET",
                headers={
                    "Accept": "application/vnd.cpc.pickup+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _update_pickup(job: lib.Job) -> str:
            payload = job.data.serialize()
            return lib.request(
                url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest/{payload['pickuprequest']}",
                data=payload["data"],
                trace=self.trace_as("xml"),
                method="PUT",
                headers={
                    "Accept": "application/vnd.cpc.pickuprequest+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            )

        def _process(job: lib.Job):
            if job.data is None:
                return job.fallback

            subprocess = {
                "update_pickup": _update_pickup,
                "get_pickup": _get_pickup,
            }
            if job.id not in subprocess:
                raise lib.ShippingSDKError(f"Unknown pickup request job id: {job.id}")

            return subprocess[job.id](job)

        pipeline: lib.Pipeline = request.serialize()
        responses = pipeline.apply(_process)

        return lib.Deserializable(responses, lib.to_element)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        pickuprequest = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/enab/{self.settings.customer_number}/pickuprequest/{pickuprequest}",
            trace=self.trace_as("xml"),
            method="DELETE",
            headers={
                "Accept": "application/vnd.cpc.pickuprequest+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": f"{self.settings.language}-CA",
            },
        )

        return lib.Deserializable(response or "<wrapper></wrapper>", lib.to_element)
