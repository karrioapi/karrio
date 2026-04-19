# type: ignore
# ruff: noqa: F403, F405, I001
from karrio.server.settings.base import *


INSTALLED_APPS += [
    "strawberry.django",
]
