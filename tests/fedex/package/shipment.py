import re
import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.fedex.package.fixture import gateway


class TestFedExShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        # Remove timeStamp for testing
        serialized_request = re.sub(
            '<ShipTimestamp>[^>]+</ShipTimestamp>', '', request.serialize())

        self.assertEqual(serialized_request, ShipmentRequestXml)

    @patch("purplship.package.mappers.fedex.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        shipment.create(self.ShipmentRequest).with_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.settings.server_url)

    def test_parse_shipment_response(self):
        with patch("purplship.package.mappers.fedex.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = shipment.create(self.ShipmentRequest).with_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedShipmentResponse))


if __name__ == "__main__":
    unittest.main()


ParsedShipmentResponse = [{'carrier': 'carrier_name', 'charges': [{'amount': 60.94, 'currency': 'USD', 'name': 'base_charge'}, {'amount': 0.0, 'currency': 'USD', 'name': 'discount'}, {'amount': 0.0, 'currency': 'USD', 'name': 'INSURED_VALUE'}, {'amount': 4.72, 'currency': 'USD', 'name': 'FUEL'}, {'amount': 22.51, 'currency': 'USD', 'name': 'CLEARANCE_ENTRY_FEE'}, {'amount': 2.93, 'currency': 'USD', 'name': 'HARMONIZED_SALES_TAX'}], 'documents': ['JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMQovS2lkcyBbMTggMCBSXQo+PgplbmRvYmoKNCAwIG9iagpbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KZW5kb2JqCjUgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLU9ibGlxdWUKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago4IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjkgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllcgovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEwIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjExIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEyIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItQm9sZE9ibGlxdWUKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxMyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1Sb21hbgovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE0IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGQKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1JdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1Cb2xkSXRhbGljCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTcgMCBvYmogCjw8Ci9DcmVhdGlvbkRhdGUgKEQ6MjAwMykKL1Byb2R1Y2VyIChGZWRFeCBTZXJ2aWNlcykKL1RpdGxlIChGZWRFeCBTaGlwcGluZyBMYWJlbCkNL0NyZWF0b3IgKEZlZEV4IEN1c3RvbWVyIEF1dG9tYXRpb24pDS9BdXRob3IgKENMUyBWZXJzaW9uIDUxMjAxMzUpCj4+CmVuZG9iagoxOCAwIG9iago8PAovVHlwZSAvUGFnZQ0vUGFyZW50IDMgMCBSCi9SZXNvdXJjZXMgPDwgL1Byb2NTZXQgNCAwIFIgCiAvRm9udCA8PCAvRjEgNSAwIFIgCi9GMiA2IDAgUiAKL0YzIDcgMCBSIAovRjQgOCAwIFIgCi9GNSA5IDAgUiAKL0Y2IDEwIDAgUiAKL0Y3IDExIDAgUiAKL0Y4IDEyIDAgUiAKL0Y5IDEzIDAgUiAKL0YxMCAxNCAwIFIgCi9GMTEgMTUgMCBSIAovRjEyIDE2IDAgUiAKID4+Ci9YT2JqZWN0IDw8IC9GZWRFeEdyb3VuZCAyMCAwIFIKL0dyb3VuZEcgMjEgMCBSCi9iYXJjb2RlMCAyMiAwIFIKL0VuZ2xpc2hPbnl4Rm9sZGluZ0VuZ2xpc2gucG5nMjcwIDIzIDAgUgo+Pgo+PgovTWVkaWFCb3ggWzAgMCA3OTIgNjEyXQovVHJpbUJveFswIDAgNzkyIDYxMl0KL0NvbnRlbnRzIDE5IDAgUgovUm90YXRlIDkwPj4KZW5kb2JqCjE5IDAgb2JqCjw8IC9MZW5ndGggMjkzNgovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0big+dU1dUSZyLGpcUTJkTVddaCw0Xic3R0BMN3VVbEkiaUdyZEFASUY4SmZYPjBuOE8+bSxqM2RPW2wpMVY9TXFEMGc3ZE1Iay1eZHAKOFpoRUg3ZDNOOk5fOz8/WFxiVCwscUk5Oic6I0tNKjF0QFxXdS9sb1tbP2JQcC9LVTYuaVRGXWIhP1RLJSFQbi1Vc1s1Jm4mKGksU3JMTVkKUzcxSVhwNl01LUl0REIzUkUzanMzTks1a2BiQDdMaHRQZFhfdDI/QF1tJkxkcEJLWm1hZnRjNG5gYWY2LF9uRFlITFxlMmxgOC5uSkRxR2sKMHFVI25vbUQ1Zy5aUTdgWVtNazZkckQiJHMhaWIsKXRqKDNnSiY2Mj0mc3FSOlhCSDlGTnVNckMqPjdmMGUpNDJOR0NJSkVkL1RiU0Z0JE0KWGhEUGlvNE1CWnMnVWxvWSdqLipfcmxxQkw/KmU0PC1KIyEyYlhdQ05FL3EyLS5ePDFxNiojaiZWOmZSVV50ZTFLKGRKa185dTNmZz87b3EKS0JaW2RiRDQnOGtPby51UEVRIzo3V1MyLScqXVFSMkI5LTBZJiFVZDBVYT1hNClVPU1PUy1VQmNOZjVQWE1eMTM4L2NQRStFIS8wK19XJzYKcWIub2dyakJkUSM+bzknNSEoPykjZDleTStXYWMuWnJBTDc/dVMkXFZOZTU4XE1lISw+WCFXNFteYGtaQkRXTmE7Nm5XXUFvUChRL3ErXDAKWiVOI0YhMFw2MCMoOW9kXFElPz9FUEZhO0kiXTNgR1N0LzcrKComZUNEWyIxND9kP25LQC5Obl1PXEVsYmlIZEswJk4qNyg0cGMhL0pjaCQKSjQ/UWluO1U0SHMpXihlYTRcUmJJMytEdUBFMWxxXkNpLltpJFcxN1VIZWJaXC4zOzBdWFhMcVldN28/UUFiIUxhbU5kNC4yL25cSElcYEIKZ0ptdUBsNl5rTCYsTzJNaUYiS1NyU2ROSWYmJVBtYmFhXkc4PVs6ZlY+cjlfWUlwYEE2QCxEM1JzcDRYSWVnLUBsISEjOURTIzkzP25jLDwKQ2ltaGAkW2M9NydpPm4kL0VxWytINmoiZlpEKE9BMmAqIWE+ayNSOzYqRyY9NWxsXDErMEU3LkRWIVhNPydebVlOIjgkcURBOFxIP0IwWy4KXzkqPDFJZ29CSyJuO1FhZCJBP2w4NVonazhoTEZPTj9vRkchZjwtQylMJUdUXDVXYU4pcl1LQzRqOT9pIzJiSVdvc2FhTSpScWRbTGw4P0cKK3VhdDUjUy9oVlprZ2UlIzg9NUAnVlY+TlE2S1UmMjNhaj9aTy5SYU8vXVZXYV4/RTpqWGNDXyZyKlxWbnNXXipxTkouOCw8aXRYMCMlOzcKJVJIZHUiPlBybXFPYGwrQyEuNSxxKVYhKjpLSVBnOTYoQTVvXUplSVIrcDdKN0pSZiktYGsqSyRNNF9GLWJfKUtxdDkmY0VFdUE7cjVGXHUKJTVGLGNMMG1jVFM6a1VHZz9Oa1gzK15fN3JJJGhzL1NFUFFUQG43Mkk2NFkkbEMva1taWzBHL2xgXEwwWDJVO2Q6JTl0OnJfUDg2ZGc+b18KVzovRjFHMDU5K2Nma0JGYkgnYXNPajMlVGxNQSh1OVdtTzBlI2hcMUM+PSs5NE8nMiRuSlRTTWciIy80MlAzLGIoS1xkXzRibTghSShQO0QKKyJNTGdxZU5jZlV0YU1vKjU+VlJUVi1rQW4qXUl0Ym9ZUVVVOyExSCtdR0g4XGw/OEI2OEk6MU9wSjRJMFwvX25QQnNXXVc+OkJBbFVzO0kKVjhUTy1LcmRbYSFxKSVMI1MyXyI6TihQa1tENjQ7JS00NFFhblZcLzovKl5KPjQxOD4wJkg2PVtPTVQ+RW4mKF9ZWCE2alxDZ2pEWmtVJTsKaFU0aWNXQzIrQmBscVopSURYMSchckc8XFMoXS86LEhcQlwvc0IyZ2VzTydfUzpmKVYpLS84Y0JUJzBuampKJiwwUms4VkpUbnE1RCxPVWMKVjc+czhvY2JeczZvOXQwUTlmRC1cWzZdMV1XR0dPLm0vZVhFIVwuXEcnPV1AS0tyPEZNTCxLayJMXVdDbVYjR0VtbD1FciY1amQuQVAqIUkKWTRhJ1o0KV5aXzxeXFMtYFpgPycxP01ERyFfLUBMJUJpLlI0VW0idGBZQ2xhMEQyPG5GX0pCN0ppOVVeYGVaKE9pa1ptJ21hKTxQTjRdclkKUWRUUz8wLmdTL1BsUCpkYWA9YVZFPiMnQ0pYS089YDpidF9LZiQwOk5Da1FFZjFMUmokL08kTEFUPEQ8UXRba15KRlxYO0dtP0RuOk0yXT4KJEBrYExtNClNXWJHNWFqZWNMaG8mc1REVEZ0IyluJEc2b2YxPCdrb1pgJSU+VGdMPTJXWzxiIW5qNFg+QUJOWW1HIi1lL0MsTDtAIyR1WkYKNk9UNXAiVHE6cUQvQTklZCs2aWtPbFRcM0lvMEFSXHV1XSJOLE1FXS01R0kjWF5gZCxhOlQ/YjtkUVZsIS1KckkxdERbdEFTK2hKVkE1JTQKW1JXJzpodVFwZTRPKXQuPihNQ0tmcy4zc1IhLiFYV0leSTpLIVVfV2NBc2RzVVRNJXBDRi1ibVI1ZzBzZy43Mk1TV1s3NG1GMF0kYSNKWmsKOUheZFFfSjY0Z2JRdFldL2lKbTg7IUZQL1taZ2hxXmZIYVJVRl5TISpyREs7MCVXXkdbTV03JDxuckNOM1xrRkRDdUZLOTksUXVzb1AiWlMKVjREWk5PaCJ0YjVSKkRkMmNKRz08KzkrMjQ/V2tdT1Ryb2hgR0o4W0NDV29ANHVCJk5IVz1tSGR1PC5XUGxQKmRpXTJeNVcnMnEuLjU5NG8KOlRnTSJKUzUzTCRqZlkpXmcmQiw2KWM9VSlkKj1KJW5fREA8YW9LTjorRzA4LixcO2tSMT9ANzZMNTBBUCc+UGE9PVFsVUAnMTVITHFGYk8KOygmLkhnNTBwO0YwMzVFL0xzRHFMKkBgQzBAQy1ZVHA1ViNpdTFbLmlycEl0LGYhKSghUDZFQy5oJ1F0ai8jSiRSOHUickwsWzwxPVlJRnIKL11aL0VKc0JmTGJEaz5waDEvXEVWOCxiVCEkWlxZZkM2aXA3Xm5cKC01Q1Y+V0IyRjYmJjVuaWRQLiVbIlZaTCsqRDZkRGtfcUJwNStQN0sKZWlELUJVPkRSOjBlKlg1UjhkUmJkdUAiRk1vOlVuUElhRGknaGpBRidwIj46TCFMTWZQNyJtWlhQSCZMOWxTaWJNMDVNNEY/XWFNZ1RIbDcKImYkalMqUXVmW1VkczE1IklEW2BTSU1JJVomU0lnXXM1a1onX2N1Sy9cQmwkVGssMk5YPHBwPE5yIzdkZTkvRTRxZ1hDOExtSD9lXENyPiMKNiFDVnBfK0FqXG9pZSRTaSIwXCZXPjpgZ180LzRTP2JcVGhVI01LaCdcb3NhOjE4O0w2UFwmOypyNk0pZEtpUkRdNmBeOWxlX14zb3JCVW8KXjRyRVFFPXBbYzxWQClcTmhtSVc7TCQ7NWdJNldXMmNfcXMlQylZQGVFNkVJLy9hOmNbZTFFVVkzJXI5QDtkIURgazJkVldkKTIpbS9YTDkKM3NmNE9hMD1ZKCwrdGZcTT1BQk8rP0hwLmxoTFtRY0FMNWsmWmgzKlJgLyZVaHI3X11Ab09sXD5lVkVhQjpXQSZCTCdcITIhLkdlcF9HTnMKLSw7YS9dW1dZLC9fSj41T0JnJGwmaXU9TzA/cGwyJT9pXkc8WyspQ2hiJyZRKnJAbzZZJyMsdTBVVWJRYm9VZSFrPEhbJmVwIT4ycis6KUwKSEMzVUpRZCRKKXJySywzKylffj4KZW5kc3RyZWFtCmVuZG9iagoyMCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ3Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDY5MgovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdCj4+c3RyZWFtCkdiIi8mOTkrXVslLiFqRmJxKT1OOU04Vjw6KChPamVZPURbTFQ5aUlNcjw2QU9MalVkbFA8ZVptckAkbEt1YDtvayxfQk07SExhJDpeTzxwCi0ray4nOSkoUVQpLSlgUiksVV5EN05nWzckRSdoVT0hSyMiRTxwN1VFNURWM3ArU1FWYVJYcidITCcjbjxsQm9JYDRSKC9UOSRJY0VbRyo9CmlHYlA1RHQ+JVNVTi1uTDtzJ3FNXGVBUzFbR1IhYmZwbm9yQUk1VSxBaD8wPS1DcCglYV5iUSdAZExcWldMZzhPU0ReNVJDYmdwYGxoaDxXCj4pLDtzZUsxS2xsTTcqPzhsQ3FgPzo5W2AhNlw/V1sxKFpfPUM+Q1BPPFAzcl9BI1RDMUxJVUIsIjNPbzIlOl5RQWlFI2IvMFtNKCplY3RzCkdAUC1kbUByXmVGPyFcL2QpRilnRDInV0VvcGIxWScuM0FXU0FtKzFRNSxAXVg7RmlJbkx0Rl5QJ1JoMVEqQCo3WDkjays8QUYmcEIiWlBoCl01Ri9DZj8pWXUsPCxcLlNXbWFuW09zLj1kbEg2ZGxdM3NZOjVuK00vP3NBKSpfc19EXnNxOmNDSk4qKlIjLzwuLydqKmxDKjIlLk9sYmcnClVNNSlNOGVfYmdsL0YtaSY1WT9AaCM5SzBaPCwuLmYnW3NCM2A9YS0jOmEqYTFWTiVpJEFDZz9ZUllmJVk8cyxtLDlfUjNhXWAlRHFkalNVCmdrTS50SFxtW3JedC1OL2xlQ0lSXG5vOTYwbC1RNjo+ISxcN3NGXGU+VjRpI2tCYnBnXCE+YlZoU1pMXm4pO2pPbEBlJ2FEVl4lPkdXIyFCCj4rSDlUIThlIllTKnAiOzxYR0MzIjN1JWknISprcU8vLF46NU8rPS1EP34+CmVuZHN0cmVhbQplbmRvYmoKMjEgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCA1NAovSGVpZ2h0IDU0Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDI1MAovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdCj4+c3RyZWFtCkdiIjBKXyNdMEIkcSFuYz9iLVptUC9yZSsrSTJCaklXLTkwUT5PN1s6JFdKKEMzQ2FBIk5zN1hANzAkLFR1JWJAWVF1aG5YIjFkLmFTVTZSCidHPTNBWTdyLWcsRycpYiZLWThPS2ZUYjJHX0suKFQ/dFJTWTJRIlc7TWI0WiZbKDFgKG5rI2UrJSI3QSh1XCxBO3JnT29yPlNFKXJ0Tm8mCiVjSzhBPTxXSDknIlgxUjg7QGFFSycqZ2tJS2I0MShSPkUpKTIwKSUvajlnYk9cMG1NZTwsJyMuXHJXPCs9SUJRUUFAMCNDYVdZV0FYUnJvCj1Jampdfj4KZW5kc3RyZWFtCmVuZG9iagoyMiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDIwOQovSGVpZ2h0IDg0Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDQ4NTgKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvYTYjSGZjJmQuaCw6XFBuRz1IaltoUUorLklQQkFSalVlR0JebC1KUF1yMTFVb0dRLG5GcSllV0kzVF4yNS5LMmZbb0NfcT5KIlAmUQpwXnQ4SjVCZkNZUCQlcnEyOGU4OWdqQFA8JydbZmVOPE80XEFoVWA1XkBHMiU+O1ZXYiJZcW90PU5bbEEpVzpWTSJtWVZYbjVWOiJeIT07XQpOQEJ1Ml4iY2BKN1cucG9sZktdTm90TnEqXFBYSyVQJVxqQUkrZC9MTiNiYltyLl9Na1tPSzdbKjJbZ1xXaFdMRWtCVlAlWCdNaUpZQSRERgpvOjVMJyQma1BoISMtRWxZP2xCXlMmNSU+YSFYVG5tQG08OFFLMF9nOC82JkFLJy5FLyxIRytQRWonMUZhN0dob2UtViktJi0qRW9STzRzYwpbWzZLcTIma2hjPC0+LTdpUlpZVT8qQGpDKzNSUSwlWk4qazwxVD8wTmhZcDhcUjlNSCtcNCNbMiwzUlAkYkQuW0ovMHU+ZEE5MyNjTUQmRwpdZVJfLD1JLWdGQlFVNU5sRW8+aSdRIloyImYhIkQ2MVYvOSNIK0RsKmE5T1lLcElJbm07VExMImAnYF9WcDInciNYbjhFUUReVWJQPCU4agovKVsqXzkhdWtsbmRFOEU6LEJqa0JSJ2laVU5fLTJmcmMna0kxRGksUVwkRm5jMCYzI1JgOCtiP290S0BMW0hTQDE4ZnA4VCFCMSpZNGArZgpfJzdTVWMjX0pxJF08UDo4U2VRSitWMS4sbFlCYGVNUzA6SVtHOGM3WlY4WixMJnQxaiY4bkMpWmxxTDhaMFxtND1ccTVnVVkjcS82NjgyNgpmQFJOVSdSTERwQ1VvR05Bc28vNiUwYEVfSjdMZ2Q3VycsbmU+UyhfQzVzSkMlNEFfbl8pUmUkMjA2V1EmZ0ZTTGRzX2FaaiZCL3Nral9jVAo+TiZzMTNqYlVHJ1EpPjopLjpzbSJtMyFmI0NAPzNcY2gldSlWPDE+XklhNyIoLz1aYCY8OVwjWGVFZEZXR1tFQkZnUmlaUU1UXldRamdsSwpqQlRPaVZETiwjKF1pcGItQGFTW1pMKjcnWGUhMGkzI15DRGk3Sj9zUFwiO2s2ajZxMSJZLEVmLiJdLGJOYVVhPkMiUk1eIW4+T2pyaUBKWApnQkFPIzQrMk5yMXAzQ2JZbkowLWJKXS1rJEZYcSg1NDQycEw4T1plZ2xUND5ZJWtRJGlVaWE5XE08WTktJTgoOm1vVD5PLG5jMUpXTVU2WAonXT42dC83TWAuXFpESyJOI1QnaGRvREInZ1pecWpFYiIwUTkpTyxSaGxsVig5LWJEdDtHQT05XWFCNU1TXD1tQkxtNF5HTmUuSV9PTSI+YQpJNU9iY1NfLEtvR1trTXMlOCFCJWR1J0RcKWJDWjVXcGppOCZfcmhkSyVLb2ZbVFJDS1VTJVdEN1wqKklDN0tsOll1dCx0YG4lcERQIkg9YAonZT4+J09zSCxnaVMhY09mTCJVNGVxXj5VQ0BBdVJnQComN0JVYD80KXQiIidITGpGXWNOR0dSKkQ4KUZyN2BENmxFUitAS2JzIzVPXVRBXApOSStCcGFtLyc3cEBXWGlDcF9IakpkbHA2Q1tMODooblYrJis/UGxzKSM6WDAxdDYjKicrNkpDRF4lLGxSYmpGWyJET0EwUk48MzxLZms7cQohR0lAWlVRSlxuKVIlVS1DYnJdJDFzOiE9UjhCMVZjMVArRj5bKjxTST1AYlw2NzBVJSg7YXI0Y2NEX1NYYkVfJ3IjZ0Jhbk4qNVcyUkBhJgpaVjVTMyQiXipfPl0wZWNWLlNLRE9HXV48WCdyJW1dZWopNTlhdSQhMFNEMUteMFw7QidqLk1ubTtGWSksQWskL2EmPm5yW0xSMmA+bjNqPApUTnIiMnAkKFJZLkkmV0VMQnA2YWo2bDVVQ0w7WSNSYjdXNVo4XjQvLnNzSDpLaydILEFqYFNULmg7WiYyLjpkb2A0MVVyYFQqLUEzOnRgOApsXko6JCxBZ1dpNFhxcEFNNjRTYFVPZUNdUllXR2w3cSoiWTs6dHNFNCFOK19nOjE3P01UNyRgRVRqR1BlaStEJjgodEJdSDttamEmbUtxSQo3ZnNdRTFfRV9hTykyQTNfXlFbMyFIVmJIWUUlVl9jIUljLSphJyU9UF1oQ2YsOSRJWzQkUVksMzgvaGxiNEBFPU1KS2cuMiYkKmlHckI7TgpNL1pXKEQsJmJecjFHOWdBLSJqIStGWWErcDxsRGVwXTVQZVZMITNnckduMWRCRHJVc0ZxJjE3IlFVPSxbQzQsRiJLM0VwPCxSXGFpVG1RbgpCWCpNYihwM1g2M3U3OXJAY3FDRiU7QTxIcEgsV2xqQ1N1dStac1guRlZNNFchT2ZPNXEnT0UuaS4sT0hOMShUY3FHXU5sbXEjdGtCPzFOcgo3aGtcWloiRScvJlBYRTJXYUxLRjltJUJNMEo3cz5LWjJaPlFEOWVfbEFgQWUwbWQ4Mz4qaFFqRFFSSXQxTFFlJ1NZKFpyY1s1PUhAJSdWIgosW1AvIWpwKm8tUTpBYU4oOUhxVVQqZSZXcisnOG8yZDBDTzY+Q0Q/QUxCOUFTZ2c1JkxIIVArb2ZIUU1MXksvXjBlNGY2ak9zKzhOWCEtWgolWkhPNSZpUG9WMyFvTSFILFVWLCNiVnFpIUBobFBnQHVUSygvX21lY0VTRFBfXiVhP2c9TF1qbjVyVV44STY/WD0uQkRCW18tJlgwKkcpWgpSSy9VMTlQby5kRixRdD4vV0JSPT1iMnRGUWE1WjIrRCJKPFNeZ0NrPVw5OjBNNm9NXlVabTdjLSUoXGw5ZGJJRCxiQ0drMVU9Sy9fbDYjRApsQnQ8Ui1nbUhCbTsoZ2FnJU1GRGArcFBLJkIvPlo/VkxpNkBwSUloaSNtbFNWVTE5XDg4M1dSZTxhWE9icWRMRFtlS0A9Xy0yaF1PRlBhXwpWZGQtKW07W2VOMkNicSJKXVpdc1JZVjtjSD9AY2VMZEF1K006InNYblxpR1BOYzJhO05LVEJRZS0pW1lcIXVjKUtMbidPWVhPLGJnc2hkSwokOHNlInEjJjthLmFETFxbKT8vPF5uWyxMQ0xXL2hxYjkySWR1W1JlRyQ8KUckVVk7dG45Kyk6PGIra0orZWpRSU9JV0lQPXUoXyNDRDg8KAoyKj1MPVYpNUZPXWYzIWtOZls3dUckPClHJFVZO3RuOSspOjxiK2tKK1lqMDwxOil0NjNecyJJN2c0LTNHUyFiTzFbIkQtVkpOQjkiZXA+XQpoRkUpNzszMjNJKU8sQ1NTZCUqYzJvLUxXU1tPMkFAXUlQXFpwbE1rVXVwaydDIiZRP1pGLXRSTSFlaSEqcyQrRTVyKFE7OnRkZE8pVkZQXgpKcjd0ImBfYVdOaS5oMVtkU1ApL1lSaW4tIVJpIWo9R0lDITlEY0o+OzRdS0BdUDdCdDJeR0U9VixLJ3NrZTxNN2srMDwmI1osSG5lI1MxKQphcGpgcGAoa0hvcEtKVTFKKExEV0BKa0UicmBhODI8LlJbaSMkOCU8ZCk8c2MnTWcpc01VRHRIKlM6M3EoLDNZZ0ttJT5QZUw7NWJEKCE+Kgo3Wi8va3BjVlNGPCxiKkMiSyxvVV06Xz1TIThAZSg8XVNfIUFIPVQnPz4vTiE7NFVULmZRTF9fQVtKQ3VKRFdebzZqOEZTMHVERWhHbTdAWQpHKSovKSleXUg5OCRRODpXaTxcQ0puQF87XFVrRCRGXWNDNzwwJmxUTGdDZ2BPKC1STV9bJzM1OTZdbmUhcCVmQTwxKDFoKlE7bzFXMkI6UgokQ1dqNmo5ZUAtZTcmPSQ6ZCo1QCxDMz90NSlRSy47ZF5wLzpcNVNYVVMtR009SXQrUW08KSM4TjpqUzItSlcuTHB0ISonVis2TkRgPWhwNgpEO3VUWy5TMEk1XSsjY0NpSDJHY0pwLFVQSC1MTUoxKXBAVi9nZkBhX3RfZnFIKTQjalc1VEREUlZoKCkrdENbREpwXltxZT9MOCg5Tlc1RwomYlFraW1XW2ZYLCNzPCI8LWg9aTI2M1VrNjQ8MThLT205MSVHKFdiNz5BNHBxOCMrXFFZMCVBLFklWjEwP3FAUVhZb0wwcjYhXWtvVV0jcwo8X1w6JSg+OTMoYkJQRVNYb2knaSRwZT8hRStDI1ZXbyRLaS1qcWpzVkBhLy1WdV1BPWc+aXJbZVFWW1ZTVz1dSDZoUiZJSSslN29UbyFoWQonLS0qKmdPZGotP1IrWi8oOjwuRk8jaU0pZzhkKUdPSClmUiprMWA8aipSYF07a0hpSD5xSW1RTmJFU21MVHE0ZltTS0BcITs8aT5OQ0JbJwpHR281NjNibj07cmsuPVtGOmVxXW0/ListUUBBWU9rb20rZTluQjVQTSc7QW9NNV4wOTZIYTVFNjtqZ1hCbGYmdVtdI3MlWU4hbCRtUzRTNwpUXDpIJD9ZU2JrVDo/dC4uYyhrcXFXXyNeKTpmIjI/a1o0WlJPMWxoUzdcZXMqTmsxczxgQT9wcShqRloqV1NMLEcqbWZnJSlRWE0rRG03YwpmY1hLazhrcGoxNSldX0JkajFySmRuRFg2X3REQzZDNVJFaklnM20+IiFEOi0lTVIzVDYyNTcmVWIrPilbcykia2Q7YTgsZSkucGU7JjpnOwplajllVlZYaWk0ZzIsYVxvJ2pnMmZnbE86QVBoYFFkNmYoJVJOU0hWQ11sYF9EXiszMD9nK0dIKC4pZFsjJGsxJ25rIVtWbkhhRjhBVlAiSApMPDs4InA7WjxpJjNNR3BVa1g7P29WdWxqXXFsWFxsPUYpW2QpIktDZnFLWW4kYztWajF0cl4+XU5lSjtscjpraFcsN1pmIyxOJEdcW1lNaAokZT4vaEE6dWBpRjZJIkxLUFhLdEpkI1RbQ21vMkotWEpEVSEtWUFOK2szcWs+OClKcDwjVlEsYF5McGBdUEpKSCdWUVpGZUw6YTJjVmxgcgo/QjREPkZgdWcnQUBvRkpya1U1LlxaTWhzJVhtSSJjcUA6RSg1XDE9WzpQSGMoNU5uLGxCSHFUazolP0kwPzg3MDNrS0JOWjxjOWBzJ1FaKApndCghNSEyKC1uO1M2JVVXT11oYDZWTWRNcSxoK25WWU02dUZdMW9iPFlrRXEyK0ZXWGVLPDc5PWk/Xi8lWnIpL2FKUHBlR1JgViRGK1o/KQpbU1RePU03Jmk4Rz9FRWouOkhGYGdddUBIWGQydDo5TCEpI0IqTD1gUk5TSEglOWtaWi04Y1koS2pBT0VARDtoWUphKmMvYykrRkwuPU8wcQo8PydcZEdoX2VvbzxJXDFWJUUsRzg/JFUocVxvIUIkVGEpKVxlTl83NDY0bStbIWFDRkIlJjNhJ0wqUElXZj9DQl1QW0pzcTpLbCk7QCVMUwpaO1U/UU5BZUpYMWkmJjRCcmVHMisqUWpjMmVsMTVMR2AlPTxdWlwjZ2ZXPixXMUQ9JkAiTylqL1lbaFVPO3JRWEEqQFQhWlBKTzpCb3JvKApZWDxXSDsxaT1BWEojXiVkYThLYWBuSl4ubT5NZV4nLmRDKU9YPFZwLTlIX3NVb20vcD4oQ0hVXSJTYV40ZUE5TUdVZUJyQlBBTjFXOkkiIQoxKDYlL0Q9cz9xIV1SP0xZYDtPR1o4TDxKW2JLaC5yaVpKVzVgTFMoZC8rUyo1PTdILDdTRT9PNl47I3RRIXBXPUNvYy9NJ3RBaCZLUVJEJApRJm9GLzIlO3MhcDtCVVMyQm8jN25SOE83RjA5LTBWTStvcWRcOk0zbWEmPGFRTFNjP2pXI0hvKGssOTw5MENVIWJBQnFjIkRCI2hhcWMpTQo9dSMyVFtWXFhoKyJdKFUoPz5DMSRYdCIiUTtaIU9VNFQ5ckp0blNzPTBVLk1rMFAyJj1KTUtMOzgkciIjY2AuaSEqYmJYbGw/XCM6dHMlXwo3ZkpxTlxpcGorXyZILVRkdGpII3FLbGJZPypIZF9GZVgzQFg6XEcnMnVwQjwyOygmOCwsKUgrbCZHVSRsWklWKlU0UXEsPzBLI15XSk9QUwpSSFw6bWRrazFFIVpLUmRMOFY1JjtaIVonLDpMdHUiWjhfUDlvTy0uQ2IkS0FMSTphRC01NGtnV0pRWl1GVGdhUVMxMmAlKD04XjwyKj88SwpQTTFNTypDNWdyLkIiXURDMTxeNj9zRFN0NDBLTSEmXz1nXVtWSnBkYl0jQmtfUix1IzxuVGZwXlVLUTNjaVJhImMrW2ZIP25QW0NNJ2xKbwpYYD88MygiPFpQOCtZLjdSbiUmaG9aV1JtJzRdO1FrYThOZlwhTzVEIWI/RHReMVE1MC9tST1sLVgpbGgxXGorXmtQb04jIis4dERlR34+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxNjUKL0hlaWdodCAxNDAwCi9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDYzOTcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwVT1gVTt0J0VxPixeTTNQPiw5MnJGZS0kJTprSk1qKkxoQyFNVW9TayIhPDwqInp6enp6enp6enp6enp6enp6enp6enp6enp6enp6egp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enohISRFKEQ7ND1kRwpkT1UsaDNCYjNzI0woLCVJdVoyamFFKkw6RCo/IU0jMSxockAtYFReImhhdFtraUxTVD1bPDYqbFowLl4pUHUxTy02JDljL0dqamdQamddXQpoYFA3RC1SISdqXC4hIjEtYTUlcFJAITk7b0pWYGlyNUM4WGtOR0pFS10sTmdVQCReW1xDQzdpdFBBcUdkTV9cMk9WPFhIJztoUEohbGI4LQoybm50cnRLSSZhcyhpLzpyPSkjJmlVVzI+QzMhRXBqWCdcUFAkLDI0UEZQQl9LJkZXa0gwKjxfVS0kLE43RDVzYz8+MD4wM2ZzQFF1Rl1nawo1OjdpPG05VSFEcVJtdTxBTjdeMnM4clNfcixFRjUjMz9ObGYvY0hXST4ldEVUNXRBUSswJWlbQ0NFYlo4OFUjR0hiPEs0K0NCQkRtYGQobgpWNnU8KVcjPjFTTjE8ai1JOD1JSCtMLUFoUSQhaXFXZl9ybnQrUjthby8/JT5PZ2MvWUU9YEZnaUtTT0xbWDRkaG0xdW1FRE1xVidXaThJPgpwWzBVU0Y4THFnUjFqSEAsLSpESUNaVk0yZCVxUzoqVCslPVlvSmpQTk1QLSwkbFI6L2hTU3VebkI2O1FMKE4qcWJ0SDMyPCtWKGpET0FRVQosWVJvQ1BmZmVbSk5uQHJALV9pZWIrREtqJGw+aVwjNyFYP2hSZkJbQ0g3WmE7bHNEYysjY2pcM0ZRWFwxUUJIPT45Lkg5NnVUZzpBRlovUQpAInE5Vlt0ZEcnKTEjPWlrRSw+WHE/PiZCVjQ3TGBPXTtBRVhPJmhFT1RsN05nOHUsXlM6dXRWLF07KCdoMTVzLXRGZ3FRaF9OXzIyUTghaApYKCRmcV9sVilFUTx1LkUzS151T3FtIT0xPy86dDI8M09rVD5lSGA7bG1EYDU8Xm5mQCpqJ25GOGdjIy9wbEFkRDBhYSJFVElpdWxjLDBBKQpLJ2dXR0VNWzQqQjJybiRrciFSSCtKNTYqZS0maCIkRG9hSShJaWhvOWFJL0A6UjVqX15DbEZtZHAzIWlyMFgzSW5LTUkpVj4iR2omaDhNVgpxXDRXPWplQVEvKmVYOTVnKkxmWTNQZkxQdHVuN2VeZVY1LTE0UEBwU1dpRUNMZGxaXmY1QitUVGE8bGJcSkdDV2IpNDFgWW0/ZHFzVEJeSwo/RlZzVkhaNlpEPydVc0cuWzJSXFklbVFwX1ZeQEhaUCo2SnJWM3RQUElVPk5UYlc7P0RrNEpXN2Q5aWhWNT8tal8qQSwlJ0M9W0dfXVs8JAprPSc7QTkhKlZcMCVMcVhFXSZSb2JnZTRYTEheKXIwQnQzRDpxVyVGIVskOHBmZUlnKkpvLjQ0bjVoS2lGZUwjb1FjTnRwWy1jP08+QiZmKwpLInFEVk9nLFxOMGtRLjAmZT0iOTczOD41PU9ANztbQmBabGIrLVo3Z25GQm9bc15oY0ldRmg0RDppRUROY05YVUBIZT05QnMkWFQ+aVlnaApDW0JSMjljbHVRPj9DZVBQZTlKP0xgY1BbMnVsTlRzMWs8Py06SiE4RkAtOyNOUE9IQkJSaj5JOzU8YzIjXE5XJmAjQUo/Vm9VdDdzckpTIgo8S0tdWio7ZSQ7LSZMIlllX3BGVEQtbSJdVl9ramsvUkBEaXRoImJBQC1zUVVSUk1QRilWIURESUMzIjxpdC91WipoRz9tTTFmQmd0LVFTNgojNSVoSjFGQElMQm0tZjRGcV5gP2IoJEg4Xk86UzRlLGNcUE5PU0xNNEUsbTJZVjw1Olt0KmYsc0cpWlQtRV0hJmJpMj5lTGlJJ1k0L151Pwo+Ukhmai9UODAxZD5qKUlwYTY5OEY4OzZVKCEySk5tMCJVSFhZYlkyXDI4dGhJT0okIi1uSEVdS1dGWHIlSS9zJTFaKGo1Ik1uUiRWcDdKYQpnZ0FMXFE9a11PQW8uP2FZZC9UTWw+REQ9LCohMF9vOTxGXFQuKShuJksvUHFLUU1zNjtvLD5NbkxoLWwtPVV0RjZoLi5VMk4ucFtUclhgbgpIRlViajFSSy8yTktCZlFKMTFPYFZBcWozJl1sRldsaCxQO0UudXNHY2thaWgjI1ROZkNuP3MsaF01Ikc0UDBHOG5NQi9eMlhNX28tOGtfNQpHIihMPSJuSixePUcrZWVzL3RlV2VsKDYnOFE5Nm1kQ2JeVnFAbnE4K09RPGxYaGVvaEUxPSRFTyltIVtzMG9AQVpfVF8kOCdJUk40RlAtcQpHSyxcOlwmUUsyPEUuODlwJlNqY2d1MzNjQU1NKSgrPDk6REdETUc6S11DPi9iT1Q+bSM7cWFQMzBiaWRwVlUwaSZEInVyJVErXlw6X0QoWwokNmQ2bVxvKz5tPFIlU1w/NEtDO2ghOi8rI0RhLlw4dGA7Pj1ecW5NdFVqa0tAVCY+TkxJKTNaIzk4TDpDclQzaS1dcVxYPXEkaSRaUyY3Mgo3S3VVL1tgWCU9aEQ5Zjh1b1pYPG1DOnBSbSRBWVEtMCEpVlomNlhvPFdzVFREJiQuPmcnSyhCQS9KbW1PPUZRIkd0PEpZNTRpOUFOZVgtbApbdShRXXFzPEdoKXI/QW5bT1dFTUFQL3AvYG9PJzokLXA5aD5jPDVSM0g3QmZyRVJdMjZpYWdHZyNJTG08OyclTzY6UFJyLkVCW2RPXXQpUQp0bCRPMVpGRzBBX2BObDFVb1Q5aDlYaTpwVnVCIWAwVCk/cEZRWDRvPUo4XGVYI1lDJUY0QHMlaDUqX2xWaWRdZllrLzIzOUJTJFBNYFslQQpDLGEtLWRQUjxQOUlKVVZvTENaKCQmZz1wRkAtOyp1J0pvMGxDLElDTi0+X1ZyIVcrRy4sOmA0dWgzXm9aZkNfSGRkdUVaWjpBQSlsaF1BZQphX1omSUJlXmpeOisqMkNtazwiXV5qb2FnXy5AZWxYWUlXNSFHcFheJkMtODI4cV4iTVJgK3RFU1NaKkE6OW0zajUtUGxCJmE9dVdNQGNDbwpOW1okKzFHZSRsXlA/RWghU2gxYWFKRilJKyhIRCNNdGtPW1ZFOjlacSMkSCw/QmEiaWBEJWJNPkw1aXJBRVRLXyJDcDtSUylxcVZScSRvKgpaKS9cNTBFNypULT0kMEIxZzJzMTA4RS9rPCM4W25lSVRpLyZTNyldY0kocFE5OzxnLGUyWWwxTiUqY1xWUV5uZ2JMcVUrZz4vKmFYJzQtWgpUS0giVkE6VCRjKCczJ0JkKW9BSEspUVQ0aVEzZHBYSl4hXT1pMS07UyQ1I2o2YUlnNTlpXiVmISgwWmEoOU0wZFcrXkJnVEJ1W0BmNyFcSQp1OmBQcE4lRyxuTXMvImI2bFtWX2xcZC1uMWhJbFd0ckAkcEBiaE9hKmVCZ1FxUjFeZ3RyI207YiROUkhFTVBFI0AvKmhBSUlLXWVfSVpVPQosc2MqJ049I0psODJNa3Baa1g2RUhFOys0PnA7ZUEnZGNuUFlqWTZqaFJ0YWxGb1o8NWEsUGQ0aVEzZCFUOEl0ZzBsa0xeYikrSUhgNGsxJApNSXNnbWFLKyZbUSlqdUItTT8xOEs7RF1VYzVcXjp0JWMwSCgpczpIaUxNJGw6WUM1WmZMKnU+ayMpLW8oaS4jbGZTQyNyPmEiaWA2Q2xscgpBQjpzWlpSbWszMTFrbG9RajQnMVtDcHBOaiJNNVhncFNTMElLT3FOaUIiS19DSUhMKHBAUm9JdTpiPmRDM3V0PkhJQGpgLW5aJnFISkkwaApSZ0JgaEk8KyNTaUdpX1FqLlVMSHIkXSolKF1wWVFkM2BvaUpSTXRFajlla1InWWY/U21hJTc0MV4lYHFwc1pfZDZhSFglX1szRWh1RE0wIwo6RCNQYWdLPnQ+TkQoT2xIXzkqPytHbWo3YnIlcGhINTkhMVhwWEFpJ281QlopbFA2QVlVIVQrbF0qVGtJLnA4R1lYY2REcWx0WmZbJSwmWQouLUtFXDNLKSxcR05RaVJAZG8qZ2s/TGpROi80SEU8Z15caCxvL3UtNz9icT1BU21AUlleaT5bVkZubk5YKCdjI050REdXXVdrUm5bUlY4TwonME5OPSZwJVBnJUc2aWo1UzBDcFYnWVEyRVhPQyI5ZDJtPyVuQ1QwQU9TLTttXzswXShFPW5WUyhtdGdNV2VaLi0jPGZobTA+dFxHKExJPAo4ckBhT2dyWyFPNDFSPGdWcytiKkYlaF1xP1NHNjdBTisnVjYqXEIyM2tpJkMycl5BUkslTSRpYnN1UTtyWHUrbVM9R2gyJj1qTk0+TStpbQo9KjVfW0dBVEslTD04TSkjJFFfTCJCLE8sRWkhY1IhQTA6UlNZTlBWVDU2NEAzclhEXFQtZFZESmVsZkEmbXV0Ly9XU0svV2ZiO2VgJktLOgpVTzMnRGxuQ2xoWkQ5T05JMVxMbWJRU3U/PyYyKXBUKmsvcWFsTEhUX0xcJ0N0MmtXXC0yMDMvJkUrYDNeY0pYUCkzQywqWy9mYz1HOmZwOwojRy9tVDpdKD1JOzBPXmpTS0txKSkoIjRRMk1pcXAsMicrTmZORG1pUCloJFBoV25eOjRxQmdYTE9tOUt0LU88L2kxciVhZV8iIlNYWjMnbwpVYz9iQjxbMCNhUk1iWHBYWXU6XD1mJC1mMVksK1FXdFcpZVBZPi9QYCw+NU5yIzVJTldtcWFPR2VIZEgxLnQuaCFyODs7OD81Zm0nM2ArRwpCMiRWM2peRS5vZkc6U1o+bUEpRTMwISNfM2AtU0lJVFEuP0YvXjwtPksrQWpwJiotJHElbCdWKGFwN0Y/SURxST9OaDgpbDI5Q0VjP3JgYgo7cVwwU1k7OktpVigsKDFjUixJZCxUYmIoI2tQU2Q/SlhVamBNOWRJOk42T2NQbDhOK0pcXkk7XjlEJi5wTChQPk1tTmYlRUAzZSpbZk5YXQpZPGtlczZLIjkuNyc7bWVNa0MxJUA2aSNYbEVsLiM+US9tPlAmR0BuW0lDNDRyMSNWUFspdVcrN1dxNENMOScyXD42bFhgVmlFYlpWPkhMMwphVicpUjs6QFxoRCpiKV5cdDJWR3FgQFRxZVhbImslQktFQ0hfIV5TMmtaIm0uODRWQjheRTtdamRIRmtJWCg/bkpucytibDxyZTQ4cS1gZgoyP1YvWmN1aEhoTDgwUVcwP0NjR0hET2Y9PWBMcUUsaVdtYTc6aE03Z2k1b2ZtP3IyYjMub0lSbU5BNzhdS2VebyJvNEJbcmg1JixLbCIvWApkZzhcSSJTVVsxWCRYPDA3VTpuRFEyZ144UXMqbGsoXmxlcCNQK3VwanN1XmdARlkoa05oSHVcPGlgUi9RVDBKcVhab2pcVChWcVgoOExMJwotR1EzWzFOYFFSSituJWg2NHNSbVpbU1hWKF02bUhITzlNPjtrcC1cYDA0P11YWVFVM2xXMjEsYzxEcDFaQWxbbV9LV2NRWlljPHArLG1mbwpYTSQ5Zj5yKydjYFNsJ2c2JmVRWTslKUJFKjtXLCkpXWNVVW9VdSFDTUtOYT9eQ3NPZVRaLltiJklsRUBxSWFAKkxzZEpMN2VyWFQtUEpGXAorSzplL0FeIyZcX0olUWhvcCVkLTFAJDpMKGY+VEk2NTloRScwTGNhZUskMUU5cyI4WV1AJ2ZhK1FTU2c2aG1KSm42dScqNks6KGNFb0BzWApcUnRyLGp0OiViYkA7JmotPGo7Uk9kZik5b09Ga1soTTouPz8xIkVVdEhJVidfMiwkbz0rTGw/b20rSWYnX3I2JD91RmhuJ3RoTWI8YjYubgpOa3RPO0AnV1NsXSwmLCVjX082XCopJi87JDNwaVxwPm08VFNFNTlnUzlVcmZMWD4xVl08KGpFRUNwXk9MOUFvSihuQyUnSTdmbzdnXDk+YQokPmh1aVZHaFBdUU0nJmEuKCJjaC80OHQ5cy5SanBBPG5UT2hwXTthY0IzJVpZUEBpZy5nXy04YWFecDk7Xzc+LEtjTHFaUmJqP05cOjl1YApQcUY5bU5xRDM5RygmLjYrQlgvcE9zNU1Dam5AY29YS1VcWkZPdURgbyxSckxjXTlobWlEKWBNV3JEZ101cWItN29eZFAkYUpya0hWLWxNOAomcllsPjpvOEpgOFY4QygmSUBga2ojdSdiSydONm1aWDgrMkVnS2RxUyhdN011VShmTEtyTUgyKVdtbStSWGkqYC1vOVg1MmFiJmluZ0ZWQQptVSZXZDIyUTduMHA8TjFjP2pbMSs4UlFuUCVhKjYoMmYnKkNIbzUhdSNPNmosWFEhLWJpQklCbVApIztjPlE3VlQvOFVday4yNjNeMmFbTQovTGYmU2wvQVRyJiJYPzoyWUlAL3EtRkomZT4tMmg9OUZkL11ocHBCMjBjQDhwcV9jPjI0SUU5NmpZTGxQa2ZbVl9gJz88KXJeWnJRMCZfOgpyPHJAbCZdK3FGYy8vREtgaDx1KiFPQ0FFKiVWbTNtVyElS0k5LiVaQkYiJGBzVDlRZXUxSSptR0NXZUhzR1EiRTRePStndFphRTAmaWI0NwpMRkNSP21OYlBAUDxiZ2VgJmRsJEBRajlNXFdObXAwMj1tWG5TRCRHPmVsa2thT21IRVZIbCY0QVQqcURpYU8tND9UKjopa1MzOSwxZSE/JwpCc2JGRE5UdDZHQidQIUlARjNoX0lbO0YiWHUqKWdCcnNoWkYtZCRMIkJnRktRPU44Nm4wUj5WVCtnPFNKUGxNamBGXERNV11jLkBjXjxKLwp0VDgmKlcsUWltY3A7OEY3MlJSSE4qUHJYUV1tbm87biJCZltcZiFLIipIaWRhYzFJaDQoZGRnXF0tZD8/YjFFWjxRQyYkXGJISUM4NS9qbQpjOWUuOEtCSj07T10xPlQtUDdZXyU4LVNPdXE+W1YvclldRTolZFhvOiEyJjBJdXBkQWxJS3EvLE5XaVpjW0FnaW5pc0I8KWtxS0k3SjwhaApUJHU3VkAvUGdEQUNvXDY5RTNsajVcSEhwLUBFZkVUY0wnYWBWNF1eYDYscShVOkpfYWolOjhQT1BZX2IvYGtkLEFZSmw8Rkw6bmpeXCElKgpIR1o0NW4ycGNycURFX3ErRVYwaSRdRzBjZ0BiSmsqYTIqTEo8JEJcLVF0J0ktJ1QiNDEoay5HLlxyQ20iSlRZcHM+VypfVS5LJipmY2xJPgoiNWUkRGJEV1BxM0tCa08vb0gtPTBUVUZkbFhTaWBwanRjPyJwKzBFbW1BQHIja0ZORkVeXChsZWV0Vz0taTBObmghLidrIWpaRiVEZyNjOApXQzRLKk5ePj40bW1gKy9YWTItbGMhLm9QSXJEKjtuLj9IKi9FViRLPjI/SkBwLlQqMStWY0VvQUBqc2tOZi9VKVkodHA7T0hpZXFZOnV1MApyRl9uRzxONycuK2JgNUZFUi4jJmJkME9lP1hPTyVFVVVyaVthPmQpMWsvRjRPNicvLm1oX1BqXlwiOHMqYyleX24yRF9MIW5TL1wtci1vLAppNUhcTjc/M1g+PEZwZTNxZiNQV0ghbVpHVkl1WGRrMTdVbCNtSW9hRWhDSEdNSDI+MTs3QF1NR0tnUFVAR1dIXkFWXFtcUTxuKDFlI2kjZAopaS5xRkZnPDwoPHBuKGchcmNsQU1vSWsvY0w+LF11K2lGUDw7VXM7UThIZ0dpY2NyLTI0XU1gJi5YRXM3XU1iVCEqRVdjcEM3YWgyUWVWRwpNRWsoZ1w4V2tnXyk3T3BTV3RqPytGJlJUJWorW19ZKXBmbCokJClLP0FQKS5OX2hSZShSLFksTiUhKjZCZyRRW2oxPFIuOmFwci1TImNDYwpUcGVMcSEjRiw1LF5TMWJCSnFOXm0vTWtYUjZKK2hEKDgwQlBLOjhwSSJVIiw0NVtCSnNgLj5YSSF0T1UtIl5zJm1yITtGL0ByYC82S05SPApxKW5gSWcnJFNgSGszPzMyZ1hgYiJqMCooLD5lPEhDPHM9bUVEYztLUG0lX0VVRmBUbDcpIkI+ZSlBJWdFKiU7VU4zNEotWE0lWltrPW1SUgpkVElUQCNFdUMkPCwzSzIqPTx0YUtzbGRnVE5YLzYwMVxKXjRoXVpqJm1cK2wqb2wqSlI5dFtQOEI7Sl8oOT4tPiZiVmZUZXBtZStqY1taNAouXVEoWUlGcmktZFVSUkwiN2EuQmUvcjgjUTYyTGdjPTJJLVQqYjo7WGkkJ3FBVEJpXzlidVsvYmVuT1Q1cGEmenp6aSFmVmRtLCVvcX4+CmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDI0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMDQgMDAwMDAgbiAKMDAwMDAwMDE2MiAwMDAwMCBuIAowMDAwMDAwMjE0IDAwMDAwIG4gCjAwMDAwMDAzMTIgMDAwMDAgbiAKMDAwMDAwMDQxNSAwMDAwMCBuIAowMDAwMDAwNTIxIDAwMDAwIG4gCjAwMDAwMDA2MzEgMDAwMDAgbiAKMDAwMDAwMDcyNyAwMDAwMCBuIAowMDAwMDAwODI5IDAwMDAwIG4gCjAwMDAwMDA5MzQgMDAwMDAgbiAKMDAwMDAwMTA0MyAwMDAwMCBuIAowMDAwMDAxMTQ0IDAwMDAwIG4gCjAwMDAwMDEyNDQgMDAwMDAgbiAKMDAwMDAwMTM0NiAwMDAwMCBuIAowMDAwMDAxNDUyIDAwMDAwIG4gCjAwMDAwMDE2MjIgMDAwMDAgbiAKMDAwMDAwMjA0MSAwMDAwMCBuIAowMDAwMDA1MDY5IDAwMDAwIG4gCjAwMDAwMDU5NDYgMDAwMDAgbiAKMDAwMDAwNjM4MCAwMDAwMCBuIAowMDAwMDExNDI0IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI0Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxODAwOQolJUVPRgo='], 'total_charge': {'amount': 91.1, 'currency': 'USD', 'name': 'Shipment charge'}, 'tracking_numbers': ['794874781227']}, [{'carrier': 'carrier_name', 'code': '3380', 'message': 'Origin - Postal-City Mismatch'}, {'carrier': 'carrier_name', 'code': '3053', 'message': 'Recipient Postal-City Mismatch'}, {'carrier': 'carrier_name', 'code': '3040', 'message': 'Shipper Postal-City Mismatch'}, {'carrier': 'carrier_name', 'code': '8266', 'message': 'Origin Location-Postal Mismatch.'}, {'carrier': 'carrier_name', 'code': '8231', 'message': 'Destination Postal-City Mismatch.'}]]

ShipmentResponseXML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <SOAP-ENV:Body>
      <ProcessShipmentReply xmlns="http://fedex.com/ws/ship/v21">
         <HighestSeverity>WARNING</HighestSeverity>
         <Notifications>
            <Severity>WARNING</Severity>
            <Source>ship</Source>
            <Code>3380</Code>
            <Message>Origin - Postal-City Mismatch</Message>
            <LocalizedMessage>Origin - Postal-City Mismatch</LocalizedMessage>
         </Notifications>
         <Notifications>
            <Severity>WARNING</Severity>
            <Source>ship</Source>
            <Code>3053</Code>
            <Message>Recipient Postal-City Mismatch</Message>
            <LocalizedMessage>Recipient Postal-City Mismatch</LocalizedMessage>
         </Notifications>
         <Notifications>
            <Severity>WARNING</Severity>
            <Source>ship</Source>
            <Code>3040</Code>
            <Message>Shipper Postal-City Mismatch</Message>
            <LocalizedMessage>Shipper Postal-City Mismatch</LocalizedMessage>
         </Notifications>
         <Notifications>
            <Severity>WARNING</Severity>
            <Source>ship</Source>
            <Code>8266</Code>
            <Message>Origin Location-Postal Mismatch.</Message>
            <LocalizedMessage>Origin Location-Postal Mismatch.</LocalizedMessage>
         </Notifications>
         <Notifications>
            <Severity>WARNING</Severity>
            <Source>ship</Source>
            <Code>8231</Code>
            <Message>Destination Postal-City Mismatch.</Message>
            <LocalizedMessage>Destination Postal-City Mismatch.</LocalizedMessage>
         </Notifications>
         <Notifications>
            <Severity>NOTE</Severity>
            <Source>ship</Source>
            <Code>2522</Code>
            <Message>Sender is the Importer of Record</Message>
            <LocalizedMessage>Sender is the Importer of Record</LocalizedMessage>
         </Notifications>
         <TransactionDetail>
            <CustomerTransactionId>ProcessShip_Basic</CustomerTransactionId>
         </TransactionDetail>
         <Version>
            <ServiceId>ship</ServiceId>
            <Major>21</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
         <JobId>230e29c7332305s0134bj243434</JobId>
         <CompletedShipmentDetail>
            <UsDomestic>false</UsDomestic>
            <CarrierCode>FDXG</CarrierCode>
            <ServiceTypeDescription>INTL</ServiceTypeDescription>
            <PackagingDescription>YOUR_PACKAGING</PackagingDescription>
            <OperationalDetail>
               <OriginLocationNumber>152</OriginLocationNumber>
               <DestinationLocationNumber>6142</DestinationLocationNumber>
               <TransitTime>THREE_DAYS</TransitTime>
               <IneligibleForMoneyBackGuarantee>true</IneligibleForMoneyBackGuarantee>
               <ServiceCode>92</ServiceCode>
               <PackagingCode>01</PackagingCode>
            </OperationalDetail>
            <ShipmentRating>
               <ActualRateType>PAYOR_ACCOUNT_PACKAGE</ActualRateType>
               <EffectiveNetDiscount>
                  <Currency>USD</Currency>
                  <Amount>0.0</Amount>
               </EffectiveNetDiscount>
               <ShipmentRateDetails>
                  <RateType>PAYOR_ACCOUNT_PACKAGE</RateType>
                  <RateZone>51</RateZone>
                  <RatedWeightMethod>DIM</RatedWeightMethod>
                  <DimDivisor>139</DimDivisor>
                  <FuelSurchargePercent>7.75</FuelSurchargePercent>
                  <TotalBillingWeight>
                     <Units>LB</Units>
                     <Value>44.0</Value>
                  </TotalBillingWeight>
                  <TotalDimWeight>
                     <Units>LB</Units>
                     <Value>44.0</Value>
                  </TotalDimWeight>
                  <TotalBaseCharge>
                     <Currency>USD</Currency>
                     <Amount>60.94</Amount>
                  </TotalBaseCharge>
                  <TotalFreightDiscounts>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalFreightDiscounts>
                  <TotalNetFreight>
                     <Currency>USD</Currency>
                     <Amount>60.94</Amount>
                  </TotalNetFreight>
                  <TotalSurcharges>
                     <Currency>USD</Currency>
                     <Amount>4.72</Amount>
                  </TotalSurcharges>
                  <TotalNetFedExCharge>
                     <Currency>USD</Currency>
                     <Amount>65.66</Amount>
                  </TotalNetFedExCharge>
                  <TotalTaxes>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalTaxes>
                  <TotalNetCharge>
                     <Currency>USD</Currency>
                     <Amount>65.66</Amount>
                  </TotalNetCharge>
                  <TotalRebates>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalRebates>
                  <TotalAncillaryFeesAndTaxes>
                     <Currency>USD</Currency>
                     <Amount>25.44</Amount>
                  </TotalAncillaryFeesAndTaxes>
                  <TotalDutiesTaxesAndFees>
                     <Currency>USD</Currency>
                     <Amount>25.44</Amount>
                  </TotalDutiesTaxesAndFees>
                  <TotalNetChargeWithDutiesAndTaxes>
                     <Currency>USD</Currency>
                     <Amount>91.1</Amount>
                  </TotalNetChargeWithDutiesAndTaxes>
                  <Surcharges>
                     <SurchargeType>INSURED_VALUE</SurchargeType>
                     <Level>PACKAGE</Level>
                     <Description>Insured value</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </Amount>
                  </Surcharges>
                  <Surcharges>
                     <SurchargeType>FUEL</SurchargeType>
                     <Level>PACKAGE</Level>
                     <Description>FedEx Ground Fuel</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>4.72</Amount>
                     </Amount>
                  </Surcharges>
                  <AncillaryFeesAndTaxes>
                     <Type>CLEARANCE_ENTRY_FEE</Type>
                     <Description>Clearance Entry Fee</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>22.51</Amount>
                     </Amount>
                  </AncillaryFeesAndTaxes>
                  <AncillaryFeesAndTaxes>
                     <Type>HARMONIZED_SALES_TAX</Type>
                     <Description>Harmonized Sales Tax</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>2.93</Amount>
                     </Amount>
                  </AncillaryFeesAndTaxes>
               </ShipmentRateDetails>
               <ShipmentRateDetails>
                  <RateType>PAYOR_LIST_PACKAGE</RateType>
                  <RateZone>51</RateZone>
                  <RatedWeightMethod>DIM</RatedWeightMethod>
                  <DimDivisor>139</DimDivisor>
                  <FuelSurchargePercent>7.75</FuelSurchargePercent>
                  <TotalBillingWeight>
                     <Units>LB</Units>
                     <Value>44.0</Value>
                  </TotalBillingWeight>
                  <TotalDimWeight>
                     <Units>LB</Units>
                     <Value>44.0</Value>
                  </TotalDimWeight>
                  <TotalBaseCharge>
                     <Currency>USD</Currency>
                     <Amount>60.94</Amount>
                  </TotalBaseCharge>
                  <TotalFreightDiscounts>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalFreightDiscounts>
                  <TotalNetFreight>
                     <Currency>USD</Currency>
                     <Amount>60.94</Amount>
                  </TotalNetFreight>
                  <TotalSurcharges>
                     <Currency>USD</Currency>
                     <Amount>4.72</Amount>
                  </TotalSurcharges>
                  <TotalNetFedExCharge>
                     <Currency>USD</Currency>
                     <Amount>65.66</Amount>
                  </TotalNetFedExCharge>
                  <TotalTaxes>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalTaxes>
                  <TotalNetCharge>
                     <Currency>USD</Currency>
                     <Amount>65.66</Amount>
                  </TotalNetCharge>
                  <TotalRebates>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </TotalRebates>
                  <TotalAncillaryFeesAndTaxes>
                     <Currency>USD</Currency>
                     <Amount>25.44</Amount>
                  </TotalAncillaryFeesAndTaxes>
                  <TotalDutiesTaxesAndFees>
                     <Currency>USD</Currency>
                     <Amount>25.44</Amount>
                  </TotalDutiesTaxesAndFees>
                  <TotalNetChargeWithDutiesAndTaxes>
                     <Currency>USD</Currency>
                     <Amount>91.1</Amount>
                  </TotalNetChargeWithDutiesAndTaxes>
                  <Surcharges>
                     <SurchargeType>INSURED_VALUE</SurchargeType>
                     <Level>PACKAGE</Level>
                     <Description>Insured value</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </Amount>
                  </Surcharges>
                  <Surcharges>
                     <SurchargeType>FUEL</SurchargeType>
                     <Level>PACKAGE</Level>
                     <Description>FedEx Ground Fuel</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>4.72</Amount>
                     </Amount>
                  </Surcharges>
                  <AncillaryFeesAndTaxes>
                     <Type>CLEARANCE_ENTRY_FEE</Type>
                     <Description>Clearance Entry Fee</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>22.51</Amount>
                     </Amount>
                  </AncillaryFeesAndTaxes>
                  <AncillaryFeesAndTaxes>
                     <Type>HARMONIZED_SALES_TAX</Type>
                     <Description>Harmonized Sales Tax</Description>
                     <Amount>
                        <Currency>USD</Currency>
                        <Amount>2.93</Amount>
                     </Amount>
                  </AncillaryFeesAndTaxes>
               </ShipmentRateDetails>
            </ShipmentRating>
            <ExportComplianceStatement>NO EEI 30.36</ExportComplianceStatement>
            <CompletedEtdDetail>
               <UploadDocumentReferenceDetails>
                  <LineNumber>1</LineNumber>
                  <CustomerReference>Customer_Reference1_For_DocumentReference</CustomerReference>
                  <DocumentProducer>CUSTOMER</DocumentProducer>
                  <DocumentType>CERTIFICATE_OF_ORIGIN</DocumentType>
                  <DocumentId>090493e180971129</DocumentId>
                  <DocumentIdProducer>CUSTOMER</DocumentIdProducer>
               </UploadDocumentReferenceDetails>
            </CompletedEtdDetail>
            <CompletedPackageDetails>
               <SequenceNumber>1</SequenceNumber>
               <TrackingIds>
                  <TrackingIdType>FEDEX</TrackingIdType>
                  <TrackingNumber>794874781227</TrackingNumber>
               </TrackingIds>
               <GroupNumber>0</GroupNumber>
               <PackageRating>
                  <ActualRateType>PAYOR_ACCOUNT_PACKAGE</ActualRateType>
                  <EffectiveNetDiscount>
                     <Currency>USD</Currency>
                     <Amount>0.0</Amount>
                  </EffectiveNetDiscount>
                  <PackageRateDetails>
                     <RateType>PAYOR_ACCOUNT_PACKAGE</RateType>
                     <RatedWeightMethod>DIM</RatedWeightMethod>
                     <BillingWeight>
                        <Units>LB</Units>
                        <Value>44.0</Value>
                     </BillingWeight>
                     <DimWeight>
                        <Units>LB</Units>
                        <Value>44.0</Value>
                     </DimWeight>
                     <BaseCharge>
                        <Currency>USD</Currency>
                        <Amount>60.94</Amount>
                     </BaseCharge>
                     <TotalFreightDiscounts>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalFreightDiscounts>
                     <NetFreight>
                        <Currency>USD</Currency>
                        <Amount>60.94</Amount>
                     </NetFreight>
                     <TotalSurcharges>
                        <Currency>USD</Currency>
                        <Amount>4.72</Amount>
                     </TotalSurcharges>
                     <NetFedExCharge>
                        <Currency>USD</Currency>
                        <Amount>65.66</Amount>
                     </NetFedExCharge>
                     <TotalTaxes>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalTaxes>
                     <NetCharge>
                        <Currency>USD</Currency>
                        <Amount>65.66</Amount>
                     </NetCharge>
                     <TotalRebates>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalRebates>
                     <Surcharges>
                        <SurchargeType>INSURED_VALUE</SurchargeType>
                        <Level>PACKAGE</Level>
                        <Description>Insured value</Description>
                        <Amount>
                           <Currency>USD</Currency>
                           <Amount>0.0</Amount>
                        </Amount>
                     </Surcharges>
                     <Surcharges>
                        <SurchargeType>FUEL</SurchargeType>
                        <Level>PACKAGE</Level>
                        <Description>FedEx Ground Fuel</Description>
                        <Amount>
                           <Currency>USD</Currency>
                           <Amount>4.72</Amount>
                        </Amount>
                     </Surcharges>
                  </PackageRateDetails>
                  <PackageRateDetails>
                     <RateType>PAYOR_LIST_PACKAGE</RateType>
                     <RatedWeightMethod>DIM</RatedWeightMethod>
                     <BillingWeight>
                        <Units>LB</Units>
                        <Value>44.0</Value>
                     </BillingWeight>
                     <DimWeight>
                        <Units>LB</Units>
                        <Value>44.0</Value>
                     </DimWeight>
                     <BaseCharge>
                        <Currency>USD</Currency>
                        <Amount>60.94</Amount>
                     </BaseCharge>
                     <TotalFreightDiscounts>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalFreightDiscounts>
                     <NetFreight>
                        <Currency>USD</Currency>
                        <Amount>60.94</Amount>
                     </NetFreight>
                     <TotalSurcharges>
                        <Currency>USD</Currency>
                        <Amount>4.72</Amount>
                     </TotalSurcharges>
                     <NetFedExCharge>
                        <Currency>USD</Currency>
                        <Amount>65.66</Amount>
                     </NetFedExCharge>
                     <TotalTaxes>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalTaxes>
                     <NetCharge>
                        <Currency>USD</Currency>
                        <Amount>65.66</Amount>
                     </NetCharge>
                     <TotalRebates>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                     </TotalRebates>
                     <Surcharges>
                        <SurchargeType>INSURED_VALUE</SurchargeType>
                        <Level>PACKAGE</Level>
                        <Description>Insured value</Description>
                        <Amount>
                           <Currency>USD</Currency>
                           <Amount>0.0</Amount>
                        </Amount>
                     </Surcharges>
                     <Surcharges>
                        <SurchargeType>FUEL</SurchargeType>
                        <Level>PACKAGE</Level>
                        <Description>FedEx Ground Fuel</Description>
                        <Amount>
                           <Currency>USD</Currency>
                           <Amount>4.72</Amount>
                        </Amount>
                     </Surcharges>
                  </PackageRateDetails>
               </PackageRating>
               <OperationalDetail>
                  <OperationalInstructions>
                     <Number>2</Number>
                     <Content>TRK#</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>7</Number>
                     <Content>9622002600008140078100794874781227</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>8</Number>
                     <Content>540J1/265A/727F</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>10</Number>
                     <Content>7948 7478 1227</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>13</Number>
                     <Content>INTL</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>15</Number>
                     <Content>N1R 7J5</Content>
                  </OperationalInstructions>
                  <OperationalInstructions>
                     <Number>18</Number>
                     <Content>9622 0026 0 (000 814 0078) 1 00 7948 7478 1227</Content>
                  </OperationalInstructions>
                  <Barcodes>
                     <BinaryBarcodes>
                        <Type>COMMON_2D</Type>
                        <Value>Wyk+HjAxHTAyTjFSN0o1HTEyNB0wMjYdNzk0ODc0NzgxMjI3HUZERUcdODE0MDA3OB0zNjMdHTEvMR0zMC4wMExCHU4dU2hpcCBUbyBTdHJlZXQgbGluZSAxHVJFQ0lQSUVOVCBDSVRZIENBTjIwHU9OHVNISVAgVE8gQ09OVEFDVCBNRSBXSVRIIExHMzAeMDYdMTBaR0kwMDcdMTFaU0hJUCBUTyBDT01QQU5ZIE1FIFdJVEggTEczMB0xMlo1MTI5ODc2NTQzHTE0WlNoaXAgdG8gU3RyZWV0IGxpbmUgMh0yMFocMTAwHTMxWjk2MjIwMDI2MDAwMDgxNDAwNzgxMDA3OTQ4NzQ3ODEyMjcdOUtUQzAwOB05OVpHSUJJMDMcVVMcMTAwHFVTRBxCb29rcxxOTyBFRUkgMzAuMzYcMDEwHFMcNDExODI2MjQ0HEVYHFkdHgQ=</Value>
                     </BinaryBarcodes>
                     <StringBarcodes>
                        <Type>FEDEX_1D</Type>
                        <Value>9622002600008140078100794874781227</Value>
                     </StringBarcodes>
                  </Barcodes>
                  <GroundServiceCode>026</GroundServiceCode>
               </OperationalDetail>
               <Label>
                  <Type>OUTBOUND_LABEL</Type>
                  <ShippingDocumentDisposition>RETURNED</ShippingDocumentDisposition>
                  <ImageType>PDF</ImageType>
                  <Resolution>200</Resolution>
                  <CopiesToPrint>1</CopiesToPrint>
                  <Parts>
                     <DocumentPartSequenceNumber>1</DocumentPartSequenceNumber>
                     <Image>JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMyAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL091dGxpbmVzCi9Db3VudCAwCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovQ291bnQgMQovS2lkcyBbMTggMCBSXQo+PgplbmRvYmoKNCAwIG9iagpbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KZW5kb2JqCjUgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKNiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EtQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhLU9ibGlxdWUKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iago4IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjkgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvQ291cmllcgovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEwIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItQm9sZAovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjExIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItT2JsaXF1ZQovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjEyIDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0NvdXJpZXItQm9sZE9ibGlxdWUKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxMyAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1Sb21hbgovRW5jb2RpbmcgL01hY1JvbWFuRW5jb2RpbmcKPj4KZW5kb2JqCjE0IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL1RpbWVzLUJvbGQKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1JdGFsaWMKL0VuY29kaW5nIC9NYWNSb21hbkVuY29kaW5nCj4+CmVuZG9iagoxNiAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9UaW1lcy1Cb2xkSXRhbGljCi9FbmNvZGluZyAvTWFjUm9tYW5FbmNvZGluZwo+PgplbmRvYmoKMTcgMCBvYmogCjw8Ci9DcmVhdGlvbkRhdGUgKEQ6MjAwMykKL1Byb2R1Y2VyIChGZWRFeCBTZXJ2aWNlcykKL1RpdGxlIChGZWRFeCBTaGlwcGluZyBMYWJlbCkNL0NyZWF0b3IgKEZlZEV4IEN1c3RvbWVyIEF1dG9tYXRpb24pDS9BdXRob3IgKENMUyBWZXJzaW9uIDUxMjAxMzUpCj4+CmVuZG9iagoxOCAwIG9iago8PAovVHlwZSAvUGFnZQ0vUGFyZW50IDMgMCBSCi9SZXNvdXJjZXMgPDwgL1Byb2NTZXQgNCAwIFIgCiAvRm9udCA8PCAvRjEgNSAwIFIgCi9GMiA2IDAgUiAKL0YzIDcgMCBSIAovRjQgOCAwIFIgCi9GNSA5IDAgUiAKL0Y2IDEwIDAgUiAKL0Y3IDExIDAgUiAKL0Y4IDEyIDAgUiAKL0Y5IDEzIDAgUiAKL0YxMCAxNCAwIFIgCi9GMTEgMTUgMCBSIAovRjEyIDE2IDAgUiAKID4+Ci9YT2JqZWN0IDw8IC9GZWRFeEdyb3VuZCAyMCAwIFIKL0dyb3VuZEcgMjEgMCBSCi9iYXJjb2RlMCAyMiAwIFIKL0VuZ2xpc2hPbnl4Rm9sZGluZ0VuZ2xpc2gucG5nMjcwIDIzIDAgUgo+Pgo+PgovTWVkaWFCb3ggWzAgMCA3OTIgNjEyXQovVHJpbUJveFswIDAgNzkyIDYxMl0KL0NvbnRlbnRzIDE5IDAgUgovUm90YXRlIDkwPj4KZW5kb2JqCjE5IDAgb2JqCjw8IC9MZW5ndGggMjkzNgovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdIAo+PgpzdHJlYW0KR2F0big+dU1dUSZyLGpcUTJkTVddaCw0Xic3R0BMN3VVbEkiaUdyZEFASUY4SmZYPjBuOE8+bSxqM2RPW2wpMVY9TXFEMGc3ZE1Iay1eZHAKOFpoRUg3ZDNOOk5fOz8/WFxiVCwscUk5Oic6I0tNKjF0QFxXdS9sb1tbP2JQcC9LVTYuaVRGXWIhP1RLJSFQbi1Vc1s1Jm4mKGksU3JMTVkKUzcxSVhwNl01LUl0REIzUkUzanMzTks1a2BiQDdMaHRQZFhfdDI/QF1tJkxkcEJLWm1hZnRjNG5gYWY2LF9uRFlITFxlMmxgOC5uSkRxR2sKMHFVI25vbUQ1Zy5aUTdgWVtNazZkckQiJHMhaWIsKXRqKDNnSiY2Mj0mc3FSOlhCSDlGTnVNckMqPjdmMGUpNDJOR0NJSkVkL1RiU0Z0JE0KWGhEUGlvNE1CWnMnVWxvWSdqLipfcmxxQkw/KmU0PC1KIyEyYlhdQ05FL3EyLS5ePDFxNiojaiZWOmZSVV50ZTFLKGRKa185dTNmZz87b3EKS0JaW2RiRDQnOGtPby51UEVRIzo3V1MyLScqXVFSMkI5LTBZJiFVZDBVYT1hNClVPU1PUy1VQmNOZjVQWE1eMTM4L2NQRStFIS8wK19XJzYKcWIub2dyakJkUSM+bzknNSEoPykjZDleTStXYWMuWnJBTDc/dVMkXFZOZTU4XE1lISw+WCFXNFteYGtaQkRXTmE7Nm5XXUFvUChRL3ErXDAKWiVOI0YhMFw2MCMoOW9kXFElPz9FUEZhO0kiXTNgR1N0LzcrKComZUNEWyIxND9kP25LQC5Obl1PXEVsYmlIZEswJk4qNyg0cGMhL0pjaCQKSjQ/UWluO1U0SHMpXihlYTRcUmJJMytEdUBFMWxxXkNpLltpJFcxN1VIZWJaXC4zOzBdWFhMcVldN28/UUFiIUxhbU5kNC4yL25cSElcYEIKZ0ptdUBsNl5rTCYsTzJNaUYiS1NyU2ROSWYmJVBtYmFhXkc4PVs6ZlY+cjlfWUlwYEE2QCxEM1JzcDRYSWVnLUBsISEjOURTIzkzP25jLDwKQ2ltaGAkW2M9NydpPm4kL0VxWytINmoiZlpEKE9BMmAqIWE+ayNSOzYqRyY9NWxsXDErMEU3LkRWIVhNPydebVlOIjgkcURBOFxIP0IwWy4KXzkqPDFJZ29CSyJuO1FhZCJBP2w4NVonazhoTEZPTj9vRkchZjwtQylMJUdUXDVXYU4pcl1LQzRqOT9pIzJiSVdvc2FhTSpScWRbTGw4P0cKK3VhdDUjUy9oVlprZ2UlIzg9NUAnVlY+TlE2S1UmMjNhaj9aTy5SYU8vXVZXYV4/RTpqWGNDXyZyKlxWbnNXXipxTkouOCw8aXRYMCMlOzcKJVJIZHUiPlBybXFPYGwrQyEuNSxxKVYhKjpLSVBnOTYoQTVvXUplSVIrcDdKN0pSZiktYGsqSyRNNF9GLWJfKUtxdDkmY0VFdUE7cjVGXHUKJTVGLGNMMG1jVFM6a1VHZz9Oa1gzK15fN3JJJGhzL1NFUFFUQG43Mkk2NFkkbEMva1taWzBHL2xgXEwwWDJVO2Q6JTl0OnJfUDg2ZGc+b18KVzovRjFHMDU5K2Nma0JGYkgnYXNPajMlVGxNQSh1OVdtTzBlI2hcMUM+PSs5NE8nMiRuSlRTTWciIy80MlAzLGIoS1xkXzRibTghSShQO0QKKyJNTGdxZU5jZlV0YU1vKjU+VlJUVi1rQW4qXUl0Ym9ZUVVVOyExSCtdR0g4XGw/OEI2OEk6MU9wSjRJMFwvX25QQnNXXVc+OkJBbFVzO0kKVjhUTy1LcmRbYSFxKSVMI1MyXyI6TihQa1tENjQ7JS00NFFhblZcLzovKl5KPjQxOD4wJkg2PVtPTVQ+RW4mKF9ZWCE2alxDZ2pEWmtVJTsKaFU0aWNXQzIrQmBscVopSURYMSchckc8XFMoXS86LEhcQlwvc0IyZ2VzTydfUzpmKVYpLS84Y0JUJzBuampKJiwwUms4VkpUbnE1RCxPVWMKVjc+czhvY2JeczZvOXQwUTlmRC1cWzZdMV1XR0dPLm0vZVhFIVwuXEcnPV1AS0tyPEZNTCxLayJMXVdDbVYjR0VtbD1FciY1amQuQVAqIUkKWTRhJ1o0KV5aXzxeXFMtYFpgPycxP01ERyFfLUBMJUJpLlI0VW0idGBZQ2xhMEQyPG5GX0pCN0ppOVVeYGVaKE9pa1ptJ21hKTxQTjRdclkKUWRUUz8wLmdTL1BsUCpkYWA9YVZFPiMnQ0pYS089YDpidF9LZiQwOk5Da1FFZjFMUmokL08kTEFUPEQ8UXRba15KRlxYO0dtP0RuOk0yXT4KJEBrYExtNClNXWJHNWFqZWNMaG8mc1REVEZ0IyluJEc2b2YxPCdrb1pgJSU+VGdMPTJXWzxiIW5qNFg+QUJOWW1HIi1lL0MsTDtAIyR1WkYKNk9UNXAiVHE6cUQvQTklZCs2aWtPbFRcM0lvMEFSXHV1XSJOLE1FXS01R0kjWF5gZCxhOlQ/YjtkUVZsIS1KckkxdERbdEFTK2hKVkE1JTQKW1JXJzpodVFwZTRPKXQuPihNQ0tmcy4zc1IhLiFYV0leSTpLIVVfV2NBc2RzVVRNJXBDRi1ibVI1ZzBzZy43Mk1TV1s3NG1GMF0kYSNKWmsKOUheZFFfSjY0Z2JRdFldL2lKbTg7IUZQL1taZ2hxXmZIYVJVRl5TISpyREs7MCVXXkdbTV03JDxuckNOM1xrRkRDdUZLOTksUXVzb1AiWlMKVjREWk5PaCJ0YjVSKkRkMmNKRz08KzkrMjQ/V2tdT1Ryb2hgR0o4W0NDV29ANHVCJk5IVz1tSGR1PC5XUGxQKmRpXTJeNVcnMnEuLjU5NG8KOlRnTSJKUzUzTCRqZlkpXmcmQiw2KWM9VSlkKj1KJW5fREA8YW9LTjorRzA4LixcO2tSMT9ANzZMNTBBUCc+UGE9PVFsVUAnMTVITHFGYk8KOygmLkhnNTBwO0YwMzVFL0xzRHFMKkBgQzBAQy1ZVHA1ViNpdTFbLmlycEl0LGYhKSghUDZFQy5oJ1F0ai8jSiRSOHUickwsWzwxPVlJRnIKL11aL0VKc0JmTGJEaz5waDEvXEVWOCxiVCEkWlxZZkM2aXA3Xm5cKC01Q1Y+V0IyRjYmJjVuaWRQLiVbIlZaTCsqRDZkRGtfcUJwNStQN0sKZWlELUJVPkRSOjBlKlg1UjhkUmJkdUAiRk1vOlVuUElhRGknaGpBRidwIj46TCFMTWZQNyJtWlhQSCZMOWxTaWJNMDVNNEY/XWFNZ1RIbDcKImYkalMqUXVmW1VkczE1IklEW2BTSU1JJVomU0lnXXM1a1onX2N1Sy9cQmwkVGssMk5YPHBwPE5yIzdkZTkvRTRxZ1hDOExtSD9lXENyPiMKNiFDVnBfK0FqXG9pZSRTaSIwXCZXPjpgZ180LzRTP2JcVGhVI01LaCdcb3NhOjE4O0w2UFwmOypyNk0pZEtpUkRdNmBeOWxlX14zb3JCVW8KXjRyRVFFPXBbYzxWQClcTmhtSVc7TCQ7NWdJNldXMmNfcXMlQylZQGVFNkVJLy9hOmNbZTFFVVkzJXI5QDtkIURgazJkVldkKTIpbS9YTDkKM3NmNE9hMD1ZKCwrdGZcTT1BQk8rP0hwLmxoTFtRY0FMNWsmWmgzKlJgLyZVaHI3X11Ab09sXD5lVkVhQjpXQSZCTCdcITIhLkdlcF9HTnMKLSw7YS9dW1dZLC9fSj41T0JnJGwmaXU9TzA/cGwyJT9pXkc8WyspQ2hiJyZRKnJAbzZZJyMsdTBVVWJRYm9VZSFrPEhbJmVwIT4ycis6KUwKSEMzVUpRZCRKKXJySywzKylffj4KZW5kc3RyZWFtCmVuZG9iagoyMCAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDExOAovSGVpZ2h0IDQ3Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDY5MgovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdCj4+c3RyZWFtCkdiIi8mOTkrXVslLiFqRmJxKT1OOU04Vjw6KChPamVZPURbTFQ5aUlNcjw2QU9MalVkbFA8ZVptckAkbEt1YDtvayxfQk07SExhJDpeTzxwCi0ray4nOSkoUVQpLSlgUiksVV5EN05nWzckRSdoVT0hSyMiRTxwN1VFNURWM3ArU1FWYVJYcidITCcjbjxsQm9JYDRSKC9UOSRJY0VbRyo9CmlHYlA1RHQ+JVNVTi1uTDtzJ3FNXGVBUzFbR1IhYmZwbm9yQUk1VSxBaD8wPS1DcCglYV5iUSdAZExcWldMZzhPU0ReNVJDYmdwYGxoaDxXCj4pLDtzZUsxS2xsTTcqPzhsQ3FgPzo5W2AhNlw/V1sxKFpfPUM+Q1BPPFAzcl9BI1RDMUxJVUIsIjNPbzIlOl5RQWlFI2IvMFtNKCplY3RzCkdAUC1kbUByXmVGPyFcL2QpRilnRDInV0VvcGIxWScuM0FXU0FtKzFRNSxAXVg7RmlJbkx0Rl5QJ1JoMVEqQCo3WDkjays8QUYmcEIiWlBoCl01Ri9DZj8pWXUsPCxcLlNXbWFuW09zLj1kbEg2ZGxdM3NZOjVuK00vP3NBKSpfc19EXnNxOmNDSk4qKlIjLzwuLydqKmxDKjIlLk9sYmcnClVNNSlNOGVfYmdsL0YtaSY1WT9AaCM5SzBaPCwuLmYnW3NCM2A9YS0jOmEqYTFWTiVpJEFDZz9ZUllmJVk8cyxtLDlfUjNhXWAlRHFkalNVCmdrTS50SFxtW3JedC1OL2xlQ0lSXG5vOTYwbC1RNjo+ISxcN3NGXGU+VjRpI2tCYnBnXCE+YlZoU1pMXm4pO2pPbEBlJ2FEVl4lPkdXIyFCCj4rSDlUIThlIllTKnAiOzxYR0MzIjN1JWknISprcU8vLF46NU8rPS1EP34+CmVuZHN0cmVhbQplbmRvYmoKMjEgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCA1NAovSGVpZ2h0IDU0Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDI1MAovRmlsdGVyIFsvQVNDSUk4NURlY29kZSAvRmxhdGVEZWNvZGVdCj4+c3RyZWFtCkdiIjBKXyNdMEIkcSFuYz9iLVptUC9yZSsrSTJCaklXLTkwUT5PN1s6JFdKKEMzQ2FBIk5zN1hANzAkLFR1JWJAWVF1aG5YIjFkLmFTVTZSCidHPTNBWTdyLWcsRycpYiZLWThPS2ZUYjJHX0suKFQ/dFJTWTJRIlc7TWI0WiZbKDFgKG5rI2UrJSI3QSh1XCxBO3JnT29yPlNFKXJ0Tm8mCiVjSzhBPTxXSDknIlgxUjg7QGFFSycqZ2tJS2I0MShSPkUpKTIwKSUvajlnYk9cMG1NZTwsJyMuXHJXPCs9SUJRUUFAMCNDYVdZV0FYUnJvCj1Jampdfj4KZW5kc3RyZWFtCmVuZG9iagoyMiAwIG9iago8PCAvVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL1dpZHRoIDIwOQovSGVpZ2h0IDg0Ci9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDQ4NTgKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIvYTYjSGZjJmQuaCw6XFBuRz1IaltoUUorLklQQkFSalVlR0JebC1KUF1yMTFVb0dRLG5GcSllV0kzVF4yNS5LMmZbb0NfcT5KIlAmUQpwXnQ4SjVCZkNZUCQlcnEyOGU4OWdqQFA8JydbZmVOPE80XEFoVWA1XkBHMiU+O1ZXYiJZcW90PU5bbEEpVzpWTSJtWVZYbjVWOiJeIT07XQpOQEJ1Ml4iY2BKN1cucG9sZktdTm90TnEqXFBYSyVQJVxqQUkrZC9MTiNiYltyLl9Na1tPSzdbKjJbZ1xXaFdMRWtCVlAlWCdNaUpZQSRERgpvOjVMJyQma1BoISMtRWxZP2xCXlMmNSU+YSFYVG5tQG08OFFLMF9nOC82JkFLJy5FLyxIRytQRWonMUZhN0dob2UtViktJi0qRW9STzRzYwpbWzZLcTIma2hjPC0+LTdpUlpZVT8qQGpDKzNSUSwlWk4qazwxVD8wTmhZcDhcUjlNSCtcNCNbMiwzUlAkYkQuW0ovMHU+ZEE5MyNjTUQmRwpdZVJfLD1JLWdGQlFVNU5sRW8+aSdRIloyImYhIkQ2MVYvOSNIK0RsKmE5T1lLcElJbm07VExMImAnYF9WcDInciNYbjhFUUReVWJQPCU4agovKVsqXzkhdWtsbmRFOEU6LEJqa0JSJ2laVU5fLTJmcmMna0kxRGksUVwkRm5jMCYzI1JgOCtiP290S0BMW0hTQDE4ZnA4VCFCMSpZNGArZgpfJzdTVWMjX0pxJF08UDo4U2VRSitWMS4sbFlCYGVNUzA6SVtHOGM3WlY4WixMJnQxaiY4bkMpWmxxTDhaMFxtND1ccTVnVVkjcS82NjgyNgpmQFJOVSdSTERwQ1VvR05Bc28vNiUwYEVfSjdMZ2Q3VycsbmU+UyhfQzVzSkMlNEFfbl8pUmUkMjA2V1EmZ0ZTTGRzX2FaaiZCL3Nral9jVAo+TiZzMTNqYlVHJ1EpPjopLjpzbSJtMyFmI0NAPzNcY2gldSlWPDE+XklhNyIoLz1aYCY8OVwjWGVFZEZXR1tFQkZnUmlaUU1UXldRamdsSwpqQlRPaVZETiwjKF1pcGItQGFTW1pMKjcnWGUhMGkzI15DRGk3Sj9zUFwiO2s2ajZxMSJZLEVmLiJdLGJOYVVhPkMiUk1eIW4+T2pyaUBKWApnQkFPIzQrMk5yMXAzQ2JZbkowLWJKXS1rJEZYcSg1NDQycEw4T1plZ2xUND5ZJWtRJGlVaWE5XE08WTktJTgoOm1vVD5PLG5jMUpXTVU2WAonXT42dC83TWAuXFpESyJOI1QnaGRvREInZ1pecWpFYiIwUTkpTyxSaGxsVig5LWJEdDtHQT05XWFCNU1TXD1tQkxtNF5HTmUuSV9PTSI+YQpJNU9iY1NfLEtvR1trTXMlOCFCJWR1J0RcKWJDWjVXcGppOCZfcmhkSyVLb2ZbVFJDS1VTJVdEN1wqKklDN0tsOll1dCx0YG4lcERQIkg9YAonZT4+J09zSCxnaVMhY09mTCJVNGVxXj5VQ0BBdVJnQComN0JVYD80KXQiIidITGpGXWNOR0dSKkQ4KUZyN2BENmxFUitAS2JzIzVPXVRBXApOSStCcGFtLyc3cEBXWGlDcF9IakpkbHA2Q1tMODooblYrJis/UGxzKSM6WDAxdDYjKicrNkpDRF4lLGxSYmpGWyJET0EwUk48MzxLZms7cQohR0lAWlVRSlxuKVIlVS1DYnJdJDFzOiE9UjhCMVZjMVArRj5bKjxTST1AYlw2NzBVJSg7YXI0Y2NEX1NYYkVfJ3IjZ0Jhbk4qNVcyUkBhJgpaVjVTMyQiXipfPl0wZWNWLlNLRE9HXV48WCdyJW1dZWopNTlhdSQhMFNEMUteMFw7QidqLk1ubTtGWSksQWskL2EmPm5yW0xSMmA+bjNqPApUTnIiMnAkKFJZLkkmV0VMQnA2YWo2bDVVQ0w7WSNSYjdXNVo4XjQvLnNzSDpLaydILEFqYFNULmg7WiYyLjpkb2A0MVVyYFQqLUEzOnRgOApsXko6JCxBZ1dpNFhxcEFNNjRTYFVPZUNdUllXR2w3cSoiWTs6dHNFNCFOK19nOjE3P01UNyRgRVRqR1BlaStEJjgodEJdSDttamEmbUtxSQo3ZnNdRTFfRV9hTykyQTNfXlFbMyFIVmJIWUUlVl9jIUljLSphJyU9UF1oQ2YsOSRJWzQkUVksMzgvaGxiNEBFPU1KS2cuMiYkKmlHckI7TgpNL1pXKEQsJmJecjFHOWdBLSJqIStGWWErcDxsRGVwXTVQZVZMITNnckduMWRCRHJVc0ZxJjE3IlFVPSxbQzQsRiJLM0VwPCxSXGFpVG1RbgpCWCpNYihwM1g2M3U3OXJAY3FDRiU7QTxIcEgsV2xqQ1N1dStac1guRlZNNFchT2ZPNXEnT0UuaS4sT0hOMShUY3FHXU5sbXEjdGtCPzFOcgo3aGtcWloiRScvJlBYRTJXYUxLRjltJUJNMEo3cz5LWjJaPlFEOWVfbEFgQWUwbWQ4Mz4qaFFqRFFSSXQxTFFlJ1NZKFpyY1s1PUhAJSdWIgosW1AvIWpwKm8tUTpBYU4oOUhxVVQqZSZXcisnOG8yZDBDTzY+Q0Q/QUxCOUFTZ2c1JkxIIVArb2ZIUU1MXksvXjBlNGY2ak9zKzhOWCEtWgolWkhPNSZpUG9WMyFvTSFILFVWLCNiVnFpIUBobFBnQHVUSygvX21lY0VTRFBfXiVhP2c9TF1qbjVyVV44STY/WD0uQkRCW18tJlgwKkcpWgpSSy9VMTlQby5kRixRdD4vV0JSPT1iMnRGUWE1WjIrRCJKPFNeZ0NrPVw5OjBNNm9NXlVabTdjLSUoXGw5ZGJJRCxiQ0drMVU9Sy9fbDYjRApsQnQ8Ui1nbUhCbTsoZ2FnJU1GRGArcFBLJkIvPlo/VkxpNkBwSUloaSNtbFNWVTE5XDg4M1dSZTxhWE9icWRMRFtlS0A9Xy0yaF1PRlBhXwpWZGQtKW07W2VOMkNicSJKXVpdc1JZVjtjSD9AY2VMZEF1K006InNYblxpR1BOYzJhO05LVEJRZS0pW1lcIXVjKUtMbidPWVhPLGJnc2hkSwokOHNlInEjJjthLmFETFxbKT8vPF5uWyxMQ0xXL2hxYjkySWR1W1JlRyQ8KUckVVk7dG45Kyk6PGIra0orZWpRSU9JV0lQPXUoXyNDRDg8KAoyKj1MPVYpNUZPXWYzIWtOZls3dUckPClHJFVZO3RuOSspOjxiK2tKK1lqMDwxOil0NjNecyJJN2c0LTNHUyFiTzFbIkQtVkpOQjkiZXA+XQpoRkUpNzszMjNJKU8sQ1NTZCUqYzJvLUxXU1tPMkFAXUlQXFpwbE1rVXVwaydDIiZRP1pGLXRSTSFlaSEqcyQrRTVyKFE7OnRkZE8pVkZQXgpKcjd0ImBfYVdOaS5oMVtkU1ApL1lSaW4tIVJpIWo9R0lDITlEY0o+OzRdS0BdUDdCdDJeR0U9VixLJ3NrZTxNN2srMDwmI1osSG5lI1MxKQphcGpgcGAoa0hvcEtKVTFKKExEV0BKa0UicmBhODI8LlJbaSMkOCU8ZCk8c2MnTWcpc01VRHRIKlM6M3EoLDNZZ0ttJT5QZUw7NWJEKCE+Kgo3Wi8va3BjVlNGPCxiKkMiSyxvVV06Xz1TIThAZSg8XVNfIUFIPVQnPz4vTiE7NFVULmZRTF9fQVtKQ3VKRFdebzZqOEZTMHVERWhHbTdAWQpHKSovKSleXUg5OCRRODpXaTxcQ0puQF87XFVrRCRGXWNDNzwwJmxUTGdDZ2BPKC1STV9bJzM1OTZdbmUhcCVmQTwxKDFoKlE7bzFXMkI6UgokQ1dqNmo5ZUAtZTcmPSQ6ZCo1QCxDMz90NSlRSy47ZF5wLzpcNVNYVVMtR009SXQrUW08KSM4TjpqUzItSlcuTHB0ISonVis2TkRgPWhwNgpEO3VUWy5TMEk1XSsjY0NpSDJHY0pwLFVQSC1MTUoxKXBAVi9nZkBhX3RfZnFIKTQjalc1VEREUlZoKCkrdENbREpwXltxZT9MOCg5Tlc1RwomYlFraW1XW2ZYLCNzPCI8LWg9aTI2M1VrNjQ8MThLT205MSVHKFdiNz5BNHBxOCMrXFFZMCVBLFklWjEwP3FAUVhZb0wwcjYhXWtvVV0jcwo8X1w6JSg+OTMoYkJQRVNYb2knaSRwZT8hRStDI1ZXbyRLaS1qcWpzVkBhLy1WdV1BPWc+aXJbZVFWW1ZTVz1dSDZoUiZJSSslN29UbyFoWQonLS0qKmdPZGotP1IrWi8oOjwuRk8jaU0pZzhkKUdPSClmUiprMWA8aipSYF07a0hpSD5xSW1RTmJFU21MVHE0ZltTS0BcITs8aT5OQ0JbJwpHR281NjNibj07cmsuPVtGOmVxXW0/ListUUBBWU9rb20rZTluQjVQTSc7QW9NNV4wOTZIYTVFNjtqZ1hCbGYmdVtdI3MlWU4hbCRtUzRTNwpUXDpIJD9ZU2JrVDo/dC4uYyhrcXFXXyNeKTpmIjI/a1o0WlJPMWxoUzdcZXMqTmsxczxgQT9wcShqRloqV1NMLEcqbWZnJSlRWE0rRG03YwpmY1hLazhrcGoxNSldX0JkajFySmRuRFg2X3REQzZDNVJFaklnM20+IiFEOi0lTVIzVDYyNTcmVWIrPilbcykia2Q7YTgsZSkucGU7JjpnOwplajllVlZYaWk0ZzIsYVxvJ2pnMmZnbE86QVBoYFFkNmYoJVJOU0hWQ11sYF9EXiszMD9nK0dIKC4pZFsjJGsxJ25rIVtWbkhhRjhBVlAiSApMPDs4InA7WjxpJjNNR3BVa1g7P29WdWxqXXFsWFxsPUYpW2QpIktDZnFLWW4kYztWajF0cl4+XU5lSjtscjpraFcsN1pmIyxOJEdcW1lNaAokZT4vaEE6dWBpRjZJIkxLUFhLdEpkI1RbQ21vMkotWEpEVSEtWUFOK2szcWs+OClKcDwjVlEsYF5McGBdUEpKSCdWUVpGZUw6YTJjVmxgcgo/QjREPkZgdWcnQUBvRkpya1U1LlxaTWhzJVhtSSJjcUA6RSg1XDE9WzpQSGMoNU5uLGxCSHFUazolP0kwPzg3MDNrS0JOWjxjOWBzJ1FaKApndCghNSEyKC1uO1M2JVVXT11oYDZWTWRNcSxoK25WWU02dUZdMW9iPFlrRXEyK0ZXWGVLPDc5PWk/Xi8lWnIpL2FKUHBlR1JgViRGK1o/KQpbU1RePU03Jmk4Rz9FRWouOkhGYGdddUBIWGQydDo5TCEpI0IqTD1gUk5TSEglOWtaWi04Y1koS2pBT0VARDtoWUphKmMvYykrRkwuPU8wcQo8PydcZEdoX2VvbzxJXDFWJUUsRzg/JFUocVxvIUIkVGEpKVxlTl83NDY0bStbIWFDRkIlJjNhJ0wqUElXZj9DQl1QW0pzcTpLbCk7QCVMUwpaO1U/UU5BZUpYMWkmJjRCcmVHMisqUWpjMmVsMTVMR2AlPTxdWlwjZ2ZXPixXMUQ9JkAiTylqL1lbaFVPO3JRWEEqQFQhWlBKTzpCb3JvKApZWDxXSDsxaT1BWEojXiVkYThLYWBuSl4ubT5NZV4nLmRDKU9YPFZwLTlIX3NVb20vcD4oQ0hVXSJTYV40ZUE5TUdVZUJyQlBBTjFXOkkiIQoxKDYlL0Q9cz9xIV1SP0xZYDtPR1o4TDxKW2JLaC5yaVpKVzVgTFMoZC8rUyo1PTdILDdTRT9PNl47I3RRIXBXPUNvYy9NJ3RBaCZLUVJEJApRJm9GLzIlO3MhcDtCVVMyQm8jN25SOE83RjA5LTBWTStvcWRcOk0zbWEmPGFRTFNjP2pXI0hvKGssOTw5MENVIWJBQnFjIkRCI2hhcWMpTQo9dSMyVFtWXFhoKyJdKFUoPz5DMSRYdCIiUTtaIU9VNFQ5ckp0blNzPTBVLk1rMFAyJj1KTUtMOzgkciIjY2AuaSEqYmJYbGw/XCM6dHMlXwo3ZkpxTlxpcGorXyZILVRkdGpII3FLbGJZPypIZF9GZVgzQFg6XEcnMnVwQjwyOygmOCwsKUgrbCZHVSRsWklWKlU0UXEsPzBLI15XSk9QUwpSSFw6bWRrazFFIVpLUmRMOFY1JjtaIVonLDpMdHUiWjhfUDlvTy0uQ2IkS0FMSTphRC01NGtnV0pRWl1GVGdhUVMxMmAlKD04XjwyKj88SwpQTTFNTypDNWdyLkIiXURDMTxeNj9zRFN0NDBLTSEmXz1nXVtWSnBkYl0jQmtfUix1IzxuVGZwXlVLUTNjaVJhImMrW2ZIP25QW0NNJ2xKbwpYYD88MygiPFpQOCtZLjdSbiUmaG9aV1JtJzRdO1FrYThOZlwhTzVEIWI/RHReMVE1MC9tST1sLVgpbGgxXGorXmtQb04jIis4dERlR34+CmVuZHN0cmVhbQplbmRvYmoKMjMgMCBvYmoKPDwgL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9XaWR0aCAxNjUKL0hlaWdodCAxNDAwCi9Db2xvclNwYWNlIC9EZXZpY2VSR0IKL0JpdHNQZXJDb21wb25lbnQgOAovTGVuZ3RoIDYzOTcKL0ZpbHRlciBbL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlXQo+PnN0cmVhbQpHYiIwVT1gVTt0J0VxPixeTTNQPiw5MnJGZS0kJTprSk1qKkxoQyFNVW9TayIhPDwqInp6enp6enp6enp6enp6enp6enp6enp6enp6enp6egp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enp6enohISRFKEQ7ND1kRwpkT1UsaDNCYjNzI0woLCVJdVoyamFFKkw6RCo/IU0jMSxockAtYFReImhhdFtraUxTVD1bPDYqbFowLl4pUHUxTy02JDljL0dqamdQamddXQpoYFA3RC1SISdqXC4hIjEtYTUlcFJAITk7b0pWYGlyNUM4WGtOR0pFS10sTmdVQCReW1xDQzdpdFBBcUdkTV9cMk9WPFhIJztoUEohbGI4LQoybm50cnRLSSZhcyhpLzpyPSkjJmlVVzI+QzMhRXBqWCdcUFAkLDI0UEZQQl9LJkZXa0gwKjxfVS0kLE43RDVzYz8+MD4wM2ZzQFF1Rl1nawo1OjdpPG05VSFEcVJtdTxBTjdeMnM4clNfcixFRjUjMz9ObGYvY0hXST4ldEVUNXRBUSswJWlbQ0NFYlo4OFUjR0hiPEs0K0NCQkRtYGQobgpWNnU8KVcjPjFTTjE8ai1JOD1JSCtMLUFoUSQhaXFXZl9ybnQrUjthby8/JT5PZ2MvWUU9YEZnaUtTT0xbWDRkaG0xdW1FRE1xVidXaThJPgpwWzBVU0Y4THFnUjFqSEAsLSpESUNaVk0yZCVxUzoqVCslPVlvSmpQTk1QLSwkbFI6L2hTU3VebkI2O1FMKE4qcWJ0SDMyPCtWKGpET0FRVQosWVJvQ1BmZmVbSk5uQHJALV9pZWIrREtqJGw+aVwjNyFYP2hSZkJbQ0g3WmE7bHNEYysjY2pcM0ZRWFwxUUJIPT45Lkg5NnVUZzpBRlovUQpAInE5Vlt0ZEcnKTEjPWlrRSw+WHE/PiZCVjQ3TGBPXTtBRVhPJmhFT1RsN05nOHUsXlM6dXRWLF07KCdoMTVzLXRGZ3FRaF9OXzIyUTghaApYKCRmcV9sVilFUTx1LkUzS151T3FtIT0xPy86dDI8M09rVD5lSGA7bG1EYDU8Xm5mQCpqJ25GOGdjIy9wbEFkRDBhYSJFVElpdWxjLDBBKQpLJ2dXR0VNWzQqQjJybiRrciFSSCtKNTYqZS0maCIkRG9hSShJaWhvOWFJL0A6UjVqX15DbEZtZHAzIWlyMFgzSW5LTUkpVj4iR2omaDhNVgpxXDRXPWplQVEvKmVYOTVnKkxmWTNQZkxQdHVuN2VeZVY1LTE0UEBwU1dpRUNMZGxaXmY1QitUVGE8bGJcSkdDV2IpNDFgWW0/ZHFzVEJeSwo/RlZzVkhaNlpEPydVc0cuWzJSXFklbVFwX1ZeQEhaUCo2SnJWM3RQUElVPk5UYlc7P0RrNEpXN2Q5aWhWNT8tal8qQSwlJ0M9W0dfXVs8JAprPSc7QTkhKlZcMCVMcVhFXSZSb2JnZTRYTEheKXIwQnQzRDpxVyVGIVskOHBmZUlnKkpvLjQ0bjVoS2lGZUwjb1FjTnRwWy1jP08+QiZmKwpLInFEVk9nLFxOMGtRLjAmZT0iOTczOD41PU9ANztbQmBabGIrLVo3Z25GQm9bc15oY0ldRmg0RDppRUROY05YVUBIZT05QnMkWFQ+aVlnaApDW0JSMjljbHVRPj9DZVBQZTlKP0xgY1BbMnVsTlRzMWs8Py06SiE4RkAtOyNOUE9IQkJSaj5JOzU8YzIjXE5XJmAjQUo/Vm9VdDdzckpTIgo8S0tdWio7ZSQ7LSZMIlllX3BGVEQtbSJdVl9ramsvUkBEaXRoImJBQC1zUVVSUk1QRilWIURESUMzIjxpdC91WipoRz9tTTFmQmd0LVFTNgojNSVoSjFGQElMQm0tZjRGcV5gP2IoJEg4Xk86UzRlLGNcUE5PU0xNNEUsbTJZVjw1Olt0KmYsc0cpWlQtRV0hJmJpMj5lTGlJJ1k0L151Pwo+Ukhmai9UODAxZD5qKUlwYTY5OEY4OzZVKCEySk5tMCJVSFhZYlkyXDI4dGhJT0okIi1uSEVdS1dGWHIlSS9zJTFaKGo1Ik1uUiRWcDdKYQpnZ0FMXFE9a11PQW8uP2FZZC9UTWw+REQ9LCohMF9vOTxGXFQuKShuJksvUHFLUU1zNjtvLD5NbkxoLWwtPVV0RjZoLi5VMk4ucFtUclhgbgpIRlViajFSSy8yTktCZlFKMTFPYFZBcWozJl1sRldsaCxQO0UudXNHY2thaWgjI1ROZkNuP3MsaF01Ikc0UDBHOG5NQi9eMlhNX28tOGtfNQpHIihMPSJuSixePUcrZWVzL3RlV2VsKDYnOFE5Nm1kQ2JeVnFAbnE4K09RPGxYaGVvaEUxPSRFTyltIVtzMG9AQVpfVF8kOCdJUk40RlAtcQpHSyxcOlwmUUsyPEUuODlwJlNqY2d1MzNjQU1NKSgrPDk6REdETUc6S11DPi9iT1Q+bSM7cWFQMzBiaWRwVlUwaSZEInVyJVErXlw6X0QoWwokNmQ2bVxvKz5tPFIlU1w/NEtDO2ghOi8rI0RhLlw4dGA7Pj1ecW5NdFVqa0tAVCY+TkxJKTNaIzk4TDpDclQzaS1dcVxYPXEkaSRaUyY3Mgo3S3VVL1tgWCU9aEQ5Zjh1b1pYPG1DOnBSbSRBWVEtMCEpVlomNlhvPFdzVFREJiQuPmcnSyhCQS9KbW1PPUZRIkd0PEpZNTRpOUFOZVgtbApbdShRXXFzPEdoKXI/QW5bT1dFTUFQL3AvYG9PJzokLXA5aD5jPDVSM0g3QmZyRVJdMjZpYWdHZyNJTG08OyclTzY6UFJyLkVCW2RPXXQpUQp0bCRPMVpGRzBBX2BObDFVb1Q5aDlYaTpwVnVCIWAwVCk/cEZRWDRvPUo4XGVYI1lDJUY0QHMlaDUqX2xWaWRdZllrLzIzOUJTJFBNYFslQQpDLGEtLWRQUjxQOUlKVVZvTENaKCQmZz1wRkAtOyp1J0pvMGxDLElDTi0+X1ZyIVcrRy4sOmA0dWgzXm9aZkNfSGRkdUVaWjpBQSlsaF1BZQphX1omSUJlXmpeOisqMkNtazwiXV5qb2FnXy5AZWxYWUlXNSFHcFheJkMtODI4cV4iTVJgK3RFU1NaKkE6OW0zajUtUGxCJmE9dVdNQGNDbwpOW1okKzFHZSRsXlA/RWghU2gxYWFKRilJKyhIRCNNdGtPW1ZFOjlacSMkSCw/QmEiaWBEJWJNPkw1aXJBRVRLXyJDcDtSUylxcVZScSRvKgpaKS9cNTBFNypULT0kMEIxZzJzMTA4RS9rPCM4W25lSVRpLyZTNyldY0kocFE5OzxnLGUyWWwxTiUqY1xWUV5uZ2JMcVUrZz4vKmFYJzQtWgpUS0giVkE6VCRjKCczJ0JkKW9BSEspUVQ0aVEzZHBYSl4hXT1pMS07UyQ1I2o2YUlnNTlpXiVmISgwWmEoOU0wZFcrXkJnVEJ1W0BmNyFcSQp1OmBQcE4lRyxuTXMvImI2bFtWX2xcZC1uMWhJbFd0ckAkcEBiaE9hKmVCZ1FxUjFeZ3RyI207YiROUkhFTVBFI0AvKmhBSUlLXWVfSVpVPQosc2MqJ049I0psODJNa3Baa1g2RUhFOys0PnA7ZUEnZGNuUFlqWTZqaFJ0YWxGb1o8NWEsUGQ0aVEzZCFUOEl0ZzBsa0xeYikrSUhgNGsxJApNSXNnbWFLKyZbUSlqdUItTT8xOEs7RF1VYzVcXjp0JWMwSCgpczpIaUxNJGw6WUM1WmZMKnU+ayMpLW8oaS4jbGZTQyNyPmEiaWA2Q2xscgpBQjpzWlpSbWszMTFrbG9RajQnMVtDcHBOaiJNNVhncFNTMElLT3FOaUIiS19DSUhMKHBAUm9JdTpiPmRDM3V0PkhJQGpgLW5aJnFISkkwaApSZ0JgaEk8KyNTaUdpX1FqLlVMSHIkXSolKF1wWVFkM2BvaUpSTXRFajlla1InWWY/U21hJTc0MV4lYHFwc1pfZDZhSFglX1szRWh1RE0wIwo6RCNQYWdLPnQ+TkQoT2xIXzkqPytHbWo3YnIlcGhINTkhMVhwWEFpJ281QlopbFA2QVlVIVQrbF0qVGtJLnA4R1lYY2REcWx0WmZbJSwmWQouLUtFXDNLKSxcR05RaVJAZG8qZ2s/TGpROi80SEU8Z15caCxvL3UtNz9icT1BU21AUlleaT5bVkZubk5YKCdjI050REdXXVdrUm5bUlY4TwonME5OPSZwJVBnJUc2aWo1UzBDcFYnWVEyRVhPQyI5ZDJtPyVuQ1QwQU9TLTttXzswXShFPW5WUyhtdGdNV2VaLi0jPGZobTA+dFxHKExJPAo4ckBhT2dyWyFPNDFSPGdWcytiKkYlaF1xP1NHNjdBTisnVjYqXEIyM2tpJkMycl5BUkslTSRpYnN1UTtyWHUrbVM9R2gyJj1qTk0+TStpbQo9KjVfW0dBVEslTD04TSkjJFFfTCJCLE8sRWkhY1IhQTA6UlNZTlBWVDU2NEAzclhEXFQtZFZESmVsZkEmbXV0Ly9XU0svV2ZiO2VgJktLOgpVTzMnRGxuQ2xoWkQ5T05JMVxMbWJRU3U/PyYyKXBUKmsvcWFsTEhUX0xcJ0N0MmtXXC0yMDMvJkUrYDNeY0pYUCkzQywqWy9mYz1HOmZwOwojRy9tVDpdKD1JOzBPXmpTS0txKSkoIjRRMk1pcXAsMicrTmZORG1pUCloJFBoV25eOjRxQmdYTE9tOUt0LU88L2kxciVhZV8iIlNYWjMnbwpVYz9iQjxbMCNhUk1iWHBYWXU6XD1mJC1mMVksK1FXdFcpZVBZPi9QYCw+NU5yIzVJTldtcWFPR2VIZEgxLnQuaCFyODs7OD81Zm0nM2ArRwpCMiRWM2peRS5vZkc6U1o+bUEpRTMwISNfM2AtU0lJVFEuP0YvXjwtPksrQWpwJiotJHElbCdWKGFwN0Y/SURxST9OaDgpbDI5Q0VjP3JgYgo7cVwwU1k7OktpVigsKDFjUixJZCxUYmIoI2tQU2Q/SlhVamBNOWRJOk42T2NQbDhOK0pcXkk7XjlEJi5wTChQPk1tTmYlRUAzZSpbZk5YXQpZPGtlczZLIjkuNyc7bWVNa0MxJUA2aSNYbEVsLiM+US9tPlAmR0BuW0lDNDRyMSNWUFspdVcrN1dxNENMOScyXD42bFhgVmlFYlpWPkhMMwphVicpUjs6QFxoRCpiKV5cdDJWR3FgQFRxZVhbImslQktFQ0hfIV5TMmtaIm0uODRWQjheRTtdamRIRmtJWCg/bkpucytibDxyZTQ4cS1gZgoyP1YvWmN1aEhoTDgwUVcwP0NjR0hET2Y9PWBMcUUsaVdtYTc6aE03Z2k1b2ZtP3IyYjMub0lSbU5BNzhdS2VebyJvNEJbcmg1JixLbCIvWApkZzhcSSJTVVsxWCRYPDA3VTpuRFEyZ144UXMqbGsoXmxlcCNQK3VwanN1XmdARlkoa05oSHVcPGlgUi9RVDBKcVhab2pcVChWcVgoOExMJwotR1EzWzFOYFFSSituJWg2NHNSbVpbU1hWKF02bUhITzlNPjtrcC1cYDA0P11YWVFVM2xXMjEsYzxEcDFaQWxbbV9LV2NRWlljPHArLG1mbwpYTSQ5Zj5yKydjYFNsJ2c2JmVRWTslKUJFKjtXLCkpXWNVVW9VdSFDTUtOYT9eQ3NPZVRaLltiJklsRUBxSWFAKkxzZEpMN2VyWFQtUEpGXAorSzplL0FeIyZcX0olUWhvcCVkLTFAJDpMKGY+VEk2NTloRScwTGNhZUskMUU5cyI4WV1AJ2ZhK1FTU2c2aG1KSm42dScqNks6KGNFb0BzWApcUnRyLGp0OiViYkA7JmotPGo7Uk9kZik5b09Ga1soTTouPz8xIkVVdEhJVidfMiwkbz0rTGw/b20rSWYnX3I2JD91RmhuJ3RoTWI8YjYubgpOa3RPO0AnV1NsXSwmLCVjX082XCopJi87JDNwaVxwPm08VFNFNTlnUzlVcmZMWD4xVl08KGpFRUNwXk9MOUFvSihuQyUnSTdmbzdnXDk+YQokPmh1aVZHaFBdUU0nJmEuKCJjaC80OHQ5cy5SanBBPG5UT2hwXTthY0IzJVpZUEBpZy5nXy04YWFecDk7Xzc+LEtjTHFaUmJqP05cOjl1YApQcUY5bU5xRDM5RygmLjYrQlgvcE9zNU1Dam5AY29YS1VcWkZPdURgbyxSckxjXTlobWlEKWBNV3JEZ101cWItN29eZFAkYUpya0hWLWxNOAomcllsPjpvOEpgOFY4QygmSUBga2ojdSdiSydONm1aWDgrMkVnS2RxUyhdN011VShmTEtyTUgyKVdtbStSWGkqYC1vOVg1MmFiJmluZ0ZWQQptVSZXZDIyUTduMHA8TjFjP2pbMSs4UlFuUCVhKjYoMmYnKkNIbzUhdSNPNmosWFEhLWJpQklCbVApIztjPlE3VlQvOFVday4yNjNeMmFbTQovTGYmU2wvQVRyJiJYPzoyWUlAL3EtRkomZT4tMmg9OUZkL11ocHBCMjBjQDhwcV9jPjI0SUU5NmpZTGxQa2ZbVl9gJz88KXJeWnJRMCZfOgpyPHJAbCZdK3FGYy8vREtgaDx1KiFPQ0FFKiVWbTNtVyElS0k5LiVaQkYiJGBzVDlRZXUxSSptR0NXZUhzR1EiRTRePStndFphRTAmaWI0NwpMRkNSP21OYlBAUDxiZ2VgJmRsJEBRajlNXFdObXAwMj1tWG5TRCRHPmVsa2thT21IRVZIbCY0QVQqcURpYU8tND9UKjopa1MzOSwxZSE/JwpCc2JGRE5UdDZHQidQIUlARjNoX0lbO0YiWHUqKWdCcnNoWkYtZCRMIkJnRktRPU44Nm4wUj5WVCtnPFNKUGxNamBGXERNV11jLkBjXjxKLwp0VDgmKlcsUWltY3A7OEY3MlJSSE4qUHJYUV1tbm87biJCZltcZiFLIipIaWRhYzFJaDQoZGRnXF0tZD8/YjFFWjxRQyYkXGJISUM4NS9qbQpjOWUuOEtCSj07T10xPlQtUDdZXyU4LVNPdXE+W1YvclldRTolZFhvOiEyJjBJdXBkQWxJS3EvLE5XaVpjW0FnaW5pc0I8KWtxS0k3SjwhaApUJHU3VkAvUGdEQUNvXDY5RTNsajVcSEhwLUBFZkVUY0wnYWBWNF1eYDYscShVOkpfYWolOjhQT1BZX2IvYGtkLEFZSmw8Rkw6bmpeXCElKgpIR1o0NW4ycGNycURFX3ErRVYwaSRdRzBjZ0BiSmsqYTIqTEo8JEJcLVF0J0ktJ1QiNDEoay5HLlxyQ20iSlRZcHM+VypfVS5LJipmY2xJPgoiNWUkRGJEV1BxM0tCa08vb0gtPTBUVUZkbFhTaWBwanRjPyJwKzBFbW1BQHIja0ZORkVeXChsZWV0Vz0taTBObmghLidrIWpaRiVEZyNjOApXQzRLKk5ePj40bW1gKy9YWTItbGMhLm9QSXJEKjtuLj9IKi9FViRLPjI/SkBwLlQqMStWY0VvQUBqc2tOZi9VKVkodHA7T0hpZXFZOnV1MApyRl9uRzxONycuK2JgNUZFUi4jJmJkME9lP1hPTyVFVVVyaVthPmQpMWsvRjRPNicvLm1oX1BqXlwiOHMqYyleX24yRF9MIW5TL1wtci1vLAppNUhcTjc/M1g+PEZwZTNxZiNQV0ghbVpHVkl1WGRrMTdVbCNtSW9hRWhDSEdNSDI+MTs3QF1NR0tnUFVAR1dIXkFWXFtcUTxuKDFlI2kjZAopaS5xRkZnPDwoPHBuKGchcmNsQU1vSWsvY0w+LF11K2lGUDw7VXM7UThIZ0dpY2NyLTI0XU1gJi5YRXM3XU1iVCEqRVdjcEM3YWgyUWVWRwpNRWsoZ1w4V2tnXyk3T3BTV3RqPytGJlJUJWorW19ZKXBmbCokJClLP0FQKS5OX2hSZShSLFksTiUhKjZCZyRRW2oxPFIuOmFwci1TImNDYwpUcGVMcSEjRiw1LF5TMWJCSnFOXm0vTWtYUjZKK2hEKDgwQlBLOjhwSSJVIiw0NVtCSnNgLj5YSSF0T1UtIl5zJm1yITtGL0ByYC82S05SPApxKW5gSWcnJFNgSGszPzMyZ1hgYiJqMCooLD5lPEhDPHM9bUVEYztLUG0lX0VVRmBUbDcpIkI+ZSlBJWdFKiU7VU4zNEotWE0lWltrPW1SUgpkVElUQCNFdUMkPCwzSzIqPTx0YUtzbGRnVE5YLzYwMVxKXjRoXVpqJm1cK2wqb2wqSlI5dFtQOEI7Sl8oOT4tPiZiVmZUZXBtZStqY1taNAouXVEoWUlGcmktZFVSUkwiN2EuQmUvcjgjUTYyTGdjPTJJLVQqYjo7WGkkJ3FBVEJpXzlidVsvYmVuT1Q1cGEmenp6aSFmVmRtLCVvcX4+CmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDI0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMDQgMDAwMDAgbiAKMDAwMDAwMDE2MiAwMDAwMCBuIAowMDAwMDAwMjE0IDAwMDAwIG4gCjAwMDAwMDAzMTIgMDAwMDAgbiAKMDAwMDAwMDQxNSAwMDAwMCBuIAowMDAwMDAwNTIxIDAwMDAwIG4gCjAwMDAwMDA2MzEgMDAwMDAgbiAKMDAwMDAwMDcyNyAwMDAwMCBuIAowMDAwMDAwODI5IDAwMDAwIG4gCjAwMDAwMDA5MzQgMDAwMDAgbiAKMDAwMDAwMTA0MyAwMDAwMCBuIAowMDAwMDAxMTQ0IDAwMDAwIG4gCjAwMDAwMDEyNDQgMDAwMDAgbiAKMDAwMDAwMTM0NiAwMDAwMCBuIAowMDAwMDAxNDUyIDAwMDAwIG4gCjAwMDAwMDE2MjIgMDAwMDAgbiAKMDAwMDAwMjA0MSAwMDAwMCBuIAowMDAwMDA1MDY5IDAwMDAwIG4gCjAwMDAwMDU5NDYgMDAwMDAgbiAKMDAwMDAwNjM4MCAwMDAwMCBuIAowMDAwMDExNDI0IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0luZm8gMTcgMCBSCi9TaXplIDI0Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxODAwOQolJUVPRgo=</Image>
                  </Parts>
               </Label>
               <SignatureOption>SERVICE_DEFAULT</SignatureOption>
            </CompletedPackageDetails>
         </CompletedShipmentDetail>
      </ProcessShipmentReply>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

ShipmentRequestXml = """<tns:Envelope tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/ship/v25">
    <tns:Body>
        <ns:ProcessShipmentRequest>
            <WebAuthenticationDetail>
                <UserCredential>
                    <Key>user_key</Key>
                    <Password>password</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>2349857</AccountNumber>
                <MeterNumber>1293587</MeterNumber>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>IE_v18_Ship</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>ship</ServiceId>
                <Major>21</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <RequestedShipment>
                
                <DropoffType>REGULAR_PICKUP</DropoffType>
                <ServiceType>INTERNATIONAL_PRIORITY</ServiceType>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <TotalWeight>
                    <Units>LB</Units>
                    <Value>20.</Value>
                </TotalWeight>
                <PreferredCurrency>USD</PreferredCurrency>
                <Shipper>
                    <AccountNumber>2349857</AccountNumber>
                    <Contact>
                        <PersonName>Input Your Information</PersonName>
                        <CompanyName>Input Your Information</CompanyName>
                        <PhoneNumber>Input Your Information</PhoneNumber>
                        <EMailAddress>Input Your Information</EMailAddress>
                    </Contact>
                    <Address>
                        <StreetLines>Input Your Information</StreetLines>
                        <StreetLines>Input Your Information</StreetLines>
                        <City>MEMPHIS</City>
                        <StateOrProvinceCode>TN</StateOrProvinceCode>
                        <PostalCode>38117</PostalCode>
                        <CountryCode>US</CountryCode>
                    </Address>
                </Shipper>
                <Recipient>
                    <Contact>
                        <PersonName>Input Your Information</PersonName>
                        <CompanyName>Input Your Information</CompanyName>
                        <PhoneNumber>Input Your Information</PhoneNumber>
                        <EMailAddress>Input Your Information</EMailAddress>
                    </Contact>
                    <Address>
                        <StreetLines>Input Your Information</StreetLines>
                        <StreetLines>Input Your Information</StreetLines>
                        <City>RICHMOND</City>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V7C4v7</PostalCode>
                        <CountryCode>CA</CountryCode>
                    </Address>
                </Recipient>
                <LabelSpecification>
                    <LabelFormatType>COMMON2D</LabelFormatType>
                    <ImageType>PNG</ImageType>
                    <LabelStockType>PAPER_7X4.75</LabelStockType>
                </LabelSpecification>
                <RateRequestTypes>LIST</RateRequestTypes>
                <RateRequestTypes>PREFERRED</RateRequestTypes>
            </RequestedShipment>
        </ns:ProcessShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""

shipment_data = {
    "shipper": {
        "account_number": "2349857",
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email_address": "Input Your Information",
        "address_line_1": "Input Your Information",
        "address_line_2": "Input Your Information",
        "city": "MEMPHIS",
        "state_code": "TN",
        "postal_code": "38117",
        "country_code": "US",
    },
    "recipient": {
        "person_name": "Input Your Information",
        "company_name": "Input Your Information",
        "phone_number": "Input Your Information",
        "email_address": "Input Your Information",
        "address_line_1": "Input Your Information",
        "address_line_2": "Input Your Information",
        "city": "RICHMOND",
        "state_code": "BC",
        "postal_code": "V7C4v7",
        "country_code": "CA",
    },
    "parcel": {
        "packaging_type": "YOUR_PACKAGING",
        "weight_unit": "LB",
        "dimension_unit": "IN",
        "services": ["INTERNATIONAL_PRIORITY"],
        "weight": 20.0,
        "length": 12,
        "width": 12,
        "height": 12,
        "items": [
            {
                "id": "1",
                "quantity": 1,
                "origin_country": "US",
                "value_amount": 100.0,
                "value_currency": "USD",
            }
        ],
        "options": {
            "currency": "USD",
            "INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS": True,
        },
    },
    "payment": {
        "paid_by": "THIRD_PARTY",
        "account_number": "Input Your Information",
    },
    "customs": {
        "duty_payment": {
            "paid_by": "SENDER",
            "amount": "100.",
        }
    },
    "label": {
        "format": "COMMON2D",
        "type": "PNG",
    },
}
