# type: ignore
from karrio.server.settings.base import *

INSTALLED_APPS += [
    "karrio.server.automation",
]
KARRIO_URLS += [
    "karrio.server.automation.urls",
]
