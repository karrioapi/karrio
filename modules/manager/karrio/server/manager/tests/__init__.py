import logging

logging.disable(logging.CRITICAL)

# ruff: noqa: E402, F403

from karrio.server.manager.tests.test_addresses import *
from karrio.server.manager.tests.test_parcels import *
from karrio.server.manager.tests.test_pickups import *
from karrio.server.manager.tests.test_shipments import *
from karrio.server.manager.tests.test_trackers import *
