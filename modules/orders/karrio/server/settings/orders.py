# ruff: noqa: F403, F405, I001
from karrio.server.settings.base import *


KARRIO_URLS += ["karrio.server.orders.urls"]
INSTALLED_APPS += ["karrio.server.orders"]
