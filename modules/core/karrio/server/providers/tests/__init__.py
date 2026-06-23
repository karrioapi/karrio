# ruff: noqa: E402, F403
import logging

logging.disable(logging.CRITICAL)

from karrio.server.providers.tests.test_carrier_dynamic import *
from karrio.server.providers.tests.test_connections import *
from karrio.server.providers.tests.test_tags import *
