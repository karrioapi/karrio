from purplship.core import Settings as BaseSettings
from purplship.core.utils import Element, export


class Settings(BaseSettings):
    """Freightcom connection settings."""

    username: str
    password: str

    @property
    def server_url(self):
        return (
            "https://test.freightcom.com/rpc2"
            if self.test
            else "https://app.freightcom.com/rpc2"
        )

    @property
    def carrier(self):
        return "freightcom"


def standard_request_serializer(element: Element) -> str:
    return export(element, namespacedef_='xmlns="http://www.freightcom.net/XMLSchema"')
