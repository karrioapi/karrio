from purplship.core import Settings as BaseSettings
from purplship.core.utils import Element, export


class Settings(BaseSettings):
    """Freightcom connection settings."""

    username: str
    password: str


def standard_request_serializer(element: Element) -> str:
    return export(element, namespacedef_='xmlns="http://www.freightcom.net/XMLSchema"')
