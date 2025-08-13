import time
import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.canadapost.utils as provider_utils
import karrio.mappers.canadapost.settings as provider_settings


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

    def create_shipment(self, requests: lib.Serializable) -> lib.Deserializable:
        shipment_responses = lib.run_asynchronously(
            lambda data: lib.request(
                url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment",
                data=data,
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                    "Accept": "application/vnd.cpc.shipment-v8+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": f"{self.settings.language}-CA",
                },
            ),
            requests.serialize(),
        )
        responses: typing.List[dict] = lib.run_asynchronously(
            lambda data: dict(
                shipment=data["shipment"],
                label=(
                    lib.request(
                        decoder=lib.encode_base64,
                        url=data["href"],
                        method="GET",
                        headers={
                            "Authorization": f"Basic {self.settings.authorization}",
                            "Accept": data["media"],
                        },
                    )
                    if data["href"] is not None
                    else None
                ),
            ),
            [
                {**provider_utils.parse_label_references(_), "shipment": _}
                for _ in shipment_responses
            ],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(lib.to_element(_["shipment"]), _["label"]) for _ in __],
            requests.ctx,
        )

    def cancel_shipment(self, requests: lib.Serializable) -> lib.Deserializable:
        # retrieve shipment infos to check if refund is necessary
        infos: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            lambda shipment_id: (
                shipment_id,
                lib.request(
                    url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment/{shipment_id}",
                    trace=self.trace_as("xml"),
                    method="GET",
                    headers={
                        "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                        "Accept": "application/vnd.cpc.shipment-v8+xml",
                        "Authorization": f"Basic {self.settings.authorization}",
                        "Accept-language": f"{self.settings.language}-CA",
                    },
                ),
            ),
            requests.serialize(),
        )

        # make refund requests for submitted shipments
        refunds: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            lambda payload: (
                payload["id"],
                (
                    lib.request(
                        url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment/{payload['id']}/refund",
                        trace=self.trace_as("xml"),
                        data=payload["data"],
                        method="POST",
                        headers={
                            "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                            "Accept": "application/vnd.cpc.shipment-v8+xml",
                            "Authorization": f"Basic {self.settings.authorization}",
                            "Accept-language": f"{self.settings.language}-CA",
                        },
                    )
                    if payload["data"] is not None
                    else payload["info"]
                ),
            ),
            [
                dict(
                    id=_,
                    info=info,
                    data=provider_utils.parse_submitted_shipment(info, requests.ctx),
                )
                for _, info in infos
            ],
        )

        # make cancel requests for non-submitted shipments
        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            lambda payload: (
                payload["id"],
                (
                    lib.request(
                        url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment/{payload['id']}",
                        trace=self.trace_as("xml"),
                        method="DELETE",
                        headers={
                            "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                            "Accept": "application/vnd.cpc.shipment-v8+xml",
                            "Authorization": f"Basic {self.settings.authorization}",
                            "Accept-language": f"{self.settings.language}-CA",
                        },
                        decoder=lambda _: (
                            _
                            if lib.text(_)
                            else '<message>Shipment cancelled</message>'
                        ),
                    )
                    if payload["refunded"]
                    else payload["response"]
                ),
            ),
            [
                dict(
                    id=_,
                    response=response,
                    refunded=(
                        getattr(lib.to_element(response), "tag", None)
                        != "shipment-refund-request-info"
                    ),
                )
                for _, response in refunds
            ],
        )

        return lib.Deserializable(
            responses,
            lambda ___: [(_, lib.to_element(__)) for _, __ in ___],
        )

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

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable:
        ctx = request.ctx.copy()
        data = request.serialize()

        if ctx["retrieve_shipments"]:
            shipments = lib.run_asynchronously(
                lambda pin: lib.request(
                    url=f"{self.settings.server_url}/{self.settings.customer_number}/{self.settings.customer_number}/shipment/{pin}/details",
                    trace=self.trace_as("xml"),
                    method="GET",
                    headers={
                        "Accept": "application/vnd.cpc.shipment-v8+xml",
                        "Authorization": f"Basic {self.settings.authorization}",
                        "Accept-language": f"{self.settings.language}-CA",
                    },
                ),
                ctx["shipment_identifiers"],
            )

            group_ids = [
                _.text for _ in lib.find_element("group-id", lib.to_element(shipments))
            ]
            ctx.update(group_ids=[*set([*ctx["group_ids"], *group_ids])])

        response = lib.request(
            url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/manifest",
            data=data.replace(
                "<group-id>[GROUP_IDS]</group-id>",
                "".join(f"<group-id>{_}</group-id>" for _ in ctx["group_ids"]),
            ),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/vnd.cpc.manifest-v8+xml",
                "Accept": "application/vnd.cpc.manifest-v8+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": f"{self.settings.language}-CA",
            },
        )

        manifests = lib.run_asynchronously(
            lambda link: lib.request(
                url=link.get("href"),
                trace=self.trace_as("xml"),
                headers={
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept": (
                        lib.text(link.get("media-type"))
                        or "application/vnd.cpc.manifest-v8+xml"
                    ),
                },
            ),
            lib.find_element("link", lib.to_element(response)),
        )

        if any(manifests):
            ctx.update(
                files=lib.run_asynchronously(
                    lambda link: lib.request(
                        decoder=lib.encode_base64,
                        url=link.get("href"),
                        headers={
                            "Authorization": f"Basic {self.settings.authorization}",
                            "Accept": link.get("media-type"),
                        },
                    ),
                    [
                        _
                        for _ in lib.find_element("link", lib.to_element(manifests))
                        if _.get("rel") == "artifact"
                    ],
                )
            )

        return lib.Deserializable(response, lib.to_element, ctx)
