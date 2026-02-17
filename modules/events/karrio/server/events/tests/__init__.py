import logging

logging.disable(logging.CRITICAL)

from karrio.server.events.tests.test_tracking_tasks import *
from karrio.server.events.tests.test_webhooks import *
from karrio.server.events.tests.test_batch_webhooks import *
from karrio.server.events.tests.test_events import *
