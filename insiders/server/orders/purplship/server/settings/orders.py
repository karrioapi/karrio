from typing import List
from purplship.server.settings.base import *


PURPLSHIP_URLS: List[str] = [*PURPLSHIP_URLS, "purplship.server.orders.urls"]  # noqa
INSTALLED_APPS: List[str] = [*INSTALLED_APPS, "purplship.server.orders"]  # noqa
