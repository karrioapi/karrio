from purplship.core import Settings as BaseSettings
from purplship.core.utils import Element, export


class Settings(BaseSettings):
    """eshipper connection settings."""

    username: str
    password: str

    @property
    def server_url(self):
        return (
            "http://test.eshipper.com/rpc2"
            if self.test
            else "http://web.eshipper.com/rpc2"
        )

    @property
    def carrier_name(self):
        return "eshipper"


def standard_request_serializer(element: Element) -> str:
    return export(element, namespacedef_='xmlns="http://www.eshipper.net/XMLSchema"')
