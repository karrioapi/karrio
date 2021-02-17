import time
import uuid
import base64
import hashlib
import urllib.parse
from purplship.core.utils import DP
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """SF-Express connection settings."""

    # Carrier specific properties
    partner_id: str
    check_word: str

    id: str = None

    @property
    def carrier_name(self):
        return "sf_express"

    @property
    def server_url(self):
        return (
            "https://sfapi-sbox.sf-express.com/std/service"
            if self.test
            else "https://sfapi.sf-express.com/std/service"
        )

    def parse(self, data: str, service_code: str) -> str:
        timestamp = str(int(time.time()))
        serialized_data = urllib.parse.quote_plus(data + timestamp + self.check_word)
        m = hashlib.md5()
        m.update(serialized_data.encode('utf-8'))
        md5_str = m.digest()
        msg_digest = base64.b64encode(md5_str).decode('utf-8')

        return DP.jsonify({
            "partnerID": self.partner_id,
            "requestID": str(uuid.uuid1()),
            "serviceCode": service_code,
            "timestamp": timestamp,
            "msgDigest": msg_digest,
            "msgData": data
        })
