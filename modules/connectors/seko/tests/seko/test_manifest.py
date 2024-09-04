import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSEKOLogisticsManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v2/publishmanifestv4",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.seko.proxy.lib.request") as mock:
            mock.return_value = ManifestResponse
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["6994008906", "6994008907"],
    "address": {
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90001",
        "country_code": "US",
    },
    "options": {},
}

ParsedManifestResponse = [
    {
        "carrier_id": "seko",
        "carrier_name": "seko",
        "doc": {
            "manifest": "JVBERi0xLjcKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvUGFnZXMKL0NvdW50IDEKL0tpZHMgWyA0IDAgUiBdCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHlQREYyKQo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL01lZGlhQm94IFsgMCAwIDMuNiAzLjYgXQovQ29udGVudHMgNSAwIFIKL1Jlc291cmNlcyA2IDAgUgovVHJpbUJveCBbIDAgMCAzLjYgMy42IF0KL0JsZWVkQm94IFsgMCAwIDMuNiAzLjYgXQovUGFyZW50IDEgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9GaWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggNzEKPj4Kc3RyZWFtCnjaM1QwAEJdQyBhrGemkJzLVchloGduChaGM8DChVyGCiBYlM6ln2ioZ6CQXswFkjTRswDjolSucK48dKE0rkAQBAAu7xTjCmVuZHN0cmVhbQplbmRvYmoKNiAwIG9iago8PAovRXh0R1N0YXRlIDw8Ci9hMS4wIDw8Ci9jYSAxCj4+Cj4+Ci9YT2JqZWN0IDw8Cj4+Ci9QYXR0ZXJuIDw8Cj4+Ci9TaGFkaW5nIDw8Cj4+Ci9Gb250IDcgMCBSCj4+CmVuZG9iago3IDAgb2JqCjw8Cj4+CmVuZG9iagp4cmVmCjAgOAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA3NCAwMDAwMCBuIAowMDAwMDAwMTE0IDAwMDAwIG4gCjAwMDAwMDAxNjMgMDAwMDAgbiAKMDAwMDAwMDMyMCAwMDAwMCBuIAowMDAwMDAwNDYyIDAwMDAwIG4gCjAwMDAwMDA1NzUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA4Ci9Sb290IDMgMCBSCi9JbmZvIDIgMCBSCj4+CnN0YXJ0eHJlZgo1OTYKJSVFT0YK"
        },
        "meta": {
            "ManifestConnotes": ["01593505840002135181", "01593505840002135198"],
            "ManifestNumber": "OHG00288",
            "ManifestNumbers": ["OHG00288"],
        },
    },
    [],
]


ManifestRequest = ["6994008906", "6994008907"]

ManifestResponse = """{
  "OutboundManifest": [
    {
      "ManifestNumber": "OHG00288",
      "ManifestedConnotes": ["01593505840002135181", "01593505840002135198"],
      "ManifestContent": "JVBERi0xLjcKJfCflqQKNSAwIG9iago8PC9GaWx0ZXIgL0ZsYXRlRGVjb2RlL0xlbmd0aCA3MT4+CnN0cmVhbQp42jNUMABCXUMgYaxnppCcy1XIZaBnbgoWhjPAwoVchgogWJTOpZ9oqGegkF7MBZI00bMA46JUrnCuPHShNK5AEAQALu8U4wplbmRzdHJlYW0KZW5kb2JqCjggMCBvYmoKPDwvVHlwZSAvT2JqU3RtL04gNi9GaXJzdCAzMi9GaWx0ZXIgL0ZsYXRlRGVjb2RlL0xlbmd0aCAyMzE+PgpzdHJlYW0KeNpljzFPwzAQhXd+xY2wxHEdnA6Vh1bAgBBRWwmkqsMRn4JRiZHtSO2/5xwPHTrY1nfv7t2zhBoWoJagoK2hAVlL0CCXGlpQsrlbrcT+8kcgOhwoildnIxw0D22PYuOnMYE0Jnd1wduppwD3H4Tx0gXHml5U6qHoxWWDCU9+KG4gs0+Rn87pZZcwETCgrOr89pjdjRGf718/1CeuMXSYEoWxwO4brRuHAs+ed7ZX02tyvgLlsFkUb2Qdrv0ZDjWzqnQ++T9j4qYIj3PXlqKfQs85m5n3wf3eDq1PRPamPO835h8r6WAfCmVuZHN0cmVhbQplbmRvYmoKOSAwIG9iago8PC9UeXBlIC9YUmVmL0luZGV4IFswIDEwXS9XIFsxIDIgMl0vU2l6ZSAxMC9Sb290IDMgMCBSL0luZm8gMiAwIFIvRmlsdGVyIC9GbGF0ZURlY29kZS9MZW5ndGggNDQ+PgpzdHJlYW0KeNolyLENACAMA8F3CBJd9me6bBJk0VxxwExwwMiEWaL+pdnigtTwAG3LA9cKZW5kc3RyZWFtCmVuZG9iagpzdGFydHhyZWYKNDgwCiUlRU9GCg=="
    }
  ],
  "InboundManifest": [],
  "Error": [],
  "StatusCode": 200,
  "UnManifestedConnotes": []
}
"""
