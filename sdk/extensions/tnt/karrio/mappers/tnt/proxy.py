import urllib.parse
from karrio.core.utils import XP, request as http, Serializable, Deserializable, Job, Pipeline
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.tnt.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    # def get_rates(self, request: Serializable) -> Deserializable[str]:
    #     response = self._send_request(request, '/expressconnect/pricing/getprice')
    #
    #     return Deserializable(response, XP.to_xml)

    def get_tracking(
        self, request: Serializable
    ) -> Deserializable[str]:
        response = self._send_request(request, '/expressconnect/track.do')

        return Deserializable(response, XP.to_xml)

    # def create_shipment(
    #     self, request: Serializable
    # ) -> Deserializable[str]:
    #
    #     def process(job: Job):
    #         if job.data is None:
    #             return job.fallback
    #
    #         return self._send_request(
    #             request=job.data,
    #             path=dict(
    #                 create="/expressconnect/shipping/ship",
    #                 get_label="/expresslabel/documentation/getlabel"
    #             )[job.id],
    #         )
    #
    #     pipeline: Pipeline = request.serialize()
    #     response = pipeline.apply(process)
    #
    #     return Deserializable(XP.bundle_xml(response), XP.to_xml)

    """ Private Methods """

    def _send_request(self, request: Serializable, path: str) -> str:
        return http(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(urllib.parse.urlencode(dict(xml_in=request.serialize())), "utf-8"),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self.settings.authorization}"
            },
            method="POST",
        )

